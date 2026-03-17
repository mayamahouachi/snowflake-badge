# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests  
st.title(f"Customize your smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie !"""
)
smoothiefroot_response =  requests.get("https://my.smoothiefroot.com/api/fruit/watermelon") 
st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)



name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your smoothie will be :", name_on_order)


cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe= session.table("smoothies.public.fruit_options")
#table
#st.dataframe(data=my_dataframe, use_container_width=True) 
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

#multiselect
ingredients_list=st.multiselect('Choose up to 5 ingredients:',my_dataframe,
                               max_selections=5)
#inspect ingredients_list
if ingredients_list:
    ingredients_string=''
    st.write(pd_df.columns.tolist())

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
        pd_df.columns = [col.upper() for col in pd_df.columns]
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen+' Nutrition Information')
        smoothiefroot_response =  requests.get("https://my.smoothiefroot.com/api/fruit/{search_on}") 
        st_df = st.dataframe(data=smoothiefroot_response.json(),  width='stretch')

    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """'"""+""", '""" +name_on_order+"""')"""
    
    st.write(my_insert_stmt)
    time_to_insert=st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
