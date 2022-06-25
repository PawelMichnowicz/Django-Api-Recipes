'''
Test custom Djano management commands
'''
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# patch - this is command that we are going to be mocking 
# and it adding a new argument for each calls - patched_check
@patch('core.management.commands.wait_for_db.Command.check') # .check provided by BaseCommand (check method)
class CommandTest(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        patched_check.return_value = True # when check is call - return True

        call_command('wait_for_db') # simulate running command

        patched_check.assert_called_once_with(databases=['default']) # check if command is called once with correct db

    @patch('time.sleep') # it replace sleep function with magic mock object, thanks that sleep is not execute during testing
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        patched_check.side_effect = [Psycopg2Error] * 3 + [OperationalError] * 2 + [True]  # simulate situation with 5 errors in row

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6) #check if command was called 6 times 
        patched_check.assert_called_with(databases=['default'])