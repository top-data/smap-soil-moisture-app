import streamlit as st
import ee
import geemap.foliumap as geemap
import datetime

# --- Initialize Earth Engine safely ---
try:
    ee.Initialize(project='ee-mhdsaki')
except Exception:
    ee.Authenticate()
    ee.Initialize(project='ee-mhdsaki')

# --- Streamlit title ---
st.title("🌍 SMAP Soil Moisture Viewer (Surface & Rootzone)")

# --- Define dataset and bands ---
smap_product = 'NASA/SMAP/SPL4SMGP/008'
smap_bands = {
    'Surface Soil Moisture': 'sm_surface',
    'Rootzone Soil Moisture': 'sm_rootzone'
}

# --- Sidebar date selection ---
st.sidebar.header("🗓️ Date Range")
end_date = st.sidebar.date_input("End Date", datetime.date.today())
start_date = st.sidebar.date_input("Start Date", end_date - datetime.timedelta(days=3))

# --- Load SMAP data ---
collection = ee.ImageCollection(smap_product).filterDate(str(start_date), str(end_date))
image = collection.sort('system:time_start', False).first()

# --- Create map ---
Map = geemap.Map(center=[0, 0], zoom=2, ee_initialize=False)

# --- Add layers ---
for name, band in smap_bands.items():
    vis_params = {
        'min': 0,
        'max': 0.5,
        'palette': ['#d7191c', '#fdae61', '#ffffbf', '#abd9e9', '#2c7bb6']
    }
    Map.add_layer(image.select(band), vis_params, name)

Map.add_layer_control()

# --- Display map ---
Map.to_streamlit(height=600)

st.sidebar.info("""
This app visualizes **SMAP L4 Global Soil Moisture (9-km, 3-hourly)** data.  
Select a date range and toggle between:
- Surface Soil Moisture  
- Rootzone Soil Moisture  
""")
