from db_utils import connect, disconnect, execute_query, fetch_db_result
import argparse
from file_utils import write_to_a_file, read_file
import datetime
from simple_colors import *

def prepare_alter_column_type_query(cur, schema, table_list, file_name, cur_type = 'character varying', new_type = 'text'):
    errors = []
    for table in table_list:
        print(f"\nWorking on the table {table}")
        errors, columns = fetch_db_result(cur, f"SELECT column_name FROM information_schema.columns \
            WHERE table_schema = \'{schema}\' AND table_name = \'{table}\' and data_type ilike '{cur_type}'")
        if errors:
            print(f"Error while fetching table information from the information_schema.columns.")
            return errors
        if not columns:
            print(f"The table {table} has no column with data type {cur_type}")
            continue
        for coltup in columns:
            col = coltup[-1]
            query = f"ALTER TABLE {schema}.{table} ALTER COLUMN {col} TYPE {new_type};"
            errors = write_to_a_file(query, file_name)
            if errors:
                return errors
            #print(f"Alter query for ---- {col} ---- {query} ....")
        print(f"Completed going through the table {table} \n")
    return errors

def read_and_execute_query(cur, file_name):
    errors = []
    execute = input(f"Type {cyan('Execute Queries', 'italic')} to execute the Queries at file {file_name} (CASE SENSITIVE):: ")
    if execute == 'Execute Queries':
        for query in read_file(file_name):
            errors = execute_query(cur, query)
            if errors:
                return errors
            print(f"Query for altering column {yellow(query.split(' ')[5], 'bold')} from table {yellow(query.split(' ')[2], 'bold')} executed successfully; From file {file_name} ....")  
    else:
        print("Closing without executing queries ....")
    return errors

if __name__ == '__main__':
    table_list = []
    parser = argparse.ArgumentParser(description="Get the table informations")
    subparsers = parser.add_subparsers(title="Execution parameters and db parameters")
    
    parser.add_argument(
        "--file_name",
        dest="file_name",
        help="File name to use for conducting execution.",
    )
    
    db_subparser = subparsers.add_parser("db")
    db_subparser.add_argument(
        "--schema",
        dest="schema",
        default="public",
        help="Schema of the table to be altered.",
    )
    db_subparser.add_argument(
        "--tables",
        dest="tables",
        default = [],
        action = 'append',
        required=True,
        help="List of the table which is to be altered.",
    )

    known_cmd, _ = parser.parse_known_args()
    param = vars(known_cmd)
    file_name = param['file_name'] if 'file_name' in param.keys() and 'tables' not in param.keys() else 'query_'+str(datetime.datetime.now().strftime("%D_%H:%M:%S")).replace('/','-') + '.sql'
    errors = []

    if 'tables' not in param.keys() and 'file_name' not in param.keys():
        raise Exception("Please specify action for the program execution. Use '-h' for help.")       
    
    errors, conn = connect()
    if errors:
        print(errors[-1])
        quit()

    cur = conn.cursor()
    
    if 'tables' in param.keys():
        table_list = [i.strip() for i in known_cmd.tables[-1].split(',')]
        errors = prepare_alter_column_type_query(cur, known_cmd.schema, table_list, file_name)
    
    if not errors:
        errors = read_and_execute_query(cur, file_name)
    if not errors:
        conn.commit()
    for error in errors:
        print(error)
    disconnect(cur)
