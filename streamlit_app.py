# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(f":cup_with_straw: Pending Smoothie Orders :cup_with_straw: ")

st.text("orders that need to be filled.")

session = get_active_session()
my_dataframe= session.table("smoothies.public.orders").filter(col("ORDER_FILLED"))
if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted=st.button('submit')
    
    if submitted:
        # insert=""""""
        # session.sql(insert)
        st.success("Someone clicked on the button")
    
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        
        try:
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.table(og_dataset)
        except:
            st.error("")
else: 
    st.success("There are no pending orders right now ")



    
#table
# st.dataframe(data=editable_df, use_container_width=True) 

# #multiselect
# ingredients_list=st.multiselect('Choose up to 5 ingredients:',my_dataframe)
# #inspect ingredients_list
# if ingredients_list:
#     # st.write(ingredients_list)
#     # st.text(ingredients_list)

#     ingredients_string=''

#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen+' '
#         # st.text(ingredients_string)
    
#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
#                         values ('""" + ingredients_string + """'"""+""", '""" +name_on_order+"""')"""
    
#     st.write(my_insert_stmt)
#     time_to_insert=st.button('submit order')
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")
