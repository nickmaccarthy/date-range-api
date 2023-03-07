# API to determine if two date ranges overlap

A small service, powered by [Flask](https://flask.palletsprojects.com/en/2.2.x/) that will determine if two date ranges overlap or not with a JSON response as its data return.

Dates will be parsed and convereted to datetime via my [python-datemath](https://github.com/nickmaccarthy/python-datemath) module

This project is meant to run in docker, and or docker compose for its demo.

## Requirements
- [Python 3.9+](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Make](https://www.gnu.org/software/make/manual/make.html)
- [Curl](https://curl.se/)

## Usage
This can be run locally, you will need to have the above requirements installed on your machine.  Once those are installed its as simple as running.  Please note this runs docker compose to test the API as well

```shell

$ make run

```

If you would rather build just the docker image, you can run `make build`

If we wanted to push this image a registry, we could do that with `make push-image`, **NOTE** We are not actually doing any pushes here, but only to demonstrate how we might accomplish that in say a CI/CD pipeline.

## API Request requiremenets

- This API only accepts `GET` method requests, any other methods such as `POST` will result in a [405](https://http.cat/405) HTTP response code
- The API only has one endpoint and responds to the index, i.e. `/` currently
- Date ranges are seperated by `,` in the URL, with the `range1` and `range2` arguments respectively
    - Example: `http://localhost:5001/?range1=<start>,<end>&range2=<start>,<end>`
- You can specify a multitude of date formats and this API should still work as defined by the [python-datemath](https://github.com/nickmaccarthy/python-datemath) module
    - examples:
        - using actual datemath - `?range1=now-1h,now&range2=now-30m,now` 
        - using date formats `?range1=2023-01-01,2023-01-5&range2=2021-01-01,2023-01-03`, 
        - even with minutes (ISO8601) - `/?range1=2023-01-01T00:00:00,2023-01-01T00:01:00&range2=2023-01-01T00:00:00,2023-01-01T00:00:30`
        - or just the years - `?range1=2021,2023&range2=2021,2022`
- If a dateformt provided by the user is not able to be parsed, or has an issue, we will recieve a [400](https://http.cat/400) HTTP response, with the error

## Automated Tests
Unittests are done using the [VCR.py]() and can be found in the `api_tests.py` file in this repo

The API can be tested with docker compose easily with `make run`.  This will actually use two different services, one service will run our flask API (called `api`), and the other one will test the API with our `api_tests.py` (called `tests`).  You will see the `service-api-tests` return OK if the tests pass, when you run a `make run`.

## Using the API
When you have ran `make run` the API should be avilable on your local machine and able to interacted with `CURL` quite easily

examples:
```shell
$ curl -XGET "http://127.0.0.1:5001/?range1=2021,2023&range2=2021,2022"
$ curl -XGET "http://127.0.0.1:5001/?range1=now-1h,now&range2=2021,2022"
$ curl -XGET "http://127.0.0.1:5001/?range1=2023-01-01T00:00:00,2023-01-01T00:01:00&range2=2023-01-01T00:00:00,2023-01-01T00:00:30"
```


## Files
- `app.py` - The main file that actually runs our API.  We are using the Flask frame work.  Note the `date_range_overlap()` function, that is actually determining if two ranges overlaps based on start and end times of each respective range
- `api_tests.py` - This file is meant to test the API to ensure it returns what we want.  Its meant to run in the unittest framework, and is using VCR.py to help run the API tests
- `docker-compose.yaml` - This file defines the two services we need to properly run and test this app.  It will first start up the `api` service (aka our flask app), then run the `tests` service, which runs the `api_tests.py` agaist the live running API
- `Dockerfile` - The dockerfile which determines our our Flask app/service is built
- `requirements.txt` - A file that determines which python modules we need to power our API. 
- `Makefile` - useful file to help run complex commands in a shorthand format, i.e. `make build`, `make run`, etc
