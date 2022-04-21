# Execution of varchar to text
<hr>

The code is initiated using the main.py file. 

We have 1 sub-command.

* db (It is used to prepare a new sql query file for a given schema.table)

There are 3 different flags to play with.

* --file_name 
* --schema 
* --tables 

## file_name
It has to be used only if the code from previously generated file is to be executed.
It is Used to point at the file from which the queries are to be executed. the prepared query has to be inside `prepared_queries` directory.

`python main.py --file_name <file-name>`

## schema and tables
Schema and tables fall under the `db` sub-command and; thus have to be defined after the ocurrence of the word `db`.
Schema is used to describe the schema which contains the table, default value is set to `public`.
tables is used to describe the tables whose column data type is to be changed. It also falls under the `db` sub-command.

While executing it defining tables is a must.

`python main.py db [--schema <schema-name>] --tables <table-name>`

We can also pass multiple tables at a time.

`python main.py db [--schema <schema-name>] --tables "<table-name>, <table-name>, <table-name>, ..."`


NOTE: 

* The `db` sub command is given more priority over the --file_name. Thus, --file_name has no value while using the sub-command `db`.

* While executing `db` sub command, we are asked if we want to execte the query as well by the end.

* At least a filename or a table name has to be provided for the program to execute.
