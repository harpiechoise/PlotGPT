from src.templates import fake_db_lookup, code_inyection, execute_code
from flask import Flask, request, jsonify
from langchain.llms import OpenAI
import os
from pathlib import Path
app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"hello": "World"})

llm = OpenAI(openai_api_key=os.environ["OPENAI"], temperature=.1)
# Parse the text query and return the code and analysis
@app.route("/generate_code", methods=["GET"])
def generate_code():
    query: str = request.args.get("query")
    if query is None:
        return jsonify({"error": "No query provided"})

    print("Processing")
    code, analysis = fake_db_lookup(query=query, llm=llm)
    file_path, plot_image_path, generated_code = code_inyection("/home/yo/code.py", "db.csv", code, analysis)
    execute_code(file_path)
    p = Path(plot_image_path).absolute() if plot_image_path else "Not Provided"
    
    response = {
        "code": generated_code,
        "plot": str(p)
    }
    print(response)
    

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
# code, analysis = fake_db_lookup(query="Can you plot the Sex variable in a bar plot and replace the X axis labels for 'Man' and 'Women' respectibly. And the X and Y labels can you rotate un 45 degrees, please", llm=llm)
# file_path = code_inyection("db.csv",code, analysis)

# execute_code(file_path)
