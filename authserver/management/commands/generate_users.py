import csv
import os

from authserver.forms import SignUpForm
from django.core.management.base import BaseCommand
import uuid


class Command(BaseCommand):
    help = 'Generates all user accounts'

    def handle(self, *args, **kwargs):
        with open('users.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    print(row[5])
                    username = row[5].split('@')[0]
                    body = {
                        'first_name': row[1],
                        'last_name': row[0],
                        'email': row[5],
                        'password1': f"sitech{row[3]}",
                        'password2': f"sitech{row[3]}",
                        'username': username
                    }
                    form = SignUpForm(body)
                    if form.is_valid():
                        user = form.save()
                        user.email_code = uuid.uuid4()
                        user.graduating_year = f"20{row[3]}"
                        user.save()
                        print(user.email_code)
                line_count += 1
