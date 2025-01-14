# Support Agent Chatbot

This application allows users to enter queries related to specific documentation (mParticle, Lytics, Segment, Zeotap). It uses web scraping and NLP/LLM models to provide summarized answers to the user's queries.

## How It Works

1. **User Input:** The user enters a query in the web interface.
2. **Keyword Validation:** The application checks if the query contains any valid keywords.
3. **Web Search and Scraping:** If the query is valid, the application uses SerpAPI to search the web and scrapes content from the top results using BeautifulSoup.
4. **Summarization:** The scraped content is concatenated with the conversation history and passed to the NLP/LLM summarization model to generate a descriptive answer.
5. **Response:** The summarized answer is displayed to the user.

## Example Queries

- "Tell me about mParticle"
- "What is Segment used for?"
- "Explain Zeotap"
  
## Tech Stack

- **Flask**: A lightweight WSGI web application framework in Python.
- **BeautifulSoup**: A library for parsing HTML and XML documents.
- **SerpAPI**: A real-time API to access search engine results.
- **Google Gemini API**: A library for state-of-the-art LLM models.
- **Requests**: A simple HTTP library for Python.

## Project Structure
├── requirements.txt <br>
├── app.py <br>
├── LICENSE <br>
├── scraper.py <br>
├── templates/ <br>
│ └── index.html <br>


- `app.py`: The main Flask application that handles web requests, processes user queries, and returns summarized content.
- `scraper.py`: Contains functions to search using SerpAPI and scrape content from web pages.
- `templates/index.html`: The HTML template for the web application's user interface.
- `LICENSE`: The Apache License 2.0 under which this project is licensed.

## Installation
Clone the repository:
```bash
git clone https://github.com/itsrealkarthik/Support-Agent-Chatbot.git
cd Support-Agent-Chatbot
```
Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```
## Get API keys
Go to [Serp API](https://serpapi.com/), log in, and obtain your API key.

Go to [Gemini API](https://ai.google.dev/gemini-api/docs/api-key), log in, and obtain your API key.

Set up your API keys:

- Create an `.env` file and place your `SERP_API` and `GEMINI_API` in the file.

## Usage
Run the Flask application:

```bash
python app.py
```
- Open your web browser and navigate to http://127.0.0.1:5000/.
- Enter your query in the input field and submit. The application will search the web, scrape content from the top results, and provide a summarized answer.


## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [SerpAPI](https://serpapi.com/)
- [Google Gemini](https://ai.google.dev/gemini-api/docs/api-key)
- [Requests](https://docs.python-requests.org/en/master/)

