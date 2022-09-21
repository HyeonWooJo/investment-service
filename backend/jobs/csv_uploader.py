import logging
import os
import csv

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from django.core.exceptions import ValidationError
from django.db              import transaction 

from apis.models import *
from backend.settings.base import TIME_ZONE

dir_path = os.path.dirname(os.path.realpath(__file__))

CSV_ACCOUNT_ASSET = os.path.join(dir_path, "csv/account_asset_info_set.csv")
CSV_ACCOUNT_BASIC = os.path.join(dir_path, "csv/account_basic_info_set.csv")
CSV_ASSET_GROUP   = os.path.join(dir_path, "csv/asset_group_info_set.csv")


def upload_asset_group_info(csv_asset_group):
    """
    자산군 csv file uploader
    :param: csv
    """
    with open(csv_asset_group) as in_file:
        data_reader = csv.reader(in_file)
        result = {
            "total_csv_rows": 0,
            "success_rows": 0,
            "failed_rows": 0,
            "invalid_rows": [],
        }
        for idx, row in enumerate(data_reader):
            if idx == 0:
                continue

            try:
                name, ISIN, asset_group = row[0], row[1], row[2]

                # 중복되지 않은 자산군인 데이터만 생성
                if not (name and ISIN and asset_group):
                    raise KeyError("row 데이터가 충분치 않습니다.")

                if Holding.objects.filter(name=name):
                    raise ValidationError("중복된 종목명이 존재합니다.")

                if Holding.objects.filter(isin=ISIN):
                    raise ValidationError("중복된 ISIN이 존재합니다.")

                Holding.objects.create(
                    name = name, 
                    isin = ISIN, 
                    asset_group = asset_group
                )
                result["success_rows"] += 1

            except Exception as e:
                result["failed_rows"] += 1
                result["invalid_rows"].append(
                    {"error row": idx + 1, "error detail": str(e)}
                )
                continue

            result["total_csv_rows"] += 1

        print(result)
        return result


def upload_asset_info(csv_asset_info):
    """
    자산 상세 CSV File Upload
    :param csv_asset_info:
    """
    with open(csv_asset_info) as in_file:
        data_reader = csv.reader(in_file)
        result = {
            "total_csv_rows": 0,
            "success_rows": 0,
            "failed_rows": 0,
            "invalid_rows": [],
        }
        for idx, row in enumerate(data_reader):
            if idx == 0:
                continue

            try:
                (
                    name,
                    company,
                    account_number,
                    account_name,
                    ISIN,
                    current_price,
                    holding_quantity,
                ) = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])

                if not (
                    name
                    and company
                    and account_number
                    and account_name
                    and current_price
                    and holding_quantity
                ):
                    raise ValidationError("row 데이터가 충분치 않습니다.")

                holding = Holding.objects.get(isin=ISIN)

                user = User.objects.get_or_create(name=name)[0]

                account = Account.objects.get_or_create(
                    account_name = account_name,
                    account_number = account_number,
                    user = user
                )[0]
                
                investment = Investment.objects.get_or_create(
                    account = account,
                    company = company
                )[0]

                user_holding = UserHolding.objects.get_or_create(
                    holding = holding,
                    user = user,
                    quantity = holding_quantity,
                    current_price = current_price
                )[0]

                result["success_rows"] += 1

            except Exception as e:
                result["failed_rows"] += 1
                result["invalid_rows"].append(
                    {"error row": idx + 1, "error detail": str(e)}
                )
                continue

            result["total_csv_rows"] += 1

        print(result)
        return result


def upload_asset_basic(csv_asset_basic):
    """
    기본 자산 CSV File Upload
    :param csv_asset_basic:
    """
    with open(csv_asset_basic) as in_file:
        data_reader = csv.reader(in_file)
        result = {
            "total_csv_rows": 0,
            "success_rows": 0,
            "failed_rows": 0,
            "invalid_rows": [],
        }
        test = {}
        for idx, row in enumerate(data_reader):
            if idx == 0:
                continue

            try:
                account_number, principal = row[0], row[1]
                if not (account_number and principal):
                    raise ValidationError("row 데이터가 충분치 않습니다.")

                account = Account.objects.get(account_number=account_number)
                investment = Investment.objects.get(account=account)
                investment.principal = principal
                investment.save()
                print(investment.principal)

                result["success_rows"] += 1

            except Exception as e:
                result["failed_rows"] += 1
                result["invalid_rows"].append(
                    {"error row": idx + 1, "error detail": str(e)}
                )
                continue

            result["total_csv_rows"] += 1
        
        print(result)
        return result


@transaction.atomic
def calculate_account_total_asset():
    try:
        accounts = Account.objects.all()
        for account in accounts:
            user_holdings = UserHolding.objects.filter(user=account.user)

            for user_holding in user_holdings:
                account.total_assessts += (
                    user_holding.current_price * \
                        user_holding.quantity
                )
            account.save()

    except Exception as e:
        transaction.set_rollback(rollback=True)
        raise ValidationError(str(e))


def execute_csv_uploader():
    """
    Execute all csv uploader function
    :return:
    """
    filename = os.path.join(dir_path, "../test_log.log")

    # Logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)
    logger.info("csv upload start..")

    upload_asset_group_info(CSV_ASSET_GROUP)
    upload_asset_info(CSV_ACCOUNT_ASSET)
    upload_asset_basic(CSV_ACCOUNT_BASIC)
    calculate_account_total_asset()

    logger.info("csv upload start.. end")


def start():
    """
    스케쥴러 실행
    - 실행 함수 : execute_csv_uploader
    - 주기 : 매일 06시 실행
    :return:
    """
    scheduler = BackgroundScheduler(timezone=TIME_ZONE)
    scheduler.add_job(
        execute_csv_uploader,
        id="execute_csv_uploader",
        trigger=CronTrigger(hour="6"),
        max_instances=1,
        replace_existing=True,
        coalesce=True,
    )
    scheduler.start()