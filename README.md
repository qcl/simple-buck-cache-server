# Simple Buck Cache Server
A simple demo of buck cache server

This is a simple script to run a Buck cache server which trying to confirm [binary HTTP protocol](https://buck.build/concept/http_cache_api.html#binary_http) of Buck's [HTTP Cache API](https://buck.build/concept/http_cache_api.html).

This simple python script referred [Uber's Buck cache server](https://github.com/uber/buck-http-cache) code to understand how exactly to parse `GET` and `PUT` requests. 

I don't want to handle those Java things so I decided just to write a simple python script to run a simple server for demo.
