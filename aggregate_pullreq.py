import argparse
from pathlib import Path
import sys

import polars as pl

from modules.repository import Repository
from modules.pullreq import get_pullreq_data


me = Path(__file__).resolve()


def main():
    parser = argparse.ArgumentParser(description="Retrieve the 100 latest merged PRs from the specified repository.")
    parser.add_argument("addr", help="GitHub Repository URL", type=str)
    parser.add_argument(
        "-t", "--token-file", help="GitHub Token file path. default: ./.token", type=Path, default=me.parent / ".token"
    )
    parser.add_argument(
        "-i",
        "--init",
        help="Get all merged PRs; specify if you want to retrieve more than 100 merged PRs.",
        action="store_true",
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        help="Specifies the directory to which the data will be output. default: ./data",
        type=Path,
        default=me.parent / "data",
    )
    args = parser.parse_args()

    if args.out_dir.is_file():
        print(f"Specify a dir path, not a file path. your-input: {args.out_dir}", file=sys.stderr)
        sys.exit(1)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    repo = Repository(args.addr, args.token_file)
    all_pr: pl.LazyFrame = get_pullreq_data(repo, args.init)
    all_pr.sink_parquet(args.out_dir / "pr.parquet")
    all_pr.collect().write_csv(args.out_dir / "pr.csv")
    print(f"Data file output to {args.out_dir}.")
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
    mean_pr.collect().glimpse()


if __name__ == "__main__":
    main()
