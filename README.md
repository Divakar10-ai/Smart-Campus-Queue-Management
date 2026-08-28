# Smart Campus Queue Management System

A Streamlit-based digital queue management system designed to reduce waiting time at campus service counters such as fees, library, stationery, and administrative offices.

## Features

- Student portal for joining and tracking queues
- Digital token generation
- Queue position and estimated waiting time
- Admin dashboard for managing active queues
- Digital display for current and upcoming tokens
- Analytics and reporting
- Data export utilities
- SQLite database for local persistence
- Modular Python project structure

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly / chart utilities
- QR generation utilities

## Project Structure

```text
Smart-Campus-Queue-Management/
├── app.py
├── auth.py
├── database.py
├── config.py
├── components/
├── modules/
├── utils/
├── requirements.txt
├── .gitignore
└── README.md
```

## Run Locally

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.env\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
```

## Security Note

Local database files and credentials should not be committed to a public repository. This repository is configured to ignore SQLite database files and environment files.

For a production deployment, configure authentication credentials through environment variables or a secure secrets manager.

## Author

**Divakar**

Built as a Smart Campus / Data Analytics project.
