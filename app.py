import streamlit as st 
import pickle
import numpy as np
import pandas as pd
# import the model
pipe = pickle.load(open('pipe.pkl', 'rb'))

df = pickle.load(open('df.pkl', 'rb'))

st.title("Phone Price Predictor")
Platform = st.radio("Platform", ['Android', 'iOS / iPadOS'], index=0)
MarketRegions = st.selectbox("Market_Regions", ['Asia', 'North America', 'Africa', 'Central America', 'South America', 'Eastern Europe', 'Australia', 'Europe'], index=0)
Brand = st.selectbox("Brand", df["Brand"].unique())
DisplayType = st.selectbox("Display_Type", ['AM-OLED display', 'Color IPS TFT LCD display', 'Color PLS TFT LCD display', 'Color ASV TFT LCD display', 'Color TN-TFT LCD display'], index=0)
Resolution = st.selectbox("Resolution", df["Resolution"].unique())
VideoRecording = st.selectbox("Video_Recording", ['3840x2160', '1920x1080', '7680x4320', '3480x2160', '1280x720', '4096x2160', '1080x1920', '2520x1440', '2048x1152'], index=4)
CPUName = st.selectbox("CPU_Name", ['MediaTek Helio', 'Samsung Exynos', 'HiSilicon Honor', 'Qualcomm Snapdragon', 'MediaTek Dimensity', 'Apple A11', 'UNISOC Tiger', 'Apple A16', 'UNISOC SC9863A,', 'Samsung Google', 'Apple A14', 'Apple A15', 'Apple A17', 'UNISOC Tanggula', 'MediaTek MT6739,', 'MediaTek MT6750,'], index=15)
Bluetooth = st.selectbox("Bluetooth", ['5.0', '5.1', '5.2', '4.x', '5.3'], index=1)
SecondaryDisplayType = st.selectbox("Secondary_Display_Type", ["True","False"])
WirelessCharging = st.selectbox("Wireless_Charging",["True","False"])
PixelDensity = st.number_input("Pixel_Density", value=403)
DisplayRefreshRate = st.number_input("Display_Refresh_Rate", value=120)
ROM = st.number_input("ROM", value=128.0)
RAM = st.number_input("RAM", value=3)
CPUClock = st.number_input("CPU_Clock", value=2376.0)

# Make datapoint from user input

if st.button('Predict Price'):
    query = pd.DataFrame([{
        'Platform': Platform,
        'Market Regions': MarketRegions,
        'Brand': Brand,
        'Display Type': DisplayType,
        'Resolution': Resolution,
        'Video Recording': VideoRecording,
        'CPU Name': CPUName,
        'Bluetooth': Bluetooth,
        'Secondary Display Type': SecondaryDisplayType,
        'Wireless Charging': WirelessCharging,
        'Pixel Density': PixelDensity,
        'Display Refresh Rate': DisplayRefreshRate,
        'ROM': ROM,
        'RAM': RAM,
        'CPU Clock': CPUClock,
    }])
    
    # Preprocess the features to match the model's expectations
    #query['Secondary_Display_Type'] = query['Secondary_Display_Type'].map({'True': 1, 'False': 0})
    #query['Wireless_Charging'] = query['Wireless_Charging'].map({True: 1, False: 0})
    
    predicted_price = int(np.exp(pipe.predict(query)[0])*25000)
    
    st.title(f'Predicted Price: {predicted_price} VND')
