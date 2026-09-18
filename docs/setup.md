# Setup Guide

## Prerequisites

- Python 3.11+
- pip
- Git (optional)

## Installation

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install the project dependencies

```bash
pip install -r requirements.txt
```

### 3. Run database migrations

```bash
python manage.py migrate
```

### 4. Import the dataset

```bash
python manage.py import_data
```

### 5. Compute RFM segments

```bash
python manage.py compute_rfm
```

### 6. Start the server

```bash
python manage.py runserver
```

Open http://localhost:8000 in your browser.

## Project Structure

```bash
analytics/
├── analysis/
│   └── matplotlib_charts.py
├── data/
│   └── ecommerce.csv
├── management/
│   └── commands/
├── templates/
│   └── analytics/
├── models.py
├── views.py
├── urls.py
├── admin.py
dashboard_config/
├── settings.py
├── urls.py
requirements.txt
manage.py
README.md
```

## Troubleshooting

- If no dashboard data appears, run `python manage.py import_data`.
- If RFM data is missing, run `python manage.py compute_rfm`.
- If the server port is busy, run `python manage.py runserver 8001`.
- If the charts do not render, check the terminal for a Python error and ensure the virtual environment is active.

