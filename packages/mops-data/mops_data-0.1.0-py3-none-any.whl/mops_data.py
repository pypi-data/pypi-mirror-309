import requests
from bs4 import BeautifulSoup
def get_data(no, year, season):

    url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb01'

    myload = { 'encodeURIComponent': '1', 'step': '1',  'firstin': '1',  'off': '1',  'queryName': 'co_id',

                'inpuType': 'co_id', 'TYPEK': 'all',   'isnew': 'false', 'co_id': no,  

                'year': year,  'season': str(season) }  # 'isnew': 'false' or 'true' (看最新財報)

    html = requests.post(url, data = myload)

    html.encoding = 'UTF-8'

    myhtml = html.text

    # mydata = pd.read_html(mining.text)

    return myhtml