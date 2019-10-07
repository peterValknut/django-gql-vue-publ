import MySQLdb
import json




def get_dadata_by_inn(inn):
    db = MySQLdb.connect(passwd="mypass", db="dadata", user='graphtest', charset="utf8mb4", use_unicode=True)
    cursor = db.cursor()
    cursor.execute("SELECT `inn`,`name`,`ogrn`,`region` FROM `dadata` WHERE `inn` = %s;",(inn,))
    cont = []
    for name in cursor.fetchall():
        cont.append({
            'inn':name[0],
            'name': name[1],
            'ogrn': name[2],
            'region': name[3],
        })
    cursor.close()
    return cont

def get_dadata_by_name(name):
    db = MySQLdb.connect(passwd="mypass", db="dadata", user='graphtest', charset="utf8mb4", use_unicode=True)
    cursor = db.cursor()
    cursor.execute("SELECT `inn`,`name`,`ogrn`,`region` FROM `dadata` WHERE LOWER(`name`) REGEXP %s;",(name,))
    cont = []
    for name in cursor.fetchall():
        cont.append({
            'inn':name[0],
            'name': name[1],
            'ogrn': name[2],
            'region': name[3],
        })
    cursor.close()
    return cont

def get_sbis_by_name(name):
    db = MySQLdb.connect(passwd="mypass", db="sbis", user='graphtest', charset="utf8mb4", use_unicode=True)
    cursor = db.cursor()
    cursor.execute("SELECT `inn`,`name`,`activity`,`region`, `director` FROM `sbis1` WHERE LOWER(`name`) REGEXP %s;",(name,))
    cont = []
    for name in cursor.fetchall():
        cont.append({
            'inn':name[0],
            'name': name[1],
            'activity': name[2],
            'region': name[3],
            'director': name[4],
        })
    cursor.close()
    return cont

def get_sbis_by_inn(inn):
    db = MySQLdb.connect(passwd="mypass", db="sbis", user='graphtest', charset="utf8mb4", use_unicode=True)
    cursor = db.cursor()
    cursor.execute("SELECT `inn`,`name`,`activity`,`region`, `director` FROM `sbis1` WHERE `inn` = %s;",(inn,))
    cont = []
    for name in cursor.fetchall():
        cont.append({
            'inn': name[0],
            'name': name[1],
            'activity': name[2],
            'region': name[3],
            'director': name[4],
        })
    cursor.close()
    return cont


def get_grants_by_inn(inn):
    db = MySQLdb.connect(passwd="mypass", db="president_grants", user='graphtest', charset="utf8mb4", use_unicode=True)
    cursor = db.cursor()
    cursor.execute("SELECT `inn`,`organization_name`,`grant_sum`,`address_string`, `email`, `project_name`, `project_status`, `total_sum`, `grant_name` FROM `grants` WHERE `inn` = %s;",(inn,))
    cont = []
    for name in cursor.fetchall():
        cont.append({
            'inn': name[0],
            'organization_name': name[1],
            'grant_sum': name[2],
            'address_string': name[3],
            'email': name[4],
            'project_name': name[5],
            'project_status': name[6],
            'total_sum': name[7],
            'grant_name': name[8],
        })
    cursor.close()
    return cont

def get_grants_by_name(name):
    db = MySQLdb.connect(passwd="mypass", db="president_grants", user='graphtest', charset="utf8mb4", use_unicode=True)
    cursor = db.cursor()
    cursor.execute("SELECT `inn`,`organization_name`,`grant_sum`,`address_string`, `email` FROM `grants` WHERE LOWER(`organization_name`) REGEXP %s;",(name,))
    cont = []
    for name in cursor.fetchall():
        cont.append({
            'inn': name[0],
            'organization_name': name[1],
            'grant_sum': name[2],
            'address_string': name[3],
            'email': name[4],
        })
    cursor.close()
    return cont