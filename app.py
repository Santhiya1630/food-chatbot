from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

from config import SYSTEM_PROMPT

# Load .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Get Gemini API key from .env
api_key = os.getenv("GEMINI_API_KEY") 

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured in .env file")

print("Using Gemini API key:", api_key[:10])
# Create Gemini client
client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.6-flash"


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# NORMAL TEXT CHAT
# =========================
@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "reply": "Please enter a food-related question."
            })

        prompt = f"""
{SYSTEM_PROMPT}

User Question:
{user_message}

Answer the user according to the FoodieBot rules.
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:

        print("Text Chat Error:", e)

        return jsonify({
            "reply": "Sorry, something went wrong. Please try again."
        }), 500


# =========================
# FOOD IMAGE ANALYSIS
# =========================
@app.route("/analyze-image", methods=["POST"])
def analyze_image():

    try:

        # Check whether image exists
        if "image" not in request.files:
            return jsonify({
                "reply": "Please upload a food image."
            }), 400

        image_file = request.files["image"]

        if image_file.filename == "":
            return jsonify({
                "reply": "Please select an image."
            }), 400

        # Read image bytes
        image_bytes = image_file.read()

        # Detect MIME type
        mime_type = image_file.mimetype or "image/jpeg"

        # Food analysis instruction
        image_prompt = f"""
{SYSTEM_PROMPT}

You are now analyzing a food image.

Analyze the uploaded food image and provide ALL of the following
13 details:

1. Food Name
2. Cuisine
3. Main Ingredients
4. Preparation Method
5. Taste Profile
6. Nutritional Information
7. Vegetarian / Non-Vegetarian status
8. Common Allergens
9. Serving Suggestions
10. Similar Dishes
11. Origin / Regional Information
12. General Health Considerations
13. Confidence Level

IMPORTANT RULES:

- Carefully analyze the image before answering.
- Clearly separate what is visible from what is inferred.
- Do not claim that an ingredient is definitely present if it cannot
  actually be determined from the image.
- For nutrition, give an approximate estimate only when reasonable.
- Nutrition can vary depending on recipe and portion size.
- If the exact food cannot be identified, say so clearly and provide
  the most likely possibilities.
- If the image quality is poor or the food is not visible, explain that.
- Do not invent information.
- Use simple language that a normal user can understand.
- Give all 13 sections even if some information is uncertain.

Use this format:

🍽️ Food Name:
🌎 Cuisine:
🥕 Main Ingredients:
👨‍🍳 Preparation Method:
😋 Taste Profile:
🥗 Nutritional Information:
🌱 Vegetarian / Non-Vegetarian:
⚠️ Common Allergens:
🍴 Serving Suggestions:
🍲 Similar Dishes:
📍 Origin / Regional Information:
❤️ General Health Considerations:
🎯 Confidence Level:
"""

        # Send image + prompt to Gemini
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                image_prompt,
                {
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": image_bytes
                    }
                }
            ]
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:

        print("Image Analysis Error:", e)

        return jsonify({
            "reply": "Sorry, I couldn't analyze this food image. Please try another image."
        }), 500


# =========================
# START FLASK
# =========================
if __name__ == "__main__":
    app.run(debug=True)