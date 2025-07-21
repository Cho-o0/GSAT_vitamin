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
    num1 = random.randint(10, 500)
    den1 = random.randint(50, 1000)
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

# 문제 전체 생성
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

# 초기 상태 설정
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "problems" not in st.session_state:
    st.session_state.problems = generate_all_problems()
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {}

st.title("🧮 GSAT 비타민")
left_col, right_col = st.columns(2)

# 채점 카운트
correct_count = 0

# 입력/채점 렌더링 함수
def render_problem(key, q_text, answer, label):
    user_input = st.session_state.user_inputs.get(key, "").strip()

    if not st.session_state.submitted:
        st.session_state.user_inputs[key] = st.text_input(f"[{label}] {q_text}", key=key)
    else:
        is_correct = user_input == answer
        bg_color = "#d4f4d2" if is_correct else "#ffd6d6"
        icon = "✅" if is_correct else "❌"

        st.markdown(f"""
            <div style="margin-bottom:4px;"><b>{icon} [{label}] {q_text}</b></div>
            <input type="text" value="{user_input}" disabled
                style="background-color:{bg_color}; padding:8px; border:1px solid #ccc; width:100%; font-size:16px;">
            {f'<div style="color:#d00; margin-top:4px;">정답: {answer}</div>' if not is_correct else ''}
            <hr style="margin-top:10px;">
        """, unsafe_allow_html=True)

        return 1 if is_correct else 0
    return 0

# 왼쪽 영역
with left_col:
    st.header("🟦 뺄셈 문제")
    for i in range(9):
        key = f"sub_{i}"
        q, a = st.session_state.problems[key]
        correct_count += render_problem(key, q, a, i+1)

    st.header("🟩 퍼센트 계산")
    for i in range(9):
        key = f"percent_{i}"
        q, a = st.session_state.problems[key]
        correct_count += render_problem(key, q, a, i+1)

# 오른쪽 영역
with right_col:
    st.header("🟧 분수 비교")
    for i in range(6):
        key = f"fraction_{i}"
        q, a = st.session_state.problems[key]
        st.latex(q)
        correct_count += render_problem(key, "대소 비교", a, i+1)

    st.header("🟥 곱셈 비교")
    for i in range(5):
        key = f"mult_{i}"
        q, a = st.session_state.problems[key]
        correct_count += render_problem(key, q, a, i+1)

    st.header("🟨 근사값 계산")
    for i in range(1):
        key = f"estimate_{i}"
        q, a = st.session_state.problems[key]
        correct_count += render_problem(key, q, a, i+1)

# 제출 또는 결과 요약
if not st.session_state.submitted:
    if st.button("📤 제출하기"):
        st.session_state.submitted = True
        st.rerun()
else:
    total = len(st.session_state.problems)
    st.markdown(f"""
    <div style="background-color:#f0f8ff; padding:12px; border-radius:6px; border:1px solid #ccc;">
        <b>🎯 총 정답: {correct_count} / {total} ({round(correct_count/total*100, 1)}%)</b>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 다시 풀기"):
        st.session_state.submitted = False
        st.session_state.problems = generate_all_problems()
        st.session_state.user_inputs = {}
        st.rerun()
