import datetime

import requests
import polars as pl

from fmodules.dict_wrapper import AttrDict

# Set the start and end date for the period you want to analyze
start_date = "2023-01-12"
end_date = "2023-01-19"

# Set the repository owner and name
owner = "pola-rs"
repo = "polars"

# Send a GET request to the GitHub API and store the response
response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&per_page=30")

# Store the pull requests in a list
pull_requests = response.json()

print(type(pull_requests))
#print(len(pull_requests))

print(type(pull_requests[0]))
#print(f"{pull_requests[0]=}")

pr = AttrDict(pull_requests[0])
print(type(pr.labels))
print(pr.labels)

#df = pl.DataFrame({"tags", pull_requests[0]}).with_row_count("id", 1)
#df = pl.read_json(pull_requests[0])
#print(f"{df=}")

# Iterate over the pull requests
for pull_request in pull_requests:
    # Get the date the pull request was created
    created_at = pull_request["created_at"]
    # Convert the date to a datetime object
    created_at = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    #print(pull_request)
    #print("\n\n")
