import streamlit as st 
import pickle
import numpy as np

# import the model
pipe = pickle.load(open('pipe.pkl', 'rb'))

df = pickle.load(open('df.pkl', 'rb'))

st.title("Phone Price Predictor")
SecDis=st.selectbox("Secondary Display Type",["True","False"])
WirelessCharging=st.selectbox("Wireless Charing",["True","False"])
platform=st.selectbox("Platform",df["Platform"].unique())
category=st.selectbox("Device Category",df["Device Category"].unique())
brand =st.selectbox('Brand', df['Brand'].unique())

# pixel density
density = st.number_input("Density Pixel")

# Region
Region = st.selectbox("Region", df["Market Regions"].unique())
#Zoom
zoom=st.number_input("Zoom")

#Display Type
display=st.selectbox("Display Type",df["Display Type"].unique())

ROM=st.number_input("ROM")
Refresh=st.selectbox("Dipslay Refresh Rate",[0,60,90,120,144,165,240])

#CPU Clock
CPU=st.number_input("CPU Clock")

#SIM
SIM=st.selectbox("Sec. SIM Card Slot",["True","False"])
# weight
mass = st.number_input('Weight of the laptop')

# CPU Name
CPUName=st.selectbox("CPU Name",df["CPU Name"].unique())

RAM=st.selectbox("RAM",[1,2,3,4,6,12,16,18])
bluetooth=st.number_input("bluetooth")
video_reoslution = st.selectbox('VidResolution',['1920x1080','1366x768','1600x900','1440x900','3840x2160','3200x1800',
                                               '2880x1800','2560x1600','2560x1440','2304x1440'])
resolution=st.selectbox('Resolution',['1920x1080','1366x768','1600x900','1440x900','3840x2160','3200x1800',
                                               '2880x1800','2560x1600','2560x1440','2304x1440'])
inches=st.number_input("Inches")

if st.button('Predict Price'):
    # query
    X_record=int(video_reoslution.split('x')[0])
    Y_record=int(video_reoslution.split('x')[1])
    vid_resolution=X_record*Y_record/1000000
    
    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res**2) + (Y_res**2))**0.5/inches
    query = np.array([SecDis, WirelessCharging, platform, category, brand, density, Region, zoom, display, ROM, Refresh,CPU, SIM, mass,ppi,CPUName,RAM,vid_resolution,bluetooth], dtype = object)
    
    query = query.reshape(1, 19)
    st.title(str(int(np.exp(pipe.predict(query)[0])*25000))+' VND')