import streamlit as st
import json

# 读取JSON文件
with open('dimensions.json') as f:
    dimensions = json.load(f)

with open('questions.json') as f:
    questions = json.load(f)

with open('personalities.json') as f:
    personalities = json.load(f)

# 全局变量
total_questions = 40
questions_list = questions['questions']['EI'] + questions['questions']['SN'] + questions['questions']['TF'] + questions['questions']['JP']

# 辅助函数
def calculate_probabilities(answers):
    # 分段计算每个维度的0和1的个数
    EI_count = sum(answers[i] for i in range(10))
    SN_count = sum(answers[i] for i in range(10, 20))
    TF_count = sum(answers[i] for i in range(20, 30))
    JP_count = sum(answers[i] for i in range(30, 40))
    
    # 计算每个维度中两种属性的概率
    EI_prob = {'E': EI_count / 10, 'I': (10 - EI_count) / 10}
    SN_prob = {'S': SN_count / 10, 'N': (10 - SN_count) / 10}
    TF_prob = {'T': TF_count / 10, 'F': (10 - TF_count) / 10}
    JP_prob = {'J': JP_count / 10, 'P': (10 - JP_count) / 10}
    
    # 计算16种人格的概率
    probabilities = {}
    for ei in EI_prob:
        for sn in SN_prob:
            for tf in TF_prob:
                for jp in JP_prob:
                    personality = ei + sn + tf + jp
                    probabilities[personality] = (
                        EI_prob[ei] *
                        SN_prob[sn] *
                        TF_prob[tf] *
                        JP_prob[jp]
                    )
    
    return probabilities

# Streamlit界面
st.title('MBTI人格测试')

if 'answers' not in st.session_state:
    st.session_state.answers = [-1] * total_questions

if 'checkbox_state' not in st.session_state:
    st.session_state.checkbox_state = [[False, False] for _ in range(total_questions)]

cv_dict = {"是": 1, "否": 0}

# 显示所有问题
for idx, question_data in enumerate(questions_list):
    st.write(f"{idx+1}. {question_data['question']}")
    col1, col2 = st.columns(2)
    with col1:
        if st.checkbox(f"是", key=f"yes_{idx}", value=st.session_state.checkbox_state[idx][0]):
            st.session_state.checkbox_state[idx][0] = True
            st.session_state.checkbox_state[idx][1] = False
            st.session_state.answers[idx] = cv_dict["是"]
    with col2:
        if st.checkbox(f"否", key=f"no_{idx}", value=st.session_state.checkbox_state[idx][1]):
            st.session_state.checkbox_state[idx][1] = True
            st.session_state.checkbox_state[idx][0] = False
            st.session_state.answers[idx] = cv_dict["否"]

# 提交按钮
if st.button('提交'):
    if -1 in st.session_state.answers:
        st.write("请回答所有问题")
    else:
        probabilities = calculate_probabilities(st.session_state.answers)
        sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

        st.write("下面是你每种人格可能性的概率:")

        for personality, probability in sorted_probabilities:
            st.write(f"{personality}: {probability:.2%}")

        top3 = sorted_probabilities[:3]
        st.write("最大可能前三种人格的分析")
        for personality, _ in top3:
            st.write(f"### {personalities['personalities'][personality]['name']}")
            st.write(personalities['personalities'][personality]['description'])
