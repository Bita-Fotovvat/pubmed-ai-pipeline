param(
  [Parameter(Mandatory=$true)][string]$Query
)

docker compose up -d
python src/run_dashboard.py --query $Query --overwrite

# example query in powershell: .\run.ps1 -Query "(gut microbiota AND anxiety) AND (2015[dp] : 3000[dp])"
