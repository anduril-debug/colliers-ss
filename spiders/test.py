import requests
from bs4 import BeautifulSoup


URL = "https://ss.ge/ka/udzravi-qoneba/l/bina/iyideba?Page=1&RealEstateTypeId=5&RealEstateDealTypeId=4&StatusField.FieldId=34&StatusField.Type=SingleSelect&StatusField.StandardField=Status&PriceType=false&CurrencyId=1"
response = requests.get(URL)


soup = BeautifulSoup(response.content,'html.parser')


buttons = soup.find('div', class_="latest_all_adds")

last_li = buttons.find('li', "last")

pagination = int(last_li.a.text)

print(pagination)
