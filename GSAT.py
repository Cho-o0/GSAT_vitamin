# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 16:13:01 2025

@author: URCho
"""

from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 문제 생성 함수 예시 (덧셈)
def generate_problem():
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    question = f"{a} + {b} = ?"
    answer = a + b
    return question, answer

@app.route('/')
def index():
    question, _ = generate_problem()
    return render_template('index.html', question=question)

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    user_answer = int(data['answer'])
    question = data['question']
    # question에서 a,b 추출 (간단한 예시)
    parts = question.split(' ')
    a = int(parts[0])
    b = int(parts[2])
    correct_answer = a + b
    is_correct = (user_answer == correct_answer)
    return jsonify({'correct': is_correct, 'correct_answer': correct_answer})

if __name__ == '__main__':
    app.run(debug=True)
