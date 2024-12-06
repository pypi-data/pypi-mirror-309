from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Truncate a specific table with optional RESTART IDENTITY and CASCADE"

    def add_arguments(self, parser):
        parser.add_argument(
            "table_name", type=str, help="Name of the table to truncate"
        )
        parser.add_argument(
            "--restart-identity",
            action="store_true",
            help="Restart identity columns (default: False)",
        )
        parser.add_argument(
            "--cascade",
            action="store_true",
            help="Apply CASCADE to the truncation (default: False)",
        )

    def handle(self, *args, **kwargs):
        table_name = kwargs["table_name"]
        restart_identity = kwargs["restart_identity"]
        cascade = kwargs["cascade"]

        # Build the SQL command dynamically based on the arguments
        truncate_query = f'TRUNCATE TABLE "{table_name}"'
        if restart_identity:
            truncate_query += " RESTART IDENTITY"
        if cascade:
            truncate_query += " CASCADE"
        truncate_query += ";"

        try:
            with connection.cursor() as cursor:
                cursor.execute(truncate_query)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully truncated table "{table_name}" with options: '
                    f"RESTART IDENTITY={restart_identity}, CASCADE={cascade}."
                )
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Error truncating table '{table_name}': {e}")
            )
