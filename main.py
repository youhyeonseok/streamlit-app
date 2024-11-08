import streamlit as st
import pandas as pd
import os
import random
import numpy as np
from fileManger import fileRead, fileList
from setting import Initialize
from Preprocessing import dataPreprocessing
# from modeling import modelTraing
# from visualization import visualizeTestData
# from controlGainOptimization import bayesianOptimization
from st_on_hover_tabs import on_hover_tabs
from GPT import gpt
# from miminizeOptimization import miminizeOptimization
# from basinhopping import basinhope
import warnings
# 경고 메시지 무시 설정
warnings.filterwarnings("ignore", message="I don't know how to infer vegalite type from 'empty'.*")

###############실행 방법################
#
#   command 창에 streamlit run 파일이름 --server.maxUploadSize 업로드 용량(MB)
#   실행을 원하는 파일이름을 적고 뒤에 업로드 용량을 적으셔야지 용량이 큰 파일도 업로드가 됩니다.
#   ex)
#   streamlit run main.py --server.maxUploadSize 2000
#   -> main.py를 실행하고 2GB의 데이터까지 업로드 할 수 있는 서버환경 구축됨
# 
#####################################

def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)

def session_state_ck():
    for key, _ in st.session_state.items():
        if key == "initCk":
            return True
    return False

def run():
    
    seed_everything(42)
    st.set_page_config(layout="wide", page_title = "SMEC SMART SOLUTION")

    if not session_state_ck():
        Initialize()

    ############################################################ Home 화면 커스텀 ############################################################################
    st.markdown(
        """
        <style>
        .styled-header {
            font-size: 36px; /* 텍스트 크기 */
            font-weight: bold;
            color: #0A74DA; /* 헤더 텍스트 색상 */
            text-align: center; /* 텍스트 중앙 정렬 */
            padding: 10px 0;
            border-bottom: 2px solid #0A74DA; /* 하단 테두리 */
            margin-top: 20px;
            font-family: Arial, sans-serif; /* 폰트 설정 */
        }
        </style>
        <div class="styled-header">SMEC SMART SOLUTION</div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.image("CSS/image3-Photoroom.png", caption="2025 SMART MACHINE TOP1")
    st.markdown('<style>' + open('CSS/style.css').read() + '</style>', unsafe_allow_html=True)

    ###############################################################################################################################################################

    with st.sidebar:
        tabs = on_hover_tabs(
            tabName=["DATA UPLOAD", "DATA Preprocessing", "기계학습 모델링", "데이터 가시화", "SMEC GPT"], 
            iconName=["drive_folder_upload", 'construction', 'drive_folder_upload', 'drive_folder_upload', 
                    'chat'],
            default_choice=0
        )
    if tabs == "DATA UPLOAD":

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
            <div class="styled-data-upload">DATA UPLOAD</div>
            """,
            unsafe_allow_html=True
        )

        fileRead()
        fileList()

    if tabs == "파일 불러오기":
        pass
        # fileRead()
        # fileList()

    elif tabs == "DATA Preprocessing":
        dataPreprocessing()

    elif tabs == "기계학습 모델링":
        pass
        # if st.session_state["checkPreprocessing"] == False:
        #     dataPreprocessing()
        # else:
        #     modelTraing(st.session_state["selectedData"])

    elif tabs == "데이터 가시화":
        pass
        # visualizeTestData()

    elif tabs == "SMEC GPT":
        gpt()

if __name__ == "__main__":
    run()