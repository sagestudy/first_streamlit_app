import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


def get_fruityvice_data(this_fruit_choice):
    streamlit.write("The user entered ", this_fruit_choice)
    fruityvice_response = requests.get(
        "https://fruityvice.com/api/fruit/" + this_fruit_choice
    )
    # streamlit.text(fruityvice_response.json())
    # Converts the JSON from the response into a dataframe in table format...
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
        return my_cur.fetchall()


def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(
            f"insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('{new_fruit}');"
        )
        return f"Thanks for adding {new_fruit}"


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
try:
    fruit_choice = streamlit.text_input("What fruit would you like information about?")
    if not fruit_choice:
        streamlit.text("Please select a fruit to get information...")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()
# # New Section to connect to snowflake from streamlit
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)

# New Section to connect to snowflake from streamlit
streamlit.header("The fruit load list contains:")
if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
# streamlit.write(type(my_data_rows))
fruit_list_add = streamlit.text_input("What fruit would you like to add?", "")
if streamlit.button("Add a Fruit to the List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(fruit_list_add)
    my_cnx.close()
    streamlit.text(back_from_function)
# streamlit.write(type(fruit_list_add))
# if not fruit_list_add:
#     streamlit.write("Input cannot be empty...")
# else:
#     # my_data_rows.extend((fruit_list_add, ))
#     streamlit.write(f"Thanks for adding {fruit_list_add}")
# streamlit.write(my_data_rows)
# streamlit.dataframe(my_data_rows)

# streamlit.text(f"my_data_rows: {my_data_rows}")
# streamlit.text(f"fruit_list_add: {fruit_list_add}")
