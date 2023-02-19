# aggregate_pr
[![codecov](https://codecov.io/gh/Trippy3/aggregate_pr/branch/main/graph/badge.svg?token=OS3J2YRBR2)](https://codecov.io/gh/Trippy3/aggregate_pr)
[![Actions status](https://github.com/Trippy3/aggregate_pr/actions/workflows/ci.yml/badge.svg)](https://github.com/Trippy3/aggregate_pr/actions)

Get the merged PR of the specified GitHub repository.  
Currently, output .parquet and .csv.

### Note:
- Works with Python 3.10 or later.
- To access a given repository, please obtain an access token in advance.
Please refer to [the official GitHub documentation](https://docs.github.com/en/graphql/guides/forming-calls-with-graphql#authenticating-with-graphql).

## Usage
~~~bash
$ make .venv
$ source .venv/bin/activate

(.venv) $ python aggregate_pullreq.py -h
usage: aggregate_pullreq.py [-h] [-t TOKEN_FILE] [-i] [-o OUT_DIR] addr

Retrieve the 100 latest merged PRs from the specified repository.

positional arguments:
  addr                  GitHub Repository URL

options:
  -h, --help            show this help message and exit
  -t TOKEN_FILE, --token-file TOKEN_FILE
                        GitHub Token file path. default: ./.token
  -i, --init            Get all merged PRs; specify if you want to retrieve more than 100 merged PRs.
  -o OUT_DIR, --out-dir OUT_DIR
                        Specifies the directory to which the data will be output. default: ./data


(.venv) $ python aggregate_pullreq.py https://github.com/Trippy3/aggregate_pr
Data file output to /home/gretra/seventh_gene/seventh_src/aggregate_pr/data
The total number of merged PRs obtained and average value are shown below.
Rows: 1
Columns: 6
$ total_count   <u32> 5
$ read_time_hr  <f64> 0.214
$ additions     <f64> 97.8
$ deletions     <f64> 9.8
$ difference    <f64> 107.6
$ changed_files <f64> 6.8

(.venv) $ ls ./data/pr*
./data/pr.csv  ./data/pr.parquet
~~~
- If you want to get PR for repositories, please pass a token file.
~~~bash
$ cat .token
ghp_XXXXXXXXXXXX
~~~
- If you want to get more than 100 PRs in the past, please specify the "--init" option.  
Note: Depending on the number of PRs, it may take some time to retrieve them.
~~~bash
(.venv) $ python aggregate_pullreq.py https://github.com/Trippy3/aggregate_pr --init
~~~

## Output
### Data Column
A csv and parquet with the following columns is output.
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
| url | str | PR URL |

#### Example: 
~~~
+----------+--------------------------------------+------------+------------------------------+-------------+---------------------------+---------------------------+----------------+-------------+-------------+--------------+-----------------+------------------------------------------------+
|   number | title                                | user       | labels                       |   milestone | created_at                | merged_at                 |   read_time_hr |   additions |   deletions |   difference |   changed_files | url                                            |
|----------+--------------------------------------+------------+------------------------------+-------------+---------------------------+---------------------------+----------------+-------------+-------------+--------------+-----------------+------------------------------------------------|
|        1 | Feature/first version                | Trippy3    |                              |         nan | 2023-01-20 05:21:11+00:00 | 2023-01-20 05:22:13+00:00 |           0.02 |          20 |           0 |           20 |               3 | https://github.com/Trippy3/aggregate_pr/pull/1 |
|        4 | v.0.0.1                              | Trippy3    |                              |         nan | 2023-01-24 17:40:56+00:00 | 2023-01-24 17:41:39+00:00 |           0.01 |         241 |           1 |          242 |              13 | https://github.com/Trippy3/aggregate_pr/pull/4 |
|        6 | fix the code according to the linter | Trippy3    |                              |         nan | 2023-01-25 14:21:55+00:00 | 2023-01-25 14:26:36+00:00 |           0.08 |          20 |          10 |           30 |               6 | https://github.com/Trippy3/aggregate_pr/pull/6 |
|        7 | update: support private repo         | hiro-torii | enhancement,good first issue |         nan | 2023-01-27 10:58:59+00:00 | 2023-01-27 11:56:26+00:00 |           0.96 |          11 |           7 |           18 |               1 | https://github.com/Trippy3/aggregate_pr/pull/7 |
|        9 | WIP: Feature/#2/tests                | Trippy3    | documentation,enhancement    |         nan | 2023-01-28 18:03:15+00:00 | 2023-01-28 18:03:28+00:00 |           0    |         197 |          31 |          228 |              11 | https://github.com/Trippy3/aggregate_pr/pull/9 |
+----------+--------------------------------------+------------+------------------------------+-------------+---------------------------+---------------------------+----------------+-------------+-------------+--------------+-----------------+------------------------------------------------+

~~~

-----
## Stats
![Alt](https://repobeats.axiom.co/api/embed/c2280b8673dbde0c57706cfbd19fa97aa6b0c079.svg "Repobeats analytics image")
-----
[![CodeScene general](https://codescene.io/images/analyzed-by-codescene-badge.svg)](https://codescene.io/projects/34295)
