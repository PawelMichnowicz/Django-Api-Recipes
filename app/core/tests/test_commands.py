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
# .check - provided by BaseCommand (check method)
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        patched_check.return_value = True  # when check is call - return True

        call_command('wait_for_db')  # simulate running command

        # check if command is called once with correct db
        patched_check.assert_called_once_with(databases=['default'])

    # it replace sleep function with magic mock object,
    # thanks that sleep is not execute during testing
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        # simulate situation with 5 errors in row
        patched_check.side_effect = [Psycopg2Error] * 3 + \
                                    [OperationalError] * 2 + \
                                    [True]

        call_command('wait_for_db')

        # check if command was called 6 times
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
