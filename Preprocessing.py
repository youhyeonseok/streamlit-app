import streamlit as st
import numpy as np
import pandas as pd
from streamlit_antd_components import transfer
import plotly.express as px

def get_outlier(df=None, column=None, weight=1.5):
    # target 값과 상관관계가 높은 열을 우선적으로 진행
    quantile_25 = np.percentile(df[column].values, 25)
    quantile_75 = np.percentile(df[column].values, 75)

    IQR = quantile_75 - quantile_25
    IQR_weight = IQR*weight

    lowest = quantile_25 - IQR_weight
    highest = quantile_75 + IQR_weight

    outlier_idx = df[column][ (df[column] < lowest) | (df[column] > highest) ].index
    return outlier_idx, len(outlier_idx)

def detect_outlier(data):
    dic = {}
    for col in data.dtypes[(data.dtypes != "object")].index:
        val, dic[col] = get_outlier(data, col)

    return val, dic


def is_subset(list1, list2):
    # list2의 모든 요소가 list1에 포함되는지 확인
    return all(item in list1 for item in list2)

def custom_sort(coefficients):
    # 원하는 순서대로 정렬
    sorted_coefficients = sorted(coefficients, key=lambda x: ['kp', 'ki', 'kd','settling_time'].index(x))
    return sorted_coefficients

def dataPreprocessing():

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
        <div class="styled-data-upload">Modeling Dataset Selection</div>
        """,
        unsafe_allow_html=True
    )
    selected_data_name = st.selectbox("",st.session_state["dataName"])
    st.session_state["selected_data_name"] = selected_data_name
    data = st.session_state["csv_data"][selected_data_name]
    st.dataframe(data.head(), use_container_width=True)

    ############################################### data drop na ###########################################################

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
        <div class="custom-subheader">Non Missing Values per Column</div>
    """, unsafe_allow_html=True)
    missing_count = data.isnull().sum()
    fig = px.bar(
        missing_count, 
        x=missing_count.index, 
        y=missing_count.values,
        color=missing_count.values,
        color_continuous_scale='Blues',
    )
    fig.update_layout(
        xaxis_title='Columns',
        yaxis_title='Missing Count'
    )
    graph_placeholder = st.empty()
    graph_placeholder.plotly_chart(fig)


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
        <div class="custom-subheader">Clear Missing Values</div>
    """, unsafe_allow_html=True)
    drop_cols = st.multiselect("Select Drop Columns", data.columns)
    interpolation = st.selectbox("Data Interpolation Technique Selection", ["Linear Interpolation", "Drop"], key="interpolation1")

    if st.button("Processing", key="Processing_b1"):

        with st.spinner('Processing Data'):
            if len(drop_cols) > 0:
                data = data.drop(drop_cols,axis = 1)
            if interpolation == "Drop":
                data = data.dropna()
            elif interpolation == "Linear Interpolation":
                data = data.interpolate(method='linear')
                data = data.dropna()

            missing_count = data.isnull().sum()
            fig.update_traces(
                x = missing_count.index,
                y = missing_count.values
            )
            graph_placeholder.plotly_chart(fig)
            st.toast('Processed Data', icon='😍')

#######################################################################################################################################


################################################################# data outlier ####################################################################

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
        <div class="styled-data-upload">Outlier Detection and Handling</div>
        """,
        unsafe_allow_html=True
    )

    outlier_index, outlier_info = detect_outlier(data)
    outlier_df = pd.DataFrame(list(outlier_info.values()), columns=["value"])
    outlier_df.index = list(outlier_info.keys())

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
        <div class="custom-subheader">outlier Values per Column</div>
    """, unsafe_allow_html=True)
    outlier_fig = px.bar(
        outlier_df, 
        x=outlier_df.index, 
        y=outlier_df.values.reshape(-1),
        color=outlier_df.values.reshape(-1),
        color_continuous_scale='Blues',
    )
    outlier_fig.update_layout(
        xaxis_title='Columns',
        yaxis_title='outlier Count'
    )
    st.plotly_chart(outlier_fig)
    clear_cols = st.multiselect("Select Clear Columns", data.columns)
    interpolation2 = st.selectbox("Data Interpolation Technique Selection", ["Linear Interpolation", "Drop"], key="interpolation2")

    if st.button("Processing"):

        with st.spinner('Processing Data'):
            if len(clear_cols) > 0:
                data = data.drop(clear_cols,axis = 1)

            if interpolation2 == "Drop":
                data = data.dropna()
                
            elif interpolation2 == "Linear Interpolation":
                data = data.interpolate(method='linear')
                data = data.dropna()

            missing_count = data.isnull().sum()
            fig.update_traces(
                x = missing_count.index,
                y = missing_count.values
            )
            graph_placeholder.plotly_chart(fig)
            st.toast('Processed Data', icon='😍')

################################################################################################################################################################################

    if type(data) != type(None):
        select_data,select_columns = selectFeature(data)

        target = selectTarget(select_columns)

        b1 = st.button("데이터 저장")
        if b1:
            with st.spinner('저장중...'):
                st.session_state["selectedData"] = select_data
                st.session_state["target"] = target
                st.session_state["checkPreprocessing"] = True
                st.toast('저장 완료', icon='😍')


def selectFeature(data):
    st.write("Feature 선택")
    label = ["Source", "Target"]
    selected_columns = transfer(
        items=list(data.columns),
        index=[],
        label=label
    )
    
    if is_subset(selected_columns, ['kp', 'ki', 'kd','settling_time']):
        selected_columns = custom_sort(selected_columns)

    select_data = data[selected_columns]
    select_data = select_data.dropna()
    return select_data,selected_columns

def selectTarget(selected_columns):
    st.write("Target 선택")
    target = st.radio(
    "Target 선택",
    set(selected_columns))
    return target