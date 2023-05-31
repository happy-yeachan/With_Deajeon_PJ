import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By
import pymysql 

con = pymysql.connect(host='43.200.63.156', port = 50356, user='root', password='1q2w3e!Q@W#E',
                      db='daejeonapi', charset='utf8', # 한글처리 (charset = 'utf8')
                      autocommit=True, # 결과 DB 반영 (Insert or update)
                      cursorclass=pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
                     )


cur = con.cursor()
sql = "SELECT title FROM apiapi_daejeonrest ORDER BY id" 
cur.execute(sql)
rows = cur.fetchall()
driver = webdriver.Chrome('chromedriver.exe')
print(rows)

cnt = 1
for this in rows:
    data = str(this)[11:-2]
    driver.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=대전 '+ data) 
    sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    last = soup.select("#ugc_1")
    if len(str(last))<1:
        last = soup.select("#ibu_1")

    first = str(last).find("url")+5
    end = str(last).find("jpg")+3
    if end == -1:
        end = str(last).find("png")+3
    img = str(last)[first:end]
    # sql = "UPDATE apiapi_cafe SET img_url='"+ str(img) +"' WHERE id='"+ str(cnt) +"';"
    # cur.execute(sql)
    print(this)
    print(img)
    cnt += 1

con.close()