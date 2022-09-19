import os
import django
import csv
import sys

from django.db import IntegrityError, transaction

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", 
    "backend.settings.base"
)
django.setup()

from apis.models import *

CSV_PATH_ACCOUNT_ASSET = './csv/account_asset_info_set.csv'
CSV_PATH_ACCOUNT_BASIC = './csv/asset_basic_info_set.csv'
CSV_PATH_ASSET_GROUP = './csv/asset_group_info_set.csv'


try:
    with transaction.atomic():
        """
        account_group_info_set uploader
        """
        with open(CSV_PATH_ASSET_GROUP) as in_file:
            data_reader = csv.reader(in_file)
            for row in data_reader:
                
                Holding(
                    name=row[0], 
                    isin=row[1],
                    asset_group=row[2]
                ).save()


        """
        account_asset_info_set uploader
        """
        with open(CSV_PATH_ACCOUNT_ASSET) as in_file:
            data_reader = csv.reader(in_file)
            for row in data_reader:

                for user in User.objects.all():
                    if row[0] == user.name and row[2] == user.account_set.account_number:
                        continue
                    User.objects.create(
                        name=row[0]
                    )

                    Account.objects.create(
                        account_name=row[3],
                        account_number=row[2],
                        user=row[0]
                    )

                Investment.objects.create(
                    user=row[0],
                    company=row[1]
                )

                holding = Holding.objects.get(isin=row[4])
                holding.current_price = row[5]
                holding.save()

                UserHolding.objects.create(
                    user = row[0],
                    holding = holding,
                    quantity = row[7]
                )

        """
        account_group_info_set uploader
        """
        with open(CSV_PATH_ACCOUNT_BASIC) as in_file:
            data_reader = csv.reader(in_file)
            for row in data_reader:
                
                account = Account.objects.get(account_number=row[0])
                account.account_number = row[1]
                account.save()

except IntegrityError:
    raise IntegrityError