## Summary

This section describes how to test various metadata files for information leakage of the web application’s path(s), or functionality. Furthermore, the list of directories that are to be avoided by Spiders, Robots, or Crawlers can also be created as a dependency for Map execution path through application Other information may also be collected to identify attack surface, technology details, or for use in social engineering engagement.

## Test Objectives

- Identify hidden or obfuscated paths and functionality through the analysis of metadata files.
- Extract and map other information that could lead to a better understanding of the systems at hand.

## How to Test

Any of the actions performed below with wget could also be done with curl. 

Many Dynamic Application Security Testing (DAST) tools such as ZAP and  Burp Suite include checks or parsing for these resources as part of their spider/crawler functionality. They can also be identified using  various Google Dorks or leveraging advanced search features such as `inurl:`.

### Robots

```bash
$ curl -O -Ss http://www.google.com/robots.txt && head -n5 robots.txt
User-agent: *
Disallow: /search
Allow: /search/about
Allow: /search/static
Allow: /search/howsearchworks
...
```

### Analyze robots.txt Using Google Webmaster Tools

Web site owners can use the Google “Analyze robots.txt” function to analyze the website as part of its [Google Webmaster Tools](https://www.google.com/webmasters/tools). This tool can assist with testing and the procedure is as follows:

1. Sign into Google Webmaster Tools with a Google account.
2. On the dashboard, enter the URL for the site to be analyzed.
3. Choose between the available methods and follow the on screen instruction.

### META Tags

`<META>` tags are located within the `HEAD` section of each HTML document and should be consistent across a web site in the event that the robot/spider/crawler start point does not 
begin from a document link other than webroot i.e. a [deep link](https://en.wikipedia.org/wiki/Deep_linking). Robots directive can also be specified through use of a specific [META tag](https://www.robotstxt.org/meta.html).

### Robots META Tag

If there is no `<META NAME="ROBOTS" ... >` entry then the “Robots Exclusion Protocol” defaults to `INDEX,FOLLOW` respectively. Therefore, the other two valid entries defined by the “Robots Exclusion Protocol” are prefixed with `NO...` i.e. `NOINDEX` and `NOFOLLOW`.

Based on the Disallow directive(s) listed within the `robots.txt` file in webroot, a regular expression search for `<META NAME="ROBOTS"` within each web page is undertaken and the result compared to the `robots.txt` file in webroot.

### **Sitemaps**

```xml
$ wget --no-verbose https://www.google.com/sitemap.xml && head -n8 sitemap.xml
2020-05-05 12:23:30 URL:https://www.google.com/sitemap.xml [2049] -> "sitemap.xml" [1]

<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.google.com/schemas/sitemap/0.84">
  <sitemap>
    <loc>https://www.google.com/gmail/sitemap.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.google.com/forms/sitemaps.xml</loc>
  </sitemap>
```

Exploring from there a tester may wish to retrieve the gmail sitemap `https://www.google.com/gmail/sitemap.xml`

```
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://www.google.com/intl/am/gmail/about/</loc>
    <xhtml:link href="https://www.google.com/gmail/about/" hreflang="x-default" rel="alternate"/>
    <xhtml:link href="https://www.google.com/intl/el/gmail/about/" hreflang="el" rel="alternate"/>
    <xhtml:link href="https://www.google.com/intl/it/gmail/about/" hreflang="it" rel="alternate"/>
    <xhtml:link href="https://www.google.com/intl/ar/gmail/about/" hreflang="ar" rel="alternate"/>
```

### **Security TXT**

allows websites to define security policies and contact details.

The file may be present either in the root of the webserver or in the `.well-known/` directory. Ex:

- `https://example.com/security.txt`
- `https://example.com/.well-known/security.txt`

Here is a real world example retrieved from LinkedIn 2020 May 05:

```bash
$ wget --no-verbose https://www.linkedin.com/.well-known/security.txt && cat security.txt
2020-05-07 12:56:51 URL:https://www.linkedin.com/.well-known/security.txt [333/333] -> "security.txt" [1]
# Conforms to IETF `draft-foudil-securitytxt-07`
Contact: mailto:security@linkedin.com
Contact: https://www.linkedin.com/help/linkedin/answer/62924
Encryption: https://www.linkedin.com/help/linkedin/answer/79676
Canonical: https://www.linkedin.com/.well-known/security.txt
Policy: https://www.linkedin.com/help/linkedin/answer/62924
```

### **Humans TXT**

is an initiative for knowing the people behind a website

```bash
$ wget --no-verbose  https://www.google.com/humans.txt && cat humans.txt
2020-05-07 12:57:52 URL:https://www.google.com/humans.txt [286/286] -> "humans.txt" [1]
Google is built by a large team of engineers, designers, researchers, robots, and others in many different sites across the globe. 
It is updated continuously, and built with more tools and technologies than we can shake a stick at. 
If you'd like to help us out, see careers.google.com.
```

### Other .well-known Information Sources

There are other RFCs and Internet drafts which suggest standardized uses of files within the `.well-known/` directory. Lists of which can be found [here](https://en.wikipedia.org/wiki/List_of_/.well-known/_services_offered_by_webservers) or [here](https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml).

```bash
.well-known/acme-challenge
.well-known/apple-app-site-association
.well-known/apple-developer-merchantid-domain-association
.well-known/ashrae
.well-known/humans.txt
.well-known/assetlinks.json
.well-known/autoconfig/mail
.well-known/browserid
.well-known/caldav
.well-known/carddav
.well-known/change-password
.well-known/coap
.well-known/com.apple.remotemanagement
.well-known/core
.well-known/csvm
.well-known/dat
.well-known/dnt
.well-known/dnt-policy.txt
.well-known/est
.well-known/genid
.well-known/gpc
.well-known/hoba
.well-known/host-meta
.well-known/host-meta.json
.well-known/http-opportunistic
.well-known/keybase.txt
.well-known/mercure
.well-known/matrix
.well-known/mta-sts.txt
.well-known/ni
.well-known/nodeinfo
.well-known/openid-configuration
.well-known/openorg
.well-known/openpgpkey
.well-known/posh
.well-known/pki-validation
.well-known/pubvendors.json
.well-known/reload-config
.well-known/resourcesync
.well-known/repute-template
.well-known/security.txt
.well-known/stun-key
.well-known/xrp-ledger.toml
.well-known/webfinger
.well-known/void
.well-known/uma2-configuration
.well-known/timezone
.well-known/time
```

```bash
robots.txt
sitemap.xml
security.txt
.well-known/security.txt

```
