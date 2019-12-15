import subprocess

def isDirectory(directory):
    return directory and directory[-1] == ":" 

path = "/home/achraf/Documents/TAEP/CA"

print(int(subprocess.getoutput('ls {} -R1 | wc -l'.format(path))))

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
                

print(db_entry)
print(len(db_entry))