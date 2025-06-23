# /home/ubuntu/neonadsai_backend/src/main.py

import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS # Import CORS

# Import your application modules
from src.integrations import meta_api, linkedin_api
from src.ai_services import content_generator
from src.automation import campaign_manager
from src.analytics import reporting

# Initialize Flask app
# Serve static files from the React build directory copied into src/static
static_folder_path = os.path.join(os.path.dirname(__file__), 'static')
app = Flask(__name__, static_folder=static_folder_path, static_url_path='/')
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "default_secret_key_please_change")

# Enable CORS for all domains on all routes
# For production, you might want to restrict origins:
# CORS(app, resources={r"/api/*": {"origins": "YOUR_FRONTEND_URL"}})
CORS(app)

# --- API Endpoints --- 

@app.route("/api/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@app.route("/api/generate-copy", methods=["POST"])
def api_generate_copy():
    """Endpoint to generate ad copy."""
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing prompt in request body"}), 400
    
    prompt = data["prompt"]
    num_variations = data.get("num_variations", 3)
    
    # Ensure OPENAI_API_KEY is set in the environment where the backend runs
    if not content_generator.client:
         return jsonify({"error": "OpenAI client not initialized. Check backend logs and OPENAI_API_KEY."}), 500

    variations = content_generator.generate_ad_copy(prompt, num_variations=num_variations)
    
    if any("Error:" in v for v in variations):
         # Return the error details from the generator
         return jsonify({"error": "Failed to generate ad copy", "details": variations}), 500

    return jsonify({"variations": variations}), 200

@app.route("/api/create-campaign", methods=["POST"])
def api_create_campaign():
    """Endpoint to create a multi-platform campaign."""
    data = request.get_json()
    required_fields = ["platforms", "campaign_name", "objective", "budget", "ad_prompt"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields in request body", "required": required_fields}), 400

    # TODO: Implement proper user credential handling!
    # This uses the placeholder global credentials, which is NOT suitable for production.
    # You would typically get user ID from session/token and fetch their specific credentials.
    campaign_manager.set_user_credentials("meta", {"access_token": os.getenv("TEMP_META_TOKEN"), "ad_account_id": os.getenv("TEMP_META_AD_ACCOUNT_ID")})
    campaign_manager.set_user_credentials("linkedin", {"access_token": os.getenv("TEMP_LINKEDIN_TOKEN"), "account_urn": os.getenv("TEMP_LINKEDIN_ACCOUNT_URN")})

    results = campaign_manager.create_multi_platform_campaign(
        platforms=data["platforms"],
        campaign_name=data["campaign_name"],
        objective=data["objective"],
        budget=float(data["budget"]),
        ad_prompt=data["ad_prompt"]
    )

    # Check if any platform reported an error
    has_errors = any(res.get("status") == "error" for res in results.values() if isinstance(res, dict))
    
    status_code = 500 if has_errors and not results.get("error") else 200 # Use 500 if specific platform errors occurred
    if results.get("error"): # Handle global errors like content generation failure
        status_code = 500
        
    return jsonify(results), status_code

@app.route("/api/get-performance", methods=["POST"])
def api_get_performance():
    """Endpoint to fetch multi-platform performance."""
    data = request.get_json()
    required_fields = ["platforms"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields", "required": required_fields}), 400

    date_preset = data.get("date_preset", "last_7d")
    campaign_ids = data.get("campaign_ids", {}) # e.g., {"meta": ["id1"]}

    # TODO: Implement proper user credential handling!
    reporting.set_user_credentials("meta", {"access_token": os.getenv("TEMP_META_TOKEN"), "ad_account_id": os.getenv("TEMP_META_AD_ACCOUNT_ID")})
    reporting.set_user_credentials("linkedin", {"access_token": os.getenv("TEMP_LINKEDIN_TOKEN"), "account_urn": os.getenv("TEMP_LINKEDIN_ACCOUNT_URN")})

    performance_data = reporting.get_multi_platform_performance(
        platforms=data["platforms"],
        date_preset=date_preset,
        campaign_ids=campaign_ids
    )

    return jsonify(performance_data), 200

# --- OAuth Callbacks (Example Stubs - Needs Full Implementation) ---

@app.route("/callback/linkedin")
def linkedin_callback():
    """Handles the redirect from LinkedIn after user authorization."""
    code = request.args.get("code")
    state = request.args.get("state")
    # TODO: Verify state to prevent CSRF
    # TODO: Exchange code for token using linkedin_api.exchange_linkedin_code_for_token(code)
    # TODO: Store the obtained token securely (associated with the user)
    # TODO: Redirect user back to the frontend application
    if code:
        token_data = linkedin_api.exchange_linkedin_code_for_token(code)
        if token_data:
             # In a real app, store token_data securely and redirect
             return jsonify({"message": "LinkedIn Auth Successful (Placeholder)", "data": token_data})
        else:
             return jsonify({"error": "Failed to exchange LinkedIn code for token"}), 500
    else:
        error = request.args.get("error")
        error_description = request.args.get("error_description")
        return jsonify({"error": "LinkedIn Auth Failed", "details": error_description or error}), 400

# --- Serve Frontend (Now Enabled for Production) ---
# Serve the React app's index.html for any route not handled by the API
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        # Serve static files (like CSS, JS, images) from the build directory
        return send_from_directory(app.static_folder, path)
    else:
        # Serve the index.html for the React app, letting React Router handle the path
        index_path = os.path.join(app.static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            # Fallback if index.html is missing in the build
            return jsonify({"error": "index.html not found in frontend build directory"}), 404

# --- Main Execution --- 
if __name__ == "__main__":
    # Note: For production, use a proper WSGI server like Gunicorn, not Flask's built-in server.
    # Example: gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
    app.run(host="0.0.0.0", port=5000, debug=True) # debug=True is NOT for production
