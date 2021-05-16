#https://butter-shower.tistory.com/189
from bs4 import BeautifulSoup
from datetime import datetime
import requests
 
from notion.client import *
from notion.block import *
 
 
def MK():
    keyword = ['IPO', '투자유치']
    source = 'http://find.mk.co.kr/new/search.php?page=news'

    MK_NewsList = []
    for onekeyword in keyword:
        searchlink = source + '&s_keyword=' + onekeyword
        for i in range(1, 3): #페이지 3개 크롤링
            searchlink += '&pageNum=' + str(i)
            req = requests.get(searchlink)
            soup = BeautifulSoup(req.content.decode('euc-kr', 'replace'))
 
            rawnews = soup.select('.sub_list')
 
            for onenews in rawnews:
                title = onenews.select('span > a')[0].text
                newsurl = onenews.select('span > a')[0].get('href')
                published_date = onenews.select('span.art_time')[0].text
                published_date = published_date[-24:]
                published_date = published_date[0:4] + '-' + published_date[6:8] + '-' + published_date[10:12] + ' ' + published_date[-9:]
                # now = datetime.now()
                # create_date = "%s-%02d-%s %02d:%02d:%02d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
 
                crawling_one_news = {
                    '기사 제목' : title,
                    '기사 링크' : newsurl,
                    '기사 날짜' : published_date,
                    '키워드' : onekeyword,
                    '출처' : '매일경제'
                    # '크롤링 날짜' : create_date
                }
 
                MK_NewsList.append(crawling_one_news)
 
    return MK_NewsList


def daily_economics(token_v2,url):
    # 생성할 표 페이지에 들어가는 정보입니다. 제목, url링크, 날짜 등등이 들어갑니다. (위의 뉴스 데이터 형식과 맞춰주면 됩니다.)
    def get_collection_schema():
        return {
            "title" : {"name" : "title", "type" : "text"},
            "url" : {"name" : "url", "type" : "url"},
            "crawlingdate" : {"name" : "crawlingdate", "type" : "text"},
            "publisheddate" : {"name" : "publisheddate" , "type" : "text"},
            "source" : {"name" : "source", "type" : "text"},
            "keyword" : {"name" : "keyword", "type" : "text"}
        }
    
    # 위에서 했던 작업이죠? 클라이언트를 만들고 페이지 정보를 가져옵시다.
    client = NotionClient(token_v2 = token_v2)
    page = client.get_block(url)
    
    # 위에서 작성한 url에서 새로운 페이지를 만듭니다. 이 페이지는 노션의 collection 형식의 페이지고 여기에 크롤링한 정보들을 넣어줍니다.
    chlid_page = page.children.add_new(CollectionViewPageBlock)
    child_page.collection = client.get_collection(
        client.create_record('collection', parent=child_page, schema=get_collection_schema())
    )
    
    child_page.title = "매일경제 크롤링" # 페이지 제목입니다.
    news = MK() # news 변수에 크롤링한 뉴스 내용들이 들어갑니다.
    
    for onenews in news:
        row = child_page.collection.add_row() # 표에서 한 row를 생성해줍니다.
        row.title = onenews['기사 제목']
        row.source = onenews['출처']
        row.publisheddate = onenews['기사 날짜']
        row.crawlingdate = onenews['크롤링 날짜']
        row.url = onenews['기사 링크']
        row.keyword = onenews['키워드']
    
    view = child_page.views.add_new(view_type='table') # 이렇게 view까지 선언해주면 끝!

def arxivsound(token_v2,url):
    client = NotionClient(token_v2=token_v2)

    # 스벅남 페이지 URL
    page = client.get_block(url)

    print("Page 제목은  :", page.title)

    ################################
    # API 호출로 PageBlock 추가
    ################################


    today = datetime.today()

    # dd/mm/YY
    d1 = today.strftime("%Y-%m-%d")

    page.children.add_new(PageBlock, title=d1)

    
    ####################################
    # PageBlock에 TodoBlock 추가
    ####################################
    for child in page.children :
        child_page = client.get_block(child.id)
        child_page.children.add_new(HeaderBlock, title="HeaderBlock")
        child_page.children.add_new(SubheaderBlock, title="SubheaderBlock")
        child_page.children.add_new(SubsubheaderBlock, title="SubsubheaderBlock")
        child_page.children.add_new(TextBlock, title="TextBlock")
        child_page.children.add_new(NumberedListBlock, title="NumberedListBlock")
        child_page.children.add_new(BulletedListBlock, title="BulletedListBlock")
        child_page.children.add_new(DividerBlock)
        child_page.children.add_new(NumberedListBlock, title="NumberedListBlock2")
        # child_page.title = "The title has now changed, and has *live-updated* in the browser!"
if __name__ == '__main__':

    token_v2 = "" # 여러분들이 위에서 찾은 토큰을 입력하세요
    url = "https://www.notion.so" # 여러분들의 노션 페이지 url을 입력하세요


    arxivsound(token_v2,url)
