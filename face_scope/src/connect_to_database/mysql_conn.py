import psycopg2

from face_scope.src.connect_to_database.config import mysql_db, mysql_password, mysql_user, mysql_host, mysql_port


def get_conn():
    conn = psycopg2.connect(
        dbname=mysql_db,
        user=mysql_user,
        password=mysql_password,
        host=mysql_host,
        port=mysql_port)
    return conn

get_conn()