# E-Commerce Customer Behavior Analyzer

A Django-based analytics project that studies e-commerce transaction data to understand sales performance, customer buying behavior, and customer segmentation using Pandas, NumPy, Matplotlib, and Seaborn.

## Features

- Sales analysis across categories, regions, and states
- Customer spending and purchase-pattern insights
- RFM segmentation for customer behavior analysis
- Filtered dashboard using state, category, and segment options
- Clean beginner-friendly dashboard with KPI cards and static charts
- Django admin support for records and segment data

## Tech Stack

- Backend: Django
- Database: SQLite
- Data processing: Pandas, NumPy
- Visualization: Matplotlib, Seaborn
- Frontend: HTML, CSS, Bootstrap, Tailwind CSS

## Project Workflow

1. Raw e-commerce data is loaded from the CSV file.
2. Django imports the data into the SQLite database.
3. Pandas and NumPy clean and analyze the sales data.
4. RFM values are calculated for each customer.
5. Matplotlib and Seaborn generate charts.
6. The Django template displays the dashboard and KPI cards.

## RFM Segmentation

RFM stands for Recency, Frequency, and Monetary value.

- Recency: how recently the customer purchased
- Frequency: how often the customer shops
- Monetary: how much the customer spends

The project classifies customers into segments such as Champion, Loyal, At Risk, Need Attention, and Lost.

## Visualizations

- Sales by category
- State-wise sales heatmap
- Monthly sales trend
- Discount vs profit scatter plot
- Regional sales comparison
- Customer spending distribution
- Customer segment distribution
- RFM heatmap

## Project Structure

```bash
analytics/
├── analysis/
│   └── matplotlib_charts.py
├── management/
│   └── commands/
│       ├── import_data.py
│       └── compute_rfm.py
├── migrations/
├── templates/
│   └── analytics/
│       └── dashboard.html
├── models.py
├── views.py
├── urls.py
├── admin.py
├── apps.py
├── tests.py
├── data/
│   └── ecommerce.csv
dashboard_config/
├── settings.py
├── urls.py
README.md
requirements.txt
manage.py
db.sqlite3
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py import_data
python manage.py compute_rfm
```

## How to Run

```bash
python manage.py runserver
```

Open http://localhost:8000 in the browser.

## Django Admin

Create an admin user:

```bash
python manage.py createsuperuser
```

Then open http://localhost:8000/admin/ to manage the database records.

## Future Enhancements

- Add more date-based filters
- Add category and state trend comparisons
- Improve dashboard styling for presentations
- Add downloadable CSV or PDF reports

## License

This project is for learning and interview preparation and can be adapted for personal projects or academic use.
