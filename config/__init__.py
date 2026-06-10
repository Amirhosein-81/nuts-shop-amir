try:
    import mysqlclient
except ImportError:
    import pymysql
    pymysql.install_as_MySQLdb()
    
    # گول زدن چک‌کننده‌های سخت‌گیر جنگو با یک ورژن بالاتر
    pymysql.__version__ = '3.0.0'
    pymysql.version_info = (3, 0, 0, 'final', 0)