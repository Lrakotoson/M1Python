import csv


def read_grades_from_csv(path):
    grades = {}
    with open(path, 'r') as inFile:
        csv_reader = csv.reader(inFile)
        first_line = next(csv_reader)
        items = first_line[1:]
        users = []
        for line in csv_reader:
            user = line[0]
            users.append(user)
            for i,grade in enumerate(line[1:]):
                if grade != '':
                    grades[(user, items[i])] = float(grade)
                
    return grades, users, items
    
def read_txt_to_dic(path):
    dic = {}
    with open(path, 'r', encoding='utf-8') as inFile:
        for line in inFile.readlines():
            line = line.strip()
            id, strList = line.split(" ")
            l = strList.split(',')
            dic[id] = l
    return dic