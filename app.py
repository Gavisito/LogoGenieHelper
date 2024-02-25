
import requests
from flask import Flask, render_template, jsonify, request
app = Flask(__name__, template_folder='templates', static_folder='static')

# Load API key from environment variable or configuration file
import openai
from openai_config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route('/contact')
def contact():
    return render_template('contact.html' )

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route("/generate_image", methods=['POST'])
def generate_image():
    try:
        prompt = request.form.get("CompanyName")
        tagline = request.form.get("tagline")
        style = request.form.get("style")
        companycolor = request.form.get("company-color")
        companyvalues = request.form.get("company-values")
        industry = request.form.get("industry-genre")

        if not prompt:
            return jsonify({"error": "Company Name is required."}), 400

        if style not in {"Minimalist", "Vintage", "Contemporary", "Realistic"}:
            return jsonify({"error": "Invalid style."}), 400

        # Construct prompt for DALL-E
        prompt += f" {tagline} {companycolor} {companyvalues} {style} {industry} "

        # Make API request to DALL-E
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1,
        )

        # Extract generated image URL from response
        image_url = response.get('data', [])[0].get('url')

        # Return the image URL as JSON response
        return jsonify({"image_url": image_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
