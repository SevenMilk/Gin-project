import requests
import xmltodict
import hashlib
import pandas as pd
import mysql.connector
from DBSecrets import DBParams


def db_connect():
    mydb = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
    )
    return mydb


def init_db(mycursor):
    # create databases
    mycursor.execute("CREATE TABLE {} (uk VARCHAR(32) UNIQUE KEY,\
                                       id INT,\
                                       name VARCHAR(255),\
                                       address VARCHAR(255),\
                                       lat FLOAT,\
                                       lng FLOAT,\
                                       locname VARCHAR(255),\
                                       img VARCHAR(255),\
                                       intro VARCHAR(255),\
                                       icon VARCHAR(255),\
                                       type VARCHAR(255))"
                     .format(TABLE))
    mycursor.execute("create index id_index on {}(id)".format(TABLE))


def check_db(mycursor):
    try:
        mycursor.execute("SELECT * FROM {}".format(TABLE))
        return False
    except Exception as e:
        print(e, "create table {}".format(TABLE))
        return True


def md5_encode(data):
    md5_word = hashlib.md5()
    md5_word.update(data.encode('UTF-8'))
    return md5_word.hexdigest()


def import_data():
    return requests.get("https://smartcity.taipei/xml.xml?category=0").content


def transform(data):
    df = pd.DataFrame(xmltodict.parse(data)["markers"]["marker"])
    df.rename(columns={'@id': 'id', '@name': 'name', '@address': 'address',
                       '@lat': 'lat', '@lng': 'lng', '@locname': 'locname',
                       '@img': 'img', '@intro': 'intro', '@icon': 'icon',
                       '@type': 'type'}, inplace=True)
    df = df.applymap(lambda x: x.strip(" "))
    df["uk"] = df['id']+df['name']+df['lat']+df['lng']+df['locname']+df['type']
    df["uk"] = df["uk"].apply(md5_encode)

    return df


def output(df, mycursor, mydb):
    insert_data = ("insert IGNORE into customers (id,name,address,lat,lng,\
                                                  locname,img,intro,icon,type,uk)\
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)\
                    ON DUPLICATE KEY UPDATE uk=VALUES(uk)")
    for row in df.values.tolist():
        mycursor.execute(insert_data, tuple(row))


def main():
    data = import_data()
    df = transform(data)
    mydb = db_connect()
    mycursor = mydb.cursor(buffered=True)
    if check_db(mycursor):
        init_db(mycursor)
    output(df, mycursor, mydb)
    mydb.commit()
    mycursor.close()
    mydb.close()


if __name__ == '__main__':
    db_params = DBParams()
    HOST = db_params.db_host.get_secret_value()
    USER = db_params.db_username.get_secret_value()
    PASSWORD = db_params.db_password.get_secret_value()
    DATABASE = db_params.db_database
    TABLE = db_params.db_table
    main()
