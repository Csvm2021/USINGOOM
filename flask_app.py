""" from difflib import get_close_matches
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from ChatBot import get_answer_for_question, load_ibanned_word, load_knowledge_base

app = FastAPI()

knowledge_base = load_knowledge_base('knowledge_base.json')

class Item(BaseModel):
 userText: str

@app.post("/get")
async def get_bot_response(item: Item):
 userText = item.userText
 ibanned_words = load_ibanned_word('ibanned_word.json')
 for word in ibanned_words:
    if word.lower() in userText.lower():
        return {"response": "Esta pregunta contiene una palabra prohibida. No puedo responder."}
 matches = get_close_matches(userText, [q["question"] for q in knowledge_base["question"]], n=1, cutoff=0.6)
 if matches:
    answer = get_answer_for_question(matches[0], knowledge_base)
    return {"response": answer}
 else:
    return {"response": "No sé la respuesta. ¿Puedes enseñármela?"}
 """
from flask import Flask, redirect, render_template, request, jsonify, url_for
from ChatBot import load_knowledge_base, save_knowledge_base, send_message

app = Flask(__name__)

app.secret_key = 'your secret key'

knowledge_base = load_knowledge_base('knowledge_base.json')

from flask import session

@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
      user_input = request.form.get('user_input')
      response = send_message(user_input)
      session['conversation'] = session.get('conversation', []) + [{'user': user_input, 'bot': response['response']}]
      return render_template('index.html', conversation=session['conversation'])
  return render_template('index.html')

knowledge_base = load_knowledge_base('knowledge_base.json')

@app.route('/ensenar', methods=['POST'])
def ensenar():
    global knowledge_base
    nueva_pregunta = request.form.get('nueva_pregunta')
    nueva_respuesta = request.form.get('nueva_respuesta')

    # Cargar la base de conocimientos existente
    knowledge_base = load_knowledge_base('knowledge_base.json')

    # Verificar si la pregunta ya existe en la base de conocimientos
    for item in knowledge_base['question']:
        if item['question'].lower() == nueva_pregunta.lower():
            return "La pregunta ya existe en la base de conocimientos"

    # Si la pregunta no existe, agregarla con la nueva respuesta
    knowledge_base['question'].append({
        'question': nueva_pregunta,
        'answer': nueva_respuesta
    })

    # Guardar la base de conocimientos actualizada
    save_knowledge_base('knowledge_base.json', knowledge_base)
    knowledge_base = load_knowledge_base('knowledge_base.json')

    return redirect(url_for('home'))  # Redirige de vuelta a la página principal después de enseñar al bot



if __name__ == '__main__':
   app.run(debug=True)



