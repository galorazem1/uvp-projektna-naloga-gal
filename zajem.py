import re
import orodja

for i in range(1, 16):
    url = (
        'https://firstcycling.com/ranking.php?h=1&rank=1&y=2023&page={}&wom=1'
    ).format(i)
    orodja.shrani_spletno_stran(
        url, 'strani/kolesar_{}.html'.format(i)
)








