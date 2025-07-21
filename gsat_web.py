import streamlit as st
import random
from fractions import Fraction

st.set_page_config(page_title="GSAT 비타민", layout="wide")

# 문제 생성 함수들
def subtraction_problem():
    a = random.randint(1000, 50000)
    b = random.randint(100, a - 1)
    return f"{a} - {b}", str(a - b)

def percent_problem():
    a = random.randint(100, 100000)
    b = random.randint(1, 100)
    return f"{a}의 {b}%는?", str(round(a * b / 100, 2))

def fraction_compare_problem():
    num1, den1 = random.randint(10, 500), random.randint(50, 1000)
    num2 = random.randint(10, 500)
    den2 = random.randint(50, 1000)
    f1 = Fraction(num1, den1)
    f2 = Fraction(num2, den2)
    question = f"\\frac{{{num1}}}{{{den1}}} \\; \\boxed{{▢}} \\; \\frac{{{num2}}}{{{den2}}}"
    answer = ">" if f1 > f2 else "<" if f1 < f2 else "="
    return question, answer

def multiplication_compare_problem():
    a1 = round(random.uniform(10, 500), 1)
    b1 = random.randint(100, 2000)
    a2 = round(random.uniform(10, 500), 1)
    b2 = random.randint(100, 2000)
    r1 = a1 * b1
    r2 = a2 * b2
    q = f"{a1} × {b1} ▢ {a2} × {b2}"
    a = ">" if r1 > r2 else "<" if r1 < r2 else "="
    return q, a

def estimate_problem():
    a = random.randint(10000, 99999)
    p = round(random.uniform(30, 90), 2)
    return f"{a}의 약 {p}%는?", str(round(a * p / 100, -2))

def generate_all_problems():
    problems = {}
    for i in range(9):
        problems[f"sub_{i}"] = subtraction_problem()
        problems[f"percent_{i}"] = percent_problem()
    for i in range(6):
        problems[f"fraction_{i}"] = fraction_compare_problem()
    for i in range(5):
        problems[f"mult_{i}"] = multiplication_compare_problem()
    for i in range(1):
        problems[f"estimate_{i}"] = estimate_problem()
    return problems

# 초기 상태
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "problems" not in st.session_state:
    st.session_state.problems = generate_all_problems()
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {}

# 화면 출력
if not st.session_state.submitted:
    st.title("🧮 GSAT 비타민")
    left_col, right_col = st.columns(2)

    with left_col:
        st.header("🟦 뺄셈 문제")
        for i in range(9):
            key = f"sub_{i}"
            q, a = st.session_state.problems[key]
            st.session_state.user_inputs[key] = st.text_input(f"[{i+1}] {q}", key=key)

        st.header("🟩 퍼센트 계산")
        for i in range(9):
            key = f"percent_{i}"
            q, a = st.session_state.problems[key]
            st.session_state.user_inputs[key] = st.text_input(f"[{i+1}] {q}", key=key)

    with right_col:
        st.header("🟧 분수 비교")
        for i in range(6):
            key = f"fraction_{i}"
            q, a = st.session_state.problems[key]
            st.latex(q)
            st.session_state.user_inputs[key] = st.text_input(f"[{i+1}] 대소 비교", key=key)

        st.header("🟥 곱셈 비교")
        for i in range(5):
            key = f"mult_{i}"
            q, a = st.session_state.problems[key]
            st.session_state.user_inputs[key] = st.text_input(f"[{i+1}] {q}", key=key)

        st.header("🟨 근사값 계산")
        for i in range(1):
            key = f"estimate_{i}"
            q, a = st.session_state.problems[key]
            st.session_state.user_inputs[key] = st.text_input(f"[{i+1}] {q}", key=key)

    if st.button("📤 제출하기"):
        st.session_state.submitted = True
        st.rerun()

else:
    st.title("📊 채점 결과")
    correct = 0
    total = len(st.session_state.problems)

    for key, (q, answer) in st.session_state.problems.items():
        user = st.session_state.user_inputs.get(key, "").strip()
        is_correct = user == answer
        bg_color = "#d4f4d2" if is_correct else "#ffd6d6"
        icon = "✅" if is_correct else "❌"
        label = f"{icon} {key}"

        # 렌더링
        st.markdown(f"""
            <div style="margin-bottom:6px;"><b>{label}</b><br>{q}</div>
            <input type="text" value="{user}" disabled
                style="background-color:{bg_color}; padding:8px; border:1px solid #ccc; width:100%; font-size:16px;">
            {f'<div style="color:#d00; margin-top:6px;">정답: {answer}</div>' if not is_correct else ''}
            <hr style="margin-top:12px; margin-bottom:12px;">
        """, unsafe_allow_html=True)

        if is_correct:
            correct += 1

    st.info(f"🎯 총 정답: {correct} / {total} ({round(correct/total*100, 1)}%)")

    if st.button("🔄 다시 풀기"):
        st.session_state.submitted = False
        st.session_state.problems = generate_all_problems()
        st.session_state.user_inputs = {}
        st.rerun()
