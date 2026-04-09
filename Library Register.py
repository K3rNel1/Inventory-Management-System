# Project: Inventory Tracking and Management System
# Author: Ali Zubair Shah
# GitHub: https://github.com/K3rNel1 

def main():
            
    import sqlite3
    import os

    os.system('attrib +h Inventory.db')

    conn = sqlite3.connect("Inventory.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS register (bname TEXT NOT NULL, name TEXT PRIMARY KEY , mob INTEGER, doi TEXT NOT NULL, dor TEXT NOT NULL, rm TEXT )")                                                                               #Author : Github.com/K3rnel1

    st = int(input("\n1, Issue Book \n2, Access Register\n[1/2]: "))

    if st == 1 :
        bname = input("Name of the Book : ")
        name = input("Name of the Borrower : ")
        mob = int(input(f"Contact number of {name} : "))
        doi = input("Date of Issue : ")
        dor = input("Date of Return : ")
        rm = input("Remarks : ")

        cursor.execute("INSERT OR REPLACE INTO register (bname, name, mob, doi, dor, rm) VALUES (?,?,?,?,?,?)",(bname,name,mob,doi,dor,rm))

        print ("\nTransaction Completed!")
        conn.commit()

    elif st == 2 :
        cursor.execute("SELECT * FROM register")
        data = cursor.fetchall()
        
        if data :
            for bname,name,mob,doi,dor,rm in data:
                
                print(f"\n=>  Book's name : {bname}\n    Borrower's name : {name}\n    Contact : {mob}\n    Date of Issue : {doi}\n    Date of Return : {dor}\n    Remarks : {rm}\n")

            conn.commit()

            st2 = int(input("\n1,Update Register \n2,Remove from Register\n[1/2] : "))

            if st2 == 1:
                ch = input("Enter Borrower Name: ")

                new_bname = input("New Book Name (leave blank to skip): ")
                new_mob = input("New Mobile (leave blank to skip): ")
                new_doi = input("New DOI (leave blank to skip): ")
                new_dor = input("New DOR (leave blank to skip): ")
                new_rm = input("New Remarks (leave blank to skip): ")   
            
                if new_bname:
                    cursor.execute("UPDATE register SET bname=? WHERE name=?", (new_bname, ch))

                if new_mob:
                    cursor.execute("UPDATE register SET mob=? WHERE name=?", (int(new_mob), ch))
                
                if new_doi:
                    cursor.execute("UPDATE register SET doi=? WHERE name=?", (new_doi, ch))

                if new_dor:
                    cursor.execute("UPDATE register SET dor=? WHERE name=?", (new_dor, ch))

                if new_rm:
                    cursor.execute("UPDATE register SET rm=? WHERE name=?", (new_rm, ch))

                conn.commit()
                print("\nRecord Updated!")
            
            elif st2 == 2:
                ch = input("Enter Borrower Name: ")
                cursor.execute("DELETE FROM register WHERE name=?",(ch,))
                conn.commit()
                print("\nRecord of",ch,"removed")
           
            else :
                print("\nInvalid Option")
       
        else :
                print("\nNo record found")
        conn.close()

while True :
    main()
                    
