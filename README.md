
# 📊 Streamlit Dashboard Project Description Template

I’m building a **Streamlit-based dashboard project** for **[your brand/product/company name]** called **[Project Name]**.  
Below are the complete details of the project so you can assist me precisely:

## 📌 Project Objective  
- Build an interactive, modern, responsive analytics dashboard using **Streamlit** for visualizing **[type of data — e.g., order trends, financial metrics, marketing analytics]**.  

## 📁 Project Structure  
```
/app  
├── components/         # Common reusable UI parts like navbar, sidebar, charts  
├── pages/              # Dashboard pages (dashboard, analytics, settings etc.)  
├── database/           # Database connections and SQL queries  
├── utils/              # Utilities like formatters and icon loaders  
├── assets/icons/       # PNG icons used in sidebar and navbar  
└── config.py           # Central Streamlit configuration  
main.py                 # App entry point  
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

## 📊 Technologies  
- **Streamlit** for frontend + app structure  
- **PostgreSQL** (or your DB) via custom queries  
- **Pandas / Altair / Plotly / Matplotlib** (for data + charts)

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
- Sidebar labels should animate opacity on hover  
- Sidebar icons should **not shrink on collapse**  
- No top space above main content area (content starts exactly after navbar)
- Sidebar labels change color to BSC blue on hover  
- Mobile-friendly hamburger toggle to open sidebar  
- Smooth margin transitions for content area sync  

## 📈 Future Scope  
- Add user authentication (Google OAuth)
- Add multiple dashboards (inventory, sales trends, customer analytics)
- Add chart export options (PNG, PDF)
- Role-based access control  

---

📌 **Now, based on this context — please [your request/question here]**
