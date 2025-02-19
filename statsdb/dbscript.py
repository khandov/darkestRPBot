__package__ = "db"

import mysql.connector
import json
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def create_conn():
    conn = mysql.connector.connect(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE')
    )
    if conn.is_connected():
        return conn

    return None
def drop_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS bonus
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS tech
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS nation
    """)
    conn.commit()

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nation (
                nationId INT AUTO_INCREMENT PRIMARY KEY,
                nationName TEXT UNIQUE,
                population BIGINT,
                gdp BIGINT,
                popGrowth FLOAT,
                gdpGrowth FLOAT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bonus (
                bonusId INT AUTO_INCREMENT PRIMARY KEY,
                bonusName TEXT UNIQUE,
                bonus VARCHAR(255),
                value BIGINT,
                nationId INT,
                startYear INT,
                endYear INT,
                post TEXT,
                FOREIGN KEY (nationId) REFERENCES nation(nationId)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tech (
                techId INT AUTO_INCREMENT PRIMARY KEY,
                techName TEXT UNIQUE,
                techType TEXT,
                techTemplate TEXT,
                yearDesigned DATE,
                yearInService DATE,
                nationID INT,
                FOREIGN KEY (nationID) REFERENCES nation(nationId)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS date (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def insert_nation(conn, nationName, population, gdp, popGrowth, gdpGrowth):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO nation (nationName, population, gdp, popGrowth, gdpGrowth)
            VALUES (%s, %s, %s, %s, %s)
        """, (nationName, population, gdp, popGrowth, gdpGrowth))
        conn.commit()
        return f"Nation {nationName} added successfully"	
    except mysql.connector.Error as sql_error:
        return f"SQL error: {sql_error}"
    except Exception as e:
        print(f"Error: {e}")

def read_nation(conn, nation=None):
    if(nation == None):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM nation")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM nation WHERE nationName = %s", (nation,))
            result = cursor.fetchall()
            return result[0]
        except Exception as e:
            print(f"Error: {e}")


def update_nation(conn, nationName, population=None, gdp=None, popGrowth=None, gdpGrowth=None):
    try:
        fields_to_update = []
        values = []
        if population is not None:
            fields_to_update.append("population = %s")
            values.append(population)
        if gdp is not None:
            fields_to_update.append("gdp = %s")
            values.append(gdp)
        if popGrowth is not None:
            fields_to_update.append("popGrowth = %s")
            values.append(popGrowth)
        if gdpGrowth is not None:
            fields_to_update.append("gdpGrowth = %s")
            values.append(gdpGrowth)

        cursor = conn.cursor()
        if fields_to_update:
            query = f'''
                UPDATE nation
                SET {', '.join(fields_to_update)}
                WHERE nationName = %s
            '''
            values.append(nationName)
            cursor.execute(query, values)
            conn.commit()
        else:
            print("No fields to update")
    except Exception as e:
        print(f"Error: {e}")

def delete_nation(conn, nationName):
    try:
        cursor = conn.cursor()
        nation = read_nation(conn, nationName)
        #delete all techs associated with the nation
        cursor.execute("DELETE FROM tech WHERE nationId = %s", (nation[0],))
        #delete all bonuses associated with the nation
        cursor.execute("DELETE FROM bonus WHERE nationId = %s", (nation[0],))
        #finally remove the nation
        cursor.execute("DELETE FROM nation WHERE nationId = %s", (nation[0],))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

# CRUD functions for the tech table
def insert_tech(conn, techName, techType, techTemplate, yearDesigned, yearInService, nationName: None):
    try:
        cursor = conn.cursor()
        if nationName is None:
            print(f"Error: Nation '{nationName}' not found.")
            return
        nation = read_nation(conn, nationName)
        #convert yearDesigned to date
        yearDesigned = yearDesigned + "-01-01"
        #convert yearInService to date
        yearInService = yearInService + "-01-01"
        cursor.execute("""
            INSERT INTO tech (techName, techType, techTemplate, yearDesigned, yearInService, nationId)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (techName, techType, techTemplate, yearDesigned, yearInService, nation[0]))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def read_tech(conn,nationName=None):
    if (nationName == None):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tech")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            nation = read_nation(conn, nationName)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tech WHERE nationId = %s", (nation[0],))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")

def update_tech(conn, techId, techName=None, techType=None, techTemplate=None, yearDesigned=None, yearInService=None, nationName=None):
    try:
        fields_to_update = []
        values = []
        if techName is not None:
            fields_to_update.append("techName = %s")
            values.append(techName)
        if techType is not None:
            fields_to_update.append("techType = %s")
            values.append(techType)
        if techTemplate is not None:
            fields_to_update.append("techTemplate = %s")
            values.append(techTemplate)
        if yearDesigned is not None:
            fields_to_update.append("yearDesigned = %s")
            values.append(yearDesigned)
        if yearInService is not None:
            fields_to_update.append("yearInService = %s")
            values.append(yearInService)
        if nationName is not None:
            fields_to_update.append("nationID = %s")
            nation = read_nation(conn, nationName)
            values.append(nation[0])

        cursor = conn.cursor()
        if fields_to_update:
            query = f'''
                UPDATE tech
                SET {', '.join(fields_to_update)}
                WHERE techId = %s
            '''
            values.extend([techId])
            cursor.execute(query, values)
            conn.commit()
        else:
            print("No fields to update")
    except Exception as e:
        print(f"Error: {e}")

def delete_tech(conn, techName):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tech WHERE techName = %s", (techName,))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def insert_bonus(conn, bonus, value, nationName: None, startYear, endYear, post):
    try:
        cursor = conn.cursor()
        if nationName is None:
            print(f"Error: no Nation name given.")
            return
        nation = read_nation(conn, nationName)
        if nation[0]:
            cursor.execute("""
                INSERT INTO bonus (bonus, value, nationId, startYear, endYear, post)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (bonus, value, nation[0], startYear, endYear, post))
            conn.commit()
        else :
            print(f"Error: Name '{nationName}' is invalid.")
    except Exception as e:
        print(f"Error: {e}")

