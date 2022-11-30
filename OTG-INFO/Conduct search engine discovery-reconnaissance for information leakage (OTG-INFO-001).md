## Test Objectives

To understand what sensitive design and configuration information of the application/system/organization is exposed both directly (on the organization’s website) or indirectly (on a third party website).

## How to Test

Use a search engine to search for:

- Network diagrams and configurations
- Archived posts and emails by administrators and other key staff
- Log on procedures and username formats like : admin-just123@just.co
- Usernames and password
- Error message content
- Development, test, UAT and staging versions of the website

## Search operators

Using the advanced “site:” search operator, it is possible to restrict search results to a specific domain. Do not limit testing to just one search engine 

- Baidu
- [binsearch.info](http://binsearch.info/)
- Bing
- Duck Duck Go
- ixquick/Startpage
- Google
- Shodan
- PunkSpider

Example To find the web content of [owasp.org](http://owasp.org/) indexed by a typical search engine, the syntax required is:

```text
site:owasp.org
```

To display the index.html of [owasp.org](http://owasp.org/) as cached, the syntax is:

```text
cache:owasp.org
```

## Google Hacking Database

The Google Hacking Database is list of useful search queries for Google. Queries are put in several categories:

- Footholds
- Files containing usernames
- Sensitive Directories
- Web Server Detection
- Vulnerable Files
- Vulnerable Servers
- Error Messages
- Files containing juicy info
- Files containing passwords
- Sensitive Online Shopping Info
