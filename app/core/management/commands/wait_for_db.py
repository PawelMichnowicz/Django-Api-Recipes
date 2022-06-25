'''
Django command to wait for the database to be available
'''

import time

from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    ''' Django command to wait for database '''

    def handle(self, *args, **options):  # handle - actual logic
        self.stdout.write('Waiting for databese...')
        db_up = False

        while db_up is False:
            try:
                # BaseCommand.check - check entire django project,
                # in this case check if databes is default, noqa
                self.check(databases=['default'])
                db_up = True
            except(Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Databaseis ready'))
