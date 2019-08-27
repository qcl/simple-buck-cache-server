# Simple Buck Cache Server
A simple demo of buck cache server

This is a simple script to run a Buck cache server which trying to confirm [binary HTTP protocol](https://buck.build/concept/http_cache_api.html#binary_http) of Buck's [HTTP Cache API](https://buck.build/concept/http_cache_api.html).

This simple python script referred [Uber's Buck cache server](https://github.com/uber/buck-http-cache) code to understand how exactly to parse `GET` and `PUT` requests. 

I don't want to handle those Java things so I decided just to write a simple python script to run a simple server for demo.

## Requirement
* Python3

## Start Simple-Buck-Cache-Server
```
$ python3 ./simple-buck-cache-server.py <port-number> <cache-dir>
```

For example:

```
$ python3 ./simple-buck-cache-server.py 9527 ./buck-cache
```

Then this script will listen to port `9527`  and read, write data to dir `buck-cache`. If cache dir doesn't exist, this script create it for you.

## Setup `.buckconfig`

If you want to use buck cache server, simply add it to your `.buckconfig`:

```
[cache]
  mode = http
  http_url = http://simple.buck.cache.server:9527
  cache_mode = readwrite
```

## Buck Cache Binary HTTP Protocol

This script simply implemented handlers for 2 requests below:

### GET `/artifacts/key/{key}`

Try to find `{key}.buckcache` in `<cache-dir>`, if found, just return the file with HTTP code `200`, otherwise return `404`.

### PUT `/artifacts/key`

The struct of request is: 

1. First 4 bytes (signed integer) indicate how many keys in the request. 
2. Following are keys, for each key, first 2 bytes (unsigned integer) indicates how long the key is, then bytes followed are key.
3. Data need to be cached, first part is metadata, second part is data.

Because this is just a demo, here just simply store data to `{key}.buckcache` to `<cache-dir>`. 