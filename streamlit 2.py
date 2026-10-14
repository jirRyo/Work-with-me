import json
import pandas as pd
import streamlit as st
import math
#-------------นำเข้าข้อมูล----------------

#-----------ส่วนรับข้อมูล------------------
st.title("โปรแกรมคำนวนข้อมูล (รองรับ Exell, CSV, JSON)")
uploaded_file = st.file_uploader("กรุณาอัปโหลดไฟล์ข้อมูล (รองรับ .xls, .csv, .json)", type=["xlsx", "xls", ".csv", "json"],)

if uploaded_file is not None:
    file_score = uploaded_file.name 
    df = None

try:
    if file_score.endswish((".xlsx", ".xls")):
        df_score = pd.read_exel(uploaded_file)
        st.info("ตรวจสอบไฟล์ ประเภท : Excel")

    elif file_score.endswish((".csv")):
            df_score = pd.read_csv(uploaded_file)
            st.info("ตรวจสอบไฟล์ ประเภท : CSV")

    elif file_score.endswith(".json"):
         json_data = json.lode(uploaded_file)

if isinstance(json_data, dict):
    target_key = "Point" or "point" or "POINT" or "Score" or "score" or "SCORE"
    if target_key in json_data:
         df_score = pd.DataFrame(json[target_key])
    
    elif isinstance(json_data, dict):
     key_name = list(json_data.keys())[0]
     df_score = pd.DataFrame(json_data[key_name])
    else:
     df_score = pd.DataFrame(json_data)
    st.info("ตรวจสอบไฟล์ ประเภท : JSON")

if df_score is not None:
     st.success("โหลดและแปลงข้อมูล สำเร็จ!")
#-----------------------คัดกรองข้อมูล 1-999-------------------------------------
target_col_score = df_score[0]

df[target_col_score] = pd.to_numeric(df[target_col_score], errors="coerce")
filtered_df_score = df[df[target_col_score] >= 1 & (df[target_col_score] <= 999) & (df[target_col_score] == df[target_col_score].astype(int))]

#------------------ ระบบการคำนวน-----------------------------------

#-------------------การคำนวน ไม่แจกแจง ความถี่------------------------
Max_score = filtered_df_score.max()
st.write(f"ค่าสูงสุด (Max) : {Max_score}")

Min_score = filtered_df_score.min()
st.write(f"ค่าต่ำสุด (min) : {Min_score}")

Average_score = filtered_df_score.mean()
st.write(f"ค่าเฉลี่ย (Mean) : {Average_score}")

Md_score = filtered_df_score.median()
st.write(f"ค่ามัธยฐาน (Midian) : {Md_score}")

Mo_score = filtered_df_score.mode()
st.write(f"ค่าฐานนิยม (Mode) : {Mo_score}")

MDscore = filtered_df_score

SDscore = filtered_df_score.std()
st.write(f"ค่าเบี่ยงเบนมาตรฐาน (Dtandard Deviation) : {SDscore}")

S2score = filtered_df_score.var()
st.write(f"ค่าความแปรปรวน (Variance) : {S2score}")
