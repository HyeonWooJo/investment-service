import os
import django
import csv

from django.core.exceptions import ValidationError
from django.db import transaction 

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", 
    "backend.settings.base"
)
django.setup()

from apis.models import *

CSV_PATH_ACCOUNT_ASSET = './csv/account_asset_info_set.csv'
CSV_PATH_ACCOUNT_BASIC = './csv/account_basic_info_set.csv'
CSV_PATH_ASSET_GROUP = './csv/asset_group_info_set.csv'


def upload_asset_group_info(csv_asset_group):
    """
    자산군 csv file uploader
    :param: csv
    """
    with open(CSV_PATH_ASSET_GROUP) as in_file:
        data_reader = csv.reader(in_file)
        result = {
            "total_csv_rows": 0,
            "success_rows": 0,
            "failed_rows": 0,
            "invalid_rows": [],
        }
        for idx, row in enumerate(data_reader):
            try:
                name, isin, asset_group = row[0], row[1], row[2]

                # 중복되지 않은 자산군인 데이터만 생성
                if not (name and isin and asset_group):
                    raise KeyError("row 데이터가 충분치 않습니다.")

                if Holding.objects.filter(name=name):
                    raise ValidationError("중복된 종목명이 존재합니다.")

                if Holding.objects.filter(isin=isin):
                    raise ValidationError("중복된 ISIN이 존재합니다.")

                Holding.objects.create(
                    name=name, 
                    isin=isin, 
                    asset_group=asset_group
                )
                result["success_rows"] += 1

            except Exception as e:
                result["failed_rows"] += 1
                result["invalid_rows"].append(
                    {"error row": idx + 1, "error detail": str(e)}
                )
                continue

            result["total_csv_rows"] += 1

        return result


def upload_asset_info(csv_asset_info):
    """
    자산 상세 CSV File Upload
    :param csv_asset_info:
    :param csv_asset_basic_info:
    :return:
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
            try:
                (
                    name,
                    brokerage,
                    account_number,
                    account_name,
                    ISIN,
                    current_price,
                    holding_quantity,
                ) = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])

                if not (
                    name
                    and brokerage
                    and account_number
                    and account_name
                    and current_price
                    and holding_quantity
                ):
                    raise ValidationError("row 데이터가 충분치 않습니다.")

                holding = Holding.objects.get(isin=ISIN)
                holding.current_price = current_price
                holding.save()

                user = User.objects.get_or_create(name=name)[0]

                account = Account.objects.get_or_create(
                    account_name=account_name,
                    account_number=account_number,
                )[0]
                
                investment = Investment.objects.get_or_create(
                    user=user,
                    brokerage=brokerage
                )[0]

                user_holding = UserHolding.objects.get_or_create(
                    holding=holding,
                    user=user
                )[0]

                user_holding.quantity = holding_quantity
                user_holding.save()

                result["success_rows"] += 1

            except Exception as e:
                result["failed_rows"] += 1
                result["invalid_rows"].append(
                    {"error row": idx + 1, "error detail": str(e)}
                )
                continue

            result["total_csv_rows"] += 1

        return result


def upload_asset_basic(csv_asset_basic):
    """
    기본 자산 CSV File Upload
    :param csv_asset_basic:
    :return:
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
            try:
                account_number, principal = row[0], row[1]
                if not (account_number and principal):
                    raise ValidationError("row 데이터가 충분치 않습니다.")

                account = Account.objects.get(account_number=account_number)
                investment = account.user.investment_set
                investment.principal = principal
                investment.save()

                result["success_rows"] += 1

            except Exception as e:
                result["failed_rows"] += 1
                result["invalid_rows"].append(
                    {"error row": idx + 1, "error detail": str(e)}
                )
                continue

            result["total_csv_rows"] += 1
        return result


@transaction.atomic
def calculate_account_total_asset():
    try:
        users = User.objects.all()
        for user in users:
            user_account = user.account_set
            user_account.total_assets = 0

            for user_holding in user.userholding_set.all():
                user_account.total_assets += (
                    user_holding.holding.current_price * \
                        user_holding.quantity
                )

            user_account.save()

    except Exception as e:
        transaction.set_rollback(rollback=True)
        raise ValidationError(str(e))


if __name__ == "__main__":
    upload_asset_group_info(CSV_PATH_ASSET_GROUP)
    upload_asset_info(CSV_PATH_ACCOUNT_ASSET)
    upload_asset_basic(CSV_PATH_ACCOUNT_BASIC)