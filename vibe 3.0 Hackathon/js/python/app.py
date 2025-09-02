from flask import Flask, request, jsonify, send_from_directory
import os
import openai
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder='../frontend', static_url_path='')

# OpenAI key
openai.api_key = os.getenv('OPENAI_API_KEY')

# MySQL connection helper
def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST','localhost'),
        user=os.getenv('DB_USER','root'),
        password=os.getenv('DB_PASS',''),
        database=os.getenv('DB_NAME','my_project')
    )

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Simple AI tutor endpoint
@app.route('/api/ai/learn', methods=['POST'])
def ai_learn():
    data = request.json or {}
    prompt = data.get('prompt','')
    if not prompt:
        return jsonify({'error':'no prompt'}), 400

    # build prompt for OpenAI
    system = "You are a friendly tutor. Explain simply and give a short example."
    try:
        res = openai.ChatCompletion.create(
            model=os.getenv('OPENAI_MODEL','gpt-4o-mini'),
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            max_tokens=400
        )
        answer = res['choices'][0]['message']['content'].strip()
    except Exception as e:
        answer = f"AI error: {str(e)}"

    # optionally save to DB (omitted for brevity)
    return jsonify({'answer':answer})

# Recipe recommender endpoint
@app.route('/api/ai/recipes', methods=['POST'])
def ai_recipes():
    data = request.json or {}
    ingredients = data.get('ingredients','')
    if not ingredients:
        return jsonify({'error':'no ingredients'}),400

    prompt = f"You are a helpful cook. Suggest 3 simple affordable recipes using these ingredients: {ingredients}. For each recipe give a short title and 3-5 line instructions."
    try:
        res = openai.ChatCompletion.create(
            model=os.getenv('OPENAI_MODEL','gpt-4o-mini'),
            messages=[{"role":"user","content":prompt}],
            max_tokens=500
        )
        text = res['choices'][0]['message']['content'].strip()
    except Exception as e:
        return jsonify({'error':str(e)}),500

    # Very small parser to split into recipes by blank lines or numbering
    recipes = []
    parts = [p.strip() for p in text.split('\n\n') if p.strip()]
    for p in parts[:6]:
        # naive: first line title, rest instructions
        lines = p.split('\n')
        title = lines[0][:80]
        instr = ' '.join(lines[1:]).strip()
        recipes.append({'title':title,'instructions':instr})

    # Save to DB (example)
    try:
        db = get_db()
        cur = db.cursor()
        for r in recipes:
            cur.execute("INSERT INTO recipes (title,instructions,ingredients) VALUES (%s,%s,%s)", (r['title'], r['instructions'], ingredients))
        db.commit(); cur.close(); db.close()
    except Exception:
        pass

    return jsonify({'recipes':recipes})

# Wellbeing tip
@app.route('/api/ai/wellbeing', methods=['POST'])
def ai_well():
    prompt = "Provide one short, practical wellbeing tip for a student (<=40 words)."
    try:
        res = openai.ChatCompletion.create(
            model=os.getenv('OPENAI_MODEL','gpt-4o-mini'),
            messages=[{"role":"user","content":prompt}],
            max_tokens=80
        )
        tip = res['choices'][0]['message']['content'].strip()
    except Exception as e:
        tip = f"AI error: {str(e)}"
    return jsonify({'tip':tip})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

