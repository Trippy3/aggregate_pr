# aggregate_pr
[![codecov](https://codecov.io/gh/Trippy3/aggregate_pr/branch/main/graph/badge.svg?token=OS3J2YRBR2)](https://codecov.io/gh/Trippy3/aggregate_pr)

Aggregate pull requests for a specific repository on GitHub over a period of time.  
Currently, two types of csv are output.


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
                        Start Date. ex: 2023-01-21 deafult: Monday of the week.
  -e END, --end END     End Date. ex: 2023-01-24 default: datetime.now()

(.venv) $ python aggregate_pullreq.py https://github.com/Trippy3/aggregate_pr
Warning: Token file does not exist. path: None
output: {current dir}/aggregate_pr/aggregate_pr_all_20230122_20230128.csv
output: {current dir}/aggregate_pr/aggregate_pr_mean_20230122_20230128.csv
~~~
- If you want to get PR for private repositories, please pass a token file.
~~~bash
$ cat .token_file
ghp_XXXXXXXXXXXX
~~~
- If start and end dates are not specified, the default settings are used.  
Note: Currently, only Japan Standard Time (JST) is supported.
    - The Monday of that week will be the start date.
    - The present date and time will be the end date. 

## Output
Two types of csv are output.
### 1. Details of each PR
A csv with the following columns is output.
| Column Name | Type | Description |
| :--- | :--- | :--- |
| number | int | PR Number |
| title | str | PR Tilte |
| user | str | PR Author |
| labels | str \| None | PR Labels; Multiple labels are connected by commas. |
| milestone | str \| None | PR Milestone |
| created_at | datetime | Date and time of creation of PR |
| merged_at | datetime | Date and time PR was merged |
| read_time_hr | float | Time from creation to merge of PR |
| additions | int | Additional code lines |
| deletions | int | Deletion code lines |
| difference | int | Code delta of lines |
| changed_files | int | Number of files changed |

#### Example: 
~~~
number,title,user,labels,milestone,created_at,merged_at,read_time_hr,additions,deletions,difference,changed_files
7,update: support private repo,hiro-torii,"enhancement,good first issue",,2023-01-27 10:58:59 UTC,2023-01-27 11:56:26 UTC,0.96,11,7,18,1
6,fix the code according to the linter,Trippy3,,,2023-01-25 14:21:55 UTC,2023-01-25 14:26:36 UTC,0.08,20,10,30,6
4,v.0.0.1,Trippy3,,,2023-01-24 17:40:56 UTC,2023-01-24 17:41:39 UTC,0.01,241,1,242,13
~~~

### 2. Total and average of each PR
A csv with the following columns is output.
| Column Name | Type | Description |
| :--- | :--- | :--- |
| total_count | int | Total number of each PR |
| read_time_hr | float | The average time from creation to merge for each PR |
| additions | float | Average number of additional code lines for each PR |
| deletions | float | Average number of delete code lines for each PR |
| difference | float | Average number of change code lines for each PR |
| changed_files | float | Average number of files changed for each PR |

#### Example: 
~~~
total_count,read_time_hr,additions,deletions,difference,changed_files
3,0.35000000000000003,90.66666666666667,6.0,96.66666666666667,6.666666666666667
~~~

-----
## Stats
![Alt](https://repobeats.axiom.co/api/embed/c2280b8673dbde0c57706cfbd19fa97aa6b0c079.svg "Repobeats analytics image")
