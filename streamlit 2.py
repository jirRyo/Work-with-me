import json
import pandas as pd
import streamlit as st
import math
import numpy as np

#-------------นำเข้าข้อมูล----------------

#-----------ส่วนรับข้อมูล------------------
st.title("โปรแกรมคำนวนข้อมูล (รองรับ Exell, CSV, JSON)")
uploaded_file = st.file_uploader("กรุณาอัปโหลดไฟล์ข้อมูล (รองรับ .xls, .csv, .json)", type=["xlsx", "xls", ".csv", "json"],)

df_score = None
json_data = None

if uploaded_file is not None:
    try:
        file_score = uploaded_file.name 

        if file_score.endswith((".xlsx", ".xls")):
             df_score = pd.read_excel(uploaded_file, header=None)
             df_score.columns = [f"คอลัมน์_{i+1}" for i in range(df_score.shape[1])]
             st.info("ตรวจสอบไฟล์ ประเภท : Excel")

        elif file_score.endswith((".csv")):
             df_score = pd.read_csv(uploaded_file, header=None)
             df_score.columns = [f"คอลัมน์_{i+1}" for i in range(df_score.shape[1])]
             st.info("ตรวจสอบไฟล์ ประเภท : CSV")

        elif file_score.endswith(".json"):
         json_data = json.load(uploaded_file)

        if json_data is not None: 
            if isinstance(json_data, dict):
              target_key = "Point" or "point" or "POINT" or "Score" or "score" or "SCORE"

            if target_key in json_data:
              df_score = pd.DataFrame(json_data[target_key])
              df_score.columns = [f"คอลัมน์_{i+1}" for i in range(df_score.shape[1])]
              st.info("ตรวจสอบไฟล์ ประเภท : JSON")
            elif isinstance(json_data, dict):
              key_name = list(json_data.keys())[0]
              df_score = pd.DataFrame(json_data[key_name])
              df_score.columns = [f"คอลัมน์_{i+1}" for i in range(df_score.shape[1])]
              st.info("ตรวจสอบไฟล์ ประเภท : JSON")
            else:
              df_score = pd.DataFrame(json_data)
              df_score.columns = [f"คอลัมน์_{i+1}" for i in range(df_score.shape[1])]
              st.info("ตรวจสอบไฟล์ ประเภท : JSON")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์: {e}")

if df_score is not None:
     st.success("โหลดและแปลงข้อมูล สำเร็จ!")
#-----------------------คัดกรองข้อมูล 1-999-------------------------------------
     target_col_score = df_score.columns[0]

     df_score[target_col_score] = pd.to_numeric(df_score[target_col_score], errors="coerce")
     filtered_df_score = df_score[df_score[target_col_score] >= 1 
                       & (df_score[target_col_score] <= 999) 
                       & (df_score[target_col_score] == df_score[target_col_score].astype(float))]

#---------------------ระบบเลือก คอลัมน์ ที่ต้องการคำนวณ-----------------
     st.header("ตารางแสดงผลการนำเข้า ข้อมูล ")
     st.dataframe(filtered_df_score)
     number_columns = filtered_df_score.select_dtypes(include=['number']).columns.tolist()

     filtered_df_score.columns = filtered_df_score.columns.astype(str)

     all_columns = filtered_df_score.columns.tolist()

     if all_columns:
        st.warning("คำเตือน: ควรตรวจเช็คความถูกต้อง ของข้อมูลที่ต้องการคำนวณ")
        selected_column = st.selectbox("กรุณาเลือกคอลัมน์ที่ต้องการคำนวณ :", all_columns)
#------------------ ระบบการคำนวน-----------------------------------
     if selected_column:
         st.markdown("""
    <style>
    /* ปรับขนาดตัวอักษรของตัวเลือกใน st.radio */
    .stRadio label p {
        font-size: 35px !important; /* ปรับขนาดตัวเลขตามต้องการ เช่น 20px หรือ 24px */
    }
    </style>
""", unsafe_allow_html=True)
         
         st.write("-------------------------------------------------------------")
         calc_mode = st.radio(
             "🎛️ กรุณาเลือกรูปแบบการแสดงผลและการคำนวณ:",
             ("แบบไม่แจกแจงความถี่ (Ungrouped Data)", "แบบแจกแจงความถี่ (Frequency Distribution)")
         )
         st.write("-------------------------------------------------------------")
