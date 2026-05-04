# pr-review-demo-app

A small Flask + SQLite notes application used as a fixture for the live demos in the *Claude Skills for Security* talk at DC435 (2026-06-05).

It exists only as demo infrastructure. Three branches off `main` introduce three different pull requests. The talk runs Trail of Bits' `differential-review` skill against each one and reads the output on stage.

## What's in here

```
pr-review-demo-app/
├── app.py                       Flask app: login, dashboard, notes
├── seed.py                      Seeds SQLite with two users and notes
├── requirements.txt             Flask
├── templates/                   Login, dashboard, helper templates
├── .github/workflows/
│   ├── safe.yml                 GitHub Actions workflow done correctly
│   └── vulnerable.yml           Workflow with the pull_request_target trap
├── demo-assets/
│   ├── sample.har               Pre-captured HAR file for Demo 4
│   └── PROMPTS.md               Every prompt to copy/paste during the talk
└── README.md
```

## Branches

| Branch | What it adds | Skill should flag |
|---|---|---|
| `main` | Login, logout, dashboard | (baseline, no PR) |
| `feat/note-detail` | `/notes/<id>` view | **IDOR** (no ownership check) |
| `feat/search` | `/search?q=...` | **SQL injection** (f-string into LIKE) |
| `feat/create-note` | `/notes/new` (POST) | Nothing. Done correctly. |

Each branch is one commit on top of `main` and one open PR.

## GitHub Actions

The two workflow files in `.github/workflows/` are **static fixtures for Demo 3**, not real CI. GitHub Actions is disabled at the repo level so neither workflow ever runs. The auditor in Demo 3 reads them as files.

## Running locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python seed.py        # creates app.db
python app.py         # http://127.0.0.1:5000
```

Two seeded users:

| Username | Password |
|---|---|
| `alice` | `alicepass` |
| `bob` | `bobpass` |

(These are demo credentials in a deliberately insecure app. Do not reuse this code.)

## License

MIT.
