import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go

def fileRead():
    # CSV 파일 업로더 위젯 생성
    uploaded_file_csv = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file_csv is not None and not uploaded_file_csv.name in st.session_state.get("dataName", []):
        
        csv_data = pd.read_csv(uploaded_file_csv, index_col=0, encoding="CP949", low_memory=False)
        file_size = len(uploaded_file_csv.getvalue())
        
        st.session_state["csv_data"][uploaded_file_csv.name] = csv_data
        st.session_state["csv_data_row"].append({uploaded_file_csv.name: csv_data.shape[0]})
        st.session_state["csv_data_col"].append({uploaded_file_csv.name: csv_data.shape[1]})
        st.session_state["csv_data_size"].append({uploaded_file_csv.name: file_size})
        st.session_state["dataName"].append(uploaded_file_csv.name)

def fileList():
    st.write()
    st.write()
    st.markdown("""
        <style>
        .custom-subheader {
            font-size: 16px; /* Set font size */
            font-weight: bold; /* Make it bold */
            color: #0A74DA; /* Set a custom color */
            text-align: left; /* Center align the text */
            padding: 10px 0; /* Add padding to the top and bottom */
            border-radius: 8px; /* Rounded corners for a soft look */
            margin-top: 20px; /* Add space above the subheader */
        }
        </style>
        <div class="custom-subheader">UPLOADED FILES</div>
    """, unsafe_allow_html=True)

    uploaded_data_list = pd.DataFrame([], columns=["NAME", "ROW LENGTH", "COL LENGTH", "DATA SIZE"])
    temp_name, temp_row, temp_col, temp_size = [], [], [], []

    for name, row, col, size in zip(st.session_state["dataName"], st.session_state["csv_data_row"], st.session_state["csv_data_col"], st.session_state["csv_data_size"]):
        temp_name.append(name)
        temp_row.append(list(row.values())[0])
        temp_col.append(list(col.values())[0])
        temp_size.append(str(list(size.values())[0])+" byte")

    uploaded_data_list["NAME"] = temp_name
    uploaded_data_list["ROW LENGTH"] = temp_row
    uploaded_data_list["COL LENGTH"] = temp_col
    uploaded_data_list["DATA SIZE"] = temp_size

    html = '<table style="width:100%; border-collapse: collapse;">'
    html += '<thead><tr><th>NAME</th><th>ROW LENGTH</th><th>COL LENGTH</th><th>DATA SIZE</th></tr></thead>'
    html += '<tbody>'

    for i in range(len(temp_name)):
        html += f"<tr><td>{temp_name[i]}</td><td>{temp_row[i]}</td><td>{temp_col[i]}</td><td>{temp_size[i]}</td>"

    html += '</tbody></table>'
    st.markdown(html, unsafe_allow_html=True)

    ################################################################### data charting ######################################################################################
    st.markdown(
        """
        <style>
        .styled-data-upload {
            font-size: 24px; /* 텍스트 크기 */
            font-weight: bold;
            color: #0A74DA; /* 헤더 텍스트 색상 */
            text-align: left; /* 텍스트 중앙 정렬 */
            padding: 10px 0;
            border-bottom: 2px solid #0A74DA; /* 하단 테두리 */
            margin-top: 20px;
            font-family: Arial, sans-serif; /* 폰트 설정 */
        }
        </style>
        <div class="styled-data-upload">DATA OVERVIEW</div>
        """,
        unsafe_allow_html=True
    )

    # Create a custom select box with blue and black color scheme
    selected_data_name = st.selectbox(
        'SLECTE DATA:',
        temp_name,
        key='styled_selectbox',
        help="데이터를 선택하면 해당 데이터가 표시됩니다."
    )

    if selected_data_name != None:
        selected_data = st.session_state["csv_data"][selected_data_name]

        page_size = 100

        if 'page' not in st.session_state:
            st.session_state.page = 0

        def get_page_data(df, page, page_size):
            start_row = page * page_size
            end_row = (page + 1) * page_size
            return df[start_row:end_row]

        col1, col2 = st.columns([20, 1])
        with col1:
            if st.button('Previous') and st.session_state.page > 0:
                st.session_state.page -= 1
        with col2:
            if st.button('Next') and (st.session_state.page + 1) * page_size < len(selected_data):
                st.session_state.page += 1 

        page_data = get_page_data(selected_data, st.session_state.page, page_size)
        st.dataframe(page_data, use_container_width=True)
        st.markdown(f"<h5 style='text-align: left; font-size:14px;'>Page {st.session_state.page + 1} of {len(selected_data) // page_size + 1}</h5>", unsafe_allow_html=True)

        st.markdown("""
            <style>
            .custom-subheader {
                font-size: 16px; /* Set font size */
                font-weight: bold; /* Make it bold */
                color: #0A74DA; /* Set a custom color */
                text-align: left; /* Center align the text */
                padding: 10px 0; /* Add padding to the top and bottom */
                border-radius: 8px; /* Rounded corners for a soft look */
                margin-top: 20px; /* Add space above the subheader */
            }
            </style>
            <div class="custom-subheader">DATA DESCRIBE</div>
        """, unsafe_allow_html=True)
        st.dataframe(selected_data.describe(), use_container_width=True)

        st.markdown("""
            <style>
            .custom-subheader {
                font-size: 16px; /* Set font size */
                font-weight: bold; /* Make it bold */
                color: #0A74DA; /* Set a custom color */
                text-align: left; /* Center align the text */
                padding: 10px 0; /* Add padding to the top and bottom */
                border-radius: 8px; /* Rounded corners for a soft look */
                margin-top: 20px; /* Add space above the subheader */
            }
            </style>
            <div class="custom-subheader">DATA VISUALIZATION</div>
        """, unsafe_allow_html=True)

        cols = st.multiselect("Select columns", selected_data.columns)
        fig = go.Figure()
        x = [i for i in range(len(selected_data))]
        for col in cols:
            fig = fig.add_trace(go.Scatter(x=x, y=selected_data[col], name=col))

        st.plotly_chart(fig)