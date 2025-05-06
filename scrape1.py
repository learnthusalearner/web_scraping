import requests
from bs4 import BeautifulSoup
import json

pageData={
        "Title": [],
        "Content": [],
        "href":[]
}
url="https://iitk.ac.in/ccn/services/network/how-to-use-ssl-vpn"
html_fetch = requests.get(url)
soup = BeautifulSoup(html_fetch.content, 'lxml')


div_tag=soup.find('div',class_="row justify-content-center")
print(div_tag.h3.text)