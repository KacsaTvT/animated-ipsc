import mysql.connector

database = mysql.connector.connect(
    host = 'localhost', #hosztnév/ip (127.0.0.1)
    user = 'root', #felhasználó
    password = '', #jelszó
    database = 'python' #az a tábla, amiben dolgozol (nem pedig a munkamenet neve)
)
cursor = database.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS ipsc (csapat VARCHAR(255), nev VARCHAR(255), division VARCHAR(255), pontok INT(255), sector INT(255))")
##hiba esetén nézd meg az 'sql.sql' fájlt

folytat = True

while folytat:
    #print("A program elindult.")
    elso = int(input("\nVálassza ki mit szeretne tenni:\n1. Versenyzők kezelése.\n2. Versenyzők és csapatok megjelenítése.\n3. Rangsorok\n-->"))
    if elso == 1:
        elsomasodik = int(input("Műveletek:\n1. Versenyző hozzáadása\n2. Versenyző eltávolítása\n-->"))
        if elsomasodik == 1:
            sector = input("\nMelyik Sectorhoz ad hozzá?\n-->")
            if sector.isdigit():
                sectorbe = int(sector)
            else:
                print("Nem adtál meg sectort!")
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
                        masodik14 = input("Adja meg a versenyző divízióját.\n-->")
                        if masodik14 == "":
                            print("Nem adtál meg divíziót.")
                        else:
                            cursor.execute("INSERT INTO ipsc (csapat, nev, pontok, division, sector) VALUES (%s, %s, %s, %s, %s)", (masodik1, masodik12, masodik13, masodik14, sector))
                            database.commit()
            if elsomasodik == 2:
                delete = input("Adja meg a törölni kívánt versenyző nevét:\n-->")
                if delete == "":
                    print("Nem adtál meg törölni kívánt személyt.")
                else:
                    cursor.execute("DELETE FROM ipsc WHERE nev=%s", (delete,))
                    database.commit()
    if elso == 2:
        cursor.execute("SELECT csapat, nev, pontok, division FROM ipsc")
        result= cursor.fetchall()
        print("Regisztrált versenyzők:")
        for (csapat, nev, pontok, division) in result:
            print(f"Csapat: {csapat}; Név: {nev}; Pontok: {pontok}; Divízió: {division}")
    if elso == 3:
        rangsoropc = int(input("Lehetőségek:\n1. Egyéni összesítő\n2. Csapatos összesítő\n3. Division összesítő\n-->"))
        if rangsoropc == 1:
            cursor.execute("SELECT nev, SUM(pontok) as sumpont FROM ipsc GROUP BY nev ORDER BY sumpont DESC")
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
        if rangsoropc == 3:
            divisionopc = input("Melyik divízió rangsorát szeretnéd látni?\n-->")
            cursor.execute("SELECT division, nev, SUM(pontok) AS osszpontok FROM ipsc WHERE division=%s GROUP BY division, nev ORDER BY osszpontok DESC", (divisionopc,))
            helyezes_div=1
            for (division, nev, pontok) in cursor:
                print(f"{helyezes_div}. helyezett {nev} a {divisionopc} kategóriában, Összesített pontszáma: {pontok}")
                helyezes_div+=1

#terv: holtverseny kezelése