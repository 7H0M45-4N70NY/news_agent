# News Article Generation Agent

An agent that takes a topic and country as JSON input and outputs a finished news article with a title and content.

## Python Version

This project uses Python 3.10.

## Setup

1.  **Clone the repository (if you haven't already):**

    ```bash
    git clone <repository_url>
    cd news_articles/production
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up environment variables:**

    This project requires API keys for Google services. Create a file named `.env` in the root directory of the project (the same directory as `main.py` and `requirements.txt`).

    Copy the content from `env.example` into your new `.env` file:

    ```
    GOOGLE_API_KEY=your_google_api_key_here
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

    **Important:** Replace `your_google_api_key_here` and `your_gemini_api_key_here` with your actual API keys. You can obtain these from the Google Cloud Console or Google AI Studio.

## Usage

### Running the Agent Directly

To run the news article generation agent as a standalone script:

1.  Make sure your virtual environment is activated and dependencies are installed (see **Setup** above).
2.  Run the `main.py` script:

    ```bash
    python main.py
    ```

    The script is configured to generate an article on "Sports" for "India" by default. You can modify `main.py` to change the input topic and country.

    The agent will output a JSON object with the following format:

    ```json
    {
      "title": "news_article_title",
      "content": "news_article_content"
    }
    ```

### Running the FastAPI Endpoint

This project also exposes the news article generation agent as a web API using FastAPI.

1.  Make sure your virtual environment is activated and dependencies are installed (see **Setup** above).
2.  Start the FastAPI server:

    ```bash
    uvicorn api:app --reload
    ```

    This will start the FastAPI server, typically accessible at `http://127.0.0.1:8000`. The `--reload` flag means the server will automatically restart when you make changes to the code.

3.  **Accessing the API:**

    The API exposes a `POST` endpoint at `/generate_news`.

    *   **Endpoint:** `/generate_news`
    *   **Method:** `POST`
    *   **Request Body (JSON):**

        ```json
        {
          "topic": "your_topic",
          "country": "your_country"
        }
        ```

    *   **Example `curl` command to test the API:**

        Open a new terminal window (keep the FastAPI server running in the first one) and run:

        ```bash
        curl -X POST "http://127.0.0.1:8000/generate_news" \
             -H "Content-Type: application/json" \
             -d '{"topic": "Artificial Intelligence", "country": "USA"}'
        ```

    *   **Response Body (JSON):**

        ```json
        {
          "title": "Generated News Article Title",
          "content": "The full content of the generated news article."
        }
        ```

    You can also access the interactive API documentation (Swagger UI) by navigating to `http://127.0.0.1:8000/docs` in your web browser after starting the server. This allows you to test the endpoint directly from your browser.