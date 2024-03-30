import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'python'
)
cursor = database.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS ipsc (csapat VARCHAR(255), nev VARCHAR(255), pontok INT(255))")


versenyzok = {}
csapatok = {}

folytat = True
bekertv = None

while folytat:
    #print("A program elindult.")
    elso = int(input("Válassza ki mit szeretne tenni:\n1. Versenyzők kezelése.\n2. Versenyzők és csapatok megjelenítése.\n-->"))
    if elso == 1:
        elsomasodik = int(input("Műveletek:\n1. Versenyző hozzáadása\n2. Versenyző eltávolítása\n-->"))
        if elsomasodik == 1:
            masodik1 = input("Írja be a versenyző csapatát.\n-->")
            print(masodik1)
            masodik12 = input("Írj be a versenyző nevét.\n-->")
            print(masodik12)
            masodik13 = int(input("Adja meg hány pontot ért el a versenyző.\n-->"))
            cursor.execute("INSERT INTO ipsc (csapat, nev, pontok) VALUES (%s, %s, %s)", (masodik1, masodik12, masodik13))
            database.commit()
        if elsomasodik == 2:
            delete = input("Adja meg a törölni kívánt versenyző nevét:\n-->")
            cursor.execute("DELETE FROM ipsc WHERE nev=%s", (delete,))
            database.commit()
    if elso == 2:
        cursor.execute("SELECT * FROM ipsc")
        result= cursor.fetchall()
        for row in result:
            print(row, '\n')
        print("---\n----\n----\n")
    



#ami még hozzá kellene adni kövinek: rangsorolás