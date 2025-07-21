import streamlit as st
import random
from fractions import Fraction

st.set_page_config(page_title="GSAT 계산 연습", layout="wide")

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
    num2, den2 = random.randint(10, 500), random.randint(50, 1000)
    f1, f2 = Fraction(num1, den1), Fraction(num2, den2)
    question = f"\\frac{{{num1}}}{{{den1}}} \\; \\boxed{{▢}} \\; \\frac{{{num2}}}{{{den2}}}"
    answer = ">" if f1 > f2 else "<" if f1 < f2 else "="
    return question, answer

def multiplication_compare_problem():
    a1, b1 = round(random.uniform(10, 500), 1), random.randint(100, 2000)
    a2, b2 = round(random.uniform(10, 500), 1), random.randint(100, 2000)
    r1, r2 = a1 * b1, a2 * b2
    q = f"{a1} × {b1} ▢ {a2} × {b2}"
    a = ">" if r1 > r2 else "<" if r1 < r2 else "="
    return q, a

def estimate_problem():
    a = random.randint(10000, 99999)
    p = round(random.uniform(30, 90), 2)
    return f"{a}의 약 {p}%는?", str(round(a * p / 100, -2))

# 문제 생성 묶음 함수
def generate_all_problems():
    problems = {}
    for i in range(10):
        problems[f"sub_{i}"] = subtraction_problem()
        problems[f"percent_{i}"] = percent_problem()
        problems[f"fraction_{i}"] = fraction_compare_problem()
        problems[f"mult_{i}"] = multiplication_compare_problem()
        problems[f"estimate_{i}"] = estimate_problem()
    return problems

# 초기화 및 문제 로딩
if "problems" not in st.session_state or st.button("🔄 다시 풀기"):
    st.session_state.problems = generate_all_problems()
    st.session_state.user_inputs = {}

# 좌우 컬럼 구성
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

# 제출 버튼
if st.button("📤 제출하기"):
    st.subheader("📊 채점 결과")
    correct = 0
    total = len(st.session_state.problems)

    for key, (q, answer) in st.session_state.problems.items():
        user = st.session_state.user_inputs.get(key, "").strip()
        if user == answer:
            st.success(f"[{key}] ✅ 정답")
            correct += 1
        else:
            st.error(f"[{key}] ❌ 오답 | 정답: {answer}")
    st.info(f"🎯 총 정답: {correct} / {total} ({round(correct/total*100, 1)}%)")
