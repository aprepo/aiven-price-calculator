from piccolo.table import Table
from piccolo.columns import Varchar, Numeric


class Plan(Table, tablename='plans'):
    project_name = Varchar(length=255)
    service_type = Varchar(length=50)
    plan = Varchar(length=50)
    region = Varchar(length=50)
    price = Numeric()
