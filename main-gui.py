import mysql.connector
from tkinter import *
from tkinter import messagebox

# Database connection
database = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='python'
)
cursor = database.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS ipsc (csapat VARCHAR(255), nev VARCHAR(255), pontok INT(255), division VARCHAR(255), sector INT(255))")

root = Tk()
root.title("MDLSZ MDT")
root.geometry("800x600+10+20")

# Functions
def add_competitor():
    csapat = csapat_entry.get()
    nev = nev_entry.get()
    pontok = pontok_entry.get()
    division = division_entry.get()
    sector = sector_entry.get()
    if csapat and nev and pontok and division and sector:
        cursor.execute("INSERT INTO ipsc (csapat, nev, pontok, division, sector) VALUES (%s, %s, %s, %s, %s)", (csapat, nev, pontok, division, sector))
        database.commit()
        messagebox.showinfo("Sikeres", "Versenyző sikeresen hozzáadva!")
        csapat_entry.delete(0, END)
        nev_entry.delete(0, END)
        pontok_entry.delete(0, END)
        division_entry.delete(0, END)
        sector_entry.delete(0, END)
    else:
        messagebox.showerror("Hiba", "Minden mezőt tölts ki!")

def delete_competitor():
    nev = delete_entry.get()
    if nev:
        cursor.execute("DELETE FROM ipsc WHERE nev=%s", (nev,))
        database.commit()
        messagebox.showinfo("Sikeres", "Versenyző sikeresen törölve!")
        delete_entry.delete(0, END)
    else:
        messagebox.showerror("Hiba", "Minde mezőt tölts ki!")

def show_competitors():
    cursor.execute("SELECT csapat, nev, pontok, division, sector FROM ipsc")
    result = cursor.fetchall()
    result_text = "\n".join([f"{csapat}, {nev}, {pontok}, {division}, {sector}" for csapat, nev, pontok, division, sector in result])
    messagebox.showinfo("Regisztrált versenyzők", result_text)

def show_rankings():
    cursor.execute("SELECT csapat, SUM(pontok) as osszesitett_csap FROM ipsc GROUP BY csapat ORDER BY osszesitett_csap DESC")
    result = cursor.fetchall()
    result_text = "\n".join([f"{index+1}. {csapat}, {osszesitett_csap}" for index, (csapat, osszesitett_csap) in enumerate(result)])
    messagebox.showinfo("Csapat rangsor", result_text)

def show_divranking():
    keresettdiv = keresett.get()
    if keresettdiv:
        cursor.execute("SELECT division, nev, SUM(pontok) AS osszpontok FROM ipsc WHERE division=%s GROUP BY division, nev ORDER BY division, osszpontok DESC", (keresettdiv,))
        result = cursor.fetchall()
        result_text = "\n".join([f"{index+1}. {division}, {nev}, {osszpontok}" for index, (division, nev, osszpontok) in enumerate(result)])
        messagebox.showinfo("Divíziós rangsor", result_text)
        keresett.delete(0, END)
    else:
        messagebox.showerror("Hiba", "Minde mezőt tölts ki!")


def show_allrankings():
    cursor.execute("SELECT nev, SUM(pontok) AS osszpontok FROM ipsc GROUP BY nev ORDER BY osszpontok DESC")
    result = cursor.fetchall()
    result_text = "\n".join([f"{index+1}. {nev}, {osszpontok}" for index, (nev, osszpontok) in enumerate(result)])
    messagebox.showinfo("Teljes rangsor", result_text)


Label(root, text="Versenyző regisztrálása").grid(row=0, column=0)
Label(root, text="Csapat:").grid(row=2, column=0)
csapat_entry = Entry(root)
csapat_entry.grid(row=2, column=1)

Label(root, text="Név:").grid(row=3, column=0)
nev_entry = Entry(root)
nev_entry.grid(row=3, column=1)

Label(root, text="Pontok:").grid(row=4, column=0)
pontok_entry = Entry(root)
pontok_entry.grid(row=4, column=1)

Label(root, text="Divízió:").grid(row=5, column=0)
division_entry = Entry(root)
division_entry.grid(row=5, column=1)

Label(root, text="Sector:").grid(row=6, column=0)
sector_entry = Entry(root)
sector_entry.grid(row=6, column=1)

Button(root, text="Versenyző hozzáadás", command=add_competitor).grid(row=7, column=0, columnspan=2)


Label(root, text="Versenyző törlés (Név alalpján):").grid(row=8, column=0)
delete_entry = Entry(root)
delete_entry.grid(row=8, column=1)
Button(root, text="Versenyző törlés", command=delete_competitor).grid(row=9, column=0, columnspan=2)

Label(root, text="Eredmények").grid(row=10, column=0)
Button(root, text="Versenyzők listája", command=show_competitors).grid(row=11, column=0, columnspan=2)

Button(root, text="Eredmények (Csapat)", command=show_rankings).grid(row=12, column=0, columnspan=2)

Label(root, text="Keresett divízió):").grid(row=13, column=0)
keresett = Entry(root)
keresett.grid(row=13, column=1)
Button(root, text="Eredmények megjelenítése Divízió szerint", command=show_divranking).grid(row=14, column=0, columnspan=2)

Button(root, text="Eredmények (Mindenki)", command=show_allrankings).grid(row=15, column=0, columnspan=2)

root.mainloop()
