import psycopg2
import random
import time
from datetime import datetime, timedelta
from face_scope.src.connect_to_database.mysql_conn import get_conn


def batch_insert(table_name, columns, data_list):
    conn = get_conn()  # 确保这个函数返回一个有效的数据库连接
    cursor = conn.cursor()

    # 构建 SQL 插入语句
    placeholders = ', '.join(['%s'] * len(columns))  # 为每个列生成一个占位符
    columns_formatted = ', '.join(columns)
    sql = f"INSERT INTO ots.{table_name} ({columns_formatted}) VALUES ({placeholders})"

    try:
        # 批量执行插入操作
        cursor.executemany(sql, data_list)
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # 如果出错则回滚
    else:
        # 提交事务
        conn.commit()
    finally:
        # 关闭连接
        cursor.close()
        conn.close()

def generate_fake_data(number_of_records):
    data_list = []
    base_time = datetime.now()

    for i in range(1, number_of_records + 1):
        user_id = f'user_{random.randint(1, 100)}'  # 假设用户ID范围在1到100之间
        time_stamp = (base_time - timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')  # 生成时间戳
        ip = f'192.168.{random.randint(0, 255)}.{random.randint(0, 255)}'  # 生成假IP地址
        path = f'/example/path/{i}'  # 假设的文件路径
        sys_002 = f'value_{i}_002'
        sys_003 = f'value_{i}_003'
        sys_004 = f'value_{i}_004'
        create_by = f'creator_{i}'
        create_time = (base_time - timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
        update_by = f'updater_{i}'
        update_time = (base_time - timedelta(days=i, hours=-1)).strftime('%Y-%m-%d %H:%M:%S')
        status = random.choice([0, 1])  # 假设状态为0或1

        # 构造一条记录的数据，不包含id
        record = (user_id, time_stamp, ip, path, sys_002, sys_003, sys_004, create_by, create_time, update_by, update_time, status)
        data_list.append(record)

    return data_list


def create_record(user_id, ip, path, frame_face_position,status_default=0):
    # # 输出：人-id_时间_IP_picpath
    """
    根据提供的 user_id, ip 和 path 生成一条记录的数据，其他字段填充默认值，
    并返回一个包含所有这些值的列表。
    """
    # 使用当前时间作为 time、create_time 和 update_time 的值
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 默认值设置
    sys_002_default = ''
    sys_003_default = ''
    position = frame_face_position
    create_by_default = current_time
    update_by_default = None
    status_default = status_default  # 假设默认的 status 值为 0

    # 将所有的值组装成一个列表
    record = [
        user_id, current_time, ip, path,
        sys_002_default, sys_003_default, position,
        create_by_default, current_time,  # create_time 使用 current_time
        update_by_default, update_by_default,  # update_time 也使用 current_time
        status_default
    ]

    return record

def insert_batch_insert_into_sys_register(data_records):
    table_name = 'sys_register'
    columns = ['user_id', 'time', 'ip', 'path', 'sys_002', 'sys_003', 'position', 'create_by', 'create_time',
               'update_by', 'update_time', 'status']

    batch_insert(table_name, columns, data_records)

    print("批量插入成功")


if __name__ == "__main__":

    # 生成10条假数据记录
    fake_data_records = generate_fake_data(1)

    # 打印生成的假数据
    # for record in fake_data_records:
    #     print(record)
    # print("\n")

    result = create_record("user_1", "192.168.0.28", "/img/1.jpg")
    print(result)
    fake_data_records.append(result)

    # 使用示例
    insert_batch_insert_into_sys_register(fake_data_records)


