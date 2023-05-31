import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep


con = pymysql.connect(host='database-1.c8asa7yzwsf5.ap-northeast-1.rds.amazonaws.com', user='yeachan', password='dhdPcks001228',
                      db='foods', charset='utf8', # 한글처리 (charset = 'utf8')
                      autocommit=True, # 결과 DB 반영 (Insert or update)
                      cursorclass=pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
                     )

cur = con.cursor()
sql = "SELECT title FROM apiapi_daejeontour ORDER BY id" 
cur.execute(sql)
rows = cur.fetchall()

title = []

for i in rows:
    new = str(i)[11:-2]
    title.append(new)


imgs = []
driver = webdriver.Chrome('chromedriver.exe') 


cur3 = con.cursor()

for cnt in range(len(title)):
    driver.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=image&query=' + title[cnt])
    sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    last = soup.select("#main_pack > section.sc_new.sp_nimage._prs_img._imageSearchPC > div > div.photo_group._listGrid > div.photo_tile._grid > div:nth-child(1) > div > div.thumb > a > img")
    start = str(last).find('src') + 5
    end = str(last).find('style') + -2
    last = str(last)[start:end]
    print(last)

    if len(last) < 5:
        imgs.append("NULL")
        print(str(cnt+1)+"번 "+last+" -> 실패\n" + imgs[cnt])
        sql = "UPDATE apiapi_daejeontour SET img_url='NULL' WHERE id='"+ str(cnt+1) +"';"
        cur3.execute(sql)
    
    else:
        imgs.append(str(last))
        print(str(cnt+1)+"번 "+title[cnt]+" -> 성공\n" + imgs[cnt])
        sql = "UPDATE apiapi_daejeontour SET img_url='"+ str(imgs[cnt]) +"' WHERE id='"+ str(cnt+1) +"';"
        cur3.execute(sql)
    
con.close()

