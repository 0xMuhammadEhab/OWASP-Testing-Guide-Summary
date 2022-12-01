## Summary

Web server fingerprinting is a critical task for the penetration tester. Knowing the version and type of a running web server allows testers to determine known vulnerabilities and the appropriate exploits to use during testing.

## Test Objectives

Find the version and type of a running web server to determine known vulnerabilities and the appropriate exploits to use during testing.

## How to Test

- The simplest and most basic form of identifying a web server is to look at the Server field in the HTTP response header.
    
    However, this testing methodology is limited in accuracy. There are several techniques that allow a web site to obfuscate or to modify the server banner string. For example one could obtain the following answer:
    
    ```bash
    403 HTTP/1.1 Forbidden
    Date: Mon, 16 Jun 2003 02:41: 27 GMT
    Server: Unknown-Webserver/1.0
    Connection: close
    Content-Type: text/HTML; charset=iso-8859-1
    In this case, the server field of that response is obfuscated.
    ```
    

In this case, the server field of that response is obfuscated. The tester cannot know what type of web server is running based on such information.

## Protocol Behavior

### **HTTP header field ordering**

The first method consists of observing the ordering of the several headers in the response. Every web server has an inner ordering of the header. Consider the following answers as an example:

Response from Apache 1.3.23

```bash
$ nc apache.example.com 80
HEAD / HTTP/1.0

HTTP/1.1 200 OK
Date: Sun, 15 Jun 2003 17:10: 49 GMT
Server: Apache/1.3.23
Last-Modified: Thu, 27 Feb 2003 03:48: 19 GMT
ETag: 32417-c4-3e5d8a83
Accept-Ranges: bytes
Content-Length: 196
Connection: close
Content-Type: text/HTML
```

Response from IIS 5.0

```bash
$ nc iis.example.com 80
HEAD / HTTP/1.0

HTTP/1.1 200 OK
Server: Microsoft-IIS/5.0
Content-Location: http://iis.example.com/Default.htm
Date: Fri, 01 Jan 1999 20:13: 52 GMT
Content-Type: text/HTML
Accept-Ranges: bytes
Last-Modified: Fri, 01 Jan 1999 20:13: 52 GMT
ETag: W/e0d362a4c335be1: ae1
Content-Length: 133
```

Response from Netscape Enterprise 4.1

```bash
$ nc netscape.example.com 80
HEAD / HTTP/1.0

HTTP/1.1 200 OK
Server: Netscape-Enterprise/4.1
Date: Mon, 16 Jun 2003 06:01: 40 GMT
Content-type: text/HTML
Last-modified: Wed, 31 Jul 2002 15:37: 56 GMT
Content-length: 57
Accept-ranges: bytes
Connection: close
```

Response from a SunONE 6.1

```bash
$ nc sunone.example.com 80
HEAD / HTTP/1.0

HTTP/1.1 200 OK
Server: Sun-ONE-Web-Server/6.1
Date: Tue, 16 Jan 2007 15:23:37 GMT
Content-length: 0
Content-type: text/html
Date: Tue, 16 Jan 2007 15:20:26 GMT
Last-Modified: Wed, 10 Jan 2007 09:58:26 GMT
Connection: close
```

We can notice that the ordering of the Date field and the Server field differs between Apache, Netscape Enterprise, and IIS.

### **Malformed requests test**

Another useful test to execute involves sending malformed requests or requests of nonexistent pages to the server. Consider the following HTTP responses.

Response from Apache 1.3.23

```bash
$ nc apache.example.com 80
GET / HTTP/3.0

HTTP/1.1 400 Bad Request
Date: Sun, 15 Jun 2003 17:12: 37 GMT
Server: Apache/1.3.23
Connection: close
Transfer: chunked
Content-Type: text/HTML; charset=iso-8859-1
```

Response from Apache 1.3.23

```bash
$ nc apache.example.com 80
GET / JUNK/1.0

HTTP/1.1 200 OK
Date: Sun, 15 Jun 2003 17:17: 47 GMT
Server: Apache/1.3.23
Last-Modified: Thu, 27 Feb 2003 03:48: 19 GMT
ETag: 32417-c4-3e5d8a83
Accept-Ranges: bytes
Content-Length: 196
Connection: close
Content-Type: text/HTML
```

## Tools

- httprint - [http://net-square.com/httprint.html](http://net-square.com/httprint.html)
- httprecon - [http://www.computec.ch/projekte/httprecon/](http://www.computec.ch/projekte/httprecon/)
- Netcraft - [http://www.netcraft.com](http://www.netcraft.com/)
- Desenmascarame - [http://desenmascara.me](http://desenmascara.me/)

### Automated Testing

like httprint

### Online Testing

Online tools can be used if the tester wishes to test more stealthily and doesn’t wish to directly connect to the target website. An example of an online tool that often delivers a lot of information about target Web Servers, is Netcraft. With this tool we can retrieve information
about operating system, web server used, Server Uptime, Netblock Owner, history of change related to Web server and O.S.

### malReq.py
it is a very simple python script for testing malformed requests 
- https://github.com/0x3h4b/OWASP-Testing-Guide-Summary/blob/main/OWASP-Scripts/malReq.py

## References

Whitepapers

- Saumil Shah: “An Introduction to HTTP fingerprinting” - http://[www.net-square.com/httprint_paper.html](http://www.net-square.com/httprint_paper.html)
- Anant Shrivastava: “Web Application Finger Printing” - http://[anantshri.info/articles/web_app_finger_printing.html](http://anantshri.info/articles/web_app_finger_printing.html)
