
# Fxn

def create_db(cursor,db_name):
    db = f"create database {db_name}"
    cursor.execute(db)
    
def create_table(cursor,tb_name):
    tb = f"CREATE TABLE IF NOT EXISTS {tb_name} (Comments varchar(1000), Customer_Name varchar(100)); "
    cursor.execute(tb)
    
def insert_table(cursor,tb_name,lst):
    insert_query = f"INSERT INTO {tb_name}(Comments,Customer_Name) VALUES ( %(Comment)s, %(Name)s);"
    cursor.executemany(insert_query, lst)

    
    
