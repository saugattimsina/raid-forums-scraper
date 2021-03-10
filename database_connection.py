import psycopg2

def database_creator():
    try:
        conn = psycopg2.connect(database="raidforum",user="saugat1",password="saugat123",host = "127.0.0.1",port = "5432")
        cur = conn.cursor()
        print(cur)

        table_schema1 = '''CREATE TABLE IF NOT EXISTS  posts(
            post_id INT GENERATED ALWAYS AS IDENTITY,
            page_url VARCHAR(255) UNIQUE,
            page_title VARCHAR(255),
            text_content TEXT,
            date_time  VARCHAR(255),
            username  TEXT,
            user_title VARCHAR(255),
            PRIMARY KEY(post_id)
        )
        '''
        table_schema2 = ''' 
        CREATE TABLE IF NOT EXISTS comments(
            comment_id INT GENERATED ALWAYS AS IDENTITY,
            text_content TEXT,
            date_time  VARCHAR(255),
            username  TEXT,
            user_title VARCHAR(255),
            post_id  INT,
            PRIMARY KEY(comment_id),
            CONSTRAINT fk_posts FOREIGN KEY(post_id) REFERENCES posts(post_id)
        )   
        '''
        cur.execute(table_schema1)

        cur.execute(table_schema2)
        conn.commit()
        conn.close()
        print("success")
    except Exception as e:
        print(e)

  

def connection_creator():

    try:  
        conn = psycopg2.connect(database="raidforum",user="saugat1",password="saugat123",host = "127.0.0.1",port = "5432")
        
        return conn
    except Exception as e:
        print(e)
    
    
# database_creator()