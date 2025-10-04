
# 📊 Streamlit Dashboard Project Description Template

I’m building a **Analytical Dashboard Project** for **Business Analytics** using **Python** and **Streamlit**.  
Below are the complete details of the project so you can assist me precisely:

## 📖 Project Description:
A modern responsive **Streamlit dashboard** for Bombay Shaving Company operations to track and visualize order performance (by SKU, category, subcategory, and date range) using a **PostgreSQL data source**. It includes:
- Custom collapsible **sidebar**
- Fixed **navbar with toolbar**
- **Dashboard** page with filters, charts, metrics, and export options
- Clean, modern UI with custom CSS
- **Caching for improved query performance**
- Streamlit UI config overrides for:
  - No default sidebar
  - No deploy button
  - No Streamlit header/footer
  - No heading link icons
  - Zero top margin before page content  
  - Optimized mobile responsiveness

## 📌 Project Objective  
- Build an interactive, modern, responsive analytics dashboard using **Streamlit** for visualizing **[type of data — e.g., order trends, financial metrics, marketing analytics]**.

## 🗂️ Project Features

- Modern **navbar + collapsible sidebar** layout
- Dynamic **toolbar dropdowns**
- Responsive layout with mobile hamburger menu
- Dashboard filters: **category, subcategory, SKU, date range**
- Metrics cards and Plotly charts
- Chart exportable via CSV
- Centralized **icon loader and formatters**
- Clean **caching** with `st.cache_data` and `st.cache_resource`

## 📌 Tech Stack:
- **Python 3.12**
- **Streamlit 1.46.1**
- **Pandas 2.3.1**
- **SQLAlchemy 2.0.41**
- **Plotly 5.18.0**
- **psycopg2-binary 2.9.10**
- **python-dotenv 1.1.1**
- **Google OAuth via google-auth-oauthlib & google-api-python-client**
- **extra-streamlit-components**
- **streamlit-lightweight-charts**

## 📦 Requirements
```
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

## ⚙️ Streamlit Configuration:
- `st.set_page_config()`
- CSS overrides to:
  - Remove Streamlit header/footer and sidebar controls
  - Set `padding-top: 0rem` on `.block-container`
  - Remove link icons from markdown headings
  - Fix content area margins and responsiveness
  - Custom styles for navbar, sidebar, toolbar, charts, and metric cards

## 💾 Caching:
- **@st.cache_data** for metadata and queries (ttl=3600s)
- **@st.cache_resource** for one-time sidebar, navbar, layout render caching

## 📜 Database:
- **PostgreSQL**
- Table: `your_table`
- Queries via `DashboardQueries`

## 📁 Files I’ve implemented  
- main.py  
- app/components/navbar.py  
- app/components/sidebar.py  
- app/components/layout.py  
- app/pages/dashboard.py  
- app/utils/icon_loader.py  
- app/utils/formatters.py  
- app/config.py

## ✅ Custom Requirements

- Sidebar labels **animate opacity on hover**
- Sidebar icons **do not shrink** on collapse
- **No top space** above main content area (starts exactly after navbar)
- Sidebar labels change color to **BSC blue** on hover
- **Mobile-friendly hamburger toggle** to open sidebar
- Smooth **margin transitions** for content area sync

## 🛠️ Configurations

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

## 📈 Future Scope

- Add **Google OAuth** based user authentication
- Multiple dashboards:
  - **Inventory Dashboard**
  - **Sales Trends Dashboard**
  - **Customer Analytics**
- Chart export options: **PNG, PDF**
- Role-based access control system

---
## 📌 How to Run

1️⃣ Install requirements

```bash
  pip install -r requirements.txt
```

2️⃣ Set env variables in `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DEBUG=True
```

3️⃣ Run Streamlit

```bash
  streamlit run main.py
```
