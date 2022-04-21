path = "./prepared_queries/"

def write_to_a_file(query, file_name):
    errors = []
    try:
        f = open(path + file_name, "a")
        f.write(query + '\n')
    except Exception as Err:
        print(f"Error while writing into file {file_name}.")
        errors.append(Err)
    f.close()
    return errors

def read_file(file_name):
    try:
        with open(path + file_name, "r") as f:
            return f.readlines()
    except Exception as Err:
        print(f"Error while reading file {file_name}. Check if the file exists.")
        return []
