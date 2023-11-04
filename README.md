# Amazing Grace Challenge
Tools for counting recordings of Amazing Grace for the [Amazing Grace Challenge](https://amazinggracechallenge.com/).

As part of the record attempt, we need to catalog the recordings made with the `#amazinggracechallenge` hashtag
on various platforms. This repository holds the tools used to make this happen.

## Overview of software

* Load all capture session records
* Load all recording records
* Create a new capture session
* Determine the latest capture ToDate
* Start capturing, repeat until number of calls achieved OR no more records exist
	* Call API
	* Parse data into DTOs
	* Convert DTOs into recording records
	* If not already stored,
		* Save to recording record
	* If stored but different
		* Log & update the recording record
	* Update capture session information
* Save data about the capture session
* Save data about the recording records

### Imports

```powershell
python -m pip install requests
```

## YouTube

### Get an API key

Start by getting an API key

Store it in the environment
```powershell
PS C:\Code\amazinggracechallenge> $env:YOUTUBE_API_KEY='INSERT YOUR KEY HERE'
```

If using PyCharm, [create a Run Configuration](https://stackoverflow.com/a/42708480/399704) with the environment variable set.

