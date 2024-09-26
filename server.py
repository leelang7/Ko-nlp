from flask import Flask, request, jsonify
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__)

# 한국어 모델 로드 - KoGPT2
MODEL_NAME = 'kykim/gpt3-kor-small_based_on_gpt2'

# 모델과 토크나이저 초기화
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

pipe = pipeline(
    'text-generation',
    model=model,
    tokenizer=tokenizer,
    device=-1,  # CPU 사용
    pad_token_id=tokenizer.pad_token_id  # 신경 쓰이거나 필요 시 설정
)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    context = data.get('context', '')

    try:
        prompt = (f"질문: {question}\n맥락: {context}\n답변:" if context else f"질문: {question}\n답변:")
        answer = pipe(
            prompt,
            max_new_tokens=100,  # 생성 텍스트 길이 제한
            return_full_text=False,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            repetition_penalty=1.2 # 반복을 줄이기 위한 페널티
        )
        response = answer[0]['generated_text']
    except Exception as e:
        response = f"Error: {str(e)}"

    return jsonify({'answer': response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
