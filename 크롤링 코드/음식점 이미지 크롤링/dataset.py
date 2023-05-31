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
sql = "SELECT 업소명 FROM apiapi_daejeonfood ORDER BY id" 
cur.execute(sql)
rows = cur.fetchall()

cur2 = con.cursor()
sql2 = "SELECT 소재지주소 FROM apiapi_daejeonfood ORDER BY id" 
cur2.execute(sql2)
call = cur2.fetchall()


title = []

for i in rows:
    new = str(i)[9:-2]
    title.append(new)

add = []

for j in call:
    if "동구" in str(j):
        add.append("동구")
        continue
    elif "중구" in str(j):
        add.append("중구")
        continue
    elif "서구" in str(j):
        add.append("서구")
        continue
    elif "유성구" in str(j):
        add.append("유성구")
        continue
    elif "대덕구" in str(j):
        add.append("대덕구")
        continue

search = []
cnt = 0
for a in title:
    search.append(str(add[cnt])+ " " +str(a))
    cnt += 1


imgs = []
driver = webdriver.Chrome('chromedriver.exe') 


cur3 = con.cursor()

for cnt in range(370):
    fir = add[cnt]
    sec = title[cnt]
    driver.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=대전+' + fir + '+' + sec)
    sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    last = soup.select("#ibu_1")
    if len(str(last)) < 5:
        last = soup.select("#ugc_1")
        print(last)

    start = str(last).find('url') + 5
    end = str(last).find('jpg') + 3
    end2 = str(last).find('png') + 3
    
    if len(str(last)[start:end]) < 5:
        if len(str(last)[start:end2]) <5:
            imgs.append("NULL")
            print(str(cnt+1)+"번 "+sec+" -> 실패\n" + imgs[cnt])
            sql = "UPDATE apiapi_daejeonfood SET img_url='NULL' WHERE id='"+ str(cnt+1) +"';"
            cur3.execute(sql)
        else:
            imgs.append(str(last)[start:end2])
            print(str(cnt+1)+"번 "+sec+" -> 성공\n" + imgs[cnt])
            sql = "UPDATE apiapi_daejeonfood SET img_url='"+ str(imgs[cnt]) +"' WHERE id='"+ str(cnt+1) +"';"
            cur3.execute(sql)
    else:
        imgs.append(str(last)[start:end])
        print(str(cnt+1)+"번 "+sec+" -> 성공\n" + imgs[cnt])
        sql = "UPDATE apiapi_daejeonfood SET img_url='"+ str(imgs[cnt]) +"' WHERE id='"+ str(cnt+1) +"';"
        cur3.execute(sql)
    
con.close()

