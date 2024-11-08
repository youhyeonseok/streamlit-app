from scipy.optimize import basinhopping
import streamlit as st
import numpy as np
from scipy.optimize import minimize
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def predictor(x):
    model = st.session_state[st.session_state["optmodel"]]
    if st.session_state["model_name"] == "MLPkeras":
        pred = model.predict(np.array(x).reshape(1, -1))[0][0]
    else:
        pred = model.predict(np.array(x).reshape(1, -1))[0]

    return np.abs(pred - st.session_state["target_value"])

def print_fun(x, f, accepted):
        print("at minimum %.4f accepted %d" % (f, int(accepted)))

def basinhope():
    st.divider()
    st.header("basinhopping Otimization")
    st.divider()
    target_value = st.number_input("target값 입력")
    st.session_state["target_value"] = target_value

    selected_model = []
    if st.session_state["RandomForest"] != None:
        selected_model.append("RandomForest")
    if st.session_state["MLPsklearn"] != None:
        selected_model.append("MLPsklearn")
    if st.session_state["MLPkeras"] != None:
        selected_model.append("MLPkeras")
    if st.session_state["XGBoost"] != None:
        selected_model.append("XGBoost")
    model_name = st.selectbox("테스트 학습모델 선택", set(selected_model))
    st.session_state["optmodel"] = model_name
    data = st.session_state["selectedData"].drop([st.session_state["target"]],axis=1)

    pbounds = []
    for i in range(len(data.columns)):
        curr_name = data.columns[i]
        col1,col2 = st.columns(2)
        with col1:
            val1 = st.number_input(curr_name+" 최소값 입력",value=0.0)
        with col2:
            ma = data[curr_name].mean()
            val2 = st.number_input(curr_name + " 최대값 입력",value=ma)
        pbounds.append((val1,val2))
    st.session_state["model_name"] = model_name

    b1 = st.button("Search best PID parameter")
    init_point = np.array([50,0.01,1500])
    # init_point_scaled = np.array([0.5, 0.5, 0.5])
    scaler = st.session_state["scaler"]
    init_point = scaler.transform(init_point.reshape(1,3))
    print(target_value)
    if b1:
        with st.spinner('찾는중...'):
            minimizer_kwargs = dict(method="L-BFGS-B",bounds=pbounds)
            res = basinhopping(predictor, init_point.flatten(),minimizer_kwargs=minimizer_kwargs,niter=200,callback=print_fun)
            point = np.array(res.x)
            x_opt = scaler.inverse_transform(point.reshape(1,3))

            for i in range(len(res.x)):
                st.write("Opt X{}:".format(i),res.x[i])
            st.write("Opt Y:", predictor(point)+target_value)
            st.write("Y Error: {:.2f}%".format(res.fun/target_value*100))
            st.write("X: Kp={0:.4f}, Ki={1:.4f}, Kd={2:.4f}".format(x_opt[0,0], x_opt[0,1],x_opt[0,2]))