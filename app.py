from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load a pre-trained AI model for text classification / toxicity detection
# Yeh model khud text ko analyze karega bina kisi fixed word list ke
print("Loading AI Model... Please wait...")
ai_classifier = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)
print("AI Model Loaded Successfully!")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    comment = data.get('text', '')
    
    if not comment.strip():
        return jsonify({
            'category': 'Safe',
            'severity': 'Low',
            'explanation': 'Empty comment.',
            'rewrite': 'N/A'
        })

    try:
        # AI Model prediction
        predictions = ai_classifier(comment)
        
        # 'unitary/toxic-bert' returns scores for labels like 'toxic', 'severe_toxic', etc.
        # Let's check if the top toxic score is high (> 0.5)
        is_toxic = False
        toxic_score = 0.0
        
        for item in predictions[0]:
            if item['label'] in ['toxic', 'severe_toxic', 'insult', 'obscene'] and item['score'] > 0.5:
                is_toxic = True
                toxic_score = item['score']
                break
        
        if is_toxic:
            category = "Harassment / Hate Speech (AI Detected)"
            severity = "High" if toxic_score > 0.8 else "Medium"
            explanation = f"AI Model detected toxicity with a confidence score of {round(toxic_score * 100, 2)}%."
            rewrite = "Kripya sanyam banaye rakhein aur respectful bhasha ka prayog karein."
        else:
            category = "Safe"
            severity = "Low"
            explanation = "AI Model analyzed the context and found no toxic or harmful content."
            rewrite = "N/A (Comment is already polite)"

    except Exception as e:
        # Fallback agar internet ya model load hone mein koi issue ho
        category = "Safe"
        severity = "Low"
        explanation = f"Analyzed via AI pipeline (Error fallback: {str(e)})"
        rewrite = "N/A"

    return jsonify({
        'category': category,
        'severity': severity,
        'explanation': explanation,
        'rewrite': rewrite
    })

if __name__ == '__main__':
    app.run(debug=True)