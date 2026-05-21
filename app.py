import os
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from google import genai
from dotenv import load_dotenv

load_dotenv()


client = genai.Client(api_key=os.getenv('GEMINI_API_KEY')) #this is our api client we can use this to create the chat
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
history = list()
@app.route("/chat", methods=['POST'])
@cross_origin()
def message():
    data = request.get_json()
    prompt = data.get("message")
    prompt = " ".join(prompt.split())
    history.append(("user:", prompt))
    if(prompt == ""):
        return {
            "error":"invalid prompt"
        }
    if(prompt.split()[0] == "caliculate"):
        a = prompt.split()[1]
        b = prompt.split()[3]
        operation = prompt.split()[2]
        response = caliculate(a, b, operation)
        history.append(("ai:", response))
        return {
        "response":response, 
        "history":history
    }
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=history
)

    history.append(("ai:", response.text))
    return {
        "response":response.text, 
        "history":history
    }

def caliculate(a, b, operation):
    if a == None or b == None:
        return "Invalid inputs please check the values you have entered"
    if operation == "+":
        return str(int(a)+int(b))
    elif operation == "-":
        return str(int(a)-int(b))
    elif operation == "/":
        if b == "0":
            return "denominator cannot be zero"
        else:
            return str(int(a)/int(b))
    elif operation == "*":
        return str(int(a)*int(b))
    else:
        return "operation cannot be performed at the moment you can try adding, subtracting, multiplication, division"

if __name__ == "__main__":
    app.run(debug=True, port=8000)