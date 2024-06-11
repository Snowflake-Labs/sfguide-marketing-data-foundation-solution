# Contribution Guidelines

## How to contribute

1. Change directory to the solution/homepage directory
1. Create a python venv and activate it
   `python3 -m venv venv && source venv/bin/activate`
1. Add the DataOps.live pip repo by following the setup instructions
   1. [Create a personal access token](https://docs.dataops.live/docs/administration/dataops-cli/#step-1---create-a-personal-access-token)
   1. Add the repo:
      `pip config set global.index-url https://$DATAOPS_USERNAME:$DATAOPS_PAT@app.dataops.live/api/v4/projects/5844/packages/pypi/simple`
1. Install the dependencies `pip install -r requirements.txt`
1. Edit and source project environment variables `source .env`
1. Run the mkdocs server `mkdocs serve`
1. Open your browser at `http://127.0.0.1:8000/` and start editing the files
1. Commit your changes and open a MR
