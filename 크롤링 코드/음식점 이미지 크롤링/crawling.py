from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('chromedriver.exe') 

# driver.get('https://www.google.com/maps/search/대전+동구+한밭식당?hl=ko')
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
# last = soup.select("#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.ZKCDEc > div.RZ66Rb.FgCUCc > button > img")
# print(str(last)[28:-128])

driver.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=대전+중구+우돈마루')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
last = soup.select("#ibu_1")
start = str(last).find('url') + 5
end = str(last).find('jpg') + 3
print(str(last)[start:end])