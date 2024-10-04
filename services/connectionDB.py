from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from time import sleep
import os
import json


load_dotenv()

def connect():
    db_url = f"postgresql://postgres:postgres@{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}"
    Base = declarative_base()
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def execute_sql_query(sql, params):
    session = connect()
    if params is not None:
        result = session.execute(text(sql), params)
    else:
        result = session.execute(text(sql))
    session.commit()
    session.close()
    return result

def parse_sql_result_to_json(sql_result):
    if sql_result.returns_rows:
        result_list = []
        column_names = sql_result.keys()

        for row in sql_result:
            row_dict = {}
            column_index = 0

            for column in column_names:
                value = str(row[column_index]).strip()
                row_dict[column] = value
                column_index = column_index + 1

            result_list.append(row_dict)

        return result_list
    else:
        affected_rows = sql_result.rowcount
        return {"affected_rows": str(affected_rows)}

def process_request(sock, data):
    decoded_data = decode_response(data)
    service = decoded_data['service']
    response = json.dumps(decoded_data['data'])

    if service != 'dbcon':
        return incode_response(service, {
            "data": "Invalid Service: " + service
        })

    try:
        msg = json.loads(response)
        if 'sql' not in msg:
            return incode_response(service, {
                "data": "No SQL Query in data."
            })
        sql = msg['sql']

        if 'params' not in msg:
            params = None
        else:
            params = msg['params']

        sql_result = execute_sql_query(sql, params)
        json_result = parse_sql_result_to_json(sql_result)

        return incode_response(service, {
            "data": json_result
        })
    except Exception as err:
        return incode_response(service, {
            "data": "Error de BDD procesando la solicitud: " + str(err)
        })

def main(sock, data):
    try:
        return process_request(sock=sock, data=data)
    except Exception as e:
        print("Exception: ", e)
        sleep(5)
        main(sock, data)

if __name__ == "__main__":
    from service import main_service, decode_response, incode_response

    main_service('dbcon', main)
