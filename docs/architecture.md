# Architecture

## Overview

This project is a Django dashboard for e-commerce customer behavior analysis. The backend loads transaction data from SQLite, cleans it with Pandas and NumPy, calculates customer RFM values, and renders static charts with Matplotlib and Seaborn.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django (Python) |
| Database | SQLite via Django ORM |
| Data processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Frontend | HTML, CSS, Bootstrap, Tailwind |
| Template | Django template engine |

## Data Flow

1. CSV data is imported with the `import_data` management command.
2. The data is stored in SQLite using the Django models.
3. The dashboard view loads the records and filters them by state, category, or segment.
4. Pandas computes totals, averages, and RFM metrics.
5. Matplotlib and Seaborn generate chart images.
6. The HTML template displays the charts and KPI cards.

## Request Lifecycle

### Full Page Load (`GET /`)

1. A browser requests `/`.
2. Django routes the request to the dashboard view in `analytics/views.py`.
3. The view reads data from `Order`, `Customer`, and `RfmSegment` models.
4. Pandas converts the database rows into a DataFrame.
5. Each chart function creates a Matplotlib figure and returns an HTML image string.
6. The template renders all the chart images in the page.

### Filtered Dashboard

1. The user chooses a value from the filter form.
2. The page sends the selected values through query parameters.
3. The Django view filters the ORM query and the DataFrame.
4. Updated KPI cards and charts are rendered in the same page.

## Database Models

The project keeps the existing `Customer`, `Order`, and `RfmSegment` models. These are useful because they represent customers, transactions, and RFM segment values.

## URL Routing

| URL | View | Purpose |
|-----|------|---------|
| `/` | `dashboard` | Main dashboard |
| `/admin/` | Django admin | Manage data |

## Static Files

The dashboard uses generated PNG charts instead of a JavaScript chart library. The chart images are embedded directly into the HTML using base64 data URIs.

## Frontend Behavior

The template contains:

1. KPI cards for total sales, total orders, customers, and order value
2. Filter dropdowns for state, category, and customer segment
3. HTML cards that contain the chart images
4. Bootstrap and Tailwind classes for a clean layout

This keeps the project simple and interview-friendly.
