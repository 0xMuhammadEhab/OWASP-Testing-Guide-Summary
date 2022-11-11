## Summary

- Current HTTP standards do not include guidance on how to interpret multiple input parameters with the same name.
- Supplying multiple HTTP parameters with the same name may cause an application to interpret values in unanticipated ways.
- By exploiting these effects, an attacker may be able to bypass input validation, trigger application errors or modify internal variables values. As HTTP Parameter Pollution (in short HPP) affects a building block of all web technologies, server and client side attacks exist.

### 1. Input Validation and filters bypass

1. The ModSecurity filter would correctly blacklist the following string: `select 1,2,3 from table`, thus blocking this example URL from being processed by the web server: `/index.aspx?page=select 1,2,3` from table. However, by exploiting the concatenation of multiple HTTP parameters, an attacker could cause the application server to concatenate the string after the ModSecurity filter already accepted the input. As an example, the URL `/index.aspx?page=select 1&page=2,3 from table` would not trigger the ModSecurity filter, yet the application layer would concatenate the input back into the full malicious string.
2. Another HPP vulnerability turned out to affect Apple Cups, the well-known printing system used by many UNIX systems. Exploiting HPP, an attacker could easily trigger a Cross-Site Scripting vulnerability using the following URL: [`http://127.0.0.1:631/admin](http://127.0.0.1:631/admin)
/?kerberos=onmouseover=alert(1)&kerberos`. The application validation checkpoint could be bypassed by adding an extra kerberos argument having a valid string (e.g. empty string). As the validation checkpoint would only consider the second occurrence, the first kerberos parameter was not properly sanitized before being used to generate dynamic HTML content. Successful exploitation would result in Javascript code execution under the context of the hosting web site.

### 2. Authentication bypass

1. An even more critical HPP vulnerability was discovered in Blogger, the popular blogging platform. The bug allowed malicious users to take ownership of the victim’s blog by using the following HTTP request:
    
    ```python
    POST /add-authors.do HTTP/1.1
    
    security_token=attackertoken  
    &blogID=attackerblogidvalue
    &blogID=victimblogidvalue   
    &authorsList=goldshlager19test%40gmail.com(attacker email)   
    &ok=Invite
    ```
    
    The flaw resided in the authentication mechanism used by the web application, as the security check was performed on the first blogID parameter, whereas the actual operation used the second occurrence.
    

### 3. Expected Behavior by Application Server

- Given the URL and querystring: [`http://example.com/?color=red&](http://example.com/?color=red&-)color=blue`

| Web Application Server Backend | ASP | JSP |
| --- | --- | --- |
| ASP.NET / IIS | All occurrences concatenated
with a comma | color=red,blue |
| ASP / IIS | All occurrences concatenated
with a comma | color=red,blue |
| PHP / Apache | Last occurrence only | color=blue |
| PHP / Zeus | Last occurrence only | color=blue |
| JSP, Servlet / Apache Tomcat | First occurrence only | color=red |
| SP, Servlet / Oracle Application
Server 10g | First occurrence only | color=red |
| JSP, Servlet / Jetty | First occurrence only | color=red |
| IBM Lotus Domino | Last occurrence only | color=blue |
| IBM HTTP Server | First occurrence only | color=red |
| mod_perl, libapreq2 / Apache | First occurrence only | color=red |
| Perl CGI / Apache | First occurrence only | color=red |
| mod_wsgi (Python) / Apache | First occurrence only | color=red |
| Python / Zope | All occurrences in List data
type | color=[‘red’,’blue’] |

## How to Test

### 1. Server-side HPP

- For example: if testing the search_string parameter in the query string, the request URL would include that parameter name and value.
    
    [`http://example.com/?search_string=kittens`](http://example.com/?search_string=kittens)
    
- The particular parameter might be hidden among several other parameters, but the approach is the same; leave the other parameters in place and append the duplicate.
[`http://example.com/?mode=guest&search_string=kittens&num](http://example.com/?mode=guest&search_string=kittens&num_)_results=100`
- Append the same parameter with a different value and submit the new request.
    
    [`http://example.com/?mode=guest&search_string=kittens&num_](http://example.com/?mode=guest&search_string=kittens&num_)results=100&search_string=puppies`
    
- Analyze the response page to determine which value(s) were parsed. In the above example, the search results may show kittens, puppies, some combination of both (kittens,puppies or kittens~puppies or [‘kittens’,’puppies’]), may give an empty result, or error page.

This behavior, whether using the first, last, or combination of input parameters with the same name, is very likely to be consistent across the entire application. Whether or not this default behavior reveals a potential vulnerability depends on the specific input validation and filtering specific to a particular application.

As a general rule: if existing input validation and other security mechanisms are sufficient on single inputs, and if the server assigns only the first or last polluted parameters, then parameter pollution does not reveal a vulnerability

If the duplicate parameters are concatenated different web application components use different occurrences or testing generates an error, there is an increased likelihood of being able to use parameter pollution to trigger security vulnerabilities.

A more in-depth analysis would require three HTTP requests for each HTTP parameter:
[1] Submit an HTTP request containing the standard parameter name and value, and record the HTTP response. E.g. `page?par1=val1`
[2] Replace the parameter value with a tampered value, submit and record the HTTP response. E.g. `page?par1=HPP_TEST1`
[3] Send a new request combining step (1) and (2). Again, save the HTTP response. E.g. `page?par1=val1&par1=HPP_TEST1`
[4] Compare the responses obtained during all previous steps. If the response from (3) is different from (1) and the response from (3) is also different from (2), there is an impedance mismatch that may be eventually abused to trigger HPP vulnerabilities.

### 2. **Client-side HPP**

- Similarly to server-side HPP, manual testing is the only reliable technique to audit web applications in order to detect parameter pollution vulnerabilities affecting client-side components. While in the server-side variant the attacker leverages a vulnerable web application to access protected data or perform actions that either not permitted or not supposed to be executed, client-side attacks aim at subverting client-side components and technologies.
- To test for HPP client-side vulnerabilities, identify any form or action that allows user input and shows a result of that input back to the user. A search page is ideal, but a login box might not work (as it might not show an invalid username back to the user).
- Similarly to server-side HPP, pollute each HTTP parameter with %26HPP_TEST and look for url-decoded occurrences of the user-supplied payload:
    - `&HPP_TEST`
    - `&amp;HPP_TEST`
    - `… and others`
    
    In particular, pay attention to responses having HPP vectors within data, src, href attributes or forms actions. Again, whether or not this default behavior reveals a potential vulnerability depends on the specific input validation, filtering and application business logic. In addition, it is important to notice that this vulnerability can also affect query string parameters used in XMLHttpRequest (XHR), runtime attribute creation and other plugin technologies (e.g. Adobe Flash’s flashvars variables).
    
    ---
    
    ---
    

# Extra Info

## 1. **HPP Server Side Attacks**

- In server-side HPP, you send the servers unexpected information in an attempt to make the server-side code return unexpected results. When you make a request to a website, the site’s servers process the request and return a response
- in some cases, the servers don’t just return a web page but also run some code based on
information they receive from the URL that is sent. This code runs only on the servers, so it’s essentially invisible to you: you can see the information you send and the results you get back, but the code in between isn’t available.

### 1.1 Bank Example

[`https://www.bank.com/transfer?from=12345&to=67890&amount=5000`](https://www.bank.com/transfer?from=12345&to=67890&amount=5000)

- It’s possible the bank could assume that it will receive only one from parameter. But what happens if you submit two, as in the following URL:

[`https://www.bank.com/transfer?from=12345&to=67890&amount=5000&from=ABCDEF`](https://www.bank.com/transfer?from=12345&to=67890&amount=5000&from=ABCDEF)

```ruby
user.account = 12345
def prepare_transfer(params)
  params << user.account
  transfer_money(params) #user.account (12345) becomes params[2]
end

def transfer_money(params)
  to = params[0]
  amount = params[1]
  from = params[2]
  transfer(to,amount,from)
end
```

- so the arrangement differ from parameters to other
- the result of params array now is  [67890,5000,12345]
- if we add another parameter &from=lol

[`https://www.bank.com/transfer?to=67890&amount=5000&from=](https://www.bank.com/transfer?to=67890&amount=5000&from=ABCDEF)lol`

- the array will be  [67890,5000,lol,12345]

### 1.2 Example in java

- Suppose some code as the following
    
    ```java
    void private executeBackendRequest(HTTPRequest request){
    String amount=request.getParameter("amount");
    String beneficiary=request.getParameter("recipient");
    HttpRequest("http://backendServer.com/servlet/actions","POST",
    "action=transfer&amount="+amount+"&recipient="+beneficiary);
    }
    ```
    
- A malicious user may send a request like
    
    `http://frontendHost.com/page?amount=1000&recipient=Mat%26action%3dwithdraw`
    
- Then, the frontend will build the following back-end request
    
    ```java
    HttpRequest("http://backendServer.com/servlet/actions","POST",
    "action=transfer&amount="+amount+"&recipient="+beneficiary);
    ```
    
    `action=transfer&amount=1000&recipient=Mat&action=withdraw`
    
- Obviously depends on how the application will manage the occurrence

### 1.3 Account Take Over

[https://shahjerry33.medium.com/http-parameter-pollution-its-contaminated-85edc0805654](https://shahjerry33.medium.com/http-parameter-pollution-its-contaminated-85edc0805654)

[https://ashwinisp.medium.com/http-parameter-pollution-vulnerability-6fc1deb5bc63](https://ashwinisp.medium.com/http-parameter-pollution-vulnerability-6fc1deb5bc63)

### 1.4 URL Rewriting

- URL Rewriting could be affected as well if regexp are too permissive
    
    ```ruby
    RewriteCond %{THE_REQUEST} ^[A-Z]{3,9}\ .+page\.php.*\ HTTP/
    RewriteRule ^page\.php.*$ - [F,L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^([^/]+)$ page.php?action=view&page=$1&id=0 [L]
    ```
    
- if you enter [`http://host/abc`](http://host/abc)
- becomes: [`http://host/page.php?action=view&page=abc&id=0`](http://host/page.php?action=view&page=abc&id=0)
- An attacker may try to inject: `http://host/abc%26action%3dedit`
- and the url will be rewritten as [`http://host/page.php?action=view&page=abc&action=edit&id=0`](http://host/page.php?action=view&page=abc&action=edit&id=0)
- Obviously, the impact depends on the functionality exposed

### 1.5 Twitter Unsubscribe Notiﬁcations

[https://blog.mert.ninja/twitter-hpp-vulnerability/](https://blog.mert.ninja/twitter-hpp-vulnerability/)

## 2. **HPP Client Side Attacks**

- The HTTP Parameter Pollution (HPP) Client-side attack has to do with the client or user environment, meaning that the user’s actions (i.e. access a link in a browser) are affected and will trigger a malicious or unintended action without the user’s knowledge.

### 2.1. Example

- This Example **Copied from** [https://www.acunetix.com/blog/whitepaper-http-parameter-pollution/](https://www.acunetix.com/blog/whitepaper-http-parameter-pollution/)
- The following scenario is a webmail service website from where a user
 can view and delete his/her emails. The URL of the webmail website is:
    
    `http://host/viewemail.jsp?client_id=79643215`
    
- The link to view an email is
    
    `<a href=”viewemail.jsp?client_id=79643215&action=view”> View </a>`
    
- The link to delete an email is:
    
    `<a href=”viewemail.jsp?client_id=79643215&action=delete”> Delete </a>`
    
- When the user clicks on either of the above links, the appropriate  action will be performed. The two links are built from the URL. The ID  will be requested and will be embedded/added in the href link together with the according action. Thus:

```java
ID = Request.getParameter(“client_id”)
href_link = “viewemail.jsp?client_id=” + ID + ”&action=abc”
```

- This web application, and more precisely the client_id, is vulnerable to HPP. As seen below, an attacker creates a URL and injects another parameter ‘action’ preceded by an encoded query string delimiter (e.g. %26) after the client_id parameter. This parameter holds the value ‘delete’:
    
    `http://host/viewemailn.jsp?client_id=79643215%26action%3Ddelete`
    
- After the creation of the malicious link, the page now contains-  two  links which are injected with an extra action parameter. Thus:
    
    `<a href=viewemail.jsp?client_id=79643215&action=delete&action=view > View </a>`
    `<a href=viewemail.jsp?client_id=79643215&action=delete&action=delete > Delete </a>`
    

As shown in the table above, JSP will parse the two same parameters (action) and will return the first value. The JSP query Request.getParameter(“action”) will return ‘delete’ in both cases. Thus, the user will click either of the two links, View or Delete, but the action Delete will always be performed.

This is a simple example how an attacker can exploit an HTTP Parameter Pollution vulnerable website and cause malicious code to run or be executed without being detected.

### 2.2 Example

- This code generate a new url based on the value of `par`

```php
<? $val=htmlspecialchars($_GET['par'],ENT_QUOTES); ?>
<a href="/page.php?action=view&par='.<?=$val?>.'">View Me!</a>
```

- The attacker passes the value `123%26action=edit`
- The URL-encoded value for & is %26, which means that when the URL is parsed, the %26 is interpreted as &
- The htmlspecialchars function converts special characters, such as %26, to their HTML encoded values, turning into `&amp;`  (the HTML entity that represents & in HTML), where that
- character might have special meaning. The converted value is then stored in $val. Then a new link is generated by appending $val to the href value at ➋. So the generated link becomes  `<a href="/page.php?action=view&par=123&amp;action=edit">` . Consequently, the attacker has managed to add the additional action=edit to the href URL, which could lead to a vulnerability depending on how the application handles the
smuggled action parameter.

### resources

[https://owasp.org/www-pdf-archive/AppsecEU09_CarettoniDiPaola_v0.8.pdf](https://owasp.org/www-pdf-archive/AppsecEU09_CarettoniDiPaola_v0.8.pdf)

[https://nostarch.com/bughunting](https://nostarch.com/bughunting)
