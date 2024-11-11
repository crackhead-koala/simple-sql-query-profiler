import os
import dotenv
import argparse
import time
import statistics

import tqdm
import clickhouse_driver as cd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
            'A simple query performance tester for ClickHouse. Note that a new '
            'connection is established on every iteration, but only the query '
            'execution time is measured, not accounting for the time it takes to create '
            'a database connection.'
    )

    parser.add_argument('query', help='path to the file containing a single SQL query to measure')
    parser.add_argument(
        '-t', '--times',
        type=int,
        default=10,
        help='how many times the query should be executed; the default is 10'
    )
    parser.add_argument('-H', '--host', help='ClickHouse database host to send queries to')
    parser.add_argument('-p', '--port', type=int, help='port to use with the host')
    parser.add_argument('-u', '--username', help='user to use for the database connection')
    parser.add_argument('-P', '--password', help='password for the specified user')
    parser.add_argument('-d', '--database', help='default database')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='if set, displays a progress bar for the queries'
    )
    parser.add_argument(
        '-e', '--use_env',
        action='store_true',
        help=
            'specify whether the program should load database credentials from an .env file '
            '(it must contain the following variables: HOST, PORT, USERNAME, PASSWORD, DATABASE); note '
            'that command-line arguments are prioritized over the values provided in the .env file'
    )

    args = parser.parse_args()

    with open(args.query, 'r') as q:
        query = q.read()

    if args.use_env:
        dotenv.load_dotenv()

    query_execution_times = []
    _range = tqdm.trange(args.times, ncols=100) \
        if args.verbose \
        else range(args.times)
    for _ in _range:
        client = cd.Client(
            host=args.host or os.getenv('HOST'),
            port=args.port or int(os.getenv('PORT')),
            database=args.database or os.getenv('DATABASE'),
            user=args.username or os.getenv('USERNAME'),
            password=args.password or os.getenv('PASSWORD'),
            secure=False,
            verify=False
        )

        with client:
            start = time.perf_counter()
            _ = client.execute(query)
            end = time.perf_counter()
            query_execution_times.append(end - start)

    time_avg = statistics.mean(query_execution_times)
    time_std = statistics.stdev(query_execution_times)

    print(
        f'Average execution time of {args.times} iterations: '
        f'{time_avg:.2f}s. ± {time_std:.2f}s. (avg ± std)'
    )
