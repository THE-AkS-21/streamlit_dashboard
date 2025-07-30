# 📊 BSC Streamlit Dashboard

A modern, responsive **Streamlit-based analytics dashboard** for **Bombay Shaving Company** operations. It tracks and visualizes order performance across SKU, category, subcategory, and date ranges from a **PostgreSQL** data source.

---

## 📖 Description

This dashboard delivers high-performance analytics and sleek UI components, tailored for tracking product orders. It includes:

- 📁 Custom collapsible **sidebar**
- 📌 Fixed **navbar** with **toolbar**
- 📊 Filterable **dashboard** with metrics, charts, and exports
- 🧠 **Caching** for faster data load
- 🧼 **UI overrides** for clean, branded visuals

---

## 🎯 Objective

Build an interactive, mobile-friendly analytics dashboard to explore **daily sales trends**, **category-wise performance**, and **SKU-level metrics**.

---

## 🔧 Key Features

- Fully custom layout with top navbar and collapsible sidebar
- Interactive filters (category, subcategory, SKU, date)
- Metrics cards + Plotly and lightweight chart visualizations
- Export raw data to CSV
- Centralized icons, styles, and formatters
- SQLAlchemy database integration (PostgreSQL)
- Modular code and scalable architecture

---

## 🛠️ Tech Stack

- **Python 3.12**
- **Streamlit 1.46.1**
- **Pandas 2.3.1**
- **SQLAlchemy 2.0.41**
- **Plotly 5.18.0**
- **PostgreSQL** (via psycopg2)
- **OAuth**: Google API client + auth libraries

---

## 📁 Project Structure

```
streamlit_dashboard/
├── .streamlit/
├── app/
│   ├── components/         # Navbar, sidebar, layout, charts
│   ├── constants/          # Page constants
│   ├── database/           # PostgreSQL connection + queries
│   ├── pages/              # Dashboard, login, analytics, settings
│   ├── utils/              # Icons, formatters, CSS utilities
│   ├── assets/icons/       # UI icons (home, settings, etc.)
│   └── config.py           # Streamlit UI config
├── tests/                  # Test scripts (TBD)
├── main.py                 # App entrypoint
├── config.py               # Database config
├── requirements.txt
├── .env
```

---

## 📦 Requirements

```text
streamlit==1.46.1
pandas==2.3.1
SQLAlchemy==2.0.41
plotly==5.18.0
python-dotenv==1.1.1
psycopg2-binary==2.9.10
google-auth-oauthlib==1.0.0
google-auth-httplib2==0.1.0
google-api-python-client==2.86.0
extra-streamlit-components==0.1.56
streamlit-lightweight-charts==0.5.1
```

## 📑 Directory Structure:
```
streamlit_dashboard/
  ├──.streamlit/
  ├──app/
  │   ├── components/
  │   │     ├── content_area.py
  │   │     ├── charts.py
  │   │     ├── layout.py
  │   │     ├── sidebar_toggle_script.py
  │   │     └── toolbar.py
  │   ├── constants/
  │   │     └── pages.py
  │   ├── auth/   (not implemented)
  │   ├── database/
  │   │     ├── connection.py
  │   │     └── queries/
  │   │            └── dashboard_queries.py
  │   ├── pages/
  │   │     ├── dashboard.py
  │   │     ├── login.py
  │   │     ├── analytics.py
  │   │     └── settings.py
  │   ├── utils/
  │   │     ├── formatters.py
  │   │     ├── global_css.py
  │   │     ├── paths.py
  │   │     ├── styles.py
  │   │     └── icon_loader.py
  │   ├── assets/
  │   │     └── icons/
  │   │            └── (logo.png, home.png, analytics.png, etc.)
  │   └── config.py (init_page_config)
  ├──tests/
  ├──main.py
  ├──requirements.txt
  ├──.env
  └──config.py  (db config)
```

## 📦 Core Functionalities  
- **Custom Navbar** (fixed, with logo, title, hamburger for mobile view)
- **Collapsible Sidebar** (hover-expand or hamburger-toggle on mobile)
- **Responsive Content Area** synced with sidebar state (margin shifting on hover/collapse)
- **Dynamic dashboard page** with:
  - SKU, Date Range Filter Form  
  - Metric cards (total units, avg daily units, days with orders)
  - Interactive Chart + Raw Data Tab  
  - Download CSV option
- Mobile responsiveness with adaptive transitions

## 🎨 Styling Goals  
- Top navbar height: `50px`
- Sidebar default width: `50px`, expands to `180px` on hover
- Consistent native BSC blue (`#00AEEF`) for active/hover labels  
- No label underlines  
- Smooth transitions on sidebar hover or collapse  
- Content area margin: starts precisely at 50px top, shifts left on sidebar hover

## 📊 Dashboard Features:
- Filter orders by **Category, Subcategory, SKU, Date Range**
- View **interactive daily order trends (via lightweight-charts)**
- Key metrics:
  - Total units sold
  - Average daily units
  - Number of days with orders
- Download CSV reports
- Data from **PostgreSQL via SQLAlchemy**

---

## 🧠 Caching Strategy

- `@st.cache_data`: for database queries (ttl=3600s)
- `@st.cache_resource`: for layout components

---

## ⚙️ Streamlit Config

```python
import streamlit as st

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title="BSC Dashboard",
    page_icon="📊"
)
```

- CSS overrides via `global_css.py`
- Hides Streamlit branding & icons
- Custom padding and margins
- Icon loading from `assets/icons`

---


- Custom `st.set_page_config` with
  - `wide` layout
  - `collapsed` sidebar
  - Custom logo
- Global CSS to hide:
  - Streamlit's default **menu, deploy, rerun, hamburger**
  - All **link icons from headings**
  - All margins/paddings reset via:
    ```css
    .block-container { padding-top: 0 !important; }
    ```
- `st.query_params` to handle page routing cleanly
- `st.cache_data` for data fetching
- `st.cache_resource` for sidebar and navbar rendering

## 🗃️ Database

- PostgreSQL
- ORM: SQLAlchemy
- Queries organized in `dashboard_queries.py`

---

## 📈 Future Scope

- Add **Google OAuth** based user authentication
- Multiple dashboards:
  - **Inventory Dashboard**
  - **Sales Trends Dashboard**
  - **Customer Analytics**
- Chart export options: **PNG, PDF**
- Role-based access control system

---

## ✅ How to Run

### 1. Setup Virtual Environment
```bash
// mac/linux
python3 -m venv venv
source venv/bin/activate

// Windws
python -m venv venv
& .\venv\Scripts\Activate.ps1
```
or 
```bash
// mac/linux

//Make it Executable
chmod +x setup.sh
//Run it 
./setup.sh
```
```shell
//Windows
//Run it
.\setup.ps1
```
### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup environment variables

Create a `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DEBUG=True
```

### 3. Run Streamlit

```bash
streamlit run main.py
```

---

## 🚀 Roadmap

- Google OAuth login
- Dashboard export (PNG, PDF)
- Inventory & customer analytics modules
- Role-based access control (RBAC)
- Multi-language and dark mode

---

## 💼 License

This project is confidential and developed for internal analytics.

---

## 🤝 Contributions

Feel free to fork, PR, or raise issues if collaborating internally.
