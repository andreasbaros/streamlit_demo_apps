# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 19:25:32 2024

@author: andre
"""

import pandas as pd
import numpy as np
import openpyxl

import hmac

import xlsxwriter
import os.path
import os
import csv
import plotly.express as px
import io
import matplotlib
import plotly.graph_objects as go
import math
import scipy

#import saspy
import seaborn as sns

from IPython.display import Markdown

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Color, Fill
from openpyxl.cell import Cell
from openpyxl.styles import Font
from openpyxl.reader.excel import load_workbook

#from numerize import numerize

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

from datetime import date
from datetime import timedelta
from datetime import datetime

from PIL import Image

import matplotlib.pyplot as plt
#import seaborn as sns

#import xlwings as xw

#import xlwings as xw
import streamlit as st
#import hmac






st.set_page_config(page_title="AdWords Exercise", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    # Loading data set
    folder_path = './repositary/'
    df = pd.read_excel(folder_path + 'AdWords exercise (dataset).xlsx')
    
   
    #df['Day'] = pd.to_datetime(df['Day']).dt.strftime('%d %B %Y')
    
    
    return df
    #return df, properties, borrowers, re_collateral, dictionary



df=load_data()

Per_campaign = df.groupby(['Campaign'],dropna=False)[['Clicks','Impressions','Cost','Conversions']].sum()

Per_campaign2 = df.groupby(['Campaign','AdGroup'],dropna=False)[['Clicks','Impressions','Cost','Conversions']].sum()



Per_day=df.groupby(['Campaign','Day'],dropna=False)[['Clicks','Impressions','Cost','Conversions']].sum()
Per_day=pd.DataFrame(Per_day)
Per_day=Per_day.reset_index()



Per_campaign=pd.DataFrame(Per_campaign)
Per_campaign=Per_campaign.reset_index()

Per_campaign['Campaign']=Per_campaign['Campaign'].astype(str)

st.markdown("""## <center> :blue[**Adworks Performance August-September 2013**]</center>""",unsafe_allow_html=True)
st.write("")
st.write("")
st.write("")


st.sidebar.markdown("""<strong>Navigation Menu:</strong>""", unsafe_allow_html=True)
intro=st.sidebar.checkbox("Introduction",value=True)
main=st.sidebar.checkbox("Main page",value=True)

col1,col2,col3=st.columns([1,4,1])


tab1,tab2=st.tabs([" 📊 Data Analysis","APPENDIX"])

with tab2:
    with st.expander("Click to view **RAW DATA**"):
        st.dataframe(df)


with tab1:
    if intro:
        
        with col2:
            st.info("This web application presents the insights derived from the Performance of the Ads during August-September 2013 (2 months). Performance is broken down by campaigns and adgroups.")
    
        
        
        
    st.write("")
    st.write("")
    
    
    if main:
        col1,col2=st.columns(2)
        
        with col1:
            st.success("Max values per coumn with green color")
            st.error("Min values per column with red color")
            st.dataframe(Per_campaign.style.highlight_max(color = 'lightgreen', axis = 0,subset=['Clicks','Impressions','Cost','Conversions']).highlight_min(color = 'pink', axis = 0,subset=['Clicks','Impressions','Cost','Conversions']),hide_index=True,use_container_width=True)
            
            with st.expander("View data per AdGroup:"):
                st.dataframe(Per_campaign2,use_container_width=True)
            
            
            
        with col2:
            
            st.markdown("""#### <center> :blue[<u>**Data Insights:**</u>]""",unsafe_allow_html=True)
            container1=st.container()  
            with container1:
                st.warning("* :green[**Campaign 1**] had the maximum total Clicks as well as the maximum Conversions.  \n* :green[**Campaign 15**] had the maximum total Cost as well as the maximum Impressions, however less than half the Conversions that campaign 1 had. \n* :green[**Campaigns 3 and 7**] performed poorly in all aspects, although they had also the least Cost. ")
            #st.line_chart(Per_campaign.reset_index())  
            
            
        st.divider()
        
        col1,col2=st.columns(2)  
        
        with col1:
            bar_sel=st.selectbox("Choose metric to view in the graph:",['Clicks','Impressions','Cost','Conversions'])
            
                                
            campaign_bar = px.bar(Per_campaign, y=bar_sel, x='Campaign', color='Campaign',title=f'{bar_sel} per Campaign')
            campaign_bar.update_xaxes(type='category')
            
            st.plotly_chart(campaign_bar)
            
            
        with col2:    
            
            st.write("")
            st.write("")
            #st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            line=px.line(Per_day,x=Per_day['Day'],y=bar_sel,color='Campaign',title=f'Evolution of {bar_sel} through time')
            st.plotly_chart(line)