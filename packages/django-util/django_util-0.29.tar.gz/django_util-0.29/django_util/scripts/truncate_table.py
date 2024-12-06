from django.db import connection


def run(*args):
    """
    Truncate a specific table with optional RESTART IDENTITY and CASCADE.
    Usage:
    python manage.py runscript truncate_table --script-args table_name [restart_identity] [cascade]
    """
    if not args or len(args) < 1:
        print(
            "Usage: python manage.py runscript truncate_table --script-args table_name [restart_identity] [cascade]"
        )
        return

    table_name = args[0]
    restart_identity = "restart_identity" in args
    cascade = "cascade" in args

    # Build the TRUNCATE SQL query
    truncate_query = f'TRUNCATE TABLE "{table_name}"'
    if restart_identity:
        truncate_query += " RESTART IDENTITY"
    if cascade:
        truncate_query += " CASCADE"
    truncate_query += ";"

    try:
        with connection.cursor() as cursor:
            cursor.execute(truncate_query)
        print(
            f'Successfully truncated table "{table_name}" with options: '
            f"RESTART IDENTITY={restart_identity}, CASCADE={cascade}."
        )
    except Exception as e:
        print(f"Error truncating table '{table_name}': {e}")
