import MySQLdb
import json

def get_grants_by_inn(inn):
    db = MySQLdb.connect(passwd="mypass", db="president_grants", user='graphtest', charset="utf8mb4", use_unicode=True)
    cursor = db.cursor()
    cursor.execute("SELECT `inn`,`organization_name`,`grant_sum`,`address_string`, `email` FROM `grants` WHERE `inn` = %s;",(inn,))
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