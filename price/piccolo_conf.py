from piccolo.engine.sqlite import SQLiteEngine
from piccolo.conf.apps import AppRegistry

DB = SQLiteEngine(path='/tmp/cache.db')

#APP_REGISTRY = AppRegistry(
    #apps=["home.piccolo_app", "piccolo_admin.piccolo_app"]
#)