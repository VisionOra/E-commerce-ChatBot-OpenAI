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
    """Function to get the details of the product based on name"""
    for item in shop_bot_data:
        if product_name.lower() in item.get("Name").lower():    # matching the string with simple 'in' keyword
            return item     # if item with matching name found.
    # If Not found
    return {
        "message": "Nothing found"
    }


def check_stock(product_name):
    """This function will check the availability of the product searching by product name"""
    available_products = []
    for item in shop_bot_data:  # iterate through the products
        # 'StockAvailability' boolean variable for availability
        if product_name.lower() in item.get("Name").lower() and item.get("StockAvailability"):
            available_products.append(item)     # Multiple results can be matched.

    if len(available_products) > 0:
        return available_products   # returns if found anything
    else:
        return {"message": "Product Not found"}


def get_product_price(product_name):
    """Function to get the price of the product by product name"""
    for item in shop_bot_data:
        if product_name.lower() in item.get("Name").lower():    # string match using 'in' keyword
            return {
                "product": item.get("Name"),
                "price": item.get("Price")
            }   # returns just the product name and price.
    else:
        return {
            "message": f"Price information not available for '{product_name}'."
        }


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
    st.set_page_config(page_title="ShopBot")
    st.header("Question")
    query = st.text_input("How can I help you? ")   # Receive the query of the user.
    messages = []
    if query is not None and query != "":
        messages += [
            {"role": "system", "content": "You are a helpful assistant helping users find product details."},
            {"role": "user", "content": query}
        ]
        # create chat completions
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            functions=tools,
        )

        fun_call = response.choices[0].message.function_call    # receive the function_call object
        if fun_call:    # check if function is detected by the GPT
            args = json.loads(fun_call.arguments)   # Loads the argument of the function.
            f_name = fun_call.name  # Get function Name
            # Call the GPT detected function.
            if f_name == "get_product_details":
                answer = get_product_details(args.get("product_name"))
            elif f_name == "check_stock":
                answer = check_stock(args.get("product_name"))
            elif f_name == "get_product_price":
                answer = get_product_price(args.get("product_name"))
            # generate a response with the help of available data and returns a meaningful message.
            follow_up_response = openai.chat.completions.create(
                model="gpt-4-0613",
                messages=messages + [   # appending old message as well so GPT know what we are talking about.
                    {"role": "assistant", "content": None, "function_call": fun_call},
                    {"role": "function", "name": f_name, "content": json.dumps(answer)}
                ],
            )
            # writing a meaningful response
            st.write(follow_up_response.choices[0].message.content)
        else:
            st.write(response.choices[0].message.content)


if __name__ == '__main__':
    execute()
