import re
import orodja


for i in range(1, 16):
    url = (
        'https://firstcycling.com/ranking.php?h=1&rank=1&y=2023&page={}&wom=1'
    ).format(i)
    orodja.shrani_spletno_stran(
        url, 'strani/kolesar_{}.html'.format(i)
)

vzorec_bloka = re.compile(
    r'<td>\d+</td>.*?</tr>',
    re.DOTALL)

vzorec_kolesa = re.compile(
    r'<td>(?P<mesto>\d+?)</td>'
    r'<a href="rider.php?r=\d+?" title="(?P<ime>.\w+?\s\w+?\s?\w+?\s?\w+?)">'
    r'<a href="nation.*?>(?P<drzava>\w+?\s?\w+?\s?\w+?)</a>'
    r'<a href="team.*?>(?P<ekipa>\w+?\s?\w+?\s?\w+?\s?\w+?\s?\w+?)</a>'
    r'<td>(?P<tocke>\d*?.\?\d+).*?</td>',
    re.DOTALL)

def izloci_podatke_kolesa(blok):
    kolo = {}
    kolo_vzor = vzorec_kolesa.search(blok)
    if kolo_vzor is not None:
        kolo = kolo_vzor.groupdict()
        kolo['mesto'] = int(kolo['mesto'])
        kolo['ime'] = str(kolo['ime'])
        kolo['drzava'] = str(kolo['drzava'])
        kolo['tocke'] = int(kolo['tocke'])
    return kolo




def kolesarji_s_strani(stevilo):
    ime = 'strani/kolesar_{}.html'.format(
        stevilo)
    vsebina = orodja.vsebina_datoteke(ime)
    for blok in vzorec_bloka.finditer(vsebina):
        yield izloci_podatke_kolesa(blok.group(0))



kolesarji = []
for stevilo in range(1, 16):
    for kolesar in kolesarji_s_strani(stevilo):
        if kolesar != {}:
            kolesarji.append(kolesar)


orodja.zapisi_csv(
    kolesarji,
    ['mesto', 'ime', 'drzava', 'tocke'],
    'podatki/kolesarji.csv'
)



