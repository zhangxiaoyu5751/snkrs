# -*- coding: utf-8 -*-

import sqlite3
import config


class ConnSqlite(object):
    def __init__(self, dbInfo):
        self._dbInfo = dbInfo
        self._conn = None

    def __connect(self):
        try:
            if self._conn is not None:
                return True, None

            self._conn = sqlite3.connect(self._dbInfo['name'])
            return True, None
        except Exception as e:
            err_msg = "connect error, reason: %s, info: %s" % (str(e), str(self._dbInfo))
            return False, err_msg

    def __excute(self, sql):

        if not sql:
            return False, "bad argument"

        (success, msg) = self.__connect()

        if not success:
            return False, msg

        try:
            cursor = self._conn.cursor()
            affect = cursor.execute(sql)
            self._conn.commit()

        # cursor.close()
        # self._conn.close()
            return True, affect
        except Exception as e:
            self._conn.rollback()
            return False, "execute error, err msg: %s, sql: %s" % (e, sql)

    def insert(self, sql):
        return self.__excute(sql)

    def update(self, sql):
        return self.__excute(sql)

    def delete(self, sql):
        return self.__excute(sql)

    def query_one(self, sql):
        try:
            if self._conn is None:
                self._conn = sqlite3.connect(self._dbInfo['name'])
            cursor = self._conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            # cursor.close()
            # self._conn.close()
            return True, result
        except Exception as e:
            return False, "query error, reason: %s" % (e,)

    def query_all(self, sql):
        try:
            if self._conn is None:
                self._conn = sqlite3.connect(self._dbInfo['name'])
            cursor = self._conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()

            # cursor.close()
            # self._conn.close()
            return True, result
        except Exception as e:
            return False, "query error, reason: %s" % (e,)


if __name__ == '__main__':
    a = ConnSqlite(config.db_info)
    # 'shoe_name': h5_content,
    # 'shoe_intro': h1_content,
    # 'shoe_sell_time': sell_time,
    # 'shoe_price': sell_price

#     sql = '''create table shoe_info (
# id INTEGER PRIMARY KEY autoincrement,
# shoe_uniq_desc text,
# shoe_name text,
# shoe_intro text,
# shoe_sell_time text,
# shoe_price text,
# update_time datetime default(datetime('now', 'localtime')))'''
#     b = a.insert(sql)
#     print(b)
#
    # sql1 = ''' insert into shoe_info (shoe_name, shoe_intro, shoe_price) values ('阿萨德', 'asd', '1299')
    # '''
    # c = a.insert(sql1)
    # print(c)
    import datetime
    sql = 'select * from shoe_info where update_time >{0} '''.format(datetime.datetime.now().strftime('%Y-%m-%d'))
    print(sql)
    c = a.query_all(sql)
    print(c)
    # for item in c[1]:
    #     print(item)

