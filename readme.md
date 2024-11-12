# Simple SQL Query Profiler
This is a _very_ simple CLI tool that I built for personal use, when I need to compare a few approaches to writing a SQL query. Currently works with ClickHouse only, since it's the DBMS that I interact with the most.

## Usage

First, install dependencies:

```sh
$ pip install -r ./requrements.txt
```

Then you can run it like any other Python module:

```sh
$ python -m chperf --help

usage: chperf.py [-h] [-t TIMES] [-H HOST] [-p PORT] [-u USERNAME]
                 [-P PASSWORD] [-d DATABASE] [-e]
                 queries [queries ...]

A simple query performance tester for ClickHouse. Note that a new
connection is established on every iteration, but only the query
execution time is measured

positional arguments:
  queries               paths to the files, each containing
                        a single SQL query to measure

options:
  -h, --help            show this help message and exit
  -t, --times TIMES     how many times the query should be executed;
                        the default is 10
  -H, --host HOST       ClickHouse database host to send queries to
  -p, --port PORT       port to use with the host
  -u, --username USERNAME
                        user to use for the database connection
  -P, --password PASSWORD
                        password for the specified user
  -d, --database DATABASE
                        default database
  -e, --use_env         specify whether the program should load
                        database credentials from an .env file (it
                        must contain the following variables: HOST,
                        PORT, USERNAME, PASSWORD, DATABASE); note
                        that command-line arguments are prioritized
                        over the values provided in the .env file
```