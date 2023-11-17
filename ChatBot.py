import json
from difflib import get_close_matches
from typing import Union

def load_knowledge_base(file_path: str) -> dict:
 with open(file_path, 'r') as file:
  data: dict = json.load(file)
 return data

def save_knowledge_base(file_path: str, data: dict):
 with open(file_path, 'w') as file:
  json.dump(data, file, indent=2)

def load_ibanned_word(file_path: str) -> list[str]:
 with open(file_path, 'r') as file:
  data: dict = json.load(file)
 return data["word"]

def find_best_match(user_question: str, questions: list[str]) -> Union[str, None]:
 ibanned_words = load_ibanned_word('ibanned_word.json')
 for word in ibanned_words:
  if word.lower() in user_question.lower():
      return None
 matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
 return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> Union[str, None]:
 for q in knowledge_base["question"]:
  if q["question"] == question:
      return q["answer"]


knowledge_base = load_knowledge_base('knowledge_base.json')
def send_message(user_input: str):
    global knowledge_base
    ibanned_words = load_ibanned_word('ibanned_word.json')
    for word in ibanned_words:
        if word.lower() in user_input.lower():
            return {"response": "Esta pregunta contiene una palabra prohibida. No puedo responder."}
    
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["question"]])
    
    

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        
        return {"response": "Bot: " + answer}
    else:

        knowledge_base = load_knowledge_base('knowledge_base.json')
        return {"response": "Bot: No sé la respuesta. ¿Puedes enseñármela?"}



knowledge_base: dict = load_knowledge_base('D:\IA\knowledge_base.json')
ibanned_words: list[str] = load_ibanned_word('ibanned_word.json')


