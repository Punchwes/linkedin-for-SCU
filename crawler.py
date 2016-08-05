# coding=utf-8
import requests
import re
import json
from bs4 import BeautifulSoup, Comment
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def login(s):
    r = s.get('https://www.linkedin.com/uas/login')
    soup = BeautifulSoup(r.text, "lxml")
    soup = soup.find(id="login")
    loginCsrfParam = soup.find('input', id = 'loginCsrfParam-login')['value']
    csrfToken = soup.find('input', id = 'csrfToken-login')['value']
    sourceAlias = soup.find('input', id = 'sourceAlias-login')['value']
    isJsEnabled = soup.find('input',attrs={"name" :'isJsEnabled'})['value']
    source_app = soup.find('input', attrs={"name" :'source_app'})['value']
    tryCount = soup.find('input', id = 'tryCount')['value']
    clickedSuggestion = soup.find('input', id = 'clickedSuggestion')['value']
    signin = soup.find('input', attrs={"name" :'signin'})['value']
    session_redirect = soup.find('input', attrs={"name" :'session_redirect'})['value']
    trk = soup.find('input', attrs={"name" :'trk'})['value']
    fromEmail = soup.find('input', attrs={"name" :'fromEmail'})['value']

    payload = {
        'isJsEnabled':isJsEnabled,
        'source_app':source_app,
        'tryCount':tryCount,
        'clickedSuggestion':clickedSuggestion,
        'session_key':'forlinkedinuse@163.com',
        'session_password':'pqw950915',
        'signin':signin,
        'session_redirect':session_redirect,
        'trk':trk,
        'loginCsrfParam':loginCsrfParam,
        'fromEmail':fromEmail,
        'csrfToken':csrfToken,
        'sourceAlias':sourceAlias
    }

    s.post('https://www.linkedin.com/uas/login-submit', data=payload)
    return s

def getCompanins(s, start_url):
    r= s.get(start_url)

    html = r.text.encode("utf-8")
    code = re.search(r'<code id="voltron_srp_main-content" style="display:none;"><!--.+--></code>', html).group()
    code = code.replace(r'<code id="voltron_srp_main-content" style="display:none;"><!--', '')
    code = code.replace(r'--></code>', '')

    code_json = json.loads(code)
    company_json = code_json["content"]["page"]["voltron_unified_search_json"]["search"]["results"]

    company_list = []
    for company in company_json:
        company = company["company"]
        name = company["fmt_canonicalName"]
        fmt_industry = company["fmt_industry"]
        fmt_size= company["fmt_size"]
        fmt_location= company["fmt_location"]
        company_list.append("%s \t%s \t%s \t%s\n" % (name, fmt_industry, fmt_size, fmt_location))
    return company_list

def getPeople(code_json):
    person_json=code_json['content']['page']['voltron_unified_search_json']['search']['results']

    person_list=[]
    for person in person_json:
        if 'person' in person:
            person=person['person']
        else:
            person='it is an ad.'
        if 'fmt_name' in person:
            name=person['fmt_name']
        else:
            name='LinkedIn Member'
        if 'fmt_headline' in person:
            fmt_headline=person['fmt_headline']#fmt_headline
        else:
            fmt_headline='not specific'
        if 'fmt_industry' in person:
            fmt_industry=person['fmt_industry']
        else:
            fmt_industry='not specific'
        if 'fmt_location' in person:
            fmt_location=person['fmt_location']
        else:
            fmt_location='not specific'
        person_list.append("%s \t%s \t%s \t%s\n" % (name,fmt_headline,fmt_industry,fmt_location))
    return person_list 

def getNextPageURL(s ,start_url):
    r= s.get(start_url)

    html = r.text.encode("utf-8")
    code = re.search(r'<code id="voltron_srp_main-content" style="display:none;"><!--.+--></code>', html).group()
    code = code.replace(r'<code id="voltron_srp_main-content" style="display:none;"><!--', '')
    code = code.replace(r'--></code>', '')

    code_json = json.loads(code)
    resultPagination = code_json["content"]["page"]["voltron_unified_search_json"]["search"]["baseData"]["resultPagination"]
    if "nextPage" in resultPagination:
        if (resultPagination["nextPage"]["pageURL"].find("www.linkedin.com")!=-1):
            nextPageURL=resultPagination
        else:
            nextPageURL = "http://www.linkedin.com" + resultPagination["nextPage"]["pageURL"]
    else:
        nextPageURL = "NULL"

    return nextPageURL

def getNextPageURL(code_json):
    resultPagination=code_json["content"]["page"]["voltron_unified_search_json"]["search"]["baseData"]["resultPagination"]

    if'nextPage' in resultPagination:
        if (resultPagination["nextPage"]["pageURL"].find("www.linkedin.com")!=-1):
            nextPageURL=resultPagination["nextPage"]["pageURL"]
        else:
            nextPageURL= "http://www.linkedin.com" + resultPagination["nextPage"]["pageURL"]
    else:
        nextPageURL='NULL'
    return nextPageURL

def search(s ,start_url):
    with open("Financial Servicec AND EE Manufacturing", "wb") as of:
        while True:
            if start_url == "NULL":
                break
            r= s.get(start_url)
            html = r.text.encode("utf-8")
            code = re.search(r'<code id="voltron_srp_main-content" style="display:none;"><!--.+--></code>', html).group()
            code = code.replace(r'<code id="voltron_srp_main-content" style="display:none;"><!--', '')
            code = code.replace(r'--></code>', '')
            #code = code.replace(r"\u002d1","\u002d1")
            #code = re.sub(r"(,?)(\w+?)\s+?:", r"\1'\2' :", code)
            #code = code.replace("'","\"")
            #code=re.sub(pattern, repl, string)
            #code = code.replace('\u002d1','"\u002d1"')
            code = code.replace('"distance":\u002d1','"distance":"\u002d1"')
            code = code.replace('"distanceP":\u002d1','"distanceP":"\u002d1"')
            code = code.replace(r'\u003cB','')
            code = code.replace(r'\u003e','')
            code = code.replace(r'\u003c/B','')
            #f=open('newtestresult','w')
            #f.write(code)
            code_json = json.loads(code)
            
            start_url = getNextPageURL(code_json)
            print start_url
            person_list = getPeople(code_json)
            for line in person_list:
                of.write(line)



if __name__ == '__main__':
    s = requests.session()
    s = login(s)
    start_url = r"https://www.linkedin.com/vsearch/p?orig=FCTD&rsid=5009760981464354290453&keywords=sichuan%20university&trk=vsrp_people_sel&trkInfo=VSRPsearchId%3A5009760981464350746423,VSRPcmpt%3Atrans_nav&f_ED=11356&f_L=en&pt=people&openFacets=N,G,CC,I,ED,L&f_I=43,112"
    search(s ,start_url)

