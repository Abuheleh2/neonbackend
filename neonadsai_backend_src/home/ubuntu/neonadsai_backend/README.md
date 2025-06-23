# NeonAdsAi Backend - README

## 1. Overview

This repository contains the backend code for NeonAdsAi, an AI-powered marketing agent designed to automate ad campaign creation and management across multiple platforms (Meta, LinkedIn, Google Ads). It includes modules for:

*   Connecting to platform APIs (Meta, LinkedIn, Google Ads)
*   Generating ad copy using AI (OpenAI)
*   Orchestrating multi-platform campaign creation
*   Fetching basic performance analytics

This backend is built using Python and the Flask framework.

## 2. Prerequisites

*   Python 3.7 or higher
*   `pip` (Python package installer)
*   Access to API credentials for:
    *   Meta Marketing API (App ID, App Secret, Ad Account ID, User Access Token with required permissions)
    *   LinkedIn Marketing API (Client ID, Client Secret, Redirect URI, User Access Token with required permissions)
    *   Google Ads API (Developer Token, Client ID, Client Secret, Refresh Token, Customer ID, potentially Login Customer ID)
    *   OpenAI API (API Key)

## 3. Setup Instructions

1.  **Extract Code:** Unzip the provided `neonadsai_backend.zip` file.
2.  **Navigate to Directory:** Open your terminal or command prompt and change into the extracted `neonadsai_backend` directory:
    ```bash
    cd path/to/neonadsai_backend
    ```
3.  **Create Virtual Environment:** Create a Python virtual environment to isolate dependencies:
    ```bash
    python -m venv venv
    ```
4.  **Activate Environment:**
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
5.  **Install Dependencies:** Install all required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## 4. Configuration (Crucial Step)

This application requires API credentials to function. The code currently expects these via **environment variables**. You need to obtain these credentials from each platform's developer portal and set them in your environment *before* running the code.

**Required Environment Variables:**

*   **Meta:**
    *   `MY_APP_ID`: Your Facebook App ID.
    *   `MY_APP_SECRET`: Your Facebook App Secret.
    *   *(Note: Access Token and Ad Account ID are currently passed as arguments or hardcoded placeholders in `meta_api.py` and `campaign_manager.py`. You will need to modify the code to securely manage and use user-specific tokens, likely obtained via an OAuth flow and stored securely.)*
*   **LinkedIn:**
    *   `LINKEDIN_CLIENT_ID`: Your LinkedIn App Client ID.
    *   `LINKEDIN_CLIENT_SECRET`: Your LinkedIn App Client Secret.
    *   `LINKEDIN_REDIRECT_URI`: The Redirect URI configured in your LinkedIn App (e.g., `http://localhost:5000/callback/linkedin`).
    *   *(Note: Access Token and Account URN are handled via OAuth flow functions in `linkedin_api.py` and placeholders in `campaign_manager.py`. You need to implement the full OAuth flow in your application.)*
*   **Google Ads:**
    *   `GOOGLE_ADS_DEVELOPER_TOKEN`: Your Google Ads Developer Token.
    *   `GOOGLE_ADS_CLIENT_ID`: Your Google Ads OAuth Client ID.
    *   `GOOGLE_ADS_CLIENT_SECRET`: Your Google Ads OAuth Client Secret.
    *   `GOOGLE_ADS_REFRESH_TOKEN`: The Refresh Token obtained via OAuth for the user.
    *   `GOOGLE_ADS_CUSTOMER_ID`: The target Google Ads Customer ID (without hyphens).
    *   `GOOGLE_ADS_LOGIN_CUSTOMER_ID`: (Optional) Your Google Ads Manager Account ID if accessing accounts via a manager account.
*   **OpenAI:**
    *   `OPENAI_API_KEY`: Your OpenAI API Key.

**How to Set Environment Variables (Examples):**

*   **macOS/Linux (Temporary for current session):**
    ```bash
    export OPENAI_API_KEY="your_openai_key"
    export GOOGLE_ADS_DEVELOPER_TOKEN="your_dev_token"
    # ... set all other required variables
    ```
*   **Windows (Command Prompt - Temporary):**
    ```cmd
    set OPENAI_API_KEY=your_openai_key
    set GOOGLE_ADS_DEVELOPER_TOKEN=your_dev_token
    # ... set all other required variables
    ```
