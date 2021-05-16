import oauth2
import json
import datetime
import time
from config import *
import arxiv
import subprocess
import gscholar
from kakaotrans import Translator

from notion.client import *
from notion.block import *

# Tweet
tweet_consumer_key = ""
tweet_consumer_secret = ""

tweet_access_token = "-"
tweet_access_token_secret = ""


notion_token_v2 = "" # 여러분들이 위에서 찾은 토큰을 입력하세요
notion_url = "" # 노션 페이지 url을 입력하세요


def oauth2_request(consumer_key, consumer_secret, access_token, access_secret):
    try:
        consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
        token = oauth2.Token(key=access_token, secret=access_secret)
        client = oauth2.Client(consumer, token)
        return client
    except Exception as e:
        print(e)
        return None

def get_user_timeline(client, screen_name, count=50, include_rts='False'):
    base = "https://api.twitter.com/1.1"
    node = "/statuses/user_timeline.json"
    fields = "?screen_name={}&count={}&include_rts={}&tweet_mode=extended".format(screen_name, count, include_rts)
    #fields = "?screen_name=%s" % (screen_name)
    url = base + node + fields

    response, data = client.request(url)

    try:
        if response['status'] == '200':
            return json.loads(data.decode('utf-8'))
    except Exception as e:
        print(e)
        return None

def getTwitterTwit(tweet, jsonResult):

    tweet_id = tweet['id_str']
    tweet_message = '' if 'full_text' not in tweet.keys() else tweet['full_text']

    screen_name = '' if 'user' not in tweet.keys() else tweet['user']['screen_name']

    tweet_link = ''
    if tweet['entities']['urls']: #list
        for i, val in enumerate(tweet['entities']['urls']):
            tweet_link = tweet_link + tweet['entities']['urls'][i]['url'] + ' '
    else:
        tweet_link = ''

    hashtags = ''
    if tweet['entities']['hashtags']: #list
        for i, val in enumerate(tweet['entities']['hashtags']):
            hashtags = hashtags + tweet['entities']['hashtags'][i]['full_text'] + ' '
    else:
        hashtags = ''

    if 'created_at' in tweet.keys():
        # Twitter used UTC Format. EST = UTC + 9(Korean Time) Format ex: Fri Feb 10 03:57:27 +0000 2017
        tweet_published_date = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        tweet_published_date = tweet_published_date + datetime.timedelta(hours=+9)
        tweet_published_date = tweet_published_date.strftime('%Y-%m-%d')
    else:
        tweet_published_date = ''

    num_favorite_count = 0 if 'favorite_count' not in tweet.keys() else tweet['favorite_count']
    num_comments = 0
    num_shares = 0 if 'retweet_count' not in tweet.keys() else tweet['retweet_count']
    num_likes = num_favorite_count
    num_loves = num_wows = num_hahas = num_sads = num_angrys = 0

    arXiv_id= tweet_message[2:].split("arXiv:")[-1].split(" ")[0]

    paper_authors = tweet_message.split("''")[-1].split(", h")[0]

    if "UPDATED" in tweet_message:
        state_paper = "UPDATED"
    else:
        state_paper = "PUBLISHED_NEW"

    search = arxiv.Search(id_list=[arXiv_id])

    paper = next(search.get()) 

    paper_title = paper.title
    paper_abstract_en = paper.summary

    paper_pdf_url = paper.pdf_url

    arXiv_published_date = paper.published.strftime('%Y-%m-%d')
    arXiv_updated_date = paper.updated.strftime('%Y-%m-%d')


    paper_abstract_en = paper_abstract_en.replace("\n", " ")
    translator = Translator()


    paper_abstract_kor=translator.translate(paper_abstract_en)
    # print(abstract_kor)

    #kakao i with API directly
    #command="curl -v --get \"https://dapi.kakao.com/v2/translation/translate\" -d \"src_lang=en\" -d \"target_lang=kr\" --data-urlencode \"query={}\" -H \"Authorization: KakaoAK 2c23113da7ecacd5429a52026903fc45\"".format(abstract)
    #output = subprocess.check_output(command, shell=True)
    # file=json.loads(command.decode('utf-8'))
    # for idx, content in enumerate(file['translated_text']):
    #     print(content)

    # googletrans
    # from googletrans import Translator
    # translator = Translator()
    # result = translator.translate('안녕하세요.', dest="ja")
    # print(result[0].text)
    
    jsonResult[arXiv_id] = {'tweet_post_id':tweet_id, 'tweet_message':tweet_message,
                    'tweet_published_date':tweet_published_date, 'paper_title': paper_title, 'paper_abstract_en': paper_abstract_en, 'paper_abstract_kor': paper_abstract_kor,
                    'paper_authors':paper_authors, 'paper_pdf_url':paper_pdf_url,  'arXiv_updated_date':arXiv_updated_date, 'arXiv_published_date':arXiv_published_date, 'paper_state': state_paper}

    # temp = {arXiv_id: {'tweet_post_id':tweet_id, 'tweet_message':tweet_message,
    #                 'tweet_published_date':tweet_published_date, 'paper_title': paper_title, 'paper_abstract_en': paper_abstract_en, 'paper_abstract_kor': paper_abstract_kor,
    #                 'paper_authors':paper_authors, 'paper_pdf_url':paper_pdf_url,  'arXiv_updated_date':arXiv_updated_date, 'arXiv_published_date':arXiv_published_date, 'paper_state': state_paper}
    # }
    # jsonResult.append(temp)
    # jsonResult["arXiv_id"] = arXiv_id
    # jsonResult["arXiv_id"] = 
    
    # {'tweet_post_id':tweet_id, 'tweet_message':tweet_message,
    #                 'tweet_published_date':tweet_published_date, 'paper_title': paper_title, 'paper_abstract_en': paper_abstract_en, 'paper_abstract_kor': paper_abstract_kor,
    #                 'paper_authors':paper_authors, 'paper_pdf_url':paper_pdf_url,  'arXiv_updated_date':arXiv_updated_date, 'arXiv_published_date':arXiv_published_date, 'paper_state': state_paper}

    # jsonResult.append({'tweet_post_id':tweet_id, 'tweet_message':tweet_message,
    #                 'tweet_published_date':tweet_published_date, 'paper_title': paper_title, 'paper_abstract_en': paper_abstract_en, 'abstract_kor': paper_abstract_kor,
    #                 'authors':paper_authors, 'pdf_url':paper_pdf_url, 'arXiv_published_date': arXiv_published_date,  'arXiv_published_date':arXiv_published_date, 'arXiv_id':arXiv_id, 'state_paper': state_paper})

def check_today_tweet(jsonResult, today_YYYYMMDD):
    _jsonResult=dict()
    # print(len(jsonResult), jsonResult)

    for key in jsonResult.keys():
        if jsonResult[key]["tweet_published_date"] == today_YYYYMMDD:
            _jsonResult[key] = jsonResult[key]

    return _jsonResult
    
    # for i in jsonResult:
    #     if i['arXiv_id'] == '2105.01134v1':
    #         print(i['info']['arXiv_published_date'])
    #         break


def arxivsound(fname_json, today_YYYYMMDD):
    print(fname_json)
    with open(fname_json) as json_file:
        jsonResult = json.load(json_file)
    
    if jsonResult is {}:
        return
    
    list_new, list_update = list(), list()
    for key in jsonResult.keys():
        if jsonResult[key]["paper_state"] == "PUBLISHED_NEW":
            list_new.append(jsonResult[key])
        elif jsonResult[key]["paper_state"] == "UPDATED":
            list_update.append(jsonResult[key])
        else:
            raise ValueError
    print(list_new[0])
    print(len(list_update))

    client = NotionClient(token_v2=notion_token_v2)

    # 스벅남 페이지 URL
    page = client.get_block(notion_url)

    print("Title of the Notion Page:", page.title)


    page.children.add_new(PageBlock, title=today_YYYYMMDD)
    
    for child in page.children :
        child_page = client.get_block(child.id)
        child_page.children.add_new(HeaderBlock, title="New Papers")
        for objectPaper in list_new:
            
            paper_title=objectPaper['paper_title']
            paper_authors=objectPaper['paper_authors']
            paper_abstract_en=objectPaper['paper_abstract_en']
            paper_abstract_kor=objectPaper['paper_abstract_kor']

            paper_pdf_url=objectPaper['paper_pdf_url']
            arXiv_published_date=objectPaper['arXiv_published_date']
            arXiv_updated_date=objectPaper['arXiv_updated_date']

            # https://github.com/jamalex/notion-py/blob/master/notion/block.py
            # child_page.children.add_new(HeaderBlock, title="HeaderBlock")
            child_page.children.add_new(SubheaderBlock, title=paper_title)
            child_page.children.add_new(CalloutBlock, title=paper_abstract_en)
            # child_page.children.add_new(SubsubheaderBlock, title=paper_authors)
            child_page.children.add_new(BulletedListBlock, title="v1: "+arXiv_published_date+", Updated: "+arXiv_updated_date)
            child_page.children.add_new(BulletedListBlock, title=paper_authors)
            child_page.children.add_new(BulletedListBlock, title=paper_pdf_url)
            # child_page.children.add_new(BulletedListBlock, title=arXiv_updated_date)
            child_page.children.add_new(DividerBlock)
            # child_page.title = "The title has now changed, and has *live-updated* in the browser!"

        child_page.children.add_new(DividerBlock)
        child_page.children.add_new(HeaderBlock, title="Updated Papers")
        child_page.children.add_new(DividerBlock)
        child_page.children.add_new(DividerBlock)

        for objectPaper in list_update:
        
            paper_title=objectPaper['paper_title']
            paper_authors=objectPaper['paper_authors']
            paper_abstract=objectPaper['paper_abstract_en']
            paper_abstract_kor=objectPaper['paper_abstract_kor']

            paper_pdf_url=objectPaper['paper_pdf_url']
            paper_version=paper_pdf_url[-2:]
            arXiv_published_date=objectPaper['arXiv_published_date']
            arXiv_updated_date=objectPaper['arXiv_updated_date']

            # child_page.children.add_new(HeaderBlock, title="HeaderBlock")
            child_page.children.add_new(SubheaderBlock, title=paper_title)
            child_page.children.add_new(CalloutBlock, title=paper_abstract_en)
            # child_page.children.add_new(SubsubheaderBlock, title=paper_authors)
            child_page.children.add_new(BulletedListBlock, title="v1: "+arXiv_published_date+", Updated {}: ".format(paper_version)+arXiv_updated_date)
            child_page.children.add_new(BulletedListBlock, title=paper_authors)
            child_page.children.add_new(BulletedListBlock, title=paper_pdf_url)
            # child_page.children.add_new(BulletedListBlock, title=arXiv_updated_date)
            child_page.children.add_new(DividerBlock)
            # child_page.title = "The title has now changed, and has *live-updated* in the browser!"


def batch_previous_papers():

    # jsonResult = dict()
    fname_json='2000_number_twitter.json'
    with open(fname_json) as json_file:
        jsonResult = json.load(json_file)


    for idx in range(23,15,-1):

    # today_YYYYMMDD="2021-05-04"
        today_YYYYMMDD="2021-04-{}".format(idx)
        _fname_json='{}_twitter.json'.format(today_YYYYMMDD)

        # num_posts 만큼의 object 중, 오늘 tweet에 뜬 것만 저장 함
        _jsonResult=check_today_tweet(jsonResult, today_YYYYMMDD)

        if _jsonResult:
            # print(today_YYYYMMDD, _jsonResult)

            with open(_fname_json, 'w', encoding='utf8') as outfile:
                result = json.dumps(_jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
                outfile.write(result)

            print ('Saved in {}_twitter.json'.format(_fname_json))

            arxivsound(_fname_json, today_YYYYMMDD)
        else:
            print ('{}_twitter.json  is empty'.format(_fname_json))



def main():
    from datetime import datetime
    today = datetime.today()

    today_YYYYMMDD = today.strftime("%Y-%m-%d")
    fname_json='{}_twitter.json'.format(today_YYYYMMDD)


    tweet_id = "arxivsound"

    num_posts = 20

    jsonResult = dict()

    client = oauth2_request(tweet_consumer_key, tweet_consumer_secret, tweet_access_token, tweet_access_token_secret)
    tweets = get_user_timeline(client, tweet_id, num_posts)

    for tweet in tweets:
        getTwitterTwit(tweet, jsonResult)


    with open(fname_json, 'w', encoding='utf8') as outfile:
        result = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(result)

    print ('Saved in {}_twitter.json'.format(fname_json))


    # num_posts 만큼의 object 중, 오늘 tweet에 뜬 것만 저장 함
    jsonResult=check_today_tweet(jsonResult, today_YYYYMMDD)


    with open(fname_json, 'w', encoding='utf8') as outfile:
        result = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(result)

    print ('Saved in {}_twitter.json'.format(fname_json))

    arxivsound(fname_json, today_YYYYMMDD)



if __name__ == '__main__':
    # main()
    batch_previous_papers()
