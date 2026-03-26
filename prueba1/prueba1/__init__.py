import pymysql

# 1. Le decimos a Django que use PyMySQL como si fuera mysqlclient
pymysql.install_as_MySQLdb()

# 2. Forzamos la versión para que Django crea que tenemos la 2.2.1
pymysql.version_info = (2, 2, 1, "final", 0)