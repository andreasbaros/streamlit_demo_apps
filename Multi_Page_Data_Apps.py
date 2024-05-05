# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 13:49:15 2024

@author: andre
"""

import hmac
import streamlit as st

from PIL import Image


# def check_password():
#     """Returns True if the user had the correct password."""
    
#     def password_entered():
#         """Checks whether a password entered by the user is correct."""
#         if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]  # Don't store the password.
#         else:
#             st.session_state["password_correct"] = False
    
#     # Return True if the password is validated.
#     if st.session_state.get("password_correct", False):
#         return True

#     # Show input for password.
#     image = Image.open('data_app_logo.png')
#     st.image(image, use_column_width='auto')
    
#     st.write("")
#     st.write("")
#     st.text_input(
#         "🔐 Please enter password to access Transaction Advisory data apps:", type="password",
#         on_change=password_entered, key='password'
#     )
#     if "password_correct" in st.session_state:
#         st.error("🔒 Password incorrect. Try again.")
#     return False

#     else:
#         st.error("🔒 Password incorrect. Try again.")

# # 🔐🔓🔒
# if not check_password():
#     st.stop()  # Do not continue if check_password is not True.
    
    
#st.set_page_config(page_title="Data Multi Application", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded") 

st.set_page_config(
    page_title="Data Multi Application",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

image = Image.open('./repositary/data_app_logo.png')
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(image, use_column_width='auto')
    hide_image_fs='''
                  <style>
                  button[title="View fullscreen"]{
                         visibility:hidden;}
                  </style>
                  '''
    st.markdown(hide_image_fs,unsafe_allow_html=True) 

# st.write("# Transaction Advisory Data Applications! 📊")
st.write("")
st.write("")
st.write("")
st.write("")
st.markdown("""# <center><strong> 📊 :blue[Multi Page Data Applications] 📊</strong></center>""", unsafe_allow_html=True)
st.write("")
st.write("")
st.info("""The :green[Multi Page Data Application] is crafted to provide you with valuable insights into your data. By harnessing the capabilities of data visualization tools, you can easily identify outliers and potential errors, ensuring data integrity while monitoring key metrics effortlessly. This enables capturing critical trends that empower better-informed decision-making and thorough analysis.""")
st.sidebar.success("☝️ Select an application from the above")

st.write("")
st.write("")
st.markdown(
    """
    ## <center><strong><u> :grey[Application Definitions - Brief Descriptions]</u></strong></center>
    """,
    unsafe_allow_html=True
)

st.write("")   

st.warning(""" * The **Banking Data Application** is a comprehensive tool designed to provide insights into the portfolio of 
           customers with non-performing loans in the banking sector. This Streamlit application offers a user-friendly
           interface for exploring and understanding the data related to non-performing loans, allowing banking 
           professionals to make informed decisions and take proactive measures to manage risk.
            """)
            
            
# st.info(text)
# st.success(text)
# st.warning(text)
# st.error(text)            




