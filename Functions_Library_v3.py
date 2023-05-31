# Python functions library v3
# written by Liam Swayne

# takes a package name, and installs it with pip
# if pip is not updated, the function updates pip
def install(package):
    import importlib, subprocess, sys

    try:
        subprocess.check_call([sys.executable, "pip", "install", "--upgrade", "pip"])
        print("Successfully upgraded pip")
    except Exception:
        pass
    
    try:
        import pkg_resources
        pkg_resources.get_distribution(package)
        print("Package '"+package + "' is already installed")
    except pkg_resources.DistributionNotFound:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("Successfully installed '"+package+"' with pip")
        except Exception:
            print("ALERT! Could not install '"+package+"'")

# takes message, which will display when the alert is called
# gives the line number at which the alert was called
# ex: alert("Dangerous for loop") on line 16 gives "ALERT! Dangerous for loop <-- line 16"
def alert(message=""):
    import inspect

    message = str(message)
    frame = inspect.currentframe().f_back
    line_no = frame.f_lineno
    if message == "":
        print("ALERT! <-- line "+str(line_no))
    else:
        print("ALERT! "+message+" <-- line "+str(line_no))

# takes any built-in type of input, and converts it to the most likely type
# if a list, or list of lists is given, every item in every list is assigned its most likely type
# ex: setType("  -1    ") returns -1
# ex: setType([1, 2, "3", [4, "5"]]) returns [1, 2, 3, [4, 5]]
def setType(input):
    if isinstance(input, list):
        return [setType(item) for item in input]
    
    input = str(input)
    while input[0] == " ":
        input = input[1:]
    while input[-1] == " ":
        input = input[:-1]
    if input == "True" or input == "true":
        input = True
    elif input == "False" or input == "false":
        input = False
    else:
        try:
            input = float(input)
            if str(input).endswith(".0"):
                input = int(input)
        except ValueError:
            pass
    return input

# get html page as string from URL
def getURL(linkStr,ipaddressClassA=109,shutdown=False):
    import requests, sys, bs4, re
    
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
            text = str(bs4.BeautifulSoup(response.content, 'html.parser'))
            for i in range(len(blankTexts)):
                if re.search(blankTexts[i],text):
                    successful = False
    if successful:
        return text
    else:
        alert("getURL() <-- LINK EXTRACT FAILURE")

# prints without a newline. short for 'print same'
def prints(string):
    print(string, end='')
