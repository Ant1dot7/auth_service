from enum import Enum


class RoleEnum(str, Enum):
    superuser = 'superuser'
    admin = 'admin'
    employee = 'employee'
    customer = 'customer'
