import requests
import json

def ask_question(question, context=''):
    url = "http://localhost:5000/ask"  # Flask 서버 URL
    headers = {"Content-Type": "application/json"}
    data = {
        "question": question,
        "context": context
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 오류 발생 시 예외 발생
        answer = response.json().get('answer', '답변을 받을 수 없습니다.')
        print(f"질문: {question}")
        print(f"답변: {answer}")
    except requests.exceptions.RequestException as e:
        print(f"요청 실패: {e}")

# 사용 예제
ask_question("모델이란?")
