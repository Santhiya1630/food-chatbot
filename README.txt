FOODIEBOT - GEMINI + FLASK CHATBOT

1. Open the project folder in VS Code.
2. Install dependencies:
   pip install -r requirements.txt

3. Open .env and replace:
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
   with your actual Gemini API key.

4. Run:
   python app.py

5. Open the browser:
   http://127.0.0.1:5000

Project files:
- app.py          -> Flask backend
- config.py       -> Food chatbot rules / system prompt
- templates/index.html -> Frontend (HTML + CSS + JavaScript)
- requirements.txt -> Required Python packages
- .env            -> Gemini API key
