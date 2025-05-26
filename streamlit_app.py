# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas
# Write directly to the app
st.title(f"Jakaś tam apka :smile: {st.__version__}")
st.write(
  """Coś tam coś tam jakoś takoś!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

name_of_smoothie = st.text_input("Nazwij swojego drinka")
st.write("Nazwa drinka to", name_of_smoothie)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredienrs_list = st.multiselect('wybierz owocki do koktaju do mask pięciu', my_dataframe, max_selections=5)

if ingredienrs_list:

    ingredienrs_string = ''

    for fruit_chosen in ingredienrs_list:
        ingredienrs_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.write(ingredienrs_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredienrs_string + """','""" + name_of_smoothie +"""')"""
    
    st.write(my_insert_stmt)
    
    zatwierdz_przycisk = st.button('Zatwierdź wybór')
    if zatwierdz_przycisk:
        session.sql(my_insert_stmt).collect()
        st.success('Twoje zamówienie zostało wysłane do realizacji!', icon="✅")


