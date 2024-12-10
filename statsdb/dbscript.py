__package__ = "db"

import mysql.connector

def create_conn():
    conn = mysql.connector.connect(
        host='mysql.db.bot-hosting.net',
        port=3306,
        user='u230695_eE0kHIvC39',
        password='iw59b.Sx+Q@j91^AzDEHv9t^',
        database='s230695_dhDB'
    )
    if conn.is_connected():
        return conn

    return None
def drop_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
                        
        DROP TABLE IF EXISTS bonus
        DROP TABLE IF EXISTS nation
        DROP TABLE IF EXISTS tech
    """)
    conn.commit()

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bonus (
                nationId INT AUTO_INCREMENT,
                bonusId INT,  
                PRIMARY KEY (nationId, bonusId),   
                bonus TEXT,
                value TEXT,
                startYear DATE,
                endYear DATE,
                event TEXT
                FOREIGN KEY (nationId) REFERENCES nation(nationId),         
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nation (
                nationId INT AUTO_INCREMENT PRIMARY KEY,
                nationName TEXT,
                population INTEGER,
                gdp INTEGER,
                popGrowth FLOAT,
                gdpGrowth FLOAT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tech (
                nationId INT,
                techId INT AUTO_INCREMENT,
                PRIMARY KEY (nationId, bonusId),
                FOREIGN KEY (nationId) REFERENCES nation(nationId),  
                techType TEXT,
                techTemplate TEXT,
                yearDesigned DATE,
                yearInService DATE,
                nationID INT,
            )
        """)
        conn.commit()
    except :
        print(f"Error")


def insert_bonus(conn, bonus, value, nationId, startYear, endYear, event):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bonus (bonus, value, nationId, startYear, endYear, event) VALUES (?, ?, ?, ?, ?, ?)", 
                    (bonus, value, nationId, startYear, endYear, event))
        conn.commit()
    except:
        errorHandler("insert") 

def read_bonus(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bonus")
        return cursor.fetchall()
    except:
            errorHandler("read")

def update_bonus(conn, bonus, value, nationId, startYear, endYear, event):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE bonus SET value = ?, nationId = ?, startYear = ?, endYear = ?, event = ? WHERE bonus = ?", 
                       (value, nationId, startYear, endYear, event, bonus))
        conn.commit()
    except:
        errorHandler("update")

def delete_bonus(conn, bonus):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bonus WHERE bonus = ?", (bonus,))
        conn.commit()
    except:
        errorHandler("delete")

def errorHandler(place):
    print("At"+ place + " An error occurred:")

def initiate():    
    try:
        with create_conn() as conn:
            drop_tables(conn)
            create_tables(conn)
            # Example CRUD operations
            insert_bonus(conn, 'Holiday Bonus', '1000', 'USA', '2023-01-01', '2023-12-31', 'New Year')
            bonuses = read_bonus(conn)
            print("Bonuses:", bonuses)
            update_bonus(conn, 'Holiday Bonus', '1500', 'USA', '2023-01-01', '2023-12-31', 'New Year')
            bonuses = read_bonus(conn)
            print("Updated Bonuses:", bonuses)
            delete_bonus(conn, 'Holiday Bonus')
            bonuses = read_bonus(conn)
            print("Bonuses after deletion:", bonuses)
    except:
        print("Failed to open database:")