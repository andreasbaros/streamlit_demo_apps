# -*- coding: utf-8 -*-
"""
Created on Fri May 10 23:17:08 2024

@author: andre
"""

import pandas as pd
import streamlit as st


from pygwalker.api.streamlit import StreamlitRenderer
#file_uploaded=st.file_upload("Please upload your CSV file:")


@st.cache_data
def load_data_csv():
    df=pd.read_csv(uploaded_file)
    return df

@st.cache_data
def load_data_excel():
    df=pd.read_excel(uploaded_file)
    return df
st.set_page_config(page_title="Banking Data Analysis & Visualization App", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")

st.markdown("""# <center><strong>🧠 :grey[**Business Intelligence App**] 💼</strong></center>""", unsafe_allow_html=True)

intro='📢 This :blue[**Business Intelligence App**] allows you to upload any CSV or Excel file and dive into data visualization with :green[**PyGWalker**].  \n:green[**PyGWalker**] is an intuitive platform that allows easy, drag-and-drop interactions for a dynamic analysis experience.  \nPerfect for anyone looking to quickly visualize and understand data patterns without any coding.'


#<div class="alert alert-block alert-info"><b>Tip: </b> Use blue boxes for Tips and notes. If it's a note, you don't have to include the word "Note". </div> 
#<div class="alert alert-block alert-warning"><b>Example: </b> Use yellow boxes for examples that are not inside code cells, or use for mathematical formulas if needed. </div>
#<div class="alert alert-block alert-success"><b>Up to you: </b>Use green boxes sparingly, and only for some specific purpose that the other boxes can't cover. For example, if you have a lot of related content to link to, maybe you decide to use green boxes for related links from each section of a notebook. </div>
#<div class="alert alert-block alert-danger"><b>Just don't: </b>In general, just avoid the red boxes. </div>


st.write("")
st.write("")
col1,col2,col3=st.columns([1,2.3,1])
with col2:
   st.info(intro)

#st.markdown("""## <center><strong>🔎 :blue[Explore Your Data Instantly] 📊</strong></center>""", unsafe_allow_html=True)

#📊📈🔎📉 | Copy & Paste
st.write("")
st.write("")

tab1,tab2 = st.tabs([" 📊 Data Analytics ", "📚 References - Reading Material"])

with tab1:
    st.markdown("""## <center><strong>🔎 :blue[Explore Your Data Instantly] 📊</strong></center>""", unsafe_allow_html=True)

    col1,col2,col3=st.columns(3)
    with col2:
        with st.form("File Upload form:"):
            uploaded_file=st.file_uploader("Upload Excel/CSV file:")
            
                    
            submitted=st.form_submit_button("Submit")
    
    if submitted:
            if uploaded_file is not None:
                
                #💼🧠
                file_extension=uploaded_file.name.split('.')[-1]     
                try:
                  if file_extension=='csv':
                     df=pd.read_csv(uploaded_file)
                     #df=load_data_csv(uploaded_file)
                     st.dataframe(df.head())
                     pygwalker_app=StreamlitRenderer(df,dark="dark")
                     pygwalker_app.explorer()
                  elif file_extension=='xlsx':
                       df=pd.read_excel(uploaded_file)
                       #df=load_data_excel(uploaded_file)
                       st.dataframe(df.head())
                       pygwalker_app=StreamlitRenderer(df,dark="dark")
                       pygwalker_app.explorer()
                                # elif file_extension=='txt':
                                 #     cif_check=pd.read_csv(cif_file, delimiter='\t')
                
                except Exception as e:
                    st.error(f"Error in reading file: {e}")
                    
with tab2:
    col1,col2,col3=st.columns([3,1,1])
    with col1:
        #st.markdown("* What are non-performing loans(NPLs)?")
        st.link_button("🌎 PygWalker website", "https://kanaries.net/pygwalker")
        st.markdown("🎬 <u>:red[**YouTube videos:**]</u>",unsafe_allow_html=True)
        st.link_button("Elwynn Chen, the creator of PyGWalker, gives a walkthrough on how to get started with PyGWalker.","https://www.youtube.com/watch?v=rprn79wfB9E")
        st.link_button(" A Tableau Alternative in Python for Data Analysis (in Streamlit & Jupyter) | PyGWalker Tutorial","https://www.youtube.com/watch?v=Ynt7Etci1KU")
        st.link_button(" PyGWalker Crash Course - Data Visualization Like Tableau In Python","https://www.youtube.com/watch?v=68dFRqdxSrI")
        
        
        
        #st.markdown("* What are provisions and non-performing loan (NPL) coverage?")
        
                            
