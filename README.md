# README #

### What is this repository for? ###

Prototype for the RainbowFS project.

### Version

In development


### Requirements

- Yarn 

https://classic.yarnpkg.com/en/docs/install/


### Test the currently working features ###
#### Download 

```sh
git clone --recurse-submodules -b s3 https://github.com/Saalik/prototype-CDC.git
```


#### Tests

The repository contains some already working tests. You can launch them from the `src/tests` subdirectory.

```sh
cd src/tests/
./testMain.py
./testRecord.py
./testJournal.py
```

### Before starting to code

We need something to play the role of an [Amazon S3](
https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) endpoint.
[Zenko](https://www.zenko.io/) will play that role.  

The following commands will launch a new Zenko instance.

```sh
cd src/checkpointStore/cloudserver
yarn install --frozen-lockfile
# Start a Zenko CloudServer 
yarn start
```

### Resource

[Zenko CloudServer sources](https://github.com/scality/cloudserver)
[Amazon S3 Python SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)


### For the hackathon

- First task :  Create a script to populate the journal 
- Second task : Write a test to ensure that the S3 interface is working. Create a bucket, write some values
- Third task : Create a checkpoint.py script that
    - Retrieves information from the journal
    - Write them to Zenko CloudServer 
    - Retrieve the object from CloudServer
