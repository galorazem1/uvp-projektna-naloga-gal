import re
import orodja

url = ('https://companiesmarketcap.com/banks/largest-banks-by-market-cap/')
orodja.shrani_spletno_stran(url, 'strani/bogat_1.html')

for i in range(2, 7):
    url = (
        'https://companiesmarketcap.com/banks/largest-banks-by-market-cap/?page={}'
    ).format(i)
    orodja.shrani_spletno_stran(
        url, 'strani/bogat_{}.html'.format(i)
)






