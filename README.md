# API to determine if two date ranges overlap

A small service, powered by [Flask](https://flask.palletsprojects.com/en/2.2.x/) that will determine if two date ranges overlap or not with a JSON response as its data return.

## Requirements
- Python 3.10
- Docker
- Make

## Usage
This can be run locally, you will need to have the above requirements installed on your machine.  Once those are installed its as simple as running

```shell

$ make build run

```

## API Request requiremenets

- This API only accepts `GET` method requests, any other methods such as `POST` will result in a `405` HTTP response code
- The API only has one endpoint and responds to the index, i.e. `/` currently
- Date ranges are seperated by `,` in the URL, with the `range1` and `range2` arguments respectively
    - Example: `http://localhost:5001/?range1=<start>,<end>&range2=<start>,<end>`
- You can specify a multitude of dateformats and this API should still work as defined by the [python-datemath](https://github.com/nickmaccarthy/python-datemath) module
    - examples:
        - using actual datemath - `?range1=now-1h,now&range2=now-30m,now` 
        - using date formats `?range1=2023-01-01,2023-01-5&range2=2021-01-01,2023-01-03`, 
        - even with minutes (ISO8601) - `/?range1=2023-01-01T00:00:00,2023-01-01T00:01:00&range2=2023-01-01T00:00:00,2023-01-01T00:00:30`
        - or just the years - `?range1=2021,2023&range2=2021,2022`
- If an dateformat is not able to be parsed, or has an issue, will recieve a `400` HTTP response, with the error

## Testing
Unittests are done using the [VCR.py]() and can be found in the `tests.py` file in this repo

When the API service is running, you can run them with the 