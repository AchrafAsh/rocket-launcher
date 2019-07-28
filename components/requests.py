import sqlite3, subprocess
from components.constants import *


def create_table(table_name, attributes):
  conn = sqlite3.connect('./server/directories.db')
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS directories(
      name TEXT,
      path TEXT,
      format TEXT
    )
  ''')
  conn.commit()
  conn.close()

def suggestions(format, pattern):
  def data_base_request(format, pattern):
    conn = sqlite3.connect('./server/directories.db')
    c = conn.cursor()
    c.execute(
      "SELECT * FROM directories WHERE format=(?) AND name LIKE (?)",(format, '%'+pattern+'%')
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

  if int(subprocess.getoutput(
    'dir {} /s /b | find /c /v "::"'.format(path)
  )) > 2000:
    print('too many files, may be useless')
    # or maybe give the user the possibility to force the loading
  else:
    #retrieve and reformat the content within the path
    content = str(subprocess.getoutput('dir {} /b /s'.format(path)))
    content = content.split(sep='\n')
    db_entry = []
    for directory in content:
      name = directory.split(sep='\\')[-1]
      if '.' in name:
        format = name.split(sep='.')[-1]
      else:
        format = 'folder'
      
      if format in preferences:
        db_entry.append([name, directory, format])
    
    conn = sqlite3.connect('./server/directories.db')
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
  conn = sqlite3.connect('./server/directories.db')
  c = conn.cursor()
  c.execute('DELETE FROM directories')
  conn.commit()
  conn.close()
  print ('The database has been successfully cleared.')


