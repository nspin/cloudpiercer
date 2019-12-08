# Cloudpiercer

Cloudflare 503 challenge bypass.

This tool is composed of a challenge solver (Node.js + `jsdom`) and a Python driver for `aiohttp`.

Depends on Node.js and Python 3 with `aiohttp`.

# Example

In one shell, start the solver:
```
$ cd solver
$ npm install
$ npm start

> cloudpiercer-solver@0.1.0 start [redacted]
> node server.js

Listening on localhost:8081
```
In another shell, fetch a URL through Cloudflare:
```
$ python3 demo.py [url]
```
