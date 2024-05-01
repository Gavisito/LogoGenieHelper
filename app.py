import requests, os, datetime, pathlib, random
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, abort
from google.cloud import storage
from google.oauth2 import service_account
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from functools import wraps

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "SuperSuperSecret"

# Configure Bucket Info
BUCKET_NAME = 'test-123q'
key_path = 'lateral-imagery-415421-1823d261a821.json'
credentials = service_account.Credentials.from_service_account_file(key_path)

#Configure OAuth credentials
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Just for development, remove for production
GOOGLE_CLIENT_ID = "564696877407-elvqrch3fguo4f6p2tprf7oq5priit4n.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://lateral-imagery-415421.uk.r.appspot.com/callback"
)

# Load API key from environment variable or configuration file
import openai
from openai_config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

def list_images():
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()
    return [blob.name for blob in blobs]

def generate_signed_url(blob_name):
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(version="v4", expiration=datetime.timedelta(minutes=15), method="GET")
    return url

def login_is_required(function):  #check here
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return redirect("/index")  # Redirect to login page if user is not logged in
        else:
            return function(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    if "google_id" not in session:
        user = ""
        data = "login"
        buttonText = "Login to Google"
    else:
        user = f"{session['name']}!"
        data = "logout"
        buttonText = "Logout"
    return render_template("index.html", user=user, data=data, buttonText=buttonText)

@app.route("/about")
def about():
    if "google_id" not in session:
        user = ""
        data = "login"
        buttonText = "Login to Google"
    else:
        user = f"{session['name']}!"
        data = "logout"
        buttonText = "Logout"
    return render_template("about.html", user=user, data=data, buttonText=buttonText)

@app.route('/contact')
def contact():
    if "google_id" not in session:
        user = ""
        data = "login"
        buttonText = "Login to Google"
    else:
        user = f"{session['name']}!"
        data = "logout"
        buttonText = "Logout"
    return render_template("contact.html", user=user, data=data, buttonText=buttonText)

@app.route("/gallery")
def gallery():
    image_urls = [generate_signed_url(name) for name in list_images()]
    if "google_id" not in session:
        user = ""
        data = "login"
        buttonText = "Login to Google"
    else:
        user = f"{session['name']}!"
        data = "logout"
        buttonText = "Logout"

    user_id = session["google_id"]
    return render_template("gallery.html", image_urls=image_urls, user=user, data=data, buttonText=buttonText, user_id=user_id)

@app.route('/faq')
def faq():
    if "google_id" not in session:
        user = ""
        data = "login"
        buttonText = "Login to Google"
    else:
        user = f"{session['name']}!"
        data = "logout"
        buttonText = "Logout"
    return render_template("faq.html", user=user, data=data, buttonText=buttonText)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    try:
        flow.fetch_token(authorization_response=request.url)
    except Exception as e:
        return jsonify({"error": "Failed to authenticate."}), 500

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/protected_area")
@login_is_required
def protected_area():
    return redirect(request.url) 

@app.route("/generate_image", methods=['POST'])
def generate_image():
    try:
        prompt = request.form.get("CompanyName")
        companyname = request.form.get("CompanyName")
        tagline = request.form.get("tagline")
        style = request.form.get("style")
        companycolor = request.form.get("company-color")
        companyvalues = request.form.get("company-values")
        industry = request.form.get("industry-genre")
        addinfo = request.form.get('extra-details')

        if not prompt:
            return jsonify({"error": "Company Name is required."}), 400

        if style not in {"Minimalist", "Vintage", "Contemporary", "Realistic"}:
            return jsonify({"error": "Invalid style."}), 400

        # Construct prompt for DALL-E
        prompt += f"Create a logo with the a company name in display: {companyname} with atag line of: {tagline} and the company colors being included :{companycolor} the company logo artistically displaying their values of {companyvalues} in the art style of: {style} with the consideration of aligining the industry of {industry} attributes into the logo for the company. Additionally, ensure that each word is spelled correctly inside the logo. Here is some additonal information that the company wants to include and consider when finalizing the creation of their company logo= {addinfo}. Please ensure that you create the logo by the previous requirement they mention "

        # Make API request to DALL-E
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1,
        )

        # Extract generated image URL from response
        image_url = response.get('data', [])[0].get('url')

        user_id = session["google_id"]
        generated_image_name = f"{user_id}_{companyname.replace(' ', '_')}_{tagline.replace(' ', '_')}_{random.random()}.png"
        gen_image = requests.get(image_url)
        generated_image = gen_image.content
        content_type = gen_image.headers['Content-Type']

        client = storage.Client(credentials=credentials)
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(generated_image_name)
        blob.upload_from_string(
            generated_image,
            content_type= content_type
        )

        # Return the image URL as JSON response
        return jsonify({"image_url": image_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)