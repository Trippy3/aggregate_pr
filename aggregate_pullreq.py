import argparse
from pathlib import Path

import polars as pl

from modules.repository import Repository
from modules.date_range import DateRange
from modules.pullreq import get_pullreq_data

me = Path(__file__).resolve()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("addr", help="GitHub Repository URL", type=str)
    parser.add_argument("-t", "--token-file", help="GitHub Token file path", type=Path, default=None)
    parser.add_argument(
        "-s", "--start", help="Start Date. ex: 2023-01-21  deafult: Monday of the week.", type=str, default=None
    )
    parser.add_argument("-e", "--end", help="End Date. ex: 2023-01-24 default: datetime.now()", type=str, default=None)
    args = parser.parse_args()

    repo = Repository(args.addr, args.token_file)
    date_range = DateRange(args.start, args.end)
    all_pr: pl.LazyFrame = get_pullreq_data(repo, date_range)
    all_pr_csv: Path = (
        me.parent / f"{repo.name}_all_{date_range.start.strftime('%Y%m%d')}_{date_range.end.strftime('%Y%m%d')}.csv"
    )
    all_pr.collect().write_csv(all_pr_csv)
    print(f"output: {all_pr_csv}")
    mean_pr = all_pr.select(
        [
            pl.col("number").count().alias("total_count"),
            pl.col("read_time_hr").mean(),
            pl.col("additions").mean(),
            pl.col("deletions").mean(),
            pl.col("difference").mean(),
            pl.col("changed_files").mean(),
        ]
    )
    mean_pr_csv: Path = (
        me.parent / f"{repo.name}_mean_{date_range.start.strftime('%Y%m%d')}_{date_range.end.strftime('%Y%m%d')}.csv"
    )
    mean_pr.collect().write_csv(mean_pr_csv)
    print(f"output: {mean_pr_csv}")


if __name__ == "__main__":
    main()
