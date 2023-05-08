#IN JUPYTER NOTEBOOK- Connecting PYTHON to POSTGRES SERVER
pip install psycopg2
pip install tabulate

import psycopg2
from tabulate import tabulate

con = psycopg2.connect(
    host="localhost",
    database="cs623",
    user="postgres",
    password="******")
    
print(con)
    
#For isolation: SERIALIZABLE
con.set_isolation_level(3)
#For atomicity
con.autocommit = False

# 1.The product p1 is deleted from Product and Stock. 
try:
    cur = con.cursor()
    cur.execute("DELETE FROM product WHERE prodid = 'p1'")
#If we delete 'p1' from product the same 'p1' will be deleted in stock aslo because it is the child table containing foreign key constraints
    
except (Exception, psycopg2.DatabaseError) as err:
    print(err)
    print("Transactions could not be completed so database will be rolled back before start of transactions")
    con.rollback()
finally:
    if con:
        con.commit()
        cur.close
        con.close
        print("PostgreSQL connection is now closed")
#3.	The product p1 changes its name to pp1 in Product and Stock.
try:
    cur = con.cursor()
    cur.execute("UPDATE Product SET prodid = 'pp1' WHERE prodid = 'p1'")
#As we updated 'p1' to 'pp1', the same gets updated in stock table because it is the child table containing foreign key constraints

except (Exception, psycopg2.DatabaseError) as err:
    print(err)
    print("Transactions could not be completed so database will be rolled back before start of transactions")
    con.rollback()
finally:
    cur.execute("SET CONSTRAINTS ALL IMMEDIATE")

    if con:
        con.commit()
        cur.close
        con.close
        print("PostgreSQL connection is now closed")
        
#5.We add a product (p100, cd, 5) in Product and (p100, d2, 50) in Stock.
try:
    cur = con.cursor()
    cur.execute("INSERT INTO Product (prodid, pname, price) VALUES ('p100', 'cd', 5)")
    cur.execute("INSERT INTO Stock (prodid, depid, quantity) VALUES ('p100', 'd2', 50)")
    
except (Exception, psycopg2.DatabaseError) as err:
    print(err)
    print("Transactions could not be completed so database will be rolled back before start of transactions")
    con.rollback()
finally:
    if con:
        con.commit()
        cur.close
        con.close
        print("PostgreSQL connection is now closed")
        
