from dotenv import load_dotenv
import os
load_dotenv()

from flask import Flask, request, jsonify

from langchain_core.messages import HumanMessage, AIMessage
from functions import get_response, create_agent

app = Flask(__name__)
agent = create_agent()

@app.route('/', methods=['GET'])
def home():
  url = request.base_url
  return f'the page url is:  {url}'

@app.route('/chat', methods=['POST'])
def chat():
  data = request.json  # request stores the data posted through API (i.e. thread_id and message)
  history = data.get('history', "")  #figure out the way to send a list of messages over API
  user_query = data.get('message', "")

  response = get_response(agent, user_query, history)

  return jsonify({"response": response})

if __name__ == '__main__':
  app.run(port=os.getenv("PORT", default=5000)) #port variable is given by railway
