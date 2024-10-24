import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai = OpenAI()

# Reading json file
with open("shop_bot.json", "r") as f:
    shop_bot_data = json.load(f)

def get_product_details(product_name):
    """
    Retrieve the details of a specific product by its name.

    Args:
        product_name (str): The name of the product to search for.

    Returns:
        dict: A dictionary containing the product details if found, otherwise a message indicating no results.
    """
    for item in shop_bot_data:
        if product_name.lower() in item.get("Name").lower():
            return item
    return {"message": "Nothing found"}

def check_stock(product_name):
    """
    Check the stock availability of a specific product by its name.

    Args:
        product_name (str): The name of the product to check stock for.

    Returns:
        list or dict: A list of available products if found, otherwise a message indicating the product is not found.
    """
    available_products = []
    for item in shop_bot_data:
        if product_name.lower() in item.get("Name").lower() and item.get("StockAvailability"):
            available_products.append(item)
    if available_products:
        return available_products
    return {"message": "Product Not found"}

def get_product_price(product_name):
    """
    Retrieve the price of a specific product by its name.

    Args:
        product_name (str): The name of the product to get the price for.

    Returns:
        dict: A dictionary containing the product name and price if found, otherwise a message indicating no price information is available.
    """
    for item in shop_bot_data:
        if product_name.lower() in item.get("Name").lower():
            return {"product": item.get("Name"), "price": item.get("Price")}
    return {"message": f"Price information not available for '{product_name}'."}

# tools defined
tools = [
    {
        "name": "get_product_details",
        "description": "Retrieve product details by product name.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product."
                }
            },
            "required": ["product_name"]
        }
    },
    {
        "name": "check_stock",
        "description": "Check if a product is in stock by product name.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product."
                }
            },
            "required": ["product_name"]
        }
    },
    {
        "name": "get_product_price",
        "description": "Retrieve the price of a product by product name.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product."
                }
            },
            "required": ["product_name"]
        }
    }
]

def execute():
    """
    Execute the Streamlit app to interact with the ShopBot.

    This function sets up the Streamlit page, receives user input, calls the appropriate function based on the
    user's query, and displays the result.
    """
    st.set_page_config(page_title="ShopBot")
    st.header("Question")
    query = st.text_input("How can I help you? ")
    messages = []
    if query:
        messages += [
            {"role": "system", "content": "You are a helpful assistant helping users find product details."},
            {"role": "user", "content": query}
        ]
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            functions=tools,
        )
        fun_call = response.choices[0].message.function_call
        if fun_call:
            args = json.loads(fun_call.arguments)
            f_name = fun_call.name
            if f_name == "get_product_details":
                answer = get_product_details(args.get("product_name"))
            elif f_name == "check_stock":
                answer = check_stock(args.get("product_name"))
            elif f_name == "get_product_price":
                answer = get_product_price(args.get("product_name"))
            follow_up_response = openai.chat.completions.create(
                model="gpt-4-0613",
                messages=messages + [
                    {"role": "assistant", "content": None, "function_call": fun_call},
                    {"role": "function", "name": f_name, "content": json.dumps(answer)}
                ],
            )
            st.write(follow_up_response.choices[0].message.content)
        else:
            st.write(response.choices[0].message.content)

if __name__ == '__main__':
    execute()
