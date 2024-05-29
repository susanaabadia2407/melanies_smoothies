# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

name_on_order=st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be: ' +name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = cnx.query("select SEARCH_ON FROM smoothies.public.fruit_options")
pf_df = st.dataframe(my_dataframe)
#st.stop()
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


ingredients_list = st.multiselect('Choose up to 5 ingredients:', 
                                  my_dataframe, 
                                  max_selections = 5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''
    for x in ingredients_list:
        ingredients_string += x + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(x + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + x)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """' )"""

    time_to_insert = st.button('Submir Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        #session.sql(my_insert_stmt).collect()
        
    st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")



