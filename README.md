# aggregate_pr
Aggregate pull requests for a specific repository on GitHub over a period of time

## Usage
~~~bash
$ make .venv
$ source .venv/bin/activate
(.venv) $ python aggregate_pullreq.py -h
usage: aggregate_pullreq.py [-h] [-t TOKEN_FILE] [-s START] [-e END] addr

positional arguments:
  addr                  GitHub Repository URL

options:
  -h, --help            show this help message and exit
  -t TOKEN_FILE, --token-file TOKEN_FILE
                        GitHub Token file path
  -s START, --start START
                        Start Date. ex. 2023-01-21
  -e END, --end END     End Date. ex. 2023-01-24
(.venv) $ python aggregate_pullreq.py https://github.com/Trippy3/aggregate_pr
~~~

-----

![Alt](https://repobeats.axiom.co/api/embed/c2280b8673dbde0c57706cfbd19fa97aa6b0c079.svg "Repobeats analytics image")
