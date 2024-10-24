# E-commerce-ChatBot-OpenAI

This project implements an E-commerce chatbot using OpenAI's API to provide customer support, product recommendations, and other conversational features.

## Requirements

- Python 3.x
- OpenAI API key

## Installation

1. Clone this repository:

    ```bash
    git https://github.com/VisionOra/E-commerce-ChatBot-OpenAI.git
    cd E-commerce-ChatBot-OpenAI
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your `.env` file to include your OpenAI API key:

    ```bash
    echo "OPENAI_API_KEY=your_openai_api_key" > .env
    ```

## Running the ChatBot

1. Run the chatbot using Streamlit:

    ```bash
    streamlit run main.py
    ```

2. Access the chatbot in your browser at the provided URL (usually `http://localhost:8501`).

## Features

- Product search and recommendation
- Customer support for order status, returns, etc.
- General queries about the e-commerce store
