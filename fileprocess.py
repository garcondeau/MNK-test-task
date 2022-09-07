import platform
import subprocess
import os

import pandas as pd
from sqlalchemy import create_engine

from consts import db_info


def unpack_file(file):
    if platform.system() == "Windows":
        unrar_tool = "7z/windows/7z.exe x"
    elif platform.system() == "Darwin":
        unrar_tool = "7z/darwin/7zz"
    else:
        unrar_tool = "7z/linux/7zz"

    subprocess.run([unrar_tool, "x", file, '-o./extracted', "-y"])


def update_db():
    global mydb
    try:
        mydb = create_engine(
            "mysql+pymysql://" + db_info["DB_USER"] + ":" + db_info["DB_PSSWD"] + "@" + db_info["DB_HOST"] + "/" +
            db_info["DB_NAME"])
    except:
        print("Error while connecting to MySQL")
    mydb.engine.execute(f"CREATE DATABASE IF NOT EXISTS {db_info['DB_NAME']};")

    mydb.engine.execute(f"USE {db_info['DB_NAME']};")
    # sql = 'SELECT  main_part_number, manufacturer, category, origin, IFNULL(deposit.deposit, 0) AS deposit, price.price, REPLACE(quantity.quantity, " > ", "") as quantity, quantity.warehouse, IFNULL(price + deposit.deposit, price) AS total FROM data LEFT JOIN deposit ON data.part_number = deposit.part_number JOIN price ON data.part_number = price.part_number JOIN quantity ON data.part_number = quantity.part_number WHERE quantity.warehouse = "A" OR quantity.warehouse = "H" OR quantity.warehouse = "J" OR quantity.warehouse = "3" OR quantity.warehouse = "9" AND (price + deposit.deposit) > 2 UNION SELECT main_part_number, manufacturer, category, origin, IFNULL(deposit.deposit, 0) AS deposit, price.price, REPLACE(quantity.quantity, " > ", "") as quantity, quantity.warehouse, IFNULL(price + deposit.deposit, price) AS total FROM data RIGHT JOIN deposit ON data.part_number = deposit.part_number JOIN price ON data.part_number = price.part_number JOIN quantity ON data.part_number = quantity.part_number WHERE quantity.warehouse = "A" OR quantity.warehouse = "H" OR quantity.warehouse = "J" OR quantity.warehouse = "3" OR quantity.warehouse = "9" AND (price + deposit.deposit) > 2'
    #chunks = []
    #
    # for chunk in pd.read_sql(sql, mydb, chunksize=1000):
    #     chunks.append(chunk)
    #     print(chunk)
    # print(len(chunks))
    # result = pd.concat(chunks, ignore_index=True)
    # print(type(result))
    # print(result)
    # df_new = pd.read_sql(sql, mydb)
    for file in os.listdir("extracted"):
        if file.endswith(".txt"):
            read_file = pd.read_csv(rf'extracted/{file}')
            read_file.to_csv(rf'extracted/{file}.csv', sep="\t", index=None)
            csv_chunks = pd.read_csv(f"extracted/{file}", sep="\t", chunksize=10000)
            df = pd.concat(chunk for chunk in csv_chunks)
            df.to_sql(name="weight", con=mydb, if_exists='replace', index=True)
        else:
            csv_chunks = pd.read_csv(f"extracted/{file}", sep=";", chunksize=10000)
            data = pd.concat(chunk for chunk in csv_chunks)
            df = pd.DataFrame(data)
            mydb.engine.execute(f"USE {db_info['DB_NAME']};")
            match file:
                case "data.csv":
                    df.to_sql(name="data", if_exists='replace', con=mydb, index=True)
                case "deposit.csv":
                    df.to_sql(name="deposit", con=mydb, if_exists='replace', index=True)
                case "price.csv":
                    df.to_sql(name="price", con=mydb, if_exists='replace', index=True)
                case "quantity.csv":
                    df.to_sql(name="quantity", con=mydb, if_exists='replace', index=True)


def process_file(file):
    # unpack_file(file)
    update_db()


update_db()
