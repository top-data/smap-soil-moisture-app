import streamlit as st
import geemap.foliumap as geemap
import ee
import json
import os

st.set_page_config(page_title="SMAP Soil Moisture Map", layout="wide")
st.title("SMAP Soil Moisture Viewer")

# -----------------------------
# Earth Engine authentication
# -----------------------------
# Streamlit Cloud secret: EE_CREDENTIALS
ee_credentials = os.environ.get("EE_CREDENTIALS")

if ee_credentials is None:
    st.error("EE_CREDENTIALS not found! Please set your Streamlit secret.")
    st.stop()

# Write JSON to temp file
service_account_path = "/tmp/ee-service-account.json"
with open(service_account_path, "w") as f:
    json.dump(json.loads(ee_credentials), f)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path
ee.Initialize()

# -----------------------------
# Create Map
# -----------------------------
Map = geemap.Map(center=[0, 0], zoom=2)

smap_product = 'NASA/SMAP/SPL4SMGP/007'
smap_bands = ['sm_surface', 'sm_rootzone']

dataset = ee.ImageCollection(smap_product).select(smap_bands).first()

for band in smap_bands:
    Map.addLayer(dataset.select(band), {}, band)

Map.to_streamlit(height=700)
