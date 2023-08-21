from bs4 import BeautifulSoup
import os
import csv


# Dobljen niz pretvori v število, znebi se znakov za milijarde, milijone in dolarje
# Če na spletni strani ni podatkov o tržnem kapitali oz. ceni delnice (je N/A), funkcija vrne 0
def uredi_trg(trg_niz):
    if trg_niz.endswith("B"):
        return round(float(trg_niz.replace("$", "").replace(" B", "")), 5)
    elif trg_niz.endswith("M"):
        return round(float(trg_niz.replace("$", "").replace(" M", "")) / 1000, 5) 
    else:
        return 0

def uredi_ceno_delnice(delnica_niz):
    if delnica_niz.startswith("$"):
        return round(float(delnica_niz.replace("$", "").replace(",", "")), 5)
    else:
        return 0

# Seznam podatkov bank
banke = []

html_files_directory = "strani" 


for filename in os.listdir(html_files_directory):
    file_path = os.path.join(html_files_directory, filename)
    with open(file_path, "r") as file:
        html_content = file.read()
        juha = BeautifulSoup(html_content, "html.parser")
            
        # Find all rows with class "name-td"
        vse_banke = juha.find_all("td", class_="name-td")
            
        for banka in vse_banke:
            mesto = banka.find_previous("td", class_="rank-td").get_text()
            naziv = banka.find("div", class_="company-name").get_text()
            sifra_podjetja = banka.find("div", class_="company-code").get_text()
            drzava = banka.find_next("td", class_=None).get_text()
            

            td_right_elements = banka.find_all_next("td", class_="td-right")
            
            trzni_kapital = td_right_elements[0].get_text()
            cena_delnice = td_right_elements[1].get_text()
        
            trzni_kapital_stevilo = uredi_trg(trzni_kapital)
            
            cena_delnice_stevilo = uredi_ceno_delnice(cena_delnice)
        
            banke.append([mesto, naziv, sifra_podjetja, drzava, trzni_kapital_stevilo, cena_delnice_stevilo])

banke.sort(key=lambda x: int(x[0]))
# Zapis CSV datoteke.
csv_file_path = "banke.csv"
with open(csv_file_path, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Mesto", "Naziv", "Šifra podjetja", "Država", "Tržna kapitalizacija (milijarde $)", "Cena na delnico ($)"])
    csv_writer.writerows(banke)