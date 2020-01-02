import fdb
import datetime
import time

from lib.timeout import timeout
from credentials import credentials

# ===========
# known bugs:
# ===========
# Ignoring DESCTEMPO.  It should subtract it from the dataini WHERE clause


con = None


def new_cursor():
    while True:
        try:
            if con == None:
                reset_fdb_connection()
            return con.cursor()

        except Exception as e:
            reset_fdb_connection()
            print("ERROR: Could not create firebird cursor")
            raise e
            time.sleep(1 * 10)


def reset_fdb_connection():
    global con
    while True:

        try:
            con.rollback()
            print('database rollback executed sucessfully')
        except Exception as e:
            print('could not rollback transaction')
            print(e)

        try:
            con = fdb.connect(
                        **credentials,
                        sql_dialect=1,
                        charset='UTF8'
                    )
            return con
        except Exception as e:
            print("----------------------")
            print("ERROR: Can't connect do firebird database")
            print(e)
            time.sleep(1 * 60)


# horaini=10:01
# tipopag=Cabine
# desctempo=00:00

def get_curdatetime():

    cursor = new_cursor()
    cursor.execute("select cast('now' as date) from rdb$database")
    cur_datetime = cursor.fetchall()[0][0]
    # ignore seconds and microseconds
    return cur_datetime.replace(second=0, microsecond=0)



def make_time(hour, minute):
    return get_curdatetime().replace(hour=hour, minute=minute)

def sgl_to_time(s):
    return make_time(int(s[0:2]), int(s[3:5]))

def time_to_sgl(t):
    return '{0}:{1}'.format(str(t.hour).zfill(2),
            str(t.minute).zfill(2)) 

def apply_cabine3_disccount():    

    def get_max_horaini():
        dt_subtraction = datetime.timedelta(hours=2, minutes=59)
        return time_to_sgl(get_curdatetime() - dt_subtraction)

    # reset_fdb_connection()

    sql = ("UPDATE movimento SET tipopag='Cabine3' "
           "WHERE tipopag='Cabine' "
           "AND horaini <= '{0}'".format(get_max_horaini()))

    return new_cursor().execute(sql)

while True:
    now = '{:%Y-%m-%d %H:%M:%S} -> '.format(datetime.datetime.now())
    try:
        with timeout(7):
            apply_cabine3_disccount()
            con.commit()
            print(now + 'Cabine3 SQL Disccount command executed sucessfully executed')
    except Exception as e:
        print('----------------')
        print(now + 'ERROR: There was a problem executing SQL cabine3 discount command')
        print(e)
        reset_fdb_connection()
    finally:
        time.sleep(1 * 60)
