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
./testJournal.py
```

### Before starting to code


```sh
cd src/checkpointStore/cloudserver
yarn install --frozen-lockfile
# Start a Zenko CloudServer 
yarn start
```

### Resource

https://github.com/scality/cloudserver
https://boto3.amazonaws.com/v1/documentation/api/latest/index.html


### For the hackathon

- First task : Create a Journal population script
- Second task : Write a test to ensure S3 is working. Creation of a bucket, write information.
- Third task : Start writing the checkpoint.py code. Reading information from the journal and writing to CloudServer. Retrieve object from CloudServer
