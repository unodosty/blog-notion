#https://codingman.tistory.com/162?category=762038

import json 
import requests 
from bs4 import BeautifulSoup
import requests 

def get_access_token():
    
    client_id = "aa1fe4b4a977b163cf6035c63ba59812"

    seckey= "aa1fe4b4a977b163cf6035c63ba59812ecc1fb0c61fd260b3a868e135c637ec552673694"

    callback_url = "http://sequencedata.tistory.com"

    # https://www.tistory.com/oauth/authorize?client_id=aa1fe4b4a977b163cf6035c63ba59812&redirect_uri=http://sequencedata.tistory.com&response_type=code&state=someValue
    code = "ca0e70139e27882b66c88df826800442cb1721beac5d536dd18af10275d282bb0aaa0adf"

    token_url="https://www.tistory.com/oauth/access_token?client_id={0}&client_secret={1}&redirect_uri={2}&code={3}&grant_type=authorization_code".format(client_id, seckey, callback_url, code) 
    res = requests.get(token_url) 
    access_token = res.text.split("=")[1] 

    print(access_token)
    return access_token

def post_tistory_page(title, content, tags_str):

    access_token = "ff585aad39b4ecbca7aa912b8a83f0cb_305294c0fc9b83cb2abe477e76f147fb"
    import requests 
    import json 

    url_post = "https://www.tistory.com/apis/post/write" 


    blog_name = "http://sequencedata.tistory.com" 

    # blog_name ="Notes" 

    title = "오늘의 뉴스" 

    content = "작성할 내용 포함" 

    visibility = 0 #(0: 비공개 - 기본값, 1: 보호, 3: 발행) 

    category = 1129286 # 본인 블로그의 카테고리 id를 확인하세요. 

    publish_time = '' 
    slogan = '' 
    tag = '경제,뉴스' 

    acceptComment = 1 # 댓글허용 
    password = '' # 보호글 비밀번호 
    headers = {'Content-Type': 'application/json; charset=utf-8'} 
    params = { 'access_token': access_token, 'output': 'json', 'blogName': blog_name, 'title': title, 'content': content, 'visibility': visibility, 'category': category, 'published': publish_time, 'slogan': slogan, 'tag': tag, 'acceptComment': acceptComment, 'password': password } 
    data = json.dumps(params) 
    rw = requests.post(url_post, headers=headers, data=data) 

    if rw.status_code == 200: 
        print('Success to post writing.') 
    else: 
        print('Fail to post writing.')

    # 사진 첨부
    # https://codingman.tistory.com/162?category=762038

if __name__ == '__main__':
    access_token = get_access_token()

    PATH_HTML='/Users/kakao/Downloads/sample.html' # download from notion page

    post_tistory_page(title, content, tags_str)
