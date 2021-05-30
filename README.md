# feedi-io
## Running locally
* Use pipenv to create a virtaulenv with all required dependencies installed.
* Have a Postgres database at hand
* Set the env vars in ```src/config.py``` to configure your environment
* execute ```flask db upgrade``` in virtualenv to apple database migrations
* execute feedi.io with ```flask run```

## Docker
* To built the docker image, first export the dependencies into a pinpointed 
```requirements.txt``` file with ```pipenv lock --keep-outdated --requirements > requirements.txt```.
Then start a docker build.
* For running, don't forget to set the env vars from ```src/config.py```
* A volume mount should be created for persistent storage of pictures