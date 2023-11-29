from flask import Flask, render_template, request, jsonify
import vertexai
from vertexai.language_models import ChatModel
import os

app = Flask(__name__)
PROJECT_ID = os.environ.get('GCP_PROJECT') #Your Google Cloud Project ID
LOCATION = os.environ.get('GCP_REGION')   #Your Google Cloud Project Region
vertexai.init(project=PROJECT_ID, location=LOCATION)

def create_session():
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    chat = chat_model.start_chat()
#    chat = chat_model.start_chat(
#        context="My name is Miles. You are an astronomer, knowledgeable about the solar system.",
#        examples=[
#            InputOutputTextPair(
#                input_text="How many moons does Mars have?",
#                output_text="The planet Mars has two moons, Phobos and Deimos.",
#            ),
#        ],
#    )
    return chat

def response(chat, message):
    # you can override these parameters as needed
    parameters = {
        "temperature": 0.2,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    result = chat.send_message(message, **parameters)
    return result.text

# this is what the Flask app serves on "/"
@app.route('/')
def index():
    ###
    return render_template('index.html')

@app.route('/palm2', methods=['GET', 'POST'])
def vertex_palm():
    # user_input is the message we are sending to the chat bot
    user_input = ""
    if request.method == 'GET':
        user_input = request.args.get('user_input')
    else:
        user_input = request.form['user_input']

    chat_model = create_session()
    content = response(chat_model, user_input)
    return jsonify(content=content)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