def read_bonus(conn, nation):
    if(nation == None):
        print("No nation specified")
        return
    try:
        if nation[0]:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bonus WHERE nationId = %s", (nation[0],))
            payload = cursor.fetchall()
            if(len(payload) == 0):
                print(f"Error: No bonuses found for '{nation[1]}'.")
                return
            return payload
        else :
            print(f"Error: Name '{nation[1]}' is invalid.")
    except Exception as e:
        print(f"Error: {e}")

def update_bonus(conn, bonusId, bonusType=None, value=None, nation_name=None, startYear=None, endYear=None, event=None):
    try:
        fields_to_update = []
        values = []
        if bonusType is not None:
            fields_to_update.append("bonus = %s")
            values.append(bonusType)
        if value is not None:
            fields_to_update.append("value = %s")
            values.append(value)
        if nation_name is not None:
            fields_to_update.append("nationId = %s")
            nation = read_nation(conn, nation_name)
            values.append(nation[0])
        if startYear is not None:
            fields_to_update.append("startYear = %s")
            values.append(startYear)
        if endYear is not None:
            fields_to_update.append("endYear = %s")
            values.append(endYear)
        if event is not None:
            fields_to_update.append("event = %s")
            values.append(event)

        cursor = conn.cursor()
        if fields_to_update:
            query = f'''
                UPDATE bonus
                SET {', '.join(fields_to_update)}
                WHERE bonusId = %s
            '''
            values.append(bonusId)
            cursor.execute(query, values)
            conn.commit()
        else:
            print("No fields to update")
    except Exception as e:
        print(f"Error: {e}")

def delete_bonus(conn, bonusId):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bonus WHERE bonusId = %s", (bonusId,))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def errorHandler(place):
    print("At"+ place + " An error occurred:")

def alterDatabase():
    try:
        with create_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE nation MODIFY gdp BIGINT")
            cursor.execute("ALTER TABLE nation MODIFY population BIGINT")
            cursor.execute("ALTER TABLE bonus MODIFY value BIGINT")
            
    except Exception as e:
        print("Failed to open database:",e)

def updateDate(conn, date):
    try:
        checkExists = getDate(conn)
        if checkExists == -1:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO date (name, date) VALUES (%s, %s)", ('darkesthour', date))
            conn.commit()
        else:
            cursor = conn.cursor()
            cursor.execute("UPDATE date SET date = %s WHERE name = darkesthour", (date,))
            conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def getDate(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT date FROM date WHERE name = darkesthour")
        conn.commit()
        row = cursor.fetchone()
        return row[0] if row else -1
    except Exception as e:
        print(f"Error: {e}")

def backupDatabase():
    try:
        with create_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM nation")
            nations = cursor.fetchall()
            cursor.execute("SELECT * FROM tech")
            techs = cursor.fetchall()
            cursor.execute("SELECT * FROM bonus")
            bonuses = cursor.fetchall()
            cursor.execute("SELECT * FROM date")
            date = cursor.fetchall()
            
            backup_data = {
                "nations": nations,
                "techs": techs,
                "bonuses": bonuses,
                "date": date
            }
            
            with open('backup.json', 'w') as f:
                json.dump(backup_data, f)
                
            print("Backup successful")
    except Exception as e:
        print("Failed to open database:", e)

def restoreDatabase():
    try:
        with open('backup.json', 'r') as f:
            backup_data = json.load(f)
            
        with create_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("TRUNCATE TABLE nation")
            cursor.execute("TRUNCATE TABLE tech")
            cursor.execute("TRUNCATE TABLE bonus")
            cursor.execute("TRUNCATE TABLE date")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            for nation in backup_data["nations"]:
                cursor.execute("INSERT INTO nation (nationId, nationName, population, gdp, popGrowth, gdpGrowth) VALUES (%s, %s, %s, %s, %s, %s)", nation)
            for tech in backup_data["techs"]:
                cursor.execute("INSERT INTO tech (techId, techName, techType, techTemplate, yearDesigned, yearInService, nationId) VALUES (%s, %s, %s, %s, %s, %s, %s)", tech)
            for bonus in backup_data["bonuses"]:
                cursor.execute("INSERT INTO bonus (bonusId, bonusName, bonus, value, nationId, startYear, endYear, post) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", bonus)
            for date in backup_data["date"]:
                cursor.execute("INSERT INTO date (id, name, date) VALUES (%s, %s, %s)", date)
                
            conn.commit()
            print("Restore successful")
    except Exception as e:
        print("Failed to restore database:", e)