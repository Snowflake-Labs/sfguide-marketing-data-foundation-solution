import os
from enum import Enum
from services.session import is_local


# Costant privileges
SNOWFLAKEDB = 'IMPORTED PRIVILEGES ON SNOWFLAKE DB'
EXECUTETASK = 'EXECUTE TASK'
MANAGETASK = 'MANAGE TASK'


# Validates the app is running in snowflake and that the premission is not already active
# Return true is persion is already granted
def request_account_privileges(privileges: list) -> bool:
    if is_local(): return True
    import snowflake.permissions as permissions
    if permissions.get_held_account_privileges(privileges): return True
    permissions.request_account_privileges(privileges)