#-------------------การคำนวน ไม่แจกแจง ความถี่------------------------
     
     
     if selected_column:
        if calc_mode == "แบบไม่แจกแจงความถี่ (Ungrouped Data)":
          st.subheader("📊 ผลการคำนวณแบบไม่แจกแจงความถี่")
          
          Max_score = filtered_df_score[selected_column].max()
          st.success(f"ค่าสูงสุด (Max) :  {Max_score:.2f}")

          Min_score = filtered_df_score[selected_column].min()
          st.success(f"ค่าต่ำสุด (min) :  {Min_score:.2f}")

          Average_score = filtered_df_score[selected_column].mean()
          st.success(f"ค่าเฉลี่ย (Mean) :  {Average_score:.2f}")

          Md_score = filtered_df_score[selected_column].median()
          st.success(f"ค่ามัธยฐาน (Midian) :  {Md_score:.2f}")

          Mo_score = filtered_df_score[selected_column].mode()
          value_counts = filtered_df_score[selected_column].value_counts()
          if value_counts.iloc[0] == 1:
            Mo_score = st.error("์ไม่มี ค่าฐานนิยม")
          else:
            Mo_score = ", ".join(map(str, Mo_score.tolist()))
          st.success(f"ค่าฐานนิยม (Mode) :  {Mo_score}")

          MDscore = (filtered_df_score[selected_column] - Average_score).abs().mean()
          st.success(f"ค่าเบี่ยงเบนเฉลี่ย (Mean Absolute Deviation) :  {MDscore:.2f}")

          SDscore = filtered_df_score[selected_column].std()
          st.success(f"ค่าเบี่ยงเบนมาตรฐาน (Standard Deviation) :  {SDscore:.2f}")

          S2score = filtered_df_score[selected_column].var()
          st.success(f"ค่าความแปรปรวน (Variance) :  {S2score:.2f}")

        elif calc_mode == "แบบแจกแจงความถี่ (Frequency Distribution)":
          st.subheader("📊 ผลการคำนวณแบบแจกแจงความถี่")
          st.write("-------------------------------------------------------------")
          
          total_data = len(filtered_df_score[selected_column].dropna())

          Max_score = filtered_df_score[selected_column].max()
          Min_score = filtered_df_score[selected_column].min()
        
          R_score = Max_score - Min_score 
 #********************************************************************************************
          st.warning("โปรดเลือกชั้นที่ต้องการ เพื่อนำไปคำนวณในการหาข้อมูลแบบ แจกแจงความถี่")       
          num_classes = st.slider("เลือกจำนวนชั้น (3 - 15 ชั้น):", min_value=3, max_value=15, value=5)
          st.success(f"จำนวนชั้นที่คุณเลือกคือ: {num_classes}")

          i_Layer = int(np.ceil(R_score / num_classes)) if R_score > 0 else 1 #อัตราภาคชั้น
#-------------------คำนวณ ขีดบน ล่าง กึ่งกลาง--------------------------------------------------
          lower_limits = [Min_score + (k * i_Layer) for k in range(num_classes)]
          upper_limits = [lower + i_Layer - 1 for lower in lower_limits]

          if upper_limits[-1] < Max_score:
           upper_limits[-1] < Max_score

          lower_real = [lower - 0.5 for lower in lower_limits]
          upper_real = [upper + 0.5 for upper in upper_limits]

          midpoints = [(lower + upper) / 2.0 for lower, upper in zip(lower_limits, upper_limits)]

          frequencies = []
          for lower, upper in zip(lower_limits, upper_limits):
            count_fq = filtered_df_score[(filtered_df_score[selected_column] >= lower) & (filtered_df_score[selected_column] <= upper)].shape[0]
            frequencies.append(int(count_fq))

          sum_frequencies = sum(frequencies)

          cumulative_frequencies = np.cumsum(frequencies).tolist()

          proportions = [f / total_data if total_data > 0 else 0 for f in frequencies]

          percentages = [p * 100 for p in proportions]

