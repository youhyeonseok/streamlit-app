import streamlit as st
from streamlit_chat import message
import socket

# 서버 IP와 포트 설정
HOST = '192.168.80.104'  # 서버 IP를 지정
PORT = 8000            # 서버와 동일한 포트 번호

def get_gpt_ask(input):
    # 소켓 생성 및 서버 연결
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # 서버에 메시지 전송
    try:
        message = input.encode('utf-8')
        client_socket.sendall(message)
        data = client_socket.recv(1024)
        print("서버로부터 받은 응답:", data.decode('utf-8'))
    finally:
        client_socket.close()  # 소켓 종료
    

    return data.decode('utf-8')

def gpt():
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
        <div class="styled-data-upload">SMEC GPT</div>
        """,
        unsafe_allow_html=True
    )
    
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello, I am the SMEC Chat GPT. Ask about error codes or equipment issues."]

    if 'past' not in st.session_state:
        st.session_state['past'] = ['Hi']

    # Initialize session state for user input (default is an empty string)
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ""

    response_container = st.container()
    input_container = st.container()

    def get_text():
        input_text = st.text_input("You: ", "", key="input")
        return input_text

    # with input_container:
    #     user_input = get_text()
    #     # ask = get_gpt_ask(user_input)
    #     if user_input:
    #         st.session_state.past.append(user_input)
    #         # response = ask
    #         response = ""
    #         st.session_state.generated.append(response)
    col1, col2 = st.columns([10, 1])  # 4: wider column for text input, 1: smaller for button

    with col1:
        user_input = get_text()

    with col2:
        # Adding custom CSS to style the button
        st.markdown("""
            <style>
                .stButton>button {
                    width: 100%; /* Button width set to 100% of the column */
                    height: 50px; /* Increase button height */
                    font-size: 18px; /* Set font size */
                    border-radius: 8px; /* Rounded corners */
                    background-color: #0A74DA; /* Button background color */
                    color: white; /* Text color */
                    border: none; /* Remove border */
                }
                .stButton>button:hover {
                    background-color: #0066b3; /* Hover effect */
                }
            </style>
        """, unsafe_allow_html=True)

        if st.button("Send", key="send_button") and user_input:

            with st.spinner('generated Answer'):
                st.session_state.past.append(user_input)  # Store user input

                response = get_gpt_ask(user_input)

                st.session_state.generated.append(response)  # Store bot response
                # Clear the input field after sending
                st.session_state['user_input'] = ""  # Reset input text after button click

    with response_container:
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state['generated'][i], key=str(i))
