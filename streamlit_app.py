import streamlit
import pandas
import requests

streamlit.title("My Parents New Healthy Diner")

streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")
my_fruit_list = pandas.read_csv(
    "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
)
my_fruit_list = my_fruit_list.set_index("Fruit")

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect(
    "Pick some fruits:", list(my_fruit_list.index), ["Avocado", "Strawberries"]
)
fruits_to_show = my_fruit_list.loc[fruits_selected]
# print(fruits_to_show)
if fruits_to_show.size == 0:
    fruits_to_show = my_fruit_list.copy()
streamlit.dataframe(fruits_to_show)

# New Section to show contents from fruityvice website...
streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# streamlit.text(fruityvice_response.json())

# Converts the JSON from the response into a dataframe in table format...
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# The dataframe from above step is display on the screen...
streamlit.dataframe(fruityvice_normalized)