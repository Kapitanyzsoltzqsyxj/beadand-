import json
import os

class SzallodaFoglalasiRendszer:
    def __init__(self):
        self.szobak = {}
        self.foglalasok = {}
        self.foglalasi_azonosito_szamlalo = 1

    def szoba_hozzaadasa(self, szobaszam, szobatipus):
        self.szobak[szobaszam] = {'tipus': szobatipus, 'statusz': 'elérhető'}

    def foglalas_letrehozasa(self, szobaszam, vendeg_neve, bejelentkezesi_datum, kijelentkezesi_datum):
        if szobaszam in self.szobak and self.szobak[szobaszam]['statusz'] == 'elérhető':
            foglalasi_azonosito = self.foglalasi_azonosito_szamlalo
            self.foglalasok[foglalasi_azonosito] = {
                'szobaszam': szobaszam,
                'vendeg_neve': vendeg_neve,
                'bejelentkezesi_datum': bejelentkezesi_datum,
                'kijelentkezesi_datum': kijelentkezesi_datum
            }
            self.szobak[szobaszam]['statusz'] = 'foglalt'
            self.foglalasi_azonosito_szamlalo += 1
            return foglalasi_azonosito
        else:
            raise ValueError("A szoba nem elérhető vagy nem létezik")

    def foglalas_torlese(self, foglalasi_azonosito):
        if foglalasi_azonosito in self.foglalasok:
            szobaszam = self.foglalasok[foglalasi_azonosito]['szobaszam']
            self.szobak[szobaszam]['statusz'] = 'elérhető'
            del self.foglalasok[foglalasi_azonosito]
        else:
            raise ValueError("A foglalási azonosító nem létezik")

    def foglalasok_listazasa(self):
        return self.foglalasok

    def adatok_mentese(self, fajlnev):
        adatok = {
            'szobak': self.szobak,
            'foglalasok': self.foglalasok,
            'foglalasi_azonosito_szamlalo': self.foglalasi_azonosito_szamlalo
        }
        with open(fajlnev, 'foglalási adatok') as file:
            json.dump(adatok, file)

    def adatok_betoltese(self, fajlnev):
        if os.path.exists(fajlnev):
            with open(fajlnev, 'foglalási adatok') as file:
                adatok = json.load(file)
                self.szobak = adatok['szobak']
                self.foglalasok = adatok['foglalasok']
                self.foglalasi_azonosito_szamlalo = adatok['foglalasi_azonosito_szamlalo']

def menu():
    szalloda = SzallodaFoglalasiRendszer()
    while True:
        print("\n=== Szállodai Foglalási Rendszer ===")
        print("1. Szoba hozzáadása")
        print("2. Foglalás létrehozása")
        print("3. Foglalás törlése")
        print("4. Foglalások listázása")
        print("5. Adatok mentése")
        print("6. Adatok betöltése")
        print("0. Kilépés")
        print("====================================")

        valasztas = input("Válasszon egy lehetőséget: ")

        if valasztas == '1':
            try:
                szobaszam = input("Adja meg a szobaszámot: ")
                szobatipus = input("Adja meg a szoba típusát: ")
                szalloda.szoba_hozzaadasa(szobaszam, szobatipus)
                print(f"Sikeresen hozzáadta a(z) {szobaszam} számú szobát ({szobatipus}).")
            except Exception as e:
                print(f"Hiba történt a szoba hozzáadásakor: {e}")

        elif valasztas == '2':
            try:
                szobaszam = input("Adja meg a szobaszámot: ")
                vendeg_neve = input("Adja meg a vendég nevét: ")
                bejelentkezesi_datum = input("Adja meg a bejelentkezési dátumot (év-hónap-nap): ")
                kijelentkezesi_datum = input("Adja meg a kijelentkezési dátumot (év-hónap-map): ")
                foglalasi_azonosito = szalloda.foglalas_letrehozasa(szobaszam, vendeg_neve, bejelentkezesi_datum, kijelentkezesi_datum)
                print(f"Sikeresen létrehozta a foglalást. Foglalási azonosító: {foglalasi_azonosito}")
            except ValueError as e:
                print(e)
            except Exception as e:
                print(f"Hiba történt a foglalás létrehozásakor: {e}")

        elif valasztas == '3':
            try:
                foglalasi_azonosito = int(input("Adja meg a foglalási azonosítót: "))
                szalloda.foglalas_torlese(foglalasi_azonosito)
                print("A foglalás sikeresen törölve.")
            except ValueError as e:
                print(e)
            except Exception as e:
                print(f"Hiba történt a foglalás törlésekor: {e}")

        elif valasztas == '4':
            foglalasok = szalloda.foglalasok_listazasa()
            if foglalasok:
                print("\n=== Foglalások Listája ===")
                for azonosito, foglalas in foglalasok.items():
                    print(f"Azonosító: {azonosito}, Szobaszám: {foglalas['szobaszam']}, Vendég neve: {foglalas['vendeg_neve']}, Bejelentkezési dátum: {foglalas['bejelentkezesi_datum']}, Kijelentkezési dátum: {foglalas['kijelentkezesi_datum']}")
                print("==========================")
            else:
                print("Nincsenek foglalások.")

        elif valasztas == '5':
            try:
                fajlnev = input("Adja meg a fájlnevet: ")
                szalloda.adatok_mentese(fajlnev)
                print(f"Adatok sikeresen elmentve a(z) {fajlnev} fájlba.")
            except Exception as e:
                print(f"Hiba történt az adatok mentésekor: {e}")

        elif valasztas == '6':
            try:
                fajlnev = input("Adja meg a fájlnevet: ")
                szalloda.adatok_betoltese(fajlnev)
                print(f"Adatok sikeresen betöltve a(z) {fajlnev} fájlból.")
            except Exception as e:
                print(f"Hiba történt az adatok betöltésekor: {e}")

        elif valasztas == '0':
            print("Kilépés...")
            break

        else:
            print("Érvénytelen választás, próbálja újra.")

menu()