*   **Windows (PowerShell - Temporary):**
    ```powershell
    $env:OPENAI_API_KEY="your_openai_key"
    $env:GOOGLE_ADS_DEVELOPER_TOKEN="your_dev_token"
    # ... set all other required variables
    ```
*   **Permanent Setup:** Consider using `.env` files (with a library like `python-dotenv`) or your operating system's method for setting environment variables permanently for development. **Never commit your credentials directly into the code.**

## 5. Running the Application (Development)

The current code provides modules but doesn't have a fully configured Flask application runner in `main.py` that exposes all functionalities via API endpoints. To run the Flask development server (which currently serves a basic index page):

```bash
# Make sure your virtual environment is active and you are in the neonadsai_backend directory
flask run
```

This will typically start the server at `http://127.0.0.1:5000`.

**To use the implemented modules (e.g., `campaign_manager`, `reporting`):** You would typically:
1.  Modify `src/main.py` to add Flask routes (API endpoints) that call functions within these modules.
2.  Run the Flask application.
3.  Use tools like `curl`, Postman, or a frontend application to send requests to these endpoints.

Alternatively, you can test individual module functions by running them directly in a Python script (uncomment and adapt the `if __name__ == '__main__':` blocks within the files, ensuring credentials are set).

## 6. Basic Usage (Conceptual)

Once API endpoints are set up in `main.py`:

1.  **Authentication:** Implement OAuth flows for Meta, LinkedIn, and Google Ads to obtain user tokens and store them securely (e.g., in a database associated with the user).
2.  **Set Credentials:** Use a function (like the placeholder `set_user_credentials`) to load the correct tokens for the active user before making API calls.
3.  **Generate Content:** Call an endpoint linked to `ai_services.content_generator.generate_ad_copy` with a prompt.
4.  **Create Campaign:** Call an endpoint linked to `automation.campaign_manager.create_multi_platform_campaign` with platform selections, campaign details, budget, and the AI prompt (or selected copy).
5.  **Fetch Analytics:** Call an endpoint linked to `analytics.reporting.get_multi_platform_performance` to retrieve performance data.

## 7. Testing

As mentioned previously, end-to-end testing requires valid API credentials and handling the OAuth flows. Use your credentials (set via environment variables) to test the individual functions or the full workflow once you expose them via Flask endpoints.

*   Test API initialization for each platform.
*   Test fetching accessible accounts/customers.
*   Test AI content generation with sample prompts.
*   Test campaign creation (start with `PAUSED` status to avoid spending).
*   Test performance data fetching.

## 8. Deployment

This is a Flask application. Potential deployment options include:

*   **Traditional Server:** Deploying on a Linux server using a WSGI server like Gunicorn behind a web server like Nginx.
*   **Platform-as-a-Service (PaaS):** Services like Heroku, Google App Engine, AWS Elastic Beanstalk.
*   **Containers:** Packaging the application using Docker and deploying it to container orchestration platforms (Kubernetes, Docker Swarm) or container services (AWS ECS, Google Cloud Run).

**Using Manus Deployment:** If you want me to attempt deployment, I can use the `deploy_apply_deployment` tool. This requires the project structure to match the Flask template exactly (which it does) and `requirements.txt` to be up-to-date.

```python
# Example Manus deployment call (if requested)
# print(default_api.deploy_apply_deployment(local_dir="/home/ubuntu/neonadsai_backend", type="flask"))
```

**Important for Deployment:** Ensure all dependencies are listed in `requirements.txt`. Securely manage API credentials in the production environment (do not hardcode, use environment variables or a secrets management system).

## 9. Code Structure

*   `venv/`: Python virtual environment (excluded from zip).
*   `src/`: Main source code directory.
    *   `main.py`: Flask application entry point (needs further development for API endpoints).
    *   `models/`: Database models (if using the database feature).
    *   `routes/`: Flask Blueprints for organizing API endpoints.
    *   `static/`: Static files (HTML, CSS, JS).
    *   `integrations/`: Modules for interacting with specific platform APIs (Meta, LinkedIn, Google Ads).
    *   `ai_services/`: Module for AI content generation.
    *   `automation/`: Module for orchestrating campaign creation.
    *   `analytics/`: Module for fetching and processing performance data.
*   `requirements.txt`: List of Python dependencies.

