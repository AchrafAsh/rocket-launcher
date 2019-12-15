import sqlite3
import subprocess
from components.constants import formats

def create_table():
    conn = sqlite3.connect('directories.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS directories(
      name TEXT,
      path TEXT,
      format TEXT
    )
  ''')
    conn.commit()
    conn.close()

create_table()

def suggestions(format, pattern):
    def data_base_request(format, pattern):
        conn = sqlite3.connect('directories.db')
        c = conn.cursor()
        c.execute(
            "SELECT * FROM directories WHERE format=(?) AND name LIKE (?)", (format,
                                                                             '%'+pattern+'%')
        )
        suggestion_list = c.fetchall()
        conn.commit()
        conn.close()
        return suggestion_list

    suggestion_list = data_base_request(format, pattern)

    k = 1
    while not suggestion_list and k < len(pattern)-2:
        suggestion_list = data_base_request(format, pattern[:-k])
        k += 1

    suggestion_dict = {}
    for i in range(len(suggestion_list)):
        suggestion_dict[suggestion_list[i][0]] = suggestion_list[i][1]

    # return a dict like {name:path}
    return suggestion_dict


def load_database(path, preferences):
    '''path s quite explicit and preferences is a list of format to load
    returns nothing but insert all the values(folders and files) in commands.db'''
    def isDirectory(directory):
        return directory and directory[-1] == ":" 

    if int(subprocess.getoutput('ls {} -R1 | wc -l'.format(path)))> 2000:
        print('too many files, may be useless')
        # or maybe give the user the possibility to force the loading
    else:
        # retrieve and reformat the content within the path
        content = str(subprocess.getoutput('ls {} -R1'.format(path)))
        content = content.split(sep='\n')
        db_entry = []
        i = 0
        while i < len(content):
            if isDirectory(content[i]):
                dir_path = content[i][:-1]
                dir_name = dir_path.split(sep="/")[-1]
                dir_format = "folder"
                db_entry.append([dir_name, dir_path, dir_format])
                db_entry.append([dir_name, dir_path, dir_format])
                i += 1
                while (i < len(content) and not isDirectory(content[i])):
                    file_name = content[i]
                    if '.' in file_name:
                        file_path = dir_path + '/' + file_name
                        file_format = file_name.split(sep='.')[-1]
                        db_entry.append([file_name, file_path, file_format])
                    i += 1

        conn = sqlite3.connect('directories.db')
        c = conn.cursor()
        # add the entries in db_entry into the database
        print('this is the list of entries : ', db_entry)
        for i in range(len(db_entry)):
            try:
                c.execute(
                    'INSERT INTO directories VALUES (?,?,?)', db_entry[i]
                )
            except sqlite3.IntegrityError:
                print('This path is already loaded in the database')

        # commit the changes
        conn.commit()
        # close
        conn.close()


def clear_database():
    conn = sqlite3.connect('directories.db')
    c = conn.cursor()
    c.execute('DELETE FROM directories')
    conn.commit()
    conn.close()
    print('The database has been successfully cleared.')