#------------------การแสดงหน้าต่างรวม------------------
          freq_table = pd.DataFrame({
      "ชั้นที่": range(1, num_classes + 1),
      "ขีดจำกัดล่างแท้": lower_real,
      "ขีดจำกัดบนแท้": upper_real,
      "จุดกึ่งกลางชั้น": midpoints,
      "ความถี่ (f)": frequencies,
      "ความถี่สะสม (CF)": cumulative_frequencies,
      "สัดส่วน": proportions,
      "ร้อยละ (%)": percentages,
})
          total_row = pd.DataFrame({
     "ชั้นที่": ["รวม"],
      "ขีดจำกัดล่างแท้": [""],
      "ขีดจำกัดบนแท้": [""],
      "จุดกึ่งกลางชั้น": [""],
      "ความถี่ (f)": [sum(frequencies)],  # ผลรวมความถี่
      "ความถี่สะสม (CF)": [""],
      "สัดส่วน": [sum(proportions)],  # ผลรวมสัดส่วนควรได้ 1.0000
      "ร้อยละ (%)": [sum(percentages)],  # ผลรวมร้อยละควรได้ 100.00%
})
          final_table = pd.concat([freq_table, total_row], ignore_index=True) #การรวม หน้าต่าง เข้าด้วยกัน

          styled_table = final_table.style.format({
    "สัดส่วน": lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x,
    "ร้อยละ (%)": lambda x: f"{x:.2f}%" if isinstance(x, (int, float)) else x,
})
          st.subheader("📊 ตารางแจกแจงความถี่สมบูรณ์")
          st.dataframe(styled_table, use_container_width=True)

#-----------------------------------------------------------------------------------------------------
#-----------------------------การหาค่าสถิติ--------------------------------------------------------------
          st.write("---------------------------------------------------")
          st.header("การคำนวณค่าสถิติ")

          n = total_data

          def calculate_Quartie(k):
            target = (k * n) / 4

            for index, row in freq_table.iterrows():
              cf_current = freq_table.loc[:index, "ความถี่ (f)"].sum()
              cf_prev = freq_table.loc[:index-1, "ความถี่ (f)"].sum() if index > 0 else 0 

              if target <= cf_current:
                 L = lower_real[index] 
                 f_q = row["ความถี่ (f)"]

                 Q_val = L + (((target - cf_prev) / f_q) * i_Layer)
                 return Q_val
              
          Q1 = calculate_Quartie(1)
          Q3 = calculate_Quartie(3)

          if Q1 is not None and Q3 is not None:
            IndexR = Q3 - Q1
            Qd = IndexR / 2 

          st.success(f"ควอร์ไทล์ที่ 1 : {Q1:.2f}")
          st.success(f"ควอร์ไทล์ที่ 3 : {Q3:.2f}")
          st.success(f"พิสัยรหว่างควอร์ไทล์ : {IndexR:.2f}")
          st.success(f"ค่าเบี่ยงเบนควอร์ไทล์ : {Qd:.2f}")

#---
          f = np.array(frequencies)
          x = np.array(midpoints)

          sum_fx = np.sum( f * x)
          sum_fx_2 = np.sum( f * (x ** 2))

          if n > 1:
            numerater = (n * sum_fx_2) - (sum_fx ** 2)
            denominator = n * ( n - 1)
            S = np.sqrt(numerater / denominator)
          else:
            S = 0

          st.success(f"ค่าเบี่ยงเบนมาตราฐาน (S):  {S:.2f}")
#---

          if n > 0:
             mean_X = sum_fx / n 
          else:
             mean_X = 0 

          st.success(f"ค่าเฉลี่ยเลขคณิต (X) :  {mean_X:.2f}")

 #---
          target_md = n / 2
          median_val = 0.0

          for index in range(len(frequencies)):
            cf_current = cumulative_frequencies[index]
            cf_prev = cumulative_frequencies[index - 1] if index > 0 else 0
        
            if target_md <= cf_current:
              L = lower_real[index]
              f_md = frequencies[index]

              if f_md > 0:
                median_val = L + i_Layer * ((target_md - cf_prev) / f_md)
              break
          
          st.success(f"ค่ามัธยฐาน (Md):  {median_val:.2f}")

 #---
          max_freq = max(frequencies)
          mode_values = []
      
          if max_freq > 0:
            for index, f_val in enumerate(frequencies):
                if f_val == max_freq:
                    L_mo = lower_real[index]
                    f_mo = f_val
                    
                    f_prev = frequencies[index - 1] if index > 0 else 0
                    f_next = frequencies[index + 1] if index < len(frequencies) - 1 else 0
                    
                    d1 = f_mo - f_prev
                    d2 = f_mo - f_next
                    
                    if (d1 + d2) > 0:
                        mode_val = L_mo + (d1 / (d1 + d2)) * i_Layer
                    else:
                        mode_val = L_mo
                        
                    mode_values.append(mode_val)

          if mode_values:
            formatted_modes = ", ".join([f"{m:.2f}" for m in mode_values])
            st.success(f"ค่าฐานนิยม (Mo): {formatted_modes}")
          else:
            st.warning("ไม่พบฐานนิยม เนื่องจากความถี่ทุกชั้นเป็น 0")
#-------------------------------------------------------------------