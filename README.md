# Vitalon

A console-based personal health tracker with secure accounts, vital-sign logging,
basic screening alerts, a latest-reading dashboard, and history with text trends.

## Run

```powershell
python main.py
```

Vitalon stores local data in `users.csv` and `records.csv`. Its alert thresholds
are for basic screening only and do not replace medical advice.

## Project structure

```
vitalon/
  app.py             # application flow
  models.py          # shared data models
  data/              # CSV repositories
  services/          # authentication and vital assessment
  ui/                # console menus and reports
tests/               # automated tests
```

## Tests

```powershell
python -m unittest discover -s tests -v
```
