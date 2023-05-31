# Python functions library v1
# written by Liam Swayne

'''
IMPORTS USED:
import sys
import reqeusts
from bs4 import BeautifulSoup # pip3 install beautifulsoup4
'''

#get data type and convert function.
def getType(a):
    a = str(a)
    if a == "True":
        a = True
    elif a == "False":
        a = False
    else:
        try:
            a = float(a)
            if str(a).endswith(".0"):
                a = int(a)
        except ValueError:
            pass
    return a

#refine input function. params are prompt and capitalization.
def takeInput(prompt="", caps=True):
    a = input(str(prompt))
    if caps:
        a = a.upper()
    a = getType(a)
    return a

#get html as tring from link
def getURL(linkStr,ipaddressClassA=109,shutdown=False):
    #imports
    import sys
    import requests
    from bs4 import BeautifulSoup
    import re
    
    fail = False
    successful = False
    headers = {
            'User-Agent': ''
            }
    headers.update({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'+str(ipaddressClassA)+'.0.0.0 Safari/537.36'})
    blankTexts = [
        'meta content="Error - IMDb"',
        '<html><body><b>Http/1.1 Service Unavailable</b></body> </html>',
        '<title>404 Error - IMDb</title>'
        ]
    
    rerouteCount = 0
    while not successful:
        if rerouteCount >= 10:
            print("Reroute limit reached hile getting: "+linkStr)
            fail = True
            if shutdown:
                print("Shutting down.")
                sys.exit()
            else:
                break
        try:
            response = requests.get(linkStr, headers=headers)
            successful = True
        except:
            ConnectionError
            if ipaddressClassA <= 255:
                ipaddressClassA+=1
            else:
                ipaddressClassA = 1
            headers.update({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'+str(ipaddressClassA)+'.0.0.0 Safari/537.36'})
            print("Connection error encountered. Rerouting...")
            rerouteCount +=1
        if successful:
            text = str(BeautifulSoup(response.content, 'html.parser'))
            for i in range(len(blankTexts)):
                if re.search(blankTexts[i],text):
                    successful = False
    if not fail:
        return text
    else:
        return "LINK EXTRACT FAILURE <-- getURL()"
