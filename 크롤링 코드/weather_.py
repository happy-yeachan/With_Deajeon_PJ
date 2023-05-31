from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import pymysql 

con = pymysql.connect(host='43.200.63.156', port = 50356, user='root', password='1q2w3e!Q@W#E',
                      db='daejeonapi', charset='utf8', # 한글처리 (charset = 'utf8')
                      autocommit=True, # 결과 DB 반영 (Insert or update)
                      cursorclass=pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
                     )

driver = webdriver.Chrome('chromedriver.exe') 
driver.get("https://daejeon.kma.go.kr/")

elem = driver.find_element(By.XPATH,"//*[@id='sub_wrap']/div[2]/div[1]/div[1]/div[2]/div[2]/p[2]/img")
elem2 = driver.find_element(By.XPATH,"//*[@id='current-weather']/div[1]/div[2]/ul[1]/li[1]/span[4]")

imgurl= elem.get_attribute('src')
tmp=elem2.text[:-1]
print(tmp)
cur = con.cursor()
 
sql = "UPDATE apiapi_daejeonweather SET tmp='"+ tmp +"' WHERE id='1';"
sql2 = "UPDATE apiapi_daejeonweather SET img_url='"+ imgurl +"' WHERE id='1';"

cur.execute(sql)
cur.execute(sql2)
con.close()