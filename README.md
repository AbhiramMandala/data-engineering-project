# Data Engineering Fundamentals - Linux + Git Project

End-to-end mini project covering:
1. Secure data landing zones (Linux permissions)
2. Log analysis (grep, awk, sort, uniq, etc.)
3. REST API ingestion (Python + curl)
4. Docker containers
5. Git branching + Pull Requests

## Project structure
```
.
├── data/landing/{raw,staging,processed}/  # Task 1 + 3 landing zones
├── logs/app.log                            # Task 2 sample logs
├── scripts/
│   ├── generate_logs.py                    # create sample logs
│   ├── fetch_api.py                        # Task 3 REST ingestion
│   └── log_analysis.sh                     # Task 2 Linux analysis
├── Dockerfile                              # Task 4
├── docker-compose.yml                      # Task 4 (python + postgres)
├── requirements.txt
└── .gitignore
```

## Quickstart (Windows + Docker Desktop + Git Bash / PowerShell)

See full steps below. Start with Task 1.
