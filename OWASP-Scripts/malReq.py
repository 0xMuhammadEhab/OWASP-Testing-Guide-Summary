import requests
from http.client import HTTPConnection

res = set()
url = "http://testphp.vulnweb.com/"  # change url 
manipulated = []
version = ["1.0","1.1","2.0","3.0"]
for i in version:
    manipulated.append("HTTP/"+i)
    manipulated.append("JUNKK/"+i)


for i in manipulated:
    HTTPConnection._http_vsn_str =  i
    try:
        res.add(requests.get(url).headers["Server"])
        res.add(requests.post(url).headers["Server"])
        res.add(requests.head(url).headers["Server"])
    except :
        pass


print(res)


