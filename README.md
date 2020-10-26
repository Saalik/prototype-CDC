# README #

### What is this repository for? ###

Prototype for the RainbowFS project.

### Version

In development


### Requirements

- Yarn 

https://classic.yarnpkg.com/en/docs/install/


### Test the current working features ###
#### Download 

```sh
git clone --recurse-submodules -b s3 https://github.com/Saalik/prototype-CDC.git
```


#### Tests

```sh
cd src/tests/
./testMain.py
./testRecord.py
./testCheckpoint.py
```

### Before starting to code


```sh
cd src/checkpointStore
yarn install --frozen-lockfile
# Start a Zenko CloudServer 
yarn start
```

### Ressource

https://github.com/scality/cloudserver
https://boto3.amazonaws.com/v1/documentation/api/latest/index.html


