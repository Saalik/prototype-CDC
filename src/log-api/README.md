# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
Simple Log API for RainbowFS

* Version
0.1

### API ###
**GET /api/log/:id** return the log corresponding to **id**, 404 if not found

**GET /api/log/:id_from/:id_to** return a chunked stream of logs from **id_from** to **id_to**

**GET /api/log/high** return the high watermark log id

**GET /api/log/low** return the low watermark log id

**POST /api/log** append a new log, return a log id

**PUT /api/log** flush logs from high watermark to the latest id

**PUT /api/log/:id** flush logs from high watermark to **id**

**DELETE /api/log** truncate logs from low watermark to high watermark

**DELETE /api/log/:id** truncate logs from low watermark to **id**

### Build ###

``` sh
docker build . -t rainbowfs-log-api
```

### Run ###
``` sh
docker run --rm rainbowfs-log-api
```
