import json
import time
import mysql.connector
from ..chat import chats
import pandas as pd

class db_converter:

    ###############################################################
    def db_to_json(cnx, database_name):
        todas = 'error'
        db_meta = {}
        if cnx and cnx.is_connected():
            with cnx.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                databases = cursor.fetchall()

                for database in databases:
                    if (not database_name or (database[0] == database_name)):
                        db_meta[database[0]] = {}
                        cursor.execute('USE ' + database[0])
                        cursor.execute("SHOW TABLES")
                        tables = cursor.fetchall() 
                        
                        for table in tables:
                            cursor.execute('show fields from ' + table[0])
                            rows = cursor.fetchall() 
                            db_meta[database[0]][table[0]] = {}
                                            
                            
        return json.dumps(db_meta, indent=4)
    ###############################################################


    ###############################################################
    def connect_to_mysql(config, attempts=3, delay=2):
        attempt = 1
        
        while attempt < attempts + 1:
            try:
                cnx = mysql.connector.connect(**config)
                response = {
                    'status': 'success',
                    'connection': cnx,
                }
                return response
            except (mysql.connector.Error, IOError) as err:
                if (attempts is attempt):
                    response = {
                        'status': 'error',
                        'message': repr(err),
                    }
                    return response
                
                time.sleep(delay ** attempt)
                attempt += 1
        return None
    ###############################################################



    ###############################################################
    def executeSqlQuery(cnx, query):
        head = []
        rows = []
        if cnx and cnx.is_connected():
            with cnx.cursor() as cursor:

                try:
                    result = cursor.execute(query)
                    rows = cursor.fetchall()
                    head = cursor.column_names
                    rows.insert(0, head)
                    return {
                        'status': 'success',
                        'head': head,
                        'rows': rows,
                    }
                except (mysql.connector.Error, IOError) as err:
                    return {
                        'status': 'fail',
                        'head': head,
                        'rows': rows,
                        'message': repr(err),
                    }

        return None
    ###############################################################



    ##################################################################
    def chat_db(data):

        config = {
            'user': data['user'],
            'password': data['password'],
            'host': data['host'],
            'port': data['port'],
            'database': data['database'],
            'raise_on_warnings': True
        }
        
        conn = db_converter.connect_to_mysql(config, attempts=1)


        if (conn['status'] == 'success'):

            dbString = db_converter.db_to_json(conn['connection'], config['database'])

            db_info = {
                'database': config['database'],
                'tables': dbString,
            }

            prompt_1 = (
                f"Crie uma query SQL que atenda ao 'Comando';\n"
                f"Se o comando já for uma query SQL, melhore o comando apenas se for necessário;\n"
                f"Atenção, responda apenas a query, pronta para ser executada.\n\n"
                f"/////\n"
                f"Comando: \n"
                f"{data['prompt']}\n"
                f"/////\n\n"
                f"/////\n"
                f"Dados do Banco: \n"
                f"{db_info}\n"
                f"/////\n\n"
            )

            query = chats.basicOpenai(prompt_1)

            result = db_converter.executeSqlQuery(conn['connection'], query)

            process = {
                'command': data['prompt'],
                'query': query,
                'result': result,
            }

            df = pd.DataFrame(data=process['result']['rows'])
            html = df.to_html()

            return ({'command': data['prompt'], 'query': query,  'result': result, 'html': html})
        print(conn)
        return False
    ##################################################################
