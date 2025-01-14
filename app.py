from flask import Flask, render_template, request
from scraper import search_and_scrape
import google.generativeai as genai
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API'))
model = genai.GenerativeModel('gemini-pro')

valid_keywords = ["mparticle", "lytics", "segment", "zeotap"]
conversation_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    global conversation_history
    answer = None
    
    if request.method == "POST":
        query = request.form["query"]
        
        conversation_history.append(f"User: {query}")
        
        if any(keyword.lower() in query.lower() for keyword in valid_keywords):
            scraped_data = search_and_scrape(query)
            
            if scraped_data:
                try:
                    prompt = f"""
                    You are an expert in providing precise and contextually relevant answers to queries related to Segment, mParticle, Zeotap, and Lytics. Based on the provided query and scraped data:

                    1. If the query is directly relevant to Segment, mParticle, Zeotap, or Lytics, analyze the scraped data to generate a comprehensive and accurate answer in **neatly formatted HTML** that is ready to render.

                    2. If the query is not relevant to these topics, return the error message: **"Please ask related questions only."**

                    Format the response strictly in HTML. Do not include unnecessary or irrelevant details. Use proper HTML tags for structure (e.g., `<html>`, `<body>`, `<h1>`, `<p>`). 

                    Inputs:
                    - User Query: {query}
                    - Scraped Data: {scraped_data}
                    - Previous Conversation Context (last 5): {conversation_history}

                    Output:
                    - A neatly formatted HTML response.

                    """
                    
                    response = model.generate_content(prompt)
                    
                    answer = response.text
                    answer = answer.replace("```html", "").replace("```", "").strip()

                    conversation_history.append(f"Bot: {answer}")
                except Exception as e:
                    answer = f"An error occurred while processing your request: {str(e)}"
                    conversation_history.append(f"Bot: {answer}")
            else:
                answer = "Sorry, no relevant content found."
                conversation_history.append(f"Bot: {answer}")
        else:
            answer = "Please ask related questions only."
            conversation_history.append(f"Bot: {answer}")
    
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)