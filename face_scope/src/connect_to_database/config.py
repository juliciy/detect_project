

#开发环境
import psycopg2

#老库？
# mysql_host = '222.240.1.180'
# mysql_user = 'work'
# mysql_password = 'Work2021'
# mysql_db = 'work'
# mysql_port = 3306

# ——————————刘11.14换了数据库
# postgresql数据库
# db.src.design:5432
# username: cloud
# password: Cloud@20230614

# mysql_host = '192.168.1.4'
# mysql_user = 'work'
# mysql_password = 'Work2021'
# mysql_db = 'work'
# mysql_port = 3306


#刘11.17更换了数据库
mysql_db="cloud"
mysql_user="cloud"
mysql_password="1qaz2wsx@cloud"
mysql_host="192.168.0.2"
mysql_port = 5432


#正式环境

# mysql_host = '127.0.0.1'
# mysql_user = 'work'
# mysql_password = 'Work@20220929'
# mysql_db = 'work'
# mysql_port = 3306
#
# mysql_host = '10.90.57.171'
# mysql_user = 'work'
# mysql_password = 'Work@20220929'
# mysql_db = 'work'
# mysql_port = 3306



riyi_minutes=60
long_riyi_minutes=60*24*10
yichang_minutes=60
long_yichang_minutes=60*24*10

#开发环境
flow_minutes=60*2
#数据异常
long_flow_minutes=60*24*10
#正式环境
#flow_minutes=60*2

#开发环境
pipe_diff_pressure_minutes=60*24
#正式环境
#pipe_diff_pressure_minutes=60*24

min_inlet_pressure=0.0
max_outlet_pressure=8.5


