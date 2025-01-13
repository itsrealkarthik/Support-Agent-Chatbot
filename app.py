from flask import Flask, render_template, request
from scraper import search_and_scrape
from transformers import pipeline

app = Flask(__name__)

# Initialize the NLP model for summarization
summarization_model = pipeline("summarization", model="t5-small")

# Keywords for validation
valid_keywords = ["mparticle", "lytics", "segment", "zeotap"]

# To store conversation history (user input + bot response)
conversation_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    global conversation_history
    answer = None
    
    if request.method == "POST":
        query = request.form["query"]
        
        # Add user's query to conversation history
        conversation_history.append(f"User: {query}")
        
        # Check if the query contains valid keywords
        if any(keyword.lower() in query.lower() for keyword in valid_keywords):
            # Search using SerpAPI and scrape content from first 10 webpages
            scraped_data = search_and_scrape(query)
            print(scraped_data)
            
            if scraped_data:
                # Concatenate conversation history and scraped content for context
                context = " ".join(conversation_history) + " " + " ".join(scraped_data)
                
                # Use Summarization model to generate a descriptive answer based on the context
                summarized_answer = summarization_model(context, min_length=50, max_length=300)
                
                # Get the first summarized answer (in case the model returns a list)
                answer = summarized_answer[0]['summary_text']
                
                # Store bot's response in the conversation history
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
