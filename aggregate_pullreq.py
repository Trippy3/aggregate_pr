import argparse
from pathlib import Path
import sys

import polars as pl

from modules.repository import Repository
from modules.database import Database, DBMode
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
    if not args.token_file.exists():
        print(f"Token file does not exist. your-input: {args.token_file}", file=sys.stderr)
        sys.exit(1)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    repo = Repository(args.addr, args.token_file)
    db = Database(args.out_dir / "pr.db", DBMode.OVERWRITE if args.init else DBMode.DELTA)
    all_pr: pl.LazyFrame = get_pullreq_data(repo, args.init)
    db.write_data(all_pr)
    db.to_parquet()
    db.to_csv()
    print(f"Data file output to {args.out_dir}")
    mean_pr = db.to_ldf().select(
        [
            pl.col("number").count().alias("Total count"),
            pl.col("read_time_hr").mean().round(4).alias("Read time[hr]"),
            pl.col("additions").mean().alias("add [line/PR-count]"),
            pl.col("deletions").mean().alias("del [line/PR-count]"),
            pl.col("difference").mean().alias("delta [line/PR-count]"),
            pl.col("changed_files").mean().alias("files[count/PR-count]"),
        ]
    )
    print("The total number of merged PRs obtained and each average values are shown below.")
    with pl.Config() as cfg:
        cfg.set_tbl_cols(7)
        print(mean_pr.collect())


if __name__ == "__main__":
    main()
