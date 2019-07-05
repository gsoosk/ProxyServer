# ProxyServer
In computer networks, a proxy server is an application that acts as an intermediary for requests from clients seeking resources from other servers. A client connects to the proxy server, requesting some service, such as a file, connection, web page, or other resource available from a different server and the proxy server evaluates the request as a way to simplify and control its complexity. Proxies were invented to add structure and encapsulation to distributed systems.
![s](https://upload.wikimedia.org/wikipedia/commons/b/bb/Proxy_concept_en.svg)

This is an implementation of a Http `proxy server` application with some fantasy features in `python`.

## Features : 
* **Logging** 
    * Logs everything happens to a file.
```json
"logging": {
    "enable": <true/false>,
    "logFile": "<logFileName>"
} 
```
* **Restriction**
    * If it is enable, it can restrict clients to visit some restricted websites.
    * Also it can notify admin with email in smtp protocol. ( Actually email address and password are hardcoded in code and can be changed)
```json
"restriction": {
    "enable": <true/false>,
    "targets": [
      {
        "URL": "<webSite1Url>",
        "notify": "<true/false>"
      },
      ...
    ]
  }
```
* **HttpInjection**
    * It can show a message in a navbar header for index page of websites.
```json
"HTTPInjection": {
    "enable": <true/false>,
    "post": {
      "body": "<injectionText>"
    }
  }
```
* **Accounting** 
    * If it is enable, it can set a maximum byte usage for every user.
```json
"accounting":{
    "users":[
        {
            "IP": "<userIp>",
            "volume":"<maximumVolume>"
        },
        ...
    ]
}
```

* **Privacy**
  *  With adding a specific user agent you can increase your privacy. 
```json
 "privacy": {
    "enable": <true/false>,
    "userAgent": "<privacyText>"
  }
```
* **Caching**
  * With enabling this feature proxy can cache some repeated resources and send back again their to client. 
  * It uses Http cache system.
```json
"caching": {
    "enable": <true/false>,
    "size": <cacheSizeInResourceNum>
}
```

## How to Run :
First of all you should set config file with above features and `proxy port.

Then you can run proxy server with `python`. It's not uses any specific library and dependecies. 
```
python proxyServer.py
```