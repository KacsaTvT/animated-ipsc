import mysql.connector

database = mysql.connector.connect(
    host = 'localhost', #hosztnév/ip (127.0.0.1)
    user = 'root', #felhasználó
    password = '', #jelszó
    database = 'python' #az a tábla, amiben dolgozol (nem pedig a munkamenet neve)
)
cursor = database.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS ipsc (csapat VARCHAR(255), nev VARCHAR(255), pontok INT(255))")
##hiba esetén nézd meg az 'sql.sql' fájlt

folytat = True

while folytat:
    #print("A program elindult.")
    elso = int(input("\nVálassza ki mit szeretne tenni:\n1. Versenyzők kezelése.\n2. Versenyzők és csapatok megjelenítése.\n3. Rangsorok\n-->"))
    if elso == 1:
        elsomasodik = int(input("Műveletek:\n1. Versenyző hozzáadása\n2. Versenyző eltávolítása\n-->"))
        if elsomasodik == 1:
            masodik1 = input("Írja be a versenyző csapatát.\n-->")
            if masodik1 == "":
                print("Nem adtál meg csapatot!")
            else:
                print(masodik1)
                masodik12 = input("Írj be a versenyző nevét.\n-->")
                if masodik12 == "":
                    print("Nem adtál meg nevet!")
                else:
                    print(masodik12)
                    masodik13 = int(input("Adja meg hány pontot ért el a versenyző.\n-->"))
                    if masodik13 == "":
                        print("Nem adtál meg pontszámot")
                    else:
                        cursor.execute("INSERT INTO ipsc (csapat, nev, pontok) VALUES (%s, %s, %s)", (masodik1, masodik12, masodik13))
                        database.commit()
        if elsomasodik == 2:
            delete = input("Adja meg a törölni kívánt versenyző nevét:\n-->")
            if delete == "":
                print("Nem adtál meg törölni kívánt személyt.")
            else:
                cursor.execute("DELETE FROM ipsc WHERE nev=%s", (delete,))
                database.commit()
    if elso == 2:
        cursor.execute("SELECT csapat, nev, pontok FROM ipsc")
        result= cursor.fetchall()
        print("Regisztrált versenyzők:")
        for (csapat, nev, pontok) in result:
            print(f"{csapat}, {nev}, {pontok}")
        print("---\n---\n---\n")
    if elso == 3:
        rangsoropc = int(input("Lehetőségek:\n1. Egyéni összesítő\n2. Csapatos összesítő\n-->"))
        if rangsoropc == 1:
            cursor.execute("SELECT nev, pontok FROM ipsc ORDER BY pontok DESC")
            #cursor = cursor.fetchall()
            helyezes = 1
            for (nev, pontok) in cursor:
                print(f"{helyezes}. helyezett: {nev}, {pontok} ponttal")
                helyezes+=1
        if rangsoropc == 2:
            cursor.execute("SELECT csapat, SUM(pontok) as osszesitett_csap FROM ipsc GROUP BY csapat ORDER BY osszesitett_csap DESC")
            helyezes_csap=1
            for (csapat, osszesitett_csap) in cursor:
                print(f"{helyezes_csap}. helyezett a {csapat} csapat, Összesített pontszáma: {osszesitett_csap}")
                helyezes_csap+=1

#divíziók és sectorok hozzáadása