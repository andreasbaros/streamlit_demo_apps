# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 08:23:58 2024

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

#from IPython.display import Markdown

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



def check_password():
    """Returns True if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False
    
    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    #image = Image.open('data_app_logo.png')
    image = Image.open('./repositary/Bank_Logo.png')
    col1,col2,col3=st.columns([1,2,1])

    with col2:
        st.image(image,use_column_width='auto')
        hide_image_fs='''
                      <style>
                      button[title="View fullscreen"]{
                             visibility:hidden;}
                      </style>
                      '''
        st.markdown(hide_image_fs,unsafe_allow_html=True)              
    
    st.write("")
    st.write("")
    col1,col2,col3=st.columns([1,20,1])
    with col2:
        st.markdown("""## <center><strong>:bank: :grey[**Non-Performing Loans Analysis**] :bank:</strong></center>""", unsafe_allow_html=True)
        #st.markdown("""## <center><strong>:blue[Non-Performing Loans Analysis]</strong></center>""", unsafe_allow_html=True)

        
        st.write("")
        st.write("")
        st.markdown("The password to access the app is <mark>:green[**multiappdemo123**]</mark>", unsafe_allow_html=True)
        st.text_input(
            "🔐 Please enter password to access data apps:", type="password",
            on_change=password_entered, key="password"
        )
    if "password_correct" in st.session_state:
        #st.success("🔓 Password correct")
        st.error("🔒 Password incorrect. Try again.")
    return False
            
    # else:
    #     st.error("🔒 Password incorrect. Try again.")

# 🔐🔓🔒
if not check_password():
    st.stop()  # Do not continue if check_password is not True.




st.set_page_config(page_title="Banking Data Analysis & Visualization App", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")

#@st.cache_data
def load_data_NPL(xls_file):
    # Loading data set
    folder_path = './repositary/'
    xlsx = pd.ExcelFile(folder_path + f'banking_data_{xls_file}.xlsx')
    
    #xlsx = pd.ExcelFile(folder_path + 'demo_dataset_final_names.xlsx')

    # if xls_file == 'October 2023':
    #     xlsx = pd.ExcelFile(folder_path + 'NPL_DT_{xls_file}.xlsx')
    # else:
    #     xlsx = pd.ExcelFile(folder_path + 'NPL_DT_Nov2023_rev.xlsx')

    #dictionary=pd.read_excel(folder_path + 'Dictionary_rev.xlsx')
    
    
    #sheet_names = ['Property', 'Client', 'RE_Collateral', 'Property Unique']
    
    sheet_names = ['Data','Dictionary']
    dataframes = {}
    for sheet_name in sheet_names:
        df_sheet = pd.read_excel(xlsx, sheet_name=sheet_name)
        dataframes[sheet_name] = df_sheet

    # Handle dates in dataset
    #dataframes = {sheet_name: pd.to_datetime(dataframes[sheet_name].errors='coerce')
                  
                  
    df=dataframes['Data']
    dictionary=dataframes['Dictionary']
    #df['ReferenceDate'] = pd.to_datetime(df['ReferenceDate']).dt.strftime('%d %B %Y')
    # df['ReferenceDate'] = pd.to_datetime(df['ReferenceDate']).dt.strftime('%d/%m/%Y')
    # for col in df.select_dtypes(include=['datetime64[ns]']):
    #     df_filtered_rev[col] = pd.to_datetime(df_filtered_rev[col]).dt.date
    #     df[col] = pd.to_datetime(df[col]).dt.strftime('%d/%m/%Y')

    # Handle dates in 'Property Unique'
    # properties=dataframes['Property Unique']
    # for col in properties.select_dtypes(include=['datetime64[ns]']):
    #     #df_filtered_rev[col] = pd.to_datetime(df_filtered_rev[col]).dt.date
    #     properties[col] = pd.to_datetime(properties[col]).dt.strftime('%d/%m/%Y')

    # borrowers=dataframes['Client']
    # for col in borrowers.select_dtypes(include=['datetime64[ns]']):
    #     #df_filtered_rev[col] = pd.to_datetime(df_filtered_rev[col]).dt.date
    #     borrowers[col] = pd.to_datetime(borrowers[col]).dt.strftime('%d/%m/%Y')
    #     # filtered_rev[col] = df_filtered_rev[col].dt.date
    #     #borrowers[col] = pd.to_datetime(borrowers[col]).dt.strftime('%d/%m/%Y')

    # re_collateral = dataframes['RE_Collateral']
    # for col in re_collateral.select_dtypes(include=['datetime64[ns]']):
    # # df_filtered_rev[col] = df_filtered_rev[col].dt.date
    #     re_collateral[col] = pd.to_datetime(re_collateral[col]).dt.strftime('%d/%m/%Y')
    
    return df, dictionary
    #return df, properties, borrowers, re_collateral, dictionary

@st.cache_data
def convert_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    #return df.to_excel('exported_data.xlsx', engine='xlsxwriter').encode('utf-8')
    return df.to_csv(index=False,date_foramt="%d/%m/%Y").encode('utf-8')

@st.cache_data
def convert_to_excel(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    buffer2 = io.BytesIO()
    with pd.ExcelWriter(buffer2, engine='xlsxwriter') as writer2:
        for col in df_filtered_rev.select_dtypes(include=['datetime64[ns]']):
            df_filtered_rev[col]=pd.to_datetime(df_filtered_rev[col]).dt.strftime('%d/%m/%Y')
        
        df_filtered_rev.to_excel(writer2,sheet_name='exported_data',index=None)
        writer2.close()
    #writer2.save()
    #buffer2.seek(0)
    #return buffer2.getvalue()
    return buffer2

# output=buffer2.get_value()
# return buffer2.getvalue()

# st.cache_data
def key_metrics():
    st.write('\n')
    st_col1, st_col2, st_col3, st_col4= st.columns(4)

    with st_col1:
        st.markdown(f"Reference Date: <br><mark><strong>:blue[{df.iloc[0,0]}]</strong></mark>",unsafe_allow_html=True)
        st.write("")
        #st.metric("Total Gross Loan Amount (€)", '{:,.0f}'.format(df['GrossLoanAmount'].sum()/1000000) + 'M')
        st.metric("Total Number of Loans", '{:,.0f}'.format(int(df['IndivIDC'].nunique())))
    # st.metric("Total Number of Facilities", '{:,.0f}'.format(int(df['ContractUniqueID'].product.index[''].nunique())))
    with st_col2:
        st.metric("Total Gross Loan Amount (€)", '€{:,.2f}M'.format(df['GrossLoanAmount'].sum()/1000000))
        
        
       #st.metric("Total Provision Balance (€)", '{:,.0f}'.format(df['GrossProvisionsAmount'].sum()/1000000) + 'M')
        st.metric("Total Number of Clients", '{:,.0f}'.format(int(df['ClientIDC'].nunique())))
    # st.metric("Total Provision Balance", '{:,.0f}'.format(int(df['GrossProvisionsAmount'].sum()/1000000)))
    # st.write(Per product format)
    
    #st.metric("Total Gross Loan Amount", numerize.numerize(df.loc[:, 'GrossLoanAmount'].sum()), 2)
    
    # st.metric("")
    with st_col3:
        st.metric("Total Provision Balance (€)", '€{:,.2f}M'.format(df['GrossProvisionsAmount'].sum()/1000000))
        #st.metric("Total Gross (€)", '€{:,.2f}M'.format(df['GrossLoanAmount'].sum()/1000000))
        
       #st.metric("Total Provision Balance (€)", '{:,.0f}'.format(df['GrossProvisionsAmount'].sum()/1000000) + 'M')
        st.metric("Total Number of Group Clients", '{:,.0f}'.format(int(df['GroupIDC'].nunique())))
    
    with st_col4:
        st.metric("Total Loan Collateral Value (€)", '€{:,.2f}M'.format(df['LoanCollateralValue'].sum()/1000000))
        
       #st.metric("Total Provision Balance (€)", '{:,.0f}'.format(df['GrossProvisionsAmount'].sum()/1000000) + 'M')
       # st.metric("Total Number of Properties", '{:,.0f}'.format(land_type_formmatted2.iloc[-1,1]))
    
    # with st_col5:
    #     st.write("Soon..")
    #     #st.metric("Total OMV (€)", '€{:,.2f}M'.format(land_type.iloc[-1,0]/1000000))
        
        
def multiple_dfs(df_list, sheets, report_name, spaces):
    buffer_report = io.BytesIO()
    str_report_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    report_name2 = report_name + '_'+ str_report_datetime + '.xlsx'
    writer = pd.ExcelWriter(buffer_report, engine='xlsxwriter')
    row=0
    counter = 0
    number_range_list=[]
    name_range_list=[]
    
    
    # for dataframe, sheet_name in zip(df_list, sheets):
    #     dataframe.to_excel(writer, sheet_name=sheet_name, startrow=row_counter * len(dataframe.index) + spaces, index=False)
    #     worksheet = writer.sheets[sheet_name]
    #     number_range = 'B'+ str(row_counter * len(dataframe.index) + 2) + ':B'+ str((row_counter + 1) * len(dataframe.index) + 1)
    #     worksheet.conditional_format(number_range, {'type': 'cell', 'criteria': '>=', 'value': 0, 'format': currency_format})
    #     row_counter += 1
    
    for dataframe in df_list:
        #counter=counter+1
        # dataframe.to_excel(writer, sheet_name=sheets,startrow=row,startcol=0,index=None)
        # number_range_list.append(f"")
         
  

        counter =counter+ 1
        dataframe.to_excel(writer, sheet_name=sheets, startrow=row , startcol=0, index=None)
        #number_range_list[counter] = f"B{row+counter+1}:B{row+row+len(dataframe.index) + spaces + 1}"
        #row2=row + len(dataframe.index) + spaces + 1
        #name_range_list.append(f"$B${row+2}}}:$B${row+len(dataframe.index)}")
        
        number_range_list.append(f"$B${row+2}:$B${row+len(dataframe.index)}")
        name_range_list.append(f"$A${row+2}:$A${row+len(dataframe.index)}")
        row = row + len(dataframe.index) + spaces + 1

# writer.save()

    workbook=writer.book
    worksheet = writer.sheets['Summary tables']
# workbook=writer.book
# [{ls-409}], "#,##0.00"
    currency_format = workbook.add_format({'num_format': '€#0.##0,,"M"'})
# worksheet.set_row(1, 90, currency_format)
# worksheet.set_column('B:B', None, currency_format)
# worksheet.set_row(12, 18, currency_format)
# worksheet.set_column('B:B', None, currency_format)
    number_range_new="B2:H1000"

    worksheet.conditional_format(number_range_new, {'type': 'cell',
                                                    'criteria': '>=', 'value': 10000,
                                                    'format': currency_format})    
    
    number_range_new2="D2:H1000"
    currency_format2 = workbook.add_format({'num_format': '0.00%'})
    
    worksheet.conditional_format(number_range_new2, {'type': 'cell',
                                                    'criteria': 'between', 
                                                    'minimum': 0.00001,'maximum':1,
                                                    'format': currency_format2})    
    
    chart1 = workbook.add_chart({'type': 'bar'})
    chart1.add_series({
         #'categories': '=Summary tables!$A$32:$A$35',
         "categories":f"='Summary tables'!{name_range_list[0]}",
         "values": f"='Summary tables'!{number_range_list[0]}",
         #'name': 'Summary tables!$B$31',
         "data_labels": {'value': True, 'num_format': '€#0.0,,"M"'},
         }
        )

    chart1.set_title({"name": "Contract Size - GBV (€mln)", "name_font": {'size': 16}})
    chart1.set_x_axis({"name": "Gross Loan Amount", 'num_format': '€#0.0,,"M"',
                       'major_gridlines': {'visible': True,
                                           'line': {'color':'#DDD9C3',
                                                    'dash_type': 'dash',
                                                    'width': 1.00}}})
    #chart2.set_y_axis({'name': 'Contract Size', 'num_format': '€#0.0,,"M"', 'major_gridlines': {'visible': False}})
    chart1.set_legend({'none': True})
    chart1.set_size({'width': 520, 'height': 376})
    chart1.set_style(26)
    
    chart2 = workbook.add_chart({'type': 'column'})
    chart2.add_series({
         #'categories': '=Summary tables!$A$32:$A$35',
         "categories":f"='Summary tables'!{name_range_list[1]}",
         "values": f"='Summary tables'!{number_range_list[1]}",
         #'name': 'Summary tables!$B$31',
         "data_labels": {'value': True, 'num_format': '€#0.0,,"M"'},
         })

    chart2.set_title({"name": "Arrears Buckets (Contract Level) GBV(€mln)", "name_font": {'size': 16}})
    chart2.set_x_axis({"name":"Payment Delay Days"})
    chart2.set_y_axis({"name": "Gross Loan Amount", 'num_format': '€#0.#0,,"M"',
                       'major_gridlines': {'visible': True,
                                           'line': {'color':'#DDD9C3'}}})
                                                    # 'dash_type': 'dash',
                                                    # 'width': 1.00}}})
    #chart2.set_y_axis({'name': 'Contract Size', 'num_format': '€#0.0,,"M"', 'major_gridlines': {'visible': False}})
    chart2.set_legend({'none': True})
    chart2.set_size({'width': 520, 'height': 376})
    chart2.set_style(26)
    
    
    chart3 = workbook.add_chart({'type': 'column'})
    chart3.add_series({
         #'categories': '=Summary tables!$A$32:$A$35',
         "categories":f"='Summary tables'!{name_range_list[2]}",
         "values": f"='Summary tables'!{number_range_list[2]}",
         #'name': 'Summary tables!$B$31',
         "data_labels": {'value': True, 'num_format': '€#0.0,,"M"'},
         
         "points":[{'fill':{'color':'red'}},
                    {'fill':{'color':'green'}},
                     {'fill':{'color':'blue'}},
                     {'fill':{'color':'purple'}},          
                   ]
         })
         
    chart3.set_title({"name": "Gross Loan Amount by Portfolio Type", "name_font": {'size': 16}})
    chart3.set_x_axis({"name": "Portfolio Type"})
                       
    chart3.set_y_axis({"name": "Gross Loan Amount",'num_format': '€#0.0,,"M"',
                       'major_gridlines': {'visible': True,
                                           'line': {'color':'#DDD9C3'}}})
                                                    #'dash_type': 'dash',
                                                    #width': 1.00}}})
    #chart2.set_y_axis({'name': 'Contract Size', 'num_format': '€#0.0,,"M"', 'major_gridlines': {'visible': False}})
    chart3.set_legend({'none': True})
    chart3.set_size({'width': 520, 'height': 376})
    chart3.set_style(26)
    
    
    
    chart4 = workbook.add_chart({'type': 'pie'})
    chart4.add_series({
      "categories":f"='Summary tables'!{name_range_list[3]}",
      "values": f"='Summary tables'!{number_range_list[3]}",
      #'name': 'Summary tables!{number_range_list[2]}',
      "data_labels": {
        #'percentage': True,
        'value': True,
        'num_format': '€#0.0,, "M"',
        # 'custom': 'Summary tables!$B$32:$B$35',
        # 'value_num_format': '#,##0',
        'category': True,
        'separator': "\n",
        #'leader_lines': True,
        'position': 'best_fit',
        },
        })

    chart4.set_title({"name": "Gross Loan Amount by Product Type", "name_font": {'size': 16}})
    #chart4.set_x_axis({'name': 'Portfolio Type'})
    #chart4.set_y_axis({'name': 'Gross Loan Amount', 'num_format': '€#0.0,,"M"'})
    chart4.set_legend({'none': False})
    chart4.set_size({'width': 520, 'height': 376})
    chart4.set_style(26)
    
    
    chart5 = workbook.add_chart({'type': 'column'})
    chart5.add_series({
      "categories":f"='Summary tables'!{name_range_list[4]}",
      "values": f"='Summary tables'!{number_range_list[4]}",
      #'name': 'Summary tables!$B$31',
      "data_labels": {'value': True, 'num_format': '€#0.0,,"M"'},
      
      "points":[{'fill':{'color':'green'}},
                 {'fill':{'color':'yellow'}},
                  {'fill':{'color':'orange'}},
                  {'fill':{'color':'red'}},          
                ]
      })
    
    #chart5.set_title({"name": "Risk Class", "name_font": {'size': 16}})
    chart5.set_title({"name": "Gross Loan Amount by Risk Class", "name_font": {'size': 16}})
    chart5.set_x_axis({"name": "Risk Class"})
                       
    chart5.set_y_axis({"name": "Gross Loan Amount",'num_format': '€#0.0,,"M"',
                       'major_gridlines': {'visible': True,
                                           'line': {'color':'#DDD9C3'}}})
    
    
    chart5.set_legend({'none': True})
    chart5.set_size({'width': 520, 'height': 376})
    chart5.set_style(26)
    
    
    

    chart6 = workbook.add_chart({'type': 'doughnut'})
    chart6.add_series({
      "categories":f"='Summary tables'!{name_range_list[5]}",
      "values": f"='Summary tables'!{number_range_list[5]}",
      
      "data_labels": {
        #'percentage': True,
        'value': True,
        'num_format': '€#0.0,,"M"',
        #'value_num_format': '#,##0',
        'category': True,
        'separator': "\n",
        #'leader_lines': True,
        'position': 'best_fit',
       },
      })
    
    chart6.set_title({"name": "Non Performing Loan (NPL)", "name_font": {'size': 16}})
    chart6.set_legend({'none': False})
    chart6.set_size({'width': 520, 'height': 376})
    chart6.set_style(26)
    
    
    
    chart7 = workbook.add_chart({'type': 'bar'})
    chart7.add_series({
      "categories":f"='Summary tables'!{name_range_list[6]}",
      "values": f"='Summary tables'!{number_range_list[6]}",
      
      "data_labels": {'value': True,'num_format': '€#0.0,,"M"'},
      "points":[{'fill':{'color':'red'}},
                 {'fill':{'color':'green'}},
                  {'fill':{'color':'blue'}},
                  {'fill':{'color':'purple'}}, 
                  {'fill':{'color':'#008080'}},
                   {'fill':{'color':'#fdca26'}},
                   {'fill':{'color':'#ed7953'}}, 
                   {'fill':{'color':'#0d0887'}},
                    {'fill':{'color':'orange'}},
                    {'fill':{'color':'yellow'}}, 
                  
                  
                  
                ]
      })
    
    chart7.set_title({"name": "Top 10 Group Clients by Gross Loan Amount", "name_font": {'size': 16}})
    chart7.set_y_axis({"name": "Group Clients"})
                       
    chart7.set_x_axis({"name": "Gross Loan Amount",'num_format': '€#0.0,,"M"',
                       'major_gridlines': {'visible': True,
                                           'line': {'color':'#DDD9C3'}}})
    
    chart7.set_legend({'none': True})
    chart7.set_size({'width': 520, 'height': 376})
    chart7.set_style(26)
    
    
    
    # chart6 = workbook.add_chart({'type': 'pie'})
    # chart6.add_series({
    #    "categories":f"='Summary tables'!{name_range_list[8]}",
    #    'values': f"='Summary tables'!{number_range_list[8]}",
    #     'data_labels': {
    #     'value': True,
    #     'num_format': '€#0.0,,"M"',
    # },
    # 'points': [
    #     {'fill': {'color': 'red'}},
    #     {'fill': {'color': 'green'}},
    #     {'fill': {'color': 'blue'}},
    #     {'fill': {'color': 'purple'}},
    #     {'fill': {'color': '#008080'}},
    #     {'fill': {'color': '#d4ca26'}},
    #     ]
    # }
    #     )
    
    # chart6.set_title({'name': 'Property OMV By District', 'name_font': {'size': 16}})
    # chart6.set_x_axis({'name': 'Property Type'})
    # chart6.set_y_axis({'name': 'Gross Loan Amount', 'num_format': '€#0.0,,"M"',
    #                    'major_gridlines':{'visible':True,
    #                                       'line':{'color':'#DDD9C3'}}})
    # chart6.set_legend({'none': False})
    # chart6.set_size({'width': 520, 'height': 376})
    # chart6.set_style(26)
    
    
    worksheet.insert_chart('K2', chart1)
    worksheet.insert_chart('T2', chart2)
    worksheet.insert_chart('K21', chart3)
    worksheet.insert_chart('T21', chart4)
    worksheet.insert_chart('K42', chart5)
    worksheet.insert_chart('T42', chart6)
    #worksheet.insert_chart('T42', chart6)
    worksheet.insert_chart('K62', chart7)
    # worksheet.insert_chart('T62', chart8)
    # worksheet.insert_chart('K82', chart9)
# chartsheet.set_chart(chart3)
# chartsheet.activate()

# "B22:B29"
# worksheet.set_row(0, 9, currency_format)
# worksheet.set_row(12, 18, currency_format)
    writer.close()
    workbook.close()

    st.download_button('Download Summary Report to excel', data=buffer_report,
                       file_name=report_name2, mime='application/vnd.ms-excel',
                       type="primary", key="summary report")

# Put multiple dataframes across separate tabs/sheets
# def dfs_tabs(df_list, sheet_list, file_name):
#     writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
#     for dataframe, sheet in zip(df_list, sheet_list):
#         dataframe.to_excel(writer, sheet_name=sheet, startrow=0, startcol=0)
#     writer.save()
    
options_excel=['January 2024','February 2024', 'March 2024']
xls_file=st.sidebar.selectbox('Please select reference date:',
                              options_excel, index=len(options_excel)-1)

df,dictionary = load_data_NPL(xls_file)

# Confirm!
#df=df[df['ContractTheLdforSaleLeg']=='N']

pd.options.display.float_format = '{:.2f}'.format

st.markdown("""
<style>
span[data-baseweb="tag"] {
    background-color: blue !important;
}
</style>
""", unsafe_allow_html=True)

today=date.today()
yesterday=today-timedelta(days=1)
week_before=today-timedelta(days=7)

# Filter columns with IDs and codes and treat them as text IndivIDC, ClientIDC etc.
cd_columns = df.filter(regex='(ID.*|.*Cd.*)').columns
df[cd_columns] = df[cd_columns].astype(str)

# cd_columns2 = properties.filter(regex='(ID.*|.*Cd.*)').columns
# properties[cd_columns2] = properties[cd_columns2].astype(str)

# cd_columns3 = borrowers.filter(regex='(ID.*|.*Cd.*)').columns
# borrowers[cd_columns3] = borrowers[cd_columns3].astype(str)

df['Contract_NBV'] = df['GrossLoanAmount'] - df['GrossProvisionsAmount']



Per_NPL_flag = df.groupby('NonPerformingLoan(NPL)', dropna=False)[['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV','LoanCollateralValue']].sum()

Per_NPL_flag['Number of Facilities'] = df.groupby('NonPerformingLoan(NPL)', dropna=False)['IndivIDC'].nunique()
Per_NPL_flag['Number of CIFs'] = df.groupby('NonPerformingLoan(NPL)', dropna=False)['ClientIDC'].nunique()
Per_NPL_flag['Number of Group CIFs'] = df.groupby('NonPerformingLoan(NPL)', dropna=False)['GroupIDC'].nunique()

Per_NPL_flag.loc['Total'] = Per_NPL_flag.sum()

Per_NPL_flag[['Number of Facilities', 'Number of CIFs', 'Number of Group CIFs']] = Per_NPL_flag[['Number of Facilities', 'Number of CIFs', 'Number of Group CIFs']].astype(int)

Per_NPL_flag = Per_NPL_flag.reset_index()

Per_NPL_flag.iloc[:-1,:] = Per_NPL_flag.iloc[:-1,:].sort_values(by='GrossLoanAmount', ascending=False)

Per_NPL_flag = Per_NPL_flag.set_index(Per_NPL_flag.columns[0])

Per_NPL_flag_formatted = Per_NPL_flag.copy()
# Per_NPL_flag_formatted.iloc[:,0:4] = Per_NPL_flag_formatted.iloc[:,0:4].apply(lambda x: x.map('€{:,0f}'.format))
# Per_NPL_flag_formatted['Number of Facilities'] = Per_NPL_flag_formatted['Number of Facilities'].apply(lambda x: '{:,}'.format(x['Number of Facilities']),axis=1)
# Per_NPL_flag_formatted['Number of CIFs'] = Per_NPL_flag_formatted['Number of CIFs'].apply(lambda x: '{:,}'.format(x['Number of CIFs']),axis=1)
# Per_NPL_flag_formatted['Number of Group CIFs'] = Per_NPL_flag_formatted['Number of Group CIFs'].apply(lambda x: '{:,}'.format(x['Number of Group CIFs']),axis=1)


# Summarize Facilities dataframe per Product type add 'Number of Facilities'column and 'Total'row
Per_product = df.groupby('ProductType', dropna=False)[['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue']].sum()
Per_product['Number of Facilities'] = df.groupby('ProductType')['IndivIDC'].nunique()
Per_product['Number of CIFs'] = df.groupby('ProductType')['ClientIDC'].nunique()
Per_product['Number of Group CIFs'] = df.groupby('ProductType')['GroupIDC'].nunique()

Per_product.loc['Total'] = Per_product.sum()

Per_product[['Number of Facilities', 'Number of CIFs', 'Number of Group CIFs']] = Per_product[['Number of Facilities', 'Number of CIFs', 'Number of Group CIFs']].astype(int)

Per_product = Per_product.reset_index()
Per_product.iloc[:-1,:] = Per_product.iloc[:-1,:].sort_values(by='GrossLoanAmount', ascending=False)
Per_product = Per_product.set_index(Per_product.columns[0])

Per_product_formatted = Per_product.copy()
# Per_product_formatted.iloc[:,0:4] = Per_product_formatted.iloc[:,0:4].apply(lambda x: x.map('€{:,0f}'.format))
# Per_product_formatted['Number of Facilities'] = Per_product_formatted['Number of Facilities'].apply(lambda x: '{:,}'.format(x['Number of Facilities']),axis=1)
# Per_product_formatted['Number of CIFs'] = Per_product_formatted['Number of CIFs'].apply(lambda x: '{:,}'.format(x['Number of CIFs']),axis=1)
# Per_product_formatted['Number of Group CIFs'] = Per_product_formatted['Number of Group CIFs'].apply(lambda x: '{:,}'.format(x['Number of Group CIFs']),axis=1)


Per_risk = df.groupby('RiskClass', dropna=False)[['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue']].sum()
Per_risk['Number of Facilities'] = df.groupby('RiskClass')['IndivIDC'].nunique()
Per_risk['Number of CIFs'] = df.groupby('RiskClass')['ClientIDC'].nunique()
Per_risk['Number of Group CIFs'] = df.groupby('RiskClass')['GroupIDC'].nunique()

Per_risk.loc['Total'] = Per_risk.sum()

Per_risk[['Number of Facilities', 'Number of CIFs', 'Number of Group CIFs']] = Per_risk[['Number of Facilities', 'Number of CIFs', 'Number of Group CIFs']].astype(int)

Per_risk = Per_risk.reset_index()
#Per_risk.iloc[:-1,:] = Per_risk.iloc[:-1,:].sort_values(by='GrossLoanAmount', ascending=False)

Per_risk = Per_risk.set_index(Per_risk.columns[0])
Per_risk=Per_risk.reindex(["Low Risk","Moderate Risk","High Risk","Very High Risk","Total"])

Per_risk_formatted = Per_risk.copy()


Per_NPL_class = df.groupby('NonPerformingLoan(NPL)', dropna=False)[['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue']].sum()
Per_NPL_class['Number of Facilities'] = df.groupby('NonPerformingLoan(NPL)')['IndivIDC'].nunique()
Per_NPL_class['Number of CIFs'] = df.groupby('NonPerformingLoan(NPL)')['ClientIDC'].nunique()
Per_NPL_class['Number of Group CIFs'] = df.groupby('NonPerformingLoan(NPL)')['GroupIDC'].nunique()

Per_NPL_class.loc['Total'] = Per_NPL_class.sum()

Per_NPL_class[['Number of Facilities', 'Number of CIFs', 'Number of Group CIFs']] = Per_NPL_class[['Number of Facilities', 'Number of CIFs', 'Number of Group CIFs']].astype(int)

Per_NPL_class = Per_NPL_class.reset_index()
#Per_risk.iloc[:-1,:] = Per_risk.iloc[:-1,:].sort_values(by='GrossLoanAmount', ascending=False)

Per_NPL_class = Per_NPL_class.set_index(Per_NPL_class.columns[0])
#Per_NPL_class=Per_risk.reindex(["Low Risk","Moderate Risk","High Risk","Very High Risk","Total"])

Per_NPL_class_formatted = Per_NPL_class.copy()


riskclass_pie=px.pie(Per_risk_formatted.reset_index().iloc[:-1,:],values='GrossLoanAmount',names=Per_risk_formatted.index[:-1],
                      custom_data=['RiskClass','GrossLoanAmount'],title="Gross Loan Amount per Risk Class",color='RiskClass',
                      color_discrete_map={'Low Risk':'green',
                                 'Moderate Risk':'yellow',
                                 'High Risk':'orangered',
                                 'Very High Risk':'crimson'})



# color_discrete_map={'Low Risk':'chartreuse',
#            'Moderate Risk':'yellow',
#            'High Risk':'darksalmon',
#            'Very High Risk':'red'})
#color_discrete_map={'Low Risk':'lightcyan',
 #          'Fri':'cyan',
 #          'Sat':'royalblue',
#           'Sun':'darkblue'}
 
riskclass_pie.update_traces(textinfo='value+percent+label',
                             texttemplate='%{label}''<br>%{percent:,.2%}''<br>€%{customdata[1]:.5s}',
                             hovertemplate='%{label}''<br>%{percent:,.2%}')
 

riskclass_pie.update_layout(height=550,width=800,title_x=0.35,legend=dict(
                                            orientation="h",xanchor="center",x=0.5,font=dict(size= 16)),
    ) 

NPL_pie=px.pie(Per_NPL_class_formatted.reset_index().iloc[:-1,:],values='GrossLoanAmount',names=Per_NPL_class_formatted.index[:-1],
                      custom_data=['NonPerformingLoan(NPL)','GrossLoanAmount'],hole=0.4,title="Gross Loan Amount per NPL Flag",
                      color='NonPerformingLoan(NPL)',
                      color_discrete_map={'Yes':'crimson',
                                 'No':'green',
                                 })
 
NPL_pie.update_traces(textinfo='value+percent+label',
                             texttemplate='%{label}''<br>%{percent:,.2%}''<br>€%{customdata[1]:.5s}',
                             hovertemplate='%{label}''<br>%{percent:,.2%}')

NPL_pie.update_layout(height=550,width=800,title_x=0.35,legend=dict(
                                            orientation="h",xanchor="center",x=0.5,font=dict(size= 16)))
# Summarize Properties dataframe per Land Type add 'Number of Properties', 'Percent xxx'and 'Average'columns and 'Total'row
# land_type = properties.groupby('PropLanType', dropna=False)[['PropOMVFinal']].sum()
# land_type['Number of Properties'] = properties.groupby('PropLanType',dropna=False)[['PropID']].count()
# land_type.loc['Total'] = land_type.sum()
# land_type['Number of Properties']=land_type['Number of Properties'].astype(int)

# land_type['Percent (%) PropOMVFinal'] = 100 * (land_type['PropOMVfinal'] / land_type.loc['Total','PropOMVfinal'])
# land_type['Percent (%) PropOMVFinal']=land_type['Percent (%) PropOMVFinal'].apply(lambda x:'{:,2f}%'.format(x))
# land_type['Percent (%) Number of Properties']=100 * (land_type['Number of properties'] / land_type.loc['Total','Number of properties'])
# land_type['Percent (%) Number of Properties']=land_type['Percent (%) Number of Properties'].apply(lambda x:'{:,2f}%'.format(x))
# land_type['Average PropOMVFinal'] = land_type['PropOMVFinal'] / land_type['Number of Properties']


# min_land=(land_type['Average PropOMVfinal']/land_type['Average PropOMVfinal']).min()

# land_type['Ranking']=10*((land_type.iloc[:-1,land_type.columns.get_loc('AveragePropOMVfinal')]/land_type.iloc[:-1,land_type.columns.get_loc('AveragePropOMVfinal')].sum())-(land_type.iloc[:-1,land_type.columns.get_loc('AveragePropOMVfinal')]/land_type.iloc[:-1,land_type.columns.get_loc('AveragePropOMVfinnal')].sum()).min())/((land_type.iloc[:-1,land_type.columns.get_loc('AveragePropOMVfinal')]/
#                            land_type.iloc[:-1,land_type.columns.get_loc('AveragePropOMVfinal')].sum()).max()
#                            -(land_type.iloc[:-1,land_type.columns.get_loc('AveragePropOMVfinal')]/
#                            land_type.iloc[:-1,land_type.columns.get_loc('AveragePropOMVfinal')].sum()).min())


# land_type=land_type.reset_index()

#NOT SURE IF IT DOES ANYTHING

# land_type.iloc[:-1,:]=land_type.iloc[:-1,:].sort_values(by='PropOMVfinal',ascending=False)
# land_type=land_type.set_index(land_type.columns[0])
# land_type=land_type.sort_values(by=['Ranking'],ascending=False)

# land_type_formatted=land_type.copy()
# land_type_formatted[['PropOMVfinal','Average PropOMVfinal']]=land_type_formatted[['PropOMVfinal','Average PropOMVfinal']].apply(lambda x:x.map('€{:,2f}'.format))
# land_type_formatted=land_type_formatted[['PropOMVfinal','Percent (% PropOMVfinal)','Number of Properties',
#                                          'Percent (% Number of Properties)', 'Average PropOMVfinal','Ranking']]

# # Summarize Properties dataframe per Location District add 'Number of Properties', 'Percent xxx'and 'Average'columns and 'Total'row
# land_type2 = properties.groupby('PropLocationDistrict')[['PropOMVFinal']].sum()
# land_type2['Number of Properties'] = properties.groupby('PropLocationDistrict')[['PropID']].count()
# land_type2.loc['Total'] = land_type2.sum()

#### OI EPOMENES 2 GRAMMES MAKE SENSE ALLA EN PINTWSIA TOU CHATGPT EN TO EIXE STIN FOTO
#land_type2['Percent (%) PropOMVFinal'] = 100 * (land_type2['PropOMVFinal'] / land_type2['PropOMVFinal'].loc['Total'])
# #land_type2['Average PropOMVFinal'] = land_type2['PropOMVFinal'] / land_type2['Number of Properties']
# land_type2['Number of Properties'] = land_type2['Number of Properties'].astype(int)

# land_type_formatted2 = land_type2.copy()
# land_type_formatted2.iloc[:,0:1] = land_type_formatted2.iloc[:,0:1].apply(lambda x: x.map('€{:,.2f}'.format))

# Same result as above - second solution with pivot table instead
pivot_table = df.pivot_table(index='ProductType', values=['GrossLoanAmount','GrossLoanAmount'], aggfunc=sum)
pivot_table['Number of Facilities'] = df.groupby('ProductType')['IndivIDC'].count()
pivot_table.loc['Total'] = pivot_table.sum()
pivot_table['Number of Facilities'] = pivot_table['Number of Facilities'].astype(int)

pivot_table_formatted = pivot_table.copy()
pivot_table_formatted.iloc[:,0:2] = pivot_table_formatted.iloc[:,0:2].apply(lambda x: x.map('€{:,.2f}'.format))

df_exp=Per_product.iloc[:,:].reset_index()
df_exp_long = pd.melt(df_exp, id_vars=['ProductType'], value_vars=['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue','Number of Facilities'], var_name='Metric')
#, value_name='Value'
df_exp_long2 = pd.melt(df, id_vars=['ProductType'], value_vars=['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue'], var_name='Metric')


# Pie chart version for df_exp
fig4 = px.pie(Per_product.iloc[:-1,:], values='GrossLoanAmount', names=Per_product.index[:-1], title='Gross Loan Amount Per Product Type')


# Summarize Facilities dataframe per Portfolio Type (Retail, SME, Corporate) add 'Number of Facilities'column and 'Total'row
Per_product_ultra3 = df.groupby('ProductCategory')[['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue']].sum()

Per_product_ultra3['Number of Facilities'] = df.groupby('ProductCategory')[['IndivIDC']].nunique()
Per_product_ultra3['Number of CIFs'] = df.groupby('ProductCategory')[['ClientIDC']].nunique()
Per_product_ultra3['Number of Group CIFs'] = df.groupby('ProductCategory')[['GroupIDC']].nunique()

Per_product_ultra3.loc['Total'] = Per_product_ultra3.sum()
Per_product_ultra3[['Number of Facilities', 'Number of CIFs', 'Number of Group CIFs']] = Per_product_ultra3[['Number of Facilities', 'Number of CIFs', 'Number of Group CIFs']].astype(int)

Per_product_ultra3 = Per_product_ultra3.reset_index()
Per_product_ultra3.iloc[:-1,:] = Per_product_ultra3.iloc[:-1,:].sort_values(by='GrossLoanAmount', ascending=False)
Per_product_ultra3 = Per_product_ultra3.set_index(Per_product_ultra3.columns[0])

Per_product_ultra3_formatted = Per_product_ultra3.copy()
# Per_product_ultra3_formatted.iloc[:,0:4] = Per_product_ultra3_formatted.iloc[:,0:4].apply(lambda x: x.map('€{:,2f}'.format))
# Per_product_ultra3_formatted['Number of Facilities'] = Per_product_ultra3_formatted['Number of Facilities'].apply(lambda x: '{:,}'.format(x['Number of Facilities']), axis=1)
# Per_product_ultra3_formatted['Number of CIFs'] = Per_product_ultra3_formatted['Number of CIFs'].apply(lambda x: '{:,}'.format(x['Number of CIFs']), axis=1)
# Per_product_ultra3_formatted['Number of Group CIFs'] = Per_product_ultra3_formatted['Number of Group CIFs'].apply(lambda x: '{:,}'.format(x['Number of Group CIFs']), axis=1)

#df_exp_portfolio_cd = pd.melt(Per_product_ultra3.reset
                              
df_exp_portfolio_cd = pd.melt(Per_product_ultra3.reset_index(), id_vars=['ProductCategory'], value_vars=['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue','Number of Facilities'], var_name='metric')

#st.dataframe(df_exp_portfolio_cd)
fig3_x_cons_portfolio = px.bar(df_exp_portfolio_cd[:-5], y='ProductCategory', x='value', color='metric')

# Consolidated Plot
fig3_x_cons_portfolio.update_layout(autosize=False, width=800, height=500, yaxis={'categoryorder': 'total ascending'})
fig3_x_cons_portfolio.update_traces(texttemplate='€%{x:,.0f}', hovertemplate='Type: %{y} <br> Value: €%{x:,.0f} <extra> </extra>')

df.index+=1
# borrowers.index+=1
# properties.index+=1
# re_collateral.index+=1

# conditions=[
#     (df['ContractLegalFlag']=='F'),
#     (df['ContractLegalFlag'].isin(['B', 'R', 'N', '']) | df['ContractLegalFlag'].isna())]


# choices=['FINAL DEMAND', 'NOT TERMINATED']
# df['Terminated Flag'] = np.select(conditions, choices, default='TERMINATED')

# Per_Terminated_flag=df.groupby('Terminated Flag', dropna=False)[['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV', 'ContractREColLegagClaimRun1']].sum()
# Per_Terminated_flag['Number of Facilities'] = df.groupby('Terminated Flag', dropna=False)[['IndivIDC']].count()
# Per_Terminated_flag['Total'] = Per_Terminated_flag.sum()
# Per_Terminated_flag['Number of Facilities'] = Per_Terminated_flag['Number of Facilities'].astype(int)

# Per_Terminated_flag = Per_Terminated_flag.reset_index()
# Per_Terminated_flag.iloc[:-1,:] = Per_Terminated_flag.iloc[:-1,:].sort_values(by='GrossLoanAmount', ascending=False)
# Per_Terminated_flag = Per_Terminated_flag.set_index(Per_Terminated_flag.columns[0])

# Per_Terminated_flag_formatted = Per_Terminated_flag.copy()
# Per_Terminated_flag_formatted.iloc[:,0:4] = Per_Terminated_flag_formatted.iloc[:,0:4].apply(lambda x: x.map('€{:,0f}'.format))
# Per_Terminated_flag_formatted['Number of Facilities'] = Per_Terminated_flag_formatted.apply(lambda x: '{:,}'.format(x['Number of Facilities']),axis=1)


df_exp_portfolio_cd_v2=Per_product_ultra3.reset_index().iloc[:,:-3]
df_long_portfolio_cd_1 = pd.melt(df_exp_portfolio_cd_v2, id_vars=['ProductCategory'], var_name='Column', value_name='Value')

# Create 4 subplots of bar charts with respect to each column
fig_long_portfolio_cd_1 = px.bar(df_long_portfolio_cd_1, x='Value', y='ProductCategory', color='ProductCategory', orientation='h', facet_col='Column', facet_col_wrap=2, text='Value')
fig_long_portfolio_cd_1.update_traces(texttemplate='€%{x:.5s}',hovertemplate='Type: %{y} <br> Value: €%{x:,.0f} <extra> </extra>')
                                  
fig_long_portfolio_cd_1.update_layout(title_text='Gross Loan Amount, Provisions, Net Book Value & Loan Collateral Value per Portfolio Type',
                                     legend=dict(orientation='h'))
fig_long_portfolio_cd_1.for_each_annotation(lambda ann: ann.update(text=ann.text.split("=")[-1]))

df_woz=df[df['GrossLoanAmount'] != 0]
#df_outstdg = df[df['ContractOutstdgPrinc'] != 0]
df_dpd = df[df['PaymentDelayDays'] != 0]

bins=[0, 100000, 500000, 1000000, 3000000, 5000000, float('inf')]
labels=['0-100k', '100k-500k', '500k-1m', '1m-3m', '3m-5m', '5m+']

df_bucket = pd.DataFrame(columns=['Bucket'])
df_bucket['Gross Loan Amount Bucket'] = pd.cut(df['GrossLoanAmount'], bins=bins, labels=labels, right=False)
df_bucket['Gross Loan Amount'] = df['GrossLoanAmount']
df_bucket['GrossLoanAmount'] = df['GrossLoanAmount']
category_sums = df_bucket.groupby('Gross Loan Amount Bucket')['GrossLoanAmount'].sum().reset_index()
category_counts = df_bucket.groupby('Gross Loan Amount Bucket')['GrossLoanAmount'].count().reset_index()

#value_counts = df_bucket['Bucket'].value_counts().reset_index()
bin_df = pd.merge(category_sums, category_counts, on='Gross Loan Amount Bucket')
bin_df.columns = ['Gross Loan Amount Bucket', 'GrossLoanAmount', 'Number of Facilities']

total_sum = bin_df['GrossLoanAmount'].sum()
total_count=bin_df['Number of Facilities'].sum()
bin_df.loc[len(bin_df.index)] = ['Total', total_sum, total_count]

bin_df['Average Exposure'] = bin_df['GrossLoanAmount'] / bin_df['Number of Facilities']
bin_df['GrossLoanAmount Percentage (%)'] = (bin_df['GrossLoanAmount'] / total_sum) * 100

bin_df.index+=1

# bins_dpd=[0, 30, 91, 365, 1095, 1825, float('inf')]
# labels_dpd=['0-29', '30-90', '91-364', '1y-3y', '3y-5y', '5y+']

bins_dpd=[0,30,91,121,181,361,721,float('inf')]
labels_dpd=['0-29','30-90','91-120','121-180','181-360','361-720','720+']

df_bucket_dpd=pd.DataFrame(columns=['Bucket'])
df_bucket_dpd['Payment Delay Days Bucket']=pd.cut(df['PaymentDelayDays'],bins=bins_dpd,labels=labels_dpd,right=False)
df_bucket_dpd['GrossLoanAmount']=df['GrossLoanAmount']
category_sums_dpd=df_bucket_dpd.groupby('Payment Delay Days Bucket')['GrossLoanAmount'].sum().reset_index()
category_counts_dpd=df_bucket_dpd.groupby('Payment Delay Days Bucket')['GrossLoanAmount'].count().reset_index()

# right : bool, default True) Indicates whether bins include the rightmost edge or not.
# If right = True (the default), then the bins [1, 2, 3, 4] indicate (1,2], (2,3], (3,4].
bin_df_dpd=pd.merge(category_sums_dpd,category_counts_dpd,on='Payment Delay Days Bucket')
bin_df_dpd.columns=['Payment Delay Days Bucket','GrossLoanAmount','Number of Facilities']
total_sum_dpd=bin_df_dpd['GrossLoanAmount'].sum()
total_count_dpd=bin_df_dpd['Number of Facilities'].sum()
bin_df_dpd.loc[len(bin_df_dpd.index)] = ['Total', total_sum_dpd, total_count_dpd]

bin_df_dpd.loc[len(bin_df_dpd.index)-1] = ['Blanks', df.loc[df['PaymentDelayDays'].isnull(),'GrossLoanAmount'].sum(), df['PaymentDelayDays'].isnull().sum()]
bin_df_dpd.loc[len(bin_df_dpd.index)] = ['Total', total_sum_dpd,total_count_dpd+df['PaymentDelayDays'].isnull().sum()]

bin_df_dpd['Average Exposure'] = bin_df_dpd['GrossLoanAmount'] / bin_df_dpd['Number of Facilities']
#if df.loc[df['PaymentDelayDays'].isnull()==0:
          
bin_df_dpd['GrossLoanAmount Percentage (%)'] = (bin_df_dpd['GrossLoanAmount'] / total_sum_dpd) * 100

bin_df_dpd.index+=1

#bin_df_dpd.index+=1

bin_df_dpd_formatted=bin_df_dpd.copy()

bin_df_dpd_formatted['Number of Facilities']=bin_df_dpd_formatted['Number of Facilities'].apply(lambda x: '{:,.0f}'.format(x))
bin_df_dpd_formatted['GrossLoanAmount Percentage (%)']=bin_df_dpd_formatted['GrossLoanAmount Percentage (%)'].apply(lambda x: '{:,.2f}%'.format(x))
bin_df_dpd_formatted[['GrossLoanAmount','Average Exposure']]=bin_df_dpd_formatted[['GrossLoanAmount','Average Exposure']].apply(lambda x: x.map('€{:,.0f}'.format))

# bin_df_dpd_formatted['GrossLoanAmount']=bin_df_dpd_formatted['GrossLoanAmount'].apply(lambda x: '{:,.0f}'.format(x))
# bin_df_dpd_formatted['Average Exposure']=bin_df_dpd_formatted['Average Exposure'].apply(lambda x: '{:,.0f}'.format(x))

#"currency": "€"
bin_df_formatted=bin_df.copy()

bin_df_formatted['Number of Facilities']=bin_df_formatted['Number of Facilities'].apply(lambda x: '{:,.0f}'.format(x))
bin_df_formatted['GrossLoanAmount Percentage (%)']=bin_df_formatted['GrossLoanAmount Percentage (%)'].apply(lambda x: '{:,.2f}%'.format(x))

bin_df_formatted[['GrossLoanAmount','Average Exposure']]=bin_df_formatted[['GrossLoanAmount','Average Exposure']].apply(lambda x: x.map('€{:,.0f}'.format))


# bin_df_formatted['GrossLoanAmount']=bin_df_formatted['GrossLoanAmount'].apply(lambda x: '{:,.0f}'.format(x))
# bin_df_formatted['Average Exposure']=bin_df_formatted['Average Exposure'].apply(lambda x: '{:,.0f}'.format(x))

#bin_df_formatted.iloc[:,0]=bin_df_formatted.iloc[:,0].apply(lambda x: x.map('€{:,.2f}'.format))
#bin_df_formatted['GrossLoanAmount']=bin_df_formatted.iloc[:,0].apply(lambda x: '{:,.2f}'.format(x['GrossLoanAmount']), axis=1)

fig_table_bucket = go.Figure(data=[go.Table(columnwidth = [2,2.5,2.5,2.5],
    header=dict(values=list(bin_df_formatted.columns),
                fill_color='paleturquoise',
                align='center'),
                cells=dict(values=bin_df_formatted.iloc[:,:].T.values,
               fill_color=['lavender','whitesmoke'],format=["","",',.0f',""],
               align='center',height=30)
               )])

fig_table_bucket.update_layout(height=550, width=600, title_text="Contract Gross Loan Amount and Number of Facilities per Bucket", title_x=0.2)



#######################################################################################################################################
#################################################################### STREAMLIT UI SECTION #############################################
#######################################################################################################################################
         


image = Image.open('./repositary/Bank_Logo.png')
#st.markdown(image)
col1,col2,col3=st.columns([1,2,1])

with col2:
    st.image(image,use_column_width='auto')
    hide_image_fs='''
                  <style>
                  button[title="View fullscreen"]{
                         visibility:hidden;}
                  </style>
                  '''
    st.markdown(hide_image_fs,unsafe_allow_html=True) 
    
# st.write('\n') 
# st.write('\n') 
st.write('\n') 


st.markdown("""## <center><strong>:bank: :grey[**Non-Performing Loans Analysis**] :bank:</strong></center>""", unsafe_allow_html=True)
#st.markdown("""## <center><strong>:blue[Non-Performing Loans Analysis]</strong></center>""", unsafe_allow_html=True)

# st.markdown('''
#     :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
#     :gray[pretty] :rainbow[colors].''')
df['ReferenceDate']=pd.to_datetime(df['ReferenceDate']).dt.strftime('%d %B %Y')
st.markdown(f"""##### <center><strong>:calendar: :blue[Reference Date:] <mark>{df.iloc[0,0]}</mark><strong>""", unsafe_allow_html=True)
#st.markdown(f"Please note that :green:`Help For Sale Facilities have been :red:[excluded]` from the dataset.", icon="ℹ️")
st.write('\n')
st.write('\n')

mystyle = '''
<style>
    p {
        text-align: justify;
        
    }
</style>
'''

# i center anti justify

st.markdown(mystyle, unsafe_allow_html=True)
# col1, col2, col3 = st.columns([1,1.2,1])
# with col2:
#     st.info(f" ⚠️ **Please note that :green:[Help For Sale Facilities] have been :red[excluded] from the dataset.**")
#     # st.metric("reference Date:", df.iloc[0], col2)
#     # 📢🚨⚠️❗ | Copy & Paste
#st.write('\n')
#st.write('\n')

# st.write("")
# st.write("")
# st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)

st.sidebar.markdown("""<strong>Navigation Menu:</strong>""", unsafe_allow_html=True)
introduction=st.sidebar.checkbox("Introduction")
main_page=st.sidebar.checkbox("Main Page")

# introduction=st.sidebar.checkbox("Introduction", key='intro')
# main_page=st.sidebar.checkbox("Main Page", key='main')

if (not introduction) and (not main_page):
    col1, col2, col3 = st.columns([1,1.4,1])
    with col2:
        st.info("""👈 **Please select the sections you would like to view from the :green[navigation side-menu] on the left.**""")

if introduction:
    
    #st.header(":pushpin: Introduction")
    intro3,intro1,intro2=st.columns([1,5,1])
    with intro1:
        disclaimer="⚠️🚩 :red[**Disclaimer**]: The data presented in this application are entirely fictional and are provided solely for demonstration purposes. Any resemblance to real data or actual financial situations is purely coincidental and unintentional."
        st.info(disclaimer)
        st.markdown("""## <center><strong>:pushpin: :blue[Introduction] </strong></center>""", unsafe_allow_html=True)
    intro="📢 The :green[**Non-Performing Loans Analysis**] application is a comprehensive tool engineered to deliver insightful analytics on non-performing loan portfolios within the banking sector. This application, developed using Streamlit, features an intuitive interface that enables banking professionals to effectively explore and comprehend data concerning non-performing loans. By leveraging this tool, professionals can make well-informed decisions and implement proactive strategies to mitigate risk."

    
    
    with intro1:
        st.write("")
        st.info(intro)
    #with intro2:    
        #st.write("")
        #st.info(disclaimer)
    #st.markdown(intro,unsafe_allow_html=True)
    st.write("---")
    
# disclaimer2="⚠️🚩 :red[**Disclaimer**]: The data presented in this application are entirely fictional and are provided solely for demonstration purposes. Any resemblance to real data or actual financial situations is purely coincidental and unintentional."

# st.sidebar.info(disclaimer2)
if main_page:
    
    st.subheader("🗃️ Page Sections")
    # 🗂️📁📑
    tab2, tab1,tab3,tabref,appendix = st.tabs([" 📊 Data Analytics ", " 🔎 Data Extraction ", " Data Dictionary ","📚 References - Reading Material","📑 APPENDIX"])
    # Data Emojis | 📊 📈 🖥️ 🧮 💻 📑 🗄️ 📊 📈 🖥️ 🧮 💻 📑 🗄️ | Copy & Paste

    #st.info("In this section you can upload a CSV file with a list of CIFs you would like to extract data from the APS Data Tape. Alternatively, you can click on the switch and use the dictionary lookup.")
    
    with appendix:
        
        col1,col2,col3,col4=st.columns(4)
        with col1:
            options_excel2=['January 2024','February 2024', 'March 2024']
            xls_file2=st.selectbox('Please select reference date:',
                                          options_excel2, index=len(options_excel2)-1,key='raw_data')
    
            df2,dictionary2 = load_data_NPL(xls_file2)
            df2['ReferenceDate']=pd.to_datetime(df2['ReferenceDate']).dt.strftime('%d %B %Y')
            
            buffer = io.BytesIO()
            #current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            #str_current_datetime = str(current_datetime)
            file_export_name = f'banking_data_{xls_file2}_export'+ '.xlsx'
            
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df2.to_excel(writer, sheet_name='NPL_monthly_data', index=None)
                writer.close()
            
                st.download_button(f'Download :blue[{xls_file2}] data', data=buffer, file_name=file_export_name, mime='application/vnd.ms-excel')
            
    
    with tabref:
        col1,col2,col3=st.columns(3)
        with col1:
            #st.markdown("* What are non-performing loans(NPLs)?")
            st.link_button("📚 What are non-performing loans (NPLs)?","https://finance.ec.europa.eu/banking/non-performing-loans-npls_en")
            #st.markdown("* What are provisions and non-performing loan (NPL) coverage?")
            st.link_button("📚 What are provisions and non-performing loan (NPL) coverage?", "https://www.bankingsupervision.europa.eu/about/ssmexplained/html/provisions_and_nplcoverage.en.html")
            
        # with col2:
        #     st.link_button("📚 Go to European Commision","https://finance.ec.europa.eu/banking/non-performing-loans-npls_en")
        #     st.link_button("📚 Go to European Central Bank (ECB)", "https://www.bankingsupervision.europa.eu/about/ssmexplained/html/provisions_and_nplcoverage.en.html")
            
    with tab3:
        form_check=False
        # tab3=...
        
        # if dictionary_lookup:
        #     dictionary_lookup=st.toggle("Dictionary lookup")
        
        
        with st.form("dict_lookup"):
                dict_check=st.multiselect("Type or select Fields from dropdown list:", dictionary['Field Name'].unique())
                submitted=st.form_submit_button("View definitions for selected fields")
                
                if submitted:
                    matching_dicts=[diction for diction in dict_check if diction in dictionary['Field Name'].values]
                    if matching_dicts:
                        dict_check_f=dictionary.loc[dictionary['Field Name'].isin(dict_check)]
                        
                        form_check=True
                    else:
                      st.error("No field has been selected. Please select value(s) from dropdown list.")
        if form_check:
        # ...
        #st.write("dictionary section soon")
            dict_check_f_rev=dict_check_f.sort_values('Field Name')
            st.dataframe(dict_check_f_rev, hide_index=True)
            
            buffer = io.BytesIO()
            current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            str_current_datetime = str(current_datetime)
            file_export_name = 'field_definitions_'+ str_current_datetime + '.xlsx'
            
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                dict_check_f_rev.to_excel(writer, sheet_name='field_definitions', index=None)
                writer.close()
            
                st.download_button('Download selected fields dictionary to excel', data=buffer, file_name=file_export_name, mime='application/vnd.ms-excel')
        
        if st.toggle("View full dictionary:"):
            st.dataframe(dictionary,hide_index=True)        
            buffer = io.BytesIO()
            #current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            #str_current_datetime = str(current_datetime)
            file_export_name = 'full_dictionary'+ '.xlsx'
            
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                dictionary.to_excel(writer, sheet_name='field_definitions', index=None)
                writer.close()
            
                st.download_button('Download full dictionary to excel', data=buffer, file_name=file_export_name, mime='application/vnd.ms-excel')
            

# # Code for Streamlit expander to show full dictionary
#     dictionary.index=+1
#     with st.expander("Click to view full dictionary"):
#         st.write("")
#         st.write("")
#         st.dataframe(dictionary)
#         buffer = io.BytesIO()
#         current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#         str_current_datetime = str(current_datetime)
#         file_export_name = 'full_dictionary_'+ str_current_datetime + '.xlsx'
        
#         with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
#             dictionary.to_excel(writer, sheet_name='dictionary', index=None)
#             writer.close()
    
#             st.download_button('Download full dictionary to excel', data=buffer, file_name=file_export_name, mime='application/vnd.ms-excel')

# Other UI elements in Streamlit
    with tab2:
        
      
      #Tabs Emojis | 🗂️📁📑🗃️
      #tab3,tab5 = st.tabs(["📊 Client Data Analytics", "📝 Summary"])
    
      #with tab5:
        # st.write("")
        # st.write("")
        st.write('\n')
        st.write('\n')
        with st.expander("Key Metrics:"):
            KPI_2=key_metrics()
        st.markdown("""## <center><strong>:pushpin: :blue[Main Page] </strong></center>""", unsafe_allow_html=True)
        #st.write('\n')
        #st.write('\n')
        st.markdown(
                    '''
                    <style>
                    .streamlit-expanderHeader {
                    background-color: lightblue;
                    color: black; # Adjust this for expander header color
                    }
                    .streamlit-expanderContent {
                    background-color: lightwhitesmoke;
                    color: black; # Expander content color
                    }
                    '''
                    ,
                    unsafe_allow_html=True
                    )
        
        
            
        
        
        #st.divider()
        
        # with st.expander("Key Metrics:"):
        #     KPI_3=key_metrics()
            
        #st.divider()     
        
        markdown_conclusion=f""" As at <b>{df.iloc[0,0]}</b>, the perimeter comprised of <strong>{'{:,.0f}'.format(int(Per_product.loc['Total','Number of Facilities']))}
                                Facilities/Contracts</strong>."""
                                
       ##with a total contractual exposure of <b>{Per_product_formatted.iloc[-1,-1]}
       ##(€{(Per_product.iloc[-1,1]/1e9).round(2)}bn ContractOnBce)</b>.<br>                         
                                
        markdown_conclusion2=f""" The total average of <strong><code>{Per_product.columns[0]}</code></strong> was around <b>€{'{:,.0f}'.format(int(df.loc[:,'GrossLoanAmount'].mean()))}</b>
                                (<b>€{'{:,.0f}'.format(int(df_woz.loc[:,'GrossLoanAmount'].mean()))}</b> excluding <code> {(df['GrossLoanAmount']==0).sum(axis=0)}</code> zero values)."""
                                
        
        
        #st.markdown(markdown_conclusion, unsafe_allow_html=True)
        #st.markdown(markdown_conclusion2, unsafe_allow_html=True)
        #st.markdown(f"<u> Descriptive statistics of Perimeter as at <b><code>{df.iloc[0,0]}</code></b></u>:",unsafe_allow_html=True)
        
        

        df_stats = df[['GrossLoanAmount', 'LoanCollateralValue', 'PaymentDelayDays']]
# Dataframe display for summary report
        #st.write(df_stats.describe().applymap('{:,.2f}'.format).style.set_sticky(axis="index"))
        #st.dataframe(Per_NPL_flag_formatted)


        data_card = [["Total Gross Loan Amount",'€{:,.0f}'.format(df.loc[:, 'GrossLoanAmount'].sum())],
                      ["Total Provision Balance",'€{:,.0f}'.format(df.loc[:, 'GrossProvisionsAmount'].sum())],
                      ["Total Net Book Value",'€{:,.0f}'.format(df.loc[:, 'Contract_NBV'].sum())],
                      ["Total Net Book Value",'€{:,.0f}'.format(df.loc[:, 'Contract_NBV'].sum())],
                      ["Total Real Estate Collateral Legal Claim Value",'€{:,.0f}'.format(df.loc[:, 'LoanCollateralValue'].sum())],
                      #["Total OMV",'€{:,.0f}'.format(properties.loc[:, 'PopOMVfinal'].sum())],
                      ["Total Number of Facilities",'€{:,.0f}'.format(int(df['IndivIDC'].nunique()))],
                      ["Total Number of CIFs",'€{:,.0f}'.format(int(df['ClientIDC'].nunique()))],
                      #["Total Number of Properties",'€{:,.0f}'.format(properties.loc[:,'PropID'].nunique())]
                      ]
            # Other metrics ...
        
        kpi_card = pd.DataFrame(data_card)
        kpi_card = kpi_card.T.copy()
        kpi_card.columns=kpi_card.iloc[0]
        kpi_card=kpi_card.drop(kpi_card.index[0])
        
        kpi_card2=kpi_card.T.reset_index().copy()
        kpi_card2.columns = ['Metric', 'Value']
        
        
        df['Servicer/Bank'] = np.where(df['ClientDepRiskUnit'].isin(['DRU', 'AMU']), "Servicer", "Bank")

        Per_servicer_flag = df.groupby('Servicer/Bank', dropna=False)[['GrossLoanAmount','GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue']].sum()
        Per_servicer_flag['Number of Facilities'] = df.groupby('Servicer/Bank', dropna=False)[['IndivIDC']].count()
        Per_servicer_flag.loc['Total'] = Per_servicer_flag.sum()
        Per_servicer_flag['Number of Facilities'] = Per_servicer_flag['Number of Facilities'].astype(int)
        
        Per_servicer_flag = Per_servicer_flag.reset_index()
        Per_servicer_flag.iloc[:-1,:] = Per_servicer_flag.iloc[:-1,:].sort_values(by='GrossLoanAmount', ascending=False)
        Per_servicer_flag = Per_servicer_flag.set_index(Per_servicer_flag.columns[0])
        
        Per_servicer_flag_formatted = Per_servicer_flag.copy()
        # Per_servicer_flag_formatted.iloc[:,0:4] = Per_servicer_flag_formatted.iloc[:,0:4].apply(lambda x: x.map('€{:,0f}'.format))
        # Per_servicer_flag_formatted['Number of Facilities'] = Per_servicer_flag_formatted.apply(lambda x: '{:,}'.format(x['Number of Facilities']),axis=1)
        
        # Per_riskclass_flag = df.groupby('RiskClass', dropna=False)[['GrossLoanAmount','GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue']].sum()
        # Per_riskclass_flag['Number of Facilities'] = df.groupby('RiskClass', dropna=False)[['IndivIDC']].count()
        # Per_riskclass_flag.loc['Total'] = Per_servicer_flag.sum()
        # Per_riskclass_flag['Number of Facilities'] = Per_servicer_flag['Number of Facilities'].astype(int)
        
        # Per_riskclass_flag = Per_riskclass_flag.reset_index()
        # Per_riskclass_flag.iloc[:-1,:] = Per_riskclass_flag.iloc[:-1,:].sort_values(by='GrossLoanAmount', ascending=False)
        # Per_riskclass_flag = Per_riskclass_flag.set_index(Per_riskclass_flag.columns[0])
        
        # Per_risk
       
        
        # df['ex-CCB/Bank']=np.where(df['ContractexCCBFlg'].isin(['Y','W']),"ex-CCB","HB")
        # # Code related to 'Ex-CC/Bank'data processing
        # Per_xCCB_flag = df.groupby('ex-CCB/Bank', dropna=False)[['GrossLoanAmount','GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue']].sum()
        # Per_xCCB_flag['Number of Facilities'] = df.groupby('ex-CCB/Bank',dropna=False)[['IndivIDC']].count()
        # Per_xCCB_flag['GrossLoanAmount Percentage (%)']=Per_xCCB_flag['GrossLoanAmount']/Per_xCCB_flag['GrossLoanAmount'].sum()
        # Per_xCCB_flag.loc['Total'] = Per_xCCB_flag.sum()
        # Per_xCCB_flag['Number of Facilities'] = Per_xCCB_flag['Number of Facilities'].astype(int)
        
        # Per_xCCB_flag = Per_xCCB_flag.reset_index()
        # Per_xCCB_flag.iloc[:-1,:] = Per_xCCB_flag.iloc[:-1,:].sort_values(by='GrossLoanAmount', ascending=False)
        # Per_xCCB_flag = Per_xCCB_flag.set_index(Per_xCCB_flag.columns[0])
        
        # Per_xCCB_flag_formatted = Per_xCCB_flag.copy()
        # Per_xCCB_flag_formatted.iloc[:,0:4] = Per_xCCB_flag_formatted.iloc[:,0:4].apply(lambda x: x.map('€{:,0f}'.format))
        # Per_xCCB_flag_formatted['Number of Facilities'] = Per_xCCB_flag_formatted.apply(lambda x: '{:,}'.format(x['Number of Facilities']),axis=1)

        bin_df_dpd_rev=bin_df_dpd.copy()
        bin_df_dpd_rev['GrossLoanAmount Percentage (%)']=bin_df_dpd['GrossLoanAmount Percentage (%)']/100
        
        bin_df_rev=bin_df.copy()
        bin_df_rev['GrossLoanAmount Percentage (%)']=bin_df['GrossLoanAmount Percentage (%)']/100
        
        top_10_v=df[['GroupIDC', 'GroupName', 'GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV']].sort_values('GrossLoanAmount', ascending=True).copy()
#number_top10 = st.number_input('Select number of top Group CIFs (out of df["ClientEconomicGroupId"].unique()) to view details based on Gross Loan Amount:', min_value=1, max_value=100)
        top_10_v['GrossLoanAmount (% of total)']=(top_10_v['GrossLoanAmount']/df['GrossLoanAmount'].sum())*100
        
        top_10_v=top_10_v.groupby(['GroupIDC', 'GroupName'])[['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV','GrossLoanAmount (% of total)']].sum()
        
        top_10_v = top_10_v.sort_values('GrossLoanAmount', ascending=True)
       
        top_10_download_v = top_10_v.tail(10).copy()
        top_10_download_v.iloc[:, -1] = top_10_download_v.iloc[:, -1]/100
        
        top_10_download_v.loc['Total']=top_10_download_v.sum()
        
        top_10_download_v2=pd.DataFrame(top_10_v.reset_index().tail(10)).set_index('GroupName')
        top_10_download_v2.iloc[:, -1] = top_10_download_v2.iloc[:, -1]/100
        
        top_10_download_v2.loc['Total']=top_10_download_v2.sum()
        top_10_download_v2=top_10_download_v2.iloc[:,1:]
        
        top_10_download_v2=pd.DataFrame(top_10_download_v2)
        # Dataframe styling for visual presentation
        
        dfs=[
            bin_df_rev.style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(bin_df_formatted)], slice(None))),
            bin_df_dpd_rev.style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(bin_df_dpd_formatted)], slice(None))),
            
            # Applying styling to various dataframes based on conditions
            Per_product_ultra3.reset_index().style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(Per_product_ultra3_formatted)-1], slice(None))),
            Per_product.reset_index().style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(Per_product_formatted)-1], slice(None))),
            
            
            #Per_servicer_flag.reset_index().style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(Per_servicer_flag_formatted)-1], slice(None))),
            Per_risk.reset_index().style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(Per_risk)-1], slice(None))),
            Per_NPL_class.reset_index().style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(Per_NPL_class)-1], slice(None))),
            #Per_Terminated_flag.reset_index().style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(Per_Terminated_flag_formatted)-1], slice(None))),
            ##Per_xCCB_flag.reset_index().style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(Per_xCCB_flag_formatted)-1], slice(None))),
            #land_type.reset_index().iloc[:,:-1].sort_values(by=['PropOMVfinal']).style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(land_type_formatted)-1], slice(None))),
            #land_type2.reset_index().iloc[:,:-1].sort_values(by=['PropOMVfinal']).style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(land_type_formatted2)-1], slice(None))),
            top_10_download_v2.reset_index().style.applymap(lambda _: 'background-color: LightSkyBlue;', subset=([len(top_10_download_v)-1], slice(None)))]
            
        # Report download functionality for summary report
        multiple_dfs(dfs,'Summary tables','Summary report_',1)
        
    # with tab4:
    #     st.write('\n')
        
    #     st.markdown('''
    #                 <style>
    #                 .streamlit-expanderHeader {
    #                 background-color: lightblue;
    #                 color:black; # Adjust this for expander header color
    #                 }
    #                 .streamlit-expanderContent {
    #                 background-color: lightwhitesmoke;
    #                 color:black; # Expander content color
    #                 }
    #                 '''
    #                 ,
    #                 unsafe_allow_html=True
    #                 )
        
    #     with st.expander("Key Metrics:"):
    #         KPI_1=key_metrics()
            
    #     st.divider()     
        
        
    #     col1, col2, col3 = st.columns(3)
    #     with col1:
    #         option = st.toggle(
    #             'View raw data sample',
               
    #             help="First 10 rows are shown for reference", key='Raw data section'
    #         )
        
    #     if option:
    #         contracts_sample = df.head(10)
    #         st.write("")
    #         contracts_sample.iloc[:,0]=pd.to_datetime(contracts_sample.iloc[:,0]).dt.strftime('%d/%m/%Y')
    #         st.dataframe(contracts_sample)
        
    #     st.divider()  
    #     col1,col2,col3=st.columns([4.5,3,4])
        
    #     with col2:
    #         properties_checked = st.checkbox("👈 Click to view Property Data Analytics section")

          
    #     #     for col in borrowers_sample.select_dtypes(include=['datetime64[ns]']):
    #     #         # if filtered_reval[col]...
    #     #         borrowers_sample[col] = pd.to_datetime(borrowers_sample[col]).dt.strftime('%d/%m/%Y')
    #     #     st.dataframe(borrowers_sample)
    #     # elif option == 'Contracts':
    #     #     contracts_sample = df.head(10)
    #     #     for col in contracts_sample.select_dtypes(include=['datetime64[ns]']):
    #     #         # if filtered_reval[col]...
    #     #         contracts_sample[col] = pd.to_datetime(contracts_sample[col]).dt.strftime('%d/%m/%Y')
    #     #     st.dataframe(contracts_sample)
    #     # elif option == 'Properties':
    #     #     st.dataframe(properties.head(10))
    #     # elif option == 'RE Collateral':
    #     #     st.dataframe(re_collateral.head(10))
        
    #     st.divider()
        
    #     if properties_checked:
    #         st.markdown("<div id='linkto_top'></div>",unsafe_allow_html=True)
    #         st.write("")
    #         st.write("")
    #         st.write("")
            
    #         col1,col2,col3=st.columns([5.5,4,4])
            
    #         with col2:
    #             st.header(":blue[Graphical Analysis]")
    #             st.write("")
    #             st.write("")
    #             st.write("")
    #             st.write("")
                
    #         col1,col2=st.columns(2)     
            
            
    #         with col1:
    #             bar_pie = st.radio("📊 Select type of graphs", ["Bar charts", "Pie charts"], horizontal=True)
    #             # cmap = plt.cm.get_cmap('RdYlGn')
    #             # ranking_df = land_type_formatted.style.background_gradient(cmap=cmap, vmin=0, vmax=10, subset='Ranking')
            
    #             # fig8 = px.bar(land_type.reset_index().iloc[:,:], y='PropLanType', x='PropOMVfinal', title='Property Market Value (PropOMV) per Land Type',
    #             #               color='PropLanType', orientation='h',  
                              
    #             #               hover_data=['PropOMVfinal', 'Number of Properties', 'Percent (% PropOMVFinal)', 'Percent (% Number of Properties)'])
                
    #             #fig8.update_layout(title_x=0, yaxis={'categoryorder': 'total ascending'})
                
    #             ### AN DEN DOULEFKEI TO ORIGINAL EN I PANW GRAMMI FYGE TIS ALLES 2
    #             # fig8.update_layout(title_x=0, yaxis={'categoryorder': 'total ascending'}, template='plotly_white',
    #             #                     legend_title_text='PropLandType')
    
    
    #             # fig8.update_traces(texttemplate='€%{x:,.0f}')
    #             # fig8.update_layout(width=800, height=600, dragmode='select',
    #             #                    legend=dict(title='PropLanType', orientation='h'), plot_bgcolor='rgba(0,0,0,0)')
                
                
                
    #             # fig44_pie2 = px.pie(land_type.iloc[:-1,:], values='PropOMVfinal', names=land_type.index[:-1], 
    #             #                     custom_data=['PropOMVfinal'],hole=.4,title="Property Market Value (PropOMVfinal) per Land Type")
    #             # fig44_pie2.update_traces(textposition='inside', textinfo='value+percent+label', 
    #             #                          texttemplate='%{label}''<br>%{percent:,.2%}''<br>€%{customdata:,.0f}',
    #             #                          hovertemplate='PropOMVfinal: €%{customdata:,.0f}')
    #             # fig44_pie2.update_layout(title_x=0)
                
                
    #             # if bar_pie=='Bar charts':
    #             #     st.plotly_chart(fig8)
    #             # else:
    #             #     st.plotly_chart(fig44_pie2)
                    
    #             #st.dataframe(land_type_formatted)
    #             min_max_method = """
    #                         <div class="alert alert-block alert-info">
    #                         <b> Min-Max normalization</b> is a data scaling technique that transforms values within a specified range
    #                         (typically 0 to 1) by subtracting the minimum value and dividing by the range od the data (max-min).
                            
    #                         """
    #             # land_type_formatted['Ranking']=land_type_formatted['Ranking'].astype(float)
                
    #             # fig_table = go.Figure(data=[go.Table(columnwidth = [5.4, 4,3,2,5,3.2,4,2],
    #             #                 header=dict(values=list(land_type_formatted.reset_index().columns),
    #             #                 fill_color='paleturquoise',
    #             #                 align='center'),
    #             #                 cells=dict(values=land_type_formatted.reset_index().iloc[:,].Τ.values,
    #             #                 fill_color=['lavender','whitesmoke'],format=["","","","","","",".3f"],
    #             #                 align='center',height=30),
    #             #                 )])
                                
                                            
                               
    #             # fig_table.update_layout(height=510, width=800, title="Property Market Value (PropOMV) per Land Type", title_x=0.3)
    #             # min_max_method2= """ NOTE: The values shown in the 'PropOMVFinal (%)'column in the table below are based in the 
    #             #                   <b><mark>max-min normalization (scaling)*</mark></b> method and consists in rescaling the range
    #             #                   of <code>Average PropOMVfinal</code>."""
                                  
                                  
                                  
               
    #             min_max_method3 = """

    #                     <div class="alert alert-block alert-info">
    #                     <b><mark>*Min - Max normalization</mark></b> is a data scaling technique that transforms values within a specified range
    #                     (typically 0 to 1) by subtracting the minimum value and dividing by the range of the data (max - min).
    #                     """

    #             # with st.expander("View data in table format:"):
    #             #     st.write("")
    #             #     st.write("")
    #             #     st.markdown(min_max_method2, unsafe_allow_html=True)
    #             #     st.write("")
    #             #     #st.plotly_chart(fig_table)
    #             # #land_type_formatted[land_type_formatted.index()].style.background_gradient(cmap='RdYlGn', vmin=0, vmax=10, subset='Ranking')
    #             #     st.dataframe(land_type_formatted.reset_index().style.applymap(
    #             #         lambda _:"background-color:LightSkyBlue;",subset=([len(land_type_formatted)-1],slice(None))
    #             #         ).background_gradient(cmap='RdYlGn', vmin=0, vmax=10, subset='Ranking'),hide_index=True)
    #             #     st.write(min_max_method3, unsafe_allow_html=True)
                
    #             #     buffer = io.BytesIO()
    #             #     current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #             #     str_current_datetime = str(current_datetime)
    #             #     file_export_name = "exported_data_" + str_current_datetime + ".xlsx"
                    
    #             #     with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    #             #         land_type_formatted.reset_index().style.applymap(
    #             #             lambda _: 'background-color: LightSkyBlue;', subset=([len(land_type_formatted)-1], slice(None))
    #             #         ).background_gradient(cmap='RdYlGn', vmin=0, vmax=10, subset='Ranking').to_excel(writer, sheet_name='exported_data', index=None)
    #             #         writer.close()
                    

    #             #     st.download_button('Download table to excel', data=buffer, file_name=file_export_name, mime='application/vnd.ms-excel', key="table6")
                    
    #         with col2:
    #                 bar_pie2 = st.radio("📊 Select type of graph:", ["Bar charts", "Pie charts"], horizontal=True)
                    
    #                 # fig9 = px.bar(land_type2.iloc[:, :], x=land_type2.index[:], y='PropOMVfinal', title='Property Market Value (PropOMV) per Location District',
    #                 #               color=land_type2.index[:],orientation='v', hover_data=['PropOMVfinal', 'Number of Properties'])
    #                 # fig9.update_layout(title_x=0, xaxis={'categoryorder':'total ascending'})
    #                 # fig9.update_yaxes(title='Property Market Value (PropOMVFinal) per District')
    #                 # fig9.update_traces(texttemplate='€%{y:,.0f}')
    #                 # fig9.update_layout(width=800, height=600, dragmode='select',
    #                 #                    legend=dict(title='Location District', orientation='h'))
                    
    #                 # fig44 = px.pie(land_type2.iloc[-1:,:], values='PropOMVfinal', names=land_type2.index[:-1], custom_data=['PropOMVfinal'], hole=.4,
    #                 #                     title="Property Market Value (PropOMVFinal) per District")
    #                 # fig44.update_traces(textposition='inside', textinfo='value+percent+label',texttemplate='%{label}''<br>%{percent:,.2%}''<br>€%{customdata:,.0f}',
    #                 #                          hovertemplate='PropOMVfinal:€%{customdata:,.0f}')
    #                 # fig44.update_layout(title_x=0)
                    
    #                 # if bar_pie2 == 'Bar charts':
    #                 #     st.plotly_chart(fig9)
    #                 # else:
    #                 #     st.plotly_chart(fig44)
                    
    #                 # # Plotly Go table
    #                 # fig_table2 = go.Figure(data=[go.Table(
    #                 #     columnwidth = [3, 2, 2],
    #                 #     header=dict(values=list(land_type_formatted2.reset_index().columns),
    #                 #                 fill_color='paleturquoise',
    #                 #                 align='center'),
    #                 #     cells=dict(values=[land_type_formatted2.reset_index().iloc[:, :].T.values],
    #                 #                fill_color=['lavender','whitesmoke'],
    #                 #                align='center', height=30)
    #                 # )])
    #                 # fig_table2.update_layout(height=550, width=700, title="Property Market Value (PropOMV) per Location District", title_x=0.3)
                    
    #                 # with st.expander("View data in table format:"):
    #                 #     st.write("")
    #                 #     st.write("")
                            
    #                 #     st.dataframe(land_type_formatted2.reset_index().style.applymap(
    #                 #             lambda _: 'background-color: LightSkyBlue;', subset=([len(land_type_formatted2)-1], slice(None))
    #                 #         ),hide_index=True)
                        
    #                 #     buffer = io.BytesIO()
    #                 #     current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #                 #     str_current_datetime = str(current_datetime)
    #                 #     file_export_name = "exported_data_" + str_current_datetime + ".xlsx"
                        
    #                 #     with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    #                 #             land_type_formatted2.reset_index().style.applymap(
    #                 #                 lambda _: 'background-color: LightSkyBlue;', subset=([len(land_type_formatted2)-1], slice(None))
    #                 #             ).to_excel(writer, sheet_name='exported_data', index=None)
    #                 #             writer.close()
                        
    #                 #             #st.download_button('Download selected data', data=csv_file, file_name='cifs_extract.csv', mime='text/csv')
    #                 #             st.download_button('📥 Download table to excel', data=buffer, file_name=file_export_name, mime='application/vnd.ms-excel', key="table5")
                        
    #                 #     # PropYearBuild
    #                 #     properties_hist = properties[properties['PropYearBuild']>0]
    #                 #     prop_histogram = px.histogram(properties_hist, x="PropYearBuild", y="PropOMVFinal", title="Property Market Value (PropOMVFinal) distribution per Year Build")
    #                 #     prop_histogram.update_layout(width=800, height=600, dragmode='select',
    #                 #                                  legend=dict(title='Location District', orientation='h'))
                        
    #                 #     #st.plotly_chart(prop_histogram)
    #         st.divider()
    #         col1, col2, col3 = st.columns([5, 5, 4])
    #         with col2:
    #             st.subheader(":blue[Distribution Graphs - Level 2 Analysis]") 

    #         st.write("")
    #         st.write("")
    #         col1, col2 = st.columns(2)
    #         # with col1:
    #         #     properties_scatter = px.scatter(properties, x=properties['PropLocationDistrict'], y=properties['PropOMVfinal'],
    #         #                                     color=properties['PropLanType'], title="Property Market Value (PropOMVFinal) per District and Land Type",
    #         #                                     custom_data=['PropOwnerCIF'], size=properties['PropOMVfinal'], size_max=60)
                                                
    #         #     properties_scatter.update_traces(texttemplate='€%{x:,.0f}',
    #         #                                      hovertemplate='District: %{y}</b><br>Property Owner CIF: %{customdata}<br>Value: %{x:,.0f}<extra></extra>')
    #         #     properties_scatter.update_layout(width=800, height=600, title_x=0.2,dragmode='select',
    #         #                                      legend=dict(title='Location District', orientation='h'))
    #         #     st.plotly_chart(properties_scatter)
    #         #     #TEST THE BELOW KATI THA KSEREI
    #         #     #st.plotly_chart(properties_scatter, use_container_width=True)
            
    #         # properties_3d = properties.copy()
    #         # properties_3d = properties_3d[properties_3d['PropYearBuild']>1900]
    #         # # Log y=True, log_z=True
    #         # fig_3d_prop = px.scatter_3d(properties_3d, x='PropLandArea', y=properties_3d['PropYearBuild'], z=properties_3d['PropOMVfinal'],
    #         #                             log_x=True,log_z=True,color="PropLanType",hover_name="PropID",
    #         #                             title="Property Market Value (PropOMVFinal) per Land Type", custom_data=['PropID'],
    #         #                             hover_template="<b>Land Area: %{x}</b><br>Year Build: %{y}</b><br>Property Market Value (PropOMVFinal): %{z}<extra></extra>")
    #         # fig_3d_prop.update_layout(title_x=0,width=800, height=800,dragmode='select',legend=dict(title='ProductType',orientation='h'))
    #         # #fig_3d_prop.update_traces(marker=dict(size=3))
    #         # #st.plotly_chart(fig_3d_prop, use_container_width=True)    

    #         # # properties_scatter2 = px.scatter(properties, x=properties['PropYearBuild'], y=properties['PropOMVfinal'],
    #         #                      custom_data=['PropLocationDistrict', 'PropLanType','PropOwnerCIF'],size=properties['PropOMVfinal'],size_max=60,
    #         #                      color=properties['PropLanType'], title="Property Market Value (PropOMVFinal) per Year Build and Location District",
    #         #                      hover_template="Year Build: %{x}<br>Location District: %{customdata[0]}<br>Land Type: %{customdata[1]}<br>Property Owner CIF: %{customdata[2]}<br>Value: €%{y:,.0f}<extra></extra>")
    #         # properties_scatter2.update_layout(width=800, height=600, title_x=0.2)
    #         # st.plotly_chart(properties_scatter2)
            
    #         #with col2:
    #             # properties_scatter4 = px.scatter(properties, x=properties['PropLandArea'], y=properties['PropOMVfinal'], log_x=True,
    #             #                                  custom_data=['PropLocationDistrict','PropLanType', 'PropOwnerCIF'],
    #             #                                  color=properties['PropLocationDistrict'],size=properties['PropOMVfinal'],size_max=60,
    #             #                                  title="Property Market Value (PropOMVFinal) per Land Area and Location District"
    #             #                             )
    #             # properties_scatter4.update_traces(texttemplate="€%{y:,.0f}",
    #             #                                   hover_template="Land Area: %{x}<br>Location District: %{customdata[0]}<br>Property Owner CIF: %{customdata[1]}<br>Value: €%{y:,.0f}<extra></extra>")
    #             # properties_scatter4.update_layout(width=800, height=600, title_x=0.2, dragmode='select',
    #             #                                   legend=dict(title='Location District', orientation='h'))
    #             # st.plotly_chart(properties_scatter4)
            
    #         # properties_scatter3 = px.scatter(properties, x=properties['PropYearBuild'], y=properties['PropOMVfinal'],
    #         #                                  custom_data=['PropLocationDistrict', 'PropLanType', 'PropOwnerCIF'],
    #         #                                  color=properties['PropLocationDistrict'], title="Property Market Value (PropOMVFinal) per Year Build and Location District")
                                             
    #         # properties_scatter3.update_traces(texttemplate="€%{y:,.0f}",
    #         #                                   hover_template="Year Build: %{x}<br>Location District: %{customdata[0]}<br>Land Type: %{customdata[1]}<br>Property Owner CIF: %{customdata[2]}<br>Value: €%{y:,.0f}<extra></extra>")
             
    #         # properties_scatter3.update_layout(width=800, height=600, title_x=0.2)
    #         # st.plotly_chart(properties_scatter3)    


    #with tab3:
        
            
        
        col1, col2, col3 = st.columns(3)
        with col1:
            option = st.toggle(
                'View raw data sample',
               
                help="First 10 rows are shown for reference", key='Raw data section main'
            )
        
        if option:
            contracts_sample = df.head(10)
            st.write("")
            contracts_sample.iloc[:,0]=pd.to_datetime(contracts_sample.iloc[:,0]).dt.strftime('%d/%m/%Y')
            st.dataframe(contracts_sample)
        
        st.divider()  
        
        # col1, col2, col3 = st.columns([4.5,3,4])
        
        # with col2:
        #     st.header(":pushpin: :blue[Main page]")
        #     #contracts_checked=st.checkbox("👈 Click to view Contract Data Analytics section")
        #     contracts_checked=True
        # st.divider()  
        
        
        contracts_checked=True
        #st.divider()
        #if st.checkbox("Click to view Contract data sample:", help="First 8 rows from the APS Data Tape Contracts tab are shown for reference"):
        # if option == 'Clients':
        #     st.dataframe(borrowers.head(10))
        # elif option == 'Contracts':
        #     st.dataframe(df.head(10))
        # elif option == 'Properties':
        #     st.dataframe(properties.head(10))
        # elif option == 'RE Collateral':
        #     st.dataframe(re_collateral.head(10))
        
        #st.divider()
        col1, col2, col3 = st.columns([2, 1, 2])
        # with col2:
        
        if contracts_checked:
            # hidden div with anchor
            st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)
            # st.write("")
            # st.write("")
            # st.write("")
            st.markdown("""### <center><strong>:pushpin: :blue[Top Clients Analysis] </strong></center>""", unsafe_allow_html=True)
            # col1, col2, col3 = st.columns([5, 4, 4])
            # with col2:
            #     st.subheader(":blue[Top Group CIFs Analysis]")
            
            #col1, col2,col5, col3 = st.columns([0.5, 5.5, 0.5,5.5])
            col2,col1,col3=st.columns([2,0.5,2])
            with col2:
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                #st.write("")
            
                top_10 = df[['GroupIDC', 'GroupName', 'GrossLoanAmount',
                                'GrossProvisionsAmount', 'Contract_NBV']].sort_values('GrossLoanAmount', ascending=False).copy()
            
                number_top = st.number_input(f"🔢 Select number of Top Group Clients (out of {df['GroupIDC'].nunique()}) to view details based on Gross Loan Amount:", 
                                             min_value=1, max_value=df['GroupIDC'].nunique(), value=10, step=1)
            
                top_10['GrossLoanAmount (% of total)'] = (top_10['GrossLoanAmount']/top_10['GrossLoanAmount'].sum())*100
                top_10=top_10.groupby(['GroupIDC','GroupName'])[['GrossLoanAmount','GrossProvisionsAmount',
                                                                                         'Contract_NBV','GrossLoanAmount (% of total)']].sum()
                
                
                
                #top_10.groupby(['GroupIDC', 'GroupName'])['GrossLoanAmount (% of total)'].sum()
            
                top_10=top_10.sort_values('GrossLoanAmount', ascending=False)
            
                top_10_formatted = top_10.copy()
            
                top_10_formatted['GrossLoanAmount (% of total)'] = top_10_formatted['GrossLoanAmount (% of total)'].apply(lambda x: '{:.2f}%'.format(x))
                top_10_formatted.iloc[:, 0:3] = (top_10_formatted.iloc[:, 0:3]/1000000).apply(lambda x: x.map( '€{:,.2f}M'.format))
                
                top_10_formatted=top_10_formatted.head(number_top)
                vl=df['ClientIDC'].value_counts()
                
                #top_10_formatted = top_10.copy()
                top_10_formatted=top_10_formatted.reset_index()
                top_10_formatted.index += 1
                
                top_10_download = top_10.head(number_top).copy()
                top_10_download['GrossLoanAmount (% of total)'] = top_10_download['GrossLoanAmount (% of total)']/100
                buffer = io.BytesIO()
                current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                str_current_datetime = str(current_datetime)
                file_export_name = "exported_data_" + str_current_datetime + ".xlsx"
                
                              
                customdata=['GroupIDC']
                order_funnel = top_10_formatted.iloc[:, 1].tolist()
                #st.write(order_funnel)
                fig_funnel = px.funnel(top_10_download.reset_index(), x='GrossLoanAmount', y='GroupName',
                                       custom_data=customdata, color='GroupName')
                                      
                fig_funnel.update_traces(texttemplate='<br>€%{x:.3s}',hovertemplate='<b></b>%{y}'+'<br>Gross Loan Amount: €%{x:,.0f}'+'<br>Group IDC: %{customdata[0]}')
                fig_funnel.update_yaxes(categoryorder='total descending')
                fig_funnel.update_layout(title=f'Top {number_top} Group Clients by Gross Loan Amount', legend=dict(x=0, y=-0.08, orientation="h"), title_x=0.5)
                #fig_funnel.update_layout(title='Top {number_top} Group CIFs by Gross Loan Amount', legend=dict(x=0.3, y=-0.2, orientation="h"), title_x=0.5)
                
                fig_funnel.update_layout(showlegend=False)
                # fig_funnel.update_traces(color='GroupIDC')
                                
                fig_area_group = px.treemap(top_10_download.reset_index(), path=[px.Constant("GroupName"), 'GroupName'], 
                            names='GroupIDC', values='GrossLoanAmount', custom_data=customdata)
                
                
                
                fig_area_group.data[0].hovertemplate = '<b></b>%{label}'+'<br>Gross Loan Amount: €%{value:.3s}'+'<br>Group IDC: %{customdata[0]}'
                fig_area_group.update_traces(texttemplate= '<b></b>%{label}'+'<br>Group Clients: %{customdata[0]}'+'<br>€%{value:.3s}')
                
                fig_area_group.update_layout(title=f"Top {number_top} Group Clients by Gross Loan Amount")
                
                funnel_treemap = st.radio("📊 Select type of graph:", ["Treemap chart", "Funnel chart"], horizontal=True, key='funnel_chart_or_treemap')
                
                if funnel_treemap == 'Treemap chart':
                    st.plotly_chart(fig_area_group, use_column_width='auto')
                    #st.plotly_chart(fig_area_group)
                else:
                    st.plotly_chart(fig_funnel, use_column_width='auto')
                    #st.plotly_chart(fig_funnel)
                
            with col3:
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.info(f"The :green[top {number_top} Group Clients] account for :red[{'{:,.2f}'.format(top_10['GrossLoanAmount (% of total)'].head(number_top).sum())} %] of Total Gross Loan Amount, totalling around :red[€{'{:,.2f}M'.format(top_10['GrossLoanAmount'].head(number_top).sum()/1000000)}] out of :red[€{'{:,.2f}M'.format(df['GrossLoanAmount'].sum()/1000000)}]")
                
                    #st.dataframe(top_10_formatted,hide_index=False)
                    #top_10_download.index+=1
                    top_10_download_df=top_10_download.reset_index()
                    top_10_download_df.index+=1
                    st.dataframe(top_10_download_df)
                    
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                         top_10_download.reset_index().to_excel(writer, sheet_name='exported_data', index=None)
                    #     writer.save()
                         writer.close()
                    # st.download_button('Download selected data', data=csv_file, file_name='cifs_export.csv', mime='text/csv')
                         st.download_button('💾 Download table to excel', data=buffer, file_name=file_export_name, mime='application/vnd.ms-excel', key="table1_f")
                         
                         # 📥⬇️💾▶︎ •၊၊||၊|။||||။‌‌‌‌‌၊|• 0:10 | Copy ...
                     
            st.divider()
            st.markdown("""### <center><strong>:pushpin: :blue[Portfolio Segmentation] </strong></center>""", unsafe_allow_html=True)
            # col1,col2,col3=st.columns([5,4,4])
                
            # with col2:
            #         st.header(":blue[Portfolio Segmentation]")
                    
            st.write("")
            st.write("")
            #col1, col3,col5, col2 = st.columns([0.5, 5.5, 0.5,5.5])
            col3,col1,col2=st.columns([2,0.25,2])
            with col3:
                    #bar_pie_bucket2 = st.radio("🔲 Select type of graph:", ["Bar charts", "Pie charts"], horizontal=True, key='bucket_bar_or_pie')
                    bin_show = st.selectbox("Select amount from dropdown list to show in graph:", 
                                            options=["GrossLoanAmount", "Number of Facilities", "Average Exposure"])    
                    
               
                    color_map={'GrossLoanAmount':'LightSkyBlue','Number of Facilities':'lightgreen',
                               'Average Exposure':'crimson','GrossLoanAmount Percentage (%)':'magenta'}
                    
                    color_graph=color_map[bin_show]
                    
                    bin_df_bar3=px.bar(bin_df, x="Gross Loan Amount Bucket", y=bin_show, title=f"{bin_show} per Gross Loan Amount Bucket",
                                       color='Gross Loan Amount Bucket')
                       #bin_df_bar3.update_traces(texttemplate="%{x}<br>%{y:.3s}")
                    if bin_show=="Number of Facilities":
                           bin_df_bar3.update_traces(texttemplate="<br>%{y:,.0f}")
                    else:
                           bin_df_bar3.update_traces(texttemplate="<br>€%{y:.5s}")
                    
                    bin_df_bar3.update_layout(title_x=0.35, legend=dict(y=-0.2,orientation="h",font=dict(size= 11)))
                    #
    
                    bin_df_pie=px.pie(bin_df.iloc[:-1, :], values=bin_show, names='Gross Loan Amount Bucket', hole=.35, title=f"{bin_show} per Bucket")
                    bin_df_pie.update_traces(textposition='inside', textinfo='value+percent+label', texttemplate= '%{label}''<br>%{value:,.0f}<br>%{percent:.2%}')
                    bin_df_pie.update_layout(title_x=0.35)
                        
                    #bar_pie_bucket2="Bar charts"
                    
                    st.plotly_chart(bin_df_bar3, use_container_width=True)
                    bin_df_download=bin_df.copy()
                    bin_df_download['GrossLoanAmount Percentage (%)']=bin_df_download['GrossLoanAmount Percentage (%)']/100
                    
                    
                
            with col2:
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    
                    bin_df_bar_dpd=px.bar(bin_df_dpd, x="Payment Delay Days Bucket", y=bin_show, title=f"{bin_show} per Payment Delay Days Bucket", color="Payment Delay Days Bucket")
                    
                
                    if bin_show=="Number of Facilities":
                        bin_df_bar_dpd.update_traces(texttemplate='<br>%{y:,.0f}')
                    else:
                        bin_df_bar_dpd.update_traces(texttemplate='<br>€%{y:,.5s}')
                        
                
                
                    bin_df_bar_dpd.update_layout(title_x=0.35, legend=dict(y=-0.2,orientation="h",font=dict(size= 11)))
                    #,font=dict(size= 15)
                    st.plotly_chart(bin_df_bar_dpd,use_container_width=True)
                     #use_column_width='auto'
            
                    
            #colbl2,col2a,colbl,col2b,colbl3=st.columns([0.5,10,1.4,10,0.5])
            col3t,col1t,col2t=st.columns([2,0.25,2])
            with col3t:
                with st.expander("**View data in tabular format:**"):
                    st.write("")
                    
                    st.markdown("<strong> Gross Loan Amount and Number of Facilities per Bucket:</strong>",unsafe_allow_html=True)
                    st.dataframe(bin_df_formatted,hide_index=True)
                    # st.dataframe(bin_df_download.style.map(
                    #     lambda _: "background-color:LightSkyBlue;",subset=([len(bin_df_formatted)],slice(None))
                    #     ),hide_index=True)
                    
                    
                        
                                    
                    buffer = io.BytesIO()
                    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    str_current_datetime = str(current_datetime)
                    file_export_name = "exported_data_" + str_current_datetime + ".xlsx"
                        
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            bin_df_download.style.applymap(
                                lambda _: 'background-color: LightSkyBlue;', subset=(len(bin_df_formatted), slice(None))
                            ).to_excel(writer, sheet_name='exported_data', index=None)
                            #writer.save()
                            writer.close()
                            st.download_button('💾 Download table to excel', data=buffer, file_name=file_export_name, mime='application/vnd.ms-excel', key="table1")
                
            
            with col2t:
                    with st.expander("**View data in tabular format:**"):
                        st.write("")
                    
                        st.markdown("<strong>Gross Loan Amount and Number of Facilities per Payment Delay Days buckets:</strong>", unsafe_allow_html=True)
                        st.dataframe(bin_df_dpd_formatted,hide_index=True)
                        
                        # st.dataframe(bin_df_dpd_formatted.style.map(
                        #     lambda _: 'background-color: LightSkyBlue;', subset=([len(bin_df_dpd_formatted)], slice(None))
                        #     ),hide_index=True)
                        bin_df_dpd_download=bin_df_dpd.copy()
                        
                        
                        bin_df_dpd_download['GrossLoanAmount Percentage (%)'] = bin_df_dpd_download['GrossLoanAmount Percentage (%)']/100
                        
                        
                        
                        buffer = io.BytesIO()
                        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        str_current_datetime = str(current_datetime)
                        file_export_name = "exported_data_" + str_current_datetime + ".xlsx"
                    
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            bin_df_dpd_download.style.applymap(
                                lambda _: 'background-color: LightSkyBlue;', subset=(len(bin_df_dpd_formatted), slice(None))
                            ).to_excel(writer, sheet_name='exported_data', index=None)
                            writer.close()
                            st.download_button('💾 Download table to excel', data=buffer, file_name=file_export_name, mime='application/vnd.ms-excel', key="table_dpd_bucket1")
                
                
            
            st.divider()
            st.markdown("""### <center><strong>:pushpin: :blue[Consolidated Graphical Analysis] </strong></center>""", unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            
            # col1,col2,col3=st.columns([5.5,4,4])
                
            # with col2:
            #         st.header(":blue[Graphical Analysis]")
            #         st.write("")
            #         st.write("")
            #         st.write("")
            #         st.write("")
            col3b,colbl,col4b=st.columns([2,0.25,2])
            with col3b:           
                st.plotly_chart(NPL_pie,use_container_width=True)
                
                with st.expander("**View data in tabular format:**"):
                        st.dataframe(Per_NPL_class_formatted)
                        
            with col4b:    
                    st.plotly_chart(riskclass_pie,use_container_width=True)
                    with st.expander("**View data in tabular format:**"):
                        st.dataframe(Per_risk_formatted)
            
            st.divider()            
            col1,colbl,col2=st.columns([2,0.25,2]) 
                
            with col1:
                    select2 = st.radio("Select amount to view in the bar chart:",
                               options=['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue'],
                               horizontal=True, key='right_button_radio')
                
            with col2:
                    select3 = st.radio("Select amount to view in the bar chart:",
                               options=['GrossLoanAmount', 'GrossProvisionsAmount', 'Contract_NBV', 'LoanCollateralValue'],
                               horizontal=True)
                
            col1,colbl,col2=st.columns([2,0.25,2]) 
            with col1:
                    fig3_x_cons_portfolio = px.bar(Per_product_ultra3.reset_index().iloc[:,:], y='ProductCategory',
                                                   x=select2,title=f"""{select2} Amount per Portfolio Type""",color='ProductCategory')
                
                # Consolidated Plot
                    fig3_x_cons_portfolio.update_layout(autosize=False,width=800, height=500,yaxis={'categoryorder':'total ascending'},legend=dict(orientation='h'))
                    fig3_x_cons_portfolio.update_traces(texttemplate='€%{x:,.5s}',hovertemplate='Type: %{y} <br>Value: €%{x:,.0f} <extra></extra>')
                    
                    st.plotly_chart(fig3_x_cons_portfolio, use_container_width=True)
                    
                    with st.expander("**View data in tabular form**"):
                        st.write("\n")
                        st.dataframe(Per_product_ultra3_formatted.reset_index().style.applymap(
                            lambda _: 'background-color: LightSkyBlue;', subset=([len(Per_product_ultra3_formatted)-1], slice(None))
                        ),hide_index=True)
                    
                        buffer = io.BytesIO()
                        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        str_current_datetime = str(current_datetime)
                        file_export_name = "exported_data_" + str_current_datetime + ".xlsx"
                        
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            Per_product_ultra3_formatted.reset_index()[::1].style.applymap(
                                lambda _: 'background-color: LightSkyBlue;', subset=([len(Per_product_ultra3_formatted)-1], slice(None))
                            ).to_excel(writer, sheet_name='exported_data', index=None)
                        #writer.save()
                            writer.close()
                        
                        #st.download_button('Download selected data', data=csv_file, file_name='cifs_streamlit.csv', mime='text/csv')
                            st.download_button('📊 Download table to excel', data=buffer, file_name=file_export_name, mime="application/vnd.ms-excel", key="table2")
                            
                        
            with col2:
                    
                    fig = px.bar(Per_product.reset_index().iloc[:,:], y='ProductType', x=select3, 
                                 custom_data=['Number of Facilities'],title=f"{select3} Amount per Product Type",
                                 color='ProductType', orientation='h', width=800, height=500)
        
                    fig.update_layout(yaxis={'categoryorder':'total ascending'},legend=dict(orientation='h'))
                    fig.update_yaxes(title='Contract Product Type')
                    fig.update_traces(texttemplate='€%{x:.5s}', 
                                      hovertemplate='Type: %{y} <br>Value: €%{x:,.0f} <br>Number of Facilities: %{customdata:,.0f}<extra></extra>')
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    with st.expander("**View data in tabular form**"):
                        st.write("\n")
                        st.dataframe(Per_product_formatted.reset_index().style.applymap(
                            lambda _: 'background-color: LightSkyBlue;', subset=([len(Per_product_formatted)-1], slice(None))
                        ),height=(len(Per_product_formatted.index)+1)*35+3,hide_index=True)
                    
                        buffer = io.BytesIO()
                        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        str_current_datetime = str(current_datetime)
                        file_export_name = "exported_data_" + str_current_datetime + ".xlsx"
                        
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            Per_product_formatted.reset_index().style.applymap(
                                lambda _: 'background-color: LightSkyBlue;', subset=([len(Per_product_formatted)-1], slice(None))
                            ).to_excel(writer, sheet_name='exported_data', index=None)
                        #writer.save()
                            writer.close()
                        
                        #st.download_button('Download selected data', data=csv_file, file_name='cifs_streamlit.csv', mime='text/csv')
                            st.download_button('📊 Download table to excel', data=buffer, file_name=file_export_name, mime="application/vnd.ms-excel", key="table3")
                            
            st.divider()
            st.info("Double-click on legend to isolate specific option in the graph.")
                
            col3,colspace,col4=st.columns([2,0.25,2])
                
            with col3:
                    
                    st.plotly_chart(fig_long_portfolio_cd_1,use_container_width=True)
                    
                    
                    
                    
                    fig_DPD_scatter_portfolio=px.scatter(df,x='GrossLoanAmount',y=df['PaymentDelayDays'],
                                                         log_x=True,color='ProductCategory',hover_name='ClientIDC',
                                                         title="Payment Delay Days vs  GrossLoanAmount dispersion - Scatter Plot")
                    
                    
                    
                    fig_DPD_scatter_portfolio.update_layout(title_x=0)
                    
                    fig_DPD_scatter_portfolio.update_traces(selectedpoints=None,
                                                            unselected=dict(marker=dict(opacity=0.2)),
                                                            selected=dict(marker=dict(opacity=1)),
                                                            selector=dict(type='box'))
                    
                    fig_DPD_scatter_portfolio.update_layout(dragmode='select',
                                                            legend=dict(title='ProductType',orientation='h'),height=650,width=800)
                    
                    fig_DPD_scatter_portfolio.update_traces(texttemplate='%{x:,.0f}') #textfont_color='black'
                    
            with col4:
                    df_exp_g=df_exp.iloc[:,:-3]
                    df_long1=pd.melt(df_exp_g, id_vars=['ProductType'], var_name='Column', value_name='Value')
                    
                    fig_long1=px.bar(df_long1, y='ProductType',x='Value', color='ProductType',
                                     orientation='h',facet_col='Column', facet_col_wrap=2, text='Value')
                    
                    fig_long1.update_traces(texttemplate='€%{x:.5s}',hovertemplate='Type: %{y} <br> Value: €%{x:,.0f} <extra> </extra>')
                    
                    fig_long1.update_layout(title_text='Gross Loan Amount, Provisions, Net Book Value & Loan Collateral Value per Product Type',
                                                          legend=dict(orientation='h'))
                    fig_long1.for_each_annotation(lambda ann: ann.update(text=ann.text.split("=")[-1]))
                    
                    st.plotly_chart(fig_long1,use_container_width=True)
                    #st.write("")
                    
            
            
                    
            st.divider()
            
            #with st.expande("")
            st.markdown("""### <center><strong>:pushpin: :blue[Distribution Graphs - Level 2 Analysis] </strong></center>""", unsafe_allow_html=True)
            # col1, col2, col3=st.columns([5,5,4])
            # with col2:
            #         st.subheader(":blue[Distribution Graphs - Level 2 Analysis]")
                    
            dist1,distsp, dist2=st.columns([2,0.25,2])
                
            with dist1:
                        select_hist=st.radio("Select variable to view in the graphs:", 
                                         options=['GrossLoanAmount', 'LoanCollateralValue'],horizontal=True)
                
                    #if select_hist=='GrossLoanAmount':
                        fig5_portfolio2 = px.box(df_woz, y=select_hist, x=df_woz['ProductCategory'],
                                                 log_y=True,points="all",color='ProductCategory',
                                                 hover_name='ClientIDC', title=f"{select_hist} distribution - Box Plot (excluding zero values)",height=620)
                            
                        #log_y=True,
                        # fig5_portfolio2 = px.box(df, y=select_hist, x=df['ProductCategory'],log_y=True,points="all",color='ProductCategory',
                        #                           hover_name='ProductCategory', title=f"{select_hist} distribution - Box Plot",height=620)
                                                 
                        fig5_portfolio2.update_layout(title_x=0,height=650,width=800)
                        fig5_portfolio2.update_traces(selectedpoints=None,
                                                      unselected=dict(marker=dict(opacity=0.2)),
                                                      selected=dict(marker=dict(opacity=1)),
                                                      selector=dict(type='box'))
                                                      
                        fig5_portfolio2.update_layout(dragmode='select',
                                                      legend=dict(title='ProductCategory', orientation='h'))
                        #fig5_portfolio2.update_yaxes(range=[-3,9])
                        
                        fig5 = px.box(df_woz, y='GrossLoanAmount', x=df_woz['ProductType'],log_y=True,points="all",
                                      color='ProductType', hover_name='ClientIDC',
                                      title=f"{select_hist} per Product Type distribution - Box Plot (excluding zero values)")
                                      
                        fig5.update_layout(title_x=0,height=700,width=800)
                        fig5.update_traces(selectedpoints=None,
                                           unselected=dict(marker=dict(opacity=0.2)),
                                           selected=dict(marker=dict(opacity=1)),
                                           selector=dict(type='box'))
                                           
                        fig5.update_layout(dragmode='select',
                                           legend=dict(title='ProductType', orientation='h'))
                        #fig5.update_yaxes(range=[-3,9])
                        
                    # elif select_hist=='ContractOutsdgPrinc':
                    #         df_outstdg['ContractOutsdgPrinc'] = abs(df_outstdg['ContractOutsdgPrinc'])
                    #         fig5_portfolio2 = px.box(df_outstdg, y='ContractOutsdgPrinc', x=df_outstdg['ProductCategory'], log_y=True,
                    #                                  points="all", color='ProductCategory',
                    #                                  hover_name='ClientIDC', title=f"{select_hist} distribution - Box Plot (excluding zero values)", height=620)
                        
                    #         # fig5_portfolio2 = px.box(df, y=select_hist, x=df['ProductCategory'], log_y=True, points="all", color='ProductCategory',
                    #         #                           hover_name='ProductCategory', title=f"{select_hist} distribution - Box Plot", height=620)
                        
                    #         fig5_portfolio2.update_layout(title_x=0, height=650, width=800)
                    #         fig5_portfolio2.update_traces(selectedpoints=None,
                    #                                       unselected=dict(marker=dict(opacity=0.2)),
                    #                                       selected=dict(marker=dict(opacity=1)),
                    #                                       selector=dict(type='box'))
                        
                    #         fig5_portfolio2.update_layout(dragmode='select',
                    #                                       legend=dict(title='ProductType', orientation='h'))
                        
                    #         #fig5_portfolio2.update_yaxes(range=[-3,9])
                        
                    #         fig5 = px.box(df_outstdg, y='ContractOutsdgPrinc', x=df_outstdg['ProductType'], log_y=True, points="all",
                    #                       color='ProductType', hover_name='ClientIDC',
                    #                       title=f"{select_hist} per Product Type distribution - Box Plot (excluding zero values)")
                        
                    #         fig5.update_layout(title_x=0, height=650, width=800)
                    #         fig5.update_traces(selectedpoints=None,
                    #                            unselected=dict(marker=dict(opacity=0.2)),
                    #                            selected=dict(marker=dict(opacity=1)),
                    #                            selector=dict(type='box'))
                        
                    #         fig5.update_layout(dragmode='select',
                    #                            legend=dict(title='ProductType', orientation='h', yanchor='bottom', y=-0.4))
                    #         #fig5.update_yaxes(range=[-3,9])
                        
                    # else:
                    #         fig5_portfolio2 = px.box(df_dpd, y='PaymentDelayDays', x=df_dpd['ProductCategory'], log_y=True, points="all", color='ProductCategory',
                    #                                  hover_name='ClientIDC', title="PaymentDelayDays distribution - Box Plot (excluding zero values)", height=620)
                        
                    #         # fig5_portfolio2 = px.box(df, y=select_hist, x=df['ProductCategory'], log_y=True, points="all", color='ProductCategory',
                    #         #                           hover_name='ProductCategory', title=f"{select_hist} distribution - Box Plot", height=620)
                        
                    #         fig5_portfolio2.update_layout(title_x=0, height=650, width=800)
                    #         fig5_portfolio2.update_traces(selectedpoints=None,
                    #                                       unselected=dict(marker=dict(opacity=0.2)),
                    #                                       selected=dict(marker=dict(opacity=1)),
                    #                                       selector=dict(type='box'))
                        
                    #         fig5_portfolio2.update_layout(dragmode='select',
                    #                                       legend=dict(title='ProductType', orientation='h'))
                    #         #fig5_portfolio2.update_yaxes(range=[-3,9])   
                    #         fig5 = px.box(df_dpd, y=select_hist, x=df_dpd['ProductType'], log_y=True, points="all",
                    #                       color='ProductType', hover_name='ClientIDC',
                    #                       title=f"{select_hist} per Product Type distribution - Box Plot (excluding zero values)")
                        
                    #         fig5.update_layout(title_x=0, height=650, width=800)
                    #         fig5.update_traces(selectedpoints=None,
                    #                            unselected=dict(marker=dict(opacity=0.2)),
                    #                            selected=dict(marker=dict(opacity=1)),
                    #                            selector=dict(type='box'))
                        
                        
                    #         #### Comment the below two lines
                    #         fig5.update_layout(dragmode='select',
                    #                            legend=dict(title='ProductType', orientation='h', yanchor='bottom', y=-0.4))              
                            
                            
                            
                        st.plotly_chart(fig5_portfolio2,use_container_width=True)                                        
                                                            
                                                            
                                            
            with dist2:
                    st.write('\n')
                    st.write('\n')
                    st.write('\n')
                    st.write('\n')
                    st.write('\n')
                    
                    st.plotly_chart(fig5,use_container_width=True)

                    fig_DPD_hist=px.scatter(df, x='GrossLoanAmount', y=df['PaymentDelayDays'], log_x=True, color='ProductType',
                                            hover_name='ClientIDC', title="Payment Delay Days vs  GrossLoanAmount dispersion - Scatter Plot")
                    fig_DPD_hist.update_layout(title_x=0)
                    fig_DPD_hist.update_traces(selectedpoints=None,
                                               unselected=dict(marker=dict(opacity=0.2)),
                                               selected=dict(marker=dict(opacity=1)),
                                               selector=dict(type='box'))
                    fig_DPD_hist.update_layout(dragmode='select',
                                               legend=dict(title='ProductType', orientation='h'), height=650, width=800)
                    fig_DPD_hist.update_yaxes(title='PaymentDelayDays')
                    fig_DPD_hist.update_xaxes(title='GrossLoanAmount', tickfont_color='black')
                    
                    df_3d=df[df['GrossLoanAmount']>100000]
                    df_3d=df.copy()
                    
                    fig_3d = px.scatter_3d(df_3d, x='PaymentDelayDays', y=df_3d['GrossLoanAmount'], z=df_3d['LoanCollateralValue'],
                                           color='ProductType', hover_name='ClientIDC',
                                           log_x=True, log_y=True, log_z=True, title="3D Scatter Plot")
                    fig_3d.update_layout(title_x=0, height=800, width=650)
                    fig_3d.update_layout(dragmode='select',
                                         legend=dict(title='ProductType', orientation='h'))
                    
                    #st.plotly_chart(fig_3d)
                    
            st.divider()
            col6,colsp,col7=st.columns([2,0.25,2])
                
            select_hist_radio = st.radio('Select amount to view in the histograms:', 
                             options=['GrossLoanAmount', 'GrossProvisionsAmount', 
                                      'Contract_NBV', 'LoanCollateralValue'], 
                             horizontal=True)

            with col6:
                    st.plotly_chart(fig_DPD_scatter_portfolio,use_container_width=True)
                    select_portfolio_type=st.selectbox("Select portfolio type:",options=df['ProductCategory'].unique())
                    df_selected_portfolio_type=df[df['ProductCategory']==select_portfolio_type]
                    
                    
                    df_median_portfolio=df_selected_portfolio_type[df_selected_portfolio_type[select_hist_radio]!=0]
                    
                    fig_hist_port2 = px.histogram(df_selected_portfolio_type, x=select_hist_radio, color="ProductCategory")
                    
                    fig_hist_port2.update_traces(xbins=dict(
                            start=df_selected_portfolio_type[select_hist_radio].min(),
                            end=df_selected_portfolio_type[select_hist_radio].max(),
                            size=df_selected_portfolio_type[select_hist_radio].std()/4))
                            #size=(df_selected_portfolio_type[select_hist_radio].max() - df_selected_portfolio_type[select_hist_radio].min()) / df_selected_portfolio_type[select_hist_radio].std()/4))
                    fig_hist_port2.update_layout(autosize=False, width=800, height=550,
                                                 title=f"{select_hist_radio} histogram per Portfolio Type",
                                                 title_x=0, legend=dict(
                                                 orientation='h'))
                    
                    if df_selected_portfolio_type[select_hist_radio].sum()==0:
                        st.warning("No graph to show for selected amount.")
                    else:
                        st.plotly_chart(fig_hist_port2,use_container_width=True)
                    
            with col7:
                        st.plotly_chart(fig_DPD_hist,use_container_width=True)
                        select_product_type=st.selectbox("Select product type:", options=df['ProductType'].unique())
                        df_selected_product_type=df[df['ProductType']==select_product_type]
                        
                        df_median=df_selected_product_type[df_selected_product_type[select_hist_radio]!=0]
                        
                        fig_hist2 = px.histogram(df_selected_product_type, x=select_hist_radio, color="ProductType")
                        
                        fig_hist2.update_traces(xbins=dict(
                                start=df_selected_product_type[select_hist_radio].min(),
                                end=df_selected_product_type[select_hist_radio].max(),
                                size=df_selected_product_type[select_hist_radio].std()/4))
                                #size=(df_selected_portfolio_type[select_hist_radio].max() - df_selected_portfolio_type[select_hist_radio].min()) / df_selected_portfolio_type[select_hist_radio].std()/4))
                        fig_hist2.update_layout(autosize=False, width=800, height=550,
                                                     title=f"{select_hist_radio} histogram per Portfolio Type",
                                                     title_x=0, legend=dict(
                                                     orientation='h'))
                        
                        
                        
                        if df_selected_product_type[select_hist_radio].sum()==0:
                            st.error(f" ⚠️ {select_product_type} have zero {select_hist_radio} values. No graph to show. Please select different product type or amount.")
                        else:
                            st.plotly_chart(fig_hist2,use_container_width=True)
                    
                    # As an html button (needs styling added)
            st.markdown("<a href='#linkto_top'><center> Link to top</a>", unsafe_allow_html=True)
                
                
                    
                    #select_hist=st.selectbox() and st.radio() widgets configuration
                    
    with tab1:
        form_check=False
    
        export_type=st.radio("Export data based on:",['CIFs','Filtered Values'], horizontal=True)
        if export_type=='CIFs':
            st.info("In this section you can filter and export data from the dataset based on specific Client IDCs or Group IDCs.")
            #manual_input=st.toggle("Input CIFs manually")
            
            #if manual_input:
            group_or_cif=st.radio("Filter data based on:",['Client IDCs','Group Client IDCs'],horizontal=False)
                
            with st.form("user_input"):
                    
                    group_cif=False
                    if group_or_cif=='CLient IDCs':
                        cif_check=st.multiselect(f"Type or select :blue[{group_or_cif}] from dropdown list:", df['ClientIDC'].unique())
                    else:
                        cif_check=st.multiselect(f"Type or select :blue[{group_or_cif}] from dropdown list:", df['GroupIDC'].unique())
                        group_cif=True
                    
                    fields=st.multiselect("Select fields from Data Tape:",df.columns)
                    submitted=st.form_submit_button(f"View data for selected :blue[{group_or_cif}]")
                    if submitted:
                        if group_cif:
                            matching_cifs=[cif for cif in cif_check if cif in df['GroupIDC'].values]
                        else:
                            matching_cifs=[cif for cif in cif_check if cif in df['ClientIDC'].values]
                        if matching_cifs:
                            if group_cif:
                                df_f=df.loc[df['GroupIDC'].isin(cif_check)]
                            else:
                                df_f=df.loc[df['ClientIDC'].isin(cif_check)]
                            fields2=['ReferenceDate','GroupIDC','ClientIDC','IndivIDC']
                            fields2=fields2+fields
                            fields2=list(set(fields2))
                            df_filtered=df_f[fields2]
                            
                            form_check=True
                        else:
                                st.error(f"No {group_or_cif} have been provided or {group_or_cif} is not in the Data Tape. Please try again.")
                                
            # else:                    
            #         with st.form("user_input_2"):
            #             cif_file=st.file_uploader("Upload Excel/CSV file with CIFs ")
            #             if cif_file is not None:
            #                 file_extension=cif_file.name.split('.')[-1]     
            #                 try:
            #                     if file_extension=='csv':
            #                         cif_check2=pd.read_csv(cif_file)
            #                     elif file_extension=='xlsx':
            #                         cif_check2=pd.read_excel(cif_file)
            #                     # elif file_extension=='txt':
            #                     #     cif_check=pd.read_csv(cif_file, delimiter='\t')
            #                 except Exception as e:
            #                     st.error(f"Error in reading file: {e}")
                            
            #                 cif_check2=pd.DataFrame(cif_check2).astype(str)
            #                 cif_check2.index+=1
                            
            #                 upload_message=f"You uploaded the below <strong><code>{len(pd.unique(cif_check2['ClientIDC']))}</code></strong> unique CIFs from the file <mark>{cif_file.name}</mark>:"
            #                 st.markdown(upload_message,unsafe_allow_html=True)
                        
            #                 transpose=pd.DataFrame(cif_check2.iloc[:,0].unique())
            #                 transpose.index+=1
            #                 #transpose_df=transpose(cif_check2)
            #                 transpose.index.names=['CIFs']
            #                 transpose=transpose.T
            #                 st.dataframe(transpose,hide_index=True)
                            
            #                 cif_check2=list(cif_check2.iloc[:,0].unique())
                         
            #                 found_in_file=df[df['ClientIDC'].isin(cif_check2),'ClientIDC'].unique()
            #                 found_in_file=pd.DataFrame(found_in_file)
            #                 found_in_file.index+=1
            #                 found_in_file.index.names=['CIFs']
            #                 found_in_file_transpose=found_in_file.T
                            
            #                 upload_message_found=f"<strong><code>{len(found_in_file)}</code></strong> CIFs :green[FOUND] in the Data Tape:"
            #                 st.markdown(upload_message_found,unsafe_allow_html=True)
            #                 st.dataframe(found_in_file_transpose,hide_index=True)
                            
            #                 transpose_v2=transpose.T.copy()
            #                 transpose_v2.index.names=['index']
            #                 transpose_v2.rename(columns={ transpose_v2.columns[0]: "CIFs" }, inplace=True)
                                          
                            
            #                 found_in_file_v2=found_in_file.transpose.T.copy()
            #                 found_in_file_v2.index.names=['index']
            #                 found_in_file_v2.rename(columns={ found_in_file_v2.columns[0]: "CIFs" }, inplace=True)
                            
            #                 not_found_in_file=transpose_v2.loc[~transpose_v2['CIFs'].isin(found_in_file_v2['CIFs']), 'CIFs'].unique()
            #                 not_found_in_file=pd.DataFrame(not_found_in_file)
            #                 not_found_in_file.index+=1
            #                 not_found_in_file.index.names=['index']
            #                 not_found_in_file.rename(columns={ not_found_in_file.columns[0]: "CIFs" }, inplace=True)
                            
            #                 not_found_in_file_transpose=not_found_in_file.T.copy()
                            
            #                 upload_message_not_found="<strong><code>{len(not_found_in_file)}</code></strong> CIFs were :red:[NOT FOUND] in the Datatape:"
            #                 st.markdown(upload_message_not_found, unsafe_allow_html=True)
            #                 st.dataframe(not_found_in_file_transpose,hide_index=True)
                            
            #                 not_found_in_file=set(cif_check2).intersection(found_in_file)
                            
            #                 fields=st.multiselect("Select fields from Data Tape:", df.columns)
                            
                            
            #             submitted=st.form_submit_button("View data for selected CIFs")    
                        
            #             if submitted:
            #                 if cif_file is None:
            #                     st.error("No CIF File has been provided or CIF/CIFs not in the Data Tape.")
            #                 else:
            #                     matching_cifs=[cif for cif in cif_check2 if cif in df['ClientIDC'].values]
            #                     if matching_cifs:
            #                         df_f=df.loc[df['ClientIDC'].isin(cif_check2)]
                        
                    
            #                         fields2=['ReferenceDate', 'GroupIDC', 'ClientIDC', 'IndivIDC', 'ContractCurrentCd']
            #                         fields2=fields+fields2
            #                         fields2=list(set(fields2))
                    
            #                         df_filtered=df_f[fields2]
            #                         form_check=True
            #                     else:
            #                         st.error("No CIF(s) have been provided or CIF/CIFs not in the Data Tape.")
                    
            if form_check:
                        #df_f['ReferenceDate']=pd.to_datetime(df_f['ReferenceDate'], format='%d/%m/%Y')
                        tags=['ReferenceDate', 'GroupIDC', 'ClientIDC', 'IndivIDC']
                        # order...
                        new_order=[col for col in df_filtered.columns if col not in tags] + tags
                        new_order=new_order[-4:] + new_order[:-4]
                    
                        df_filtered=df_filtered[new_order]
                        df_filtered=df_filtered.sort_values(by=['ClientIDC']).copy()
                        
                        for col in df_filtered.select_dtypes(include=['datetime64[ns]']):
                        
                            df_filtered[col]=pd.to_datetime(df_filtered[col]).dt.strftime('%d/%m/%Y')
                    
                        export_message=f"Data Tape data: <strong><code>{len(pd.unique(df_filtered['GroupIDC']))}</code></strong> unique Groups CIFs with <strong><code>{len(pd.unique(df_filtered['ClientIDC']))}</code></strong> unique CIFs:"
                        st.markdown(export_message, unsafe_allow_html=True)
                        
                        st.dataframe(df_filtered, hide_index=True)
                        
                        
                        
                        buffer = io.BytesIO()
                        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        str_current_datetime = str(current_datetime)
                        file_export_name = "exported_data_" + str_current_datetime + ".xlsx"
                        
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            df_filtered.to_excel(writer, sheet_name='exported_data', index=None)
                            #writer.save()
                            writer.close()
                            st.download_button('Download data in excel', data=buffer,
                                               file_name=file_export_name, mime="application/vnd.ms-excel")
                            
                            
        if (export_type=='Filtered Values'):
            st.info("In this section you can export data from the NPL Data Tape by filtering the below fields",icon="ℹ️")
            #if st.checkbox("Apply Filters"):
            form_check2=False
            with st.form("data_filtering"):
                    st.warning("Click on 'Refresh-Submit selected Filters'button below each time you change something to refresh data.")
                    
                    col1,col2,col3,col4=st.columns(4)
                    # conditions=[
                    #     (df['ContractLegalFlg']=='F'),
                    #     (df['ContractLegalFlg'].isin(['B','R','N',''])) & (df['ContractLegalFlg'].isna())]
        
                    # Choices for 'DEMAND''TERMINATED', etc.
                    #df['Terminated Flag']=np.select(conditions,choices,default='TERMINATED')
                    with col1:
                        zero_val=st.checkbox("Exclude Zero On Balance Values")
                        blank_dpd=st.checkbox("Exclude blank DPD values")
                        DPD_min=st.number_input("Payment Delay Days 'greater than:",
                                                   min_value=int(df['PaymentDelayDays'].min()),
                                                   max_value=int(df['PaymentDelayDays'].max()),
                                                   value=int(df['PaymentDelayDays'].min()),step=1)
                        DPD_max=st.number_input("Payment Delay Days 'less than:",
                                                   min_value=int(df['PaymentDelayDays'].min()),
                                                   max_value=int(df['PaymentDelayDays'].max()),
                                                   value=int(df['PaymentDelayDays'].max()),step=1)
        
                        if (DPD_min>DPD_max):
                            st.error("⚠️ Error: DPD 'greater than'input must be greater than 'less than'.")
            
                        date_filter=st.radio("Filter :blue[Date Client Turned NPL]:", ['Prior than','Later than','Between dates'],horizontal=True)
                        if (date_filter=='Prior than'):
                            transfer_date_prior=st.date_input("Service Transfer Date :red[prior] than:",df['DateClientTurnedNPL'].max(),
                                                              min_value=df['DateClientTurnedNPL'].dropna().min(), 
                                                              max_value=df['DateClientTurnedNPL'].dropna().max())
                            transfer_date_later=df['DateClientTurnedNPL'].min()
                        elif (date_filter=='Later than'):
                            transfer_date_later=st.date_input("Service Transfer Date :red[later] than:",df['DateClientTurnedNPL'].min(),
                                                              min_value=df['DateClientTurnedNPL'].dropna().min(), 
                                                              max_value=df['DateClientTurnedNPL'].dropna().max())
                            transfer_date_prior=df['DateClientTurnedNPL'].max()
                            
                        elif (date_filter=='Between dates'):
                            transfer_date_prior=st.date_input("Service Transfer Date :red[prior] than:",df['DateClientTurnedNPL'].max(),
                                                              min_value=df['DateClientTurnedNPL'].dropna().min(), 
                                                              max_value=df['DateClientTurnedNPL'].dropna().max())
                            transfer_date_later=st.date_input("Service Transfer Date :red[later] than:",df['DateClientTurnedNPL'].min(),
                                                              min_value=df['DateClientTurnedNPL'].dropna().min(), 
                                                              max_value=df['DateClientTurnedNPL'].dropna().max())
            
                            if (transfer_date_later>transfer_date_prior):
                                st.error("⚠️ Error: 'Prior than'date must fall after 'less than'date.")          
                                
                                
                        else:                
                               transfer_date_prior=df['DateClientTurnedNPL'].max()       
                               transfer_date_later=df['DateClientTurnedNPL'].min()
                               
                               
                    with col2:
                        
                        # xCCB_flag=st.multiselect("Ex CCB Flag:", df['ContractexCCBFlg'].unique(), default=df['ContractexCCBFlg'].unique())
                        # if not xCCB_flag:
                        #     pass
                        # else:
                        #     df=df[df['ContractexCCBFlg'].isin(xCCB_flag)]
                    
                        
                        # terminated_flag=st.multiselect("Terminated Flag:", df['Terminated Flag'].unique(), default=df['Terminated Flag'].unique())
                        # if not terminated_flag:
                        #     # terminated_flag=st.multiselect("Terminated Flag:",df['Terminated Flag'].dropna().unique(),['FINAL DEMAND', 'TERMINATED', 'NOT TERMINATED'],key='term_flag')
                        #     pass
                        # else:
                        #     df=df[df['Terminated Flag'].isin(terminated_flag)]
                        #     # st.write("")
                        #     # st.write("")
                    
                        NPL_flag=st.multiselect("NPL Flag:", df['NonPerformingLoan(NPL)'].unique(), default=df['NonPerformingLoan(NPL)'].unique())
                        # NPL_flag=st.multiselect("NPL Flag:", df['ContractNPLFlag'].dropna().unique(), pd.DataFrame(df['ContractNPLFlag'].unique()).values)
                        if not NPL_flag:
                            # terminated_flag=st.multiselect("Terminated Flag:", df['Terminated Flag'].dropna().unique(),['FINAL DEMAND', 'TERMINATED', 'NOT TERMINATED'],key='term_flag')
                            pass
                        else:
                            df=df[df['NonPerformingLoan(NPL)'].isin(NPL_flag)]
                        
                    with col3:
                         product_type=st.multiselect("Product Type:", df['ProductType'].unique(), default=df['ProductType'].unique())
                         if not product_type:
                             # terminated_flag=st.multiselect("Terminated Flag:", df['Terminated Flag'].dropna().unique(),['FINAL DEMAND', 'TERMINATED', 'NOT TERMINATED'],key='term_flag')
                             pass
                         else:
                             df=df[df['ProductType'].isin(product_type)]  
                            # closed_flag=st.multiselect("Closed Account:", df['ContractClosedFlg'].unique(), default=df['ContractClosedFlg'].unique())
                            # if not closed_flag:
                            #     # terminated_flag=st.multiselect("Terminated Flag:", df['Terminated Flag'].dropna().unique(),['FINAL DEMAND', 'TERMINATED', 'NOT TERMINATED'],key='term_flag')
                            #     pass
                            # else:
                            #     df=df[df['ContractClosedFlg'].isin(closed_flag)]
                                
                            # HFS_flag=st.multiselect("Held for sale:", df['ContractHeldForSaleFlg'].unique(), default=df['ContractHeldForSaleFlg'].unique())
                            # if not closed_flag:
                            #     # terminated_flag=st.multiselect("Terminated Flag:", df['Terminated Flag'].dropna().unique(),['FINAL DEMAND', 'TERMINATED', 'NOT TERMINATED'],key='term_flag')
                            #     pass
                            # else:
                            #     df=df[df['ContractHeldForSaleFlg'].isin(HFS_flag)]    
                                
                                
                    with col4:            
                            DepRiskUnit=st.multiselect("Department Risk Unit:", df['ClientDepRiskUnit'].unique(), default=df['ClientDepRiskUnit'].unique())
                            if not DepRiskUnit:
                                # terminated_flag=st.multiselect("Terminated Flag:", df['Terminated Flag'].dropna().unique(),['FINAL DEMAND', 'TERMINATED', 'NOT TERMINATED'],key='term_flag')
                                pass
                            else:
                                df=df[df['ClientDepRiskUnit'].isin(DepRiskUnit)]
                                
                            
                                
                                
                    submitted_filters=st.form_submit_button("Refresh - Submit selected filters")  
                    
                    if submitted_filters:
                        df_filtered_rev=df[df['NonPerformingLoan(NPL)'].isin(NPL_flag)&
                                        
                                        df['ProductType'].isin(product_type)&
                                        df['ClientDepRiskUnit'].isin(DepRiskUnit)&
                                        ((df['DateClientTurnedNPL']<=pd.to_datetime(transfer_date_prior))&
                                        #(df['DateClientTurnedNPL']>=pd.to_datetime(transfer_date_later))|df['DateClientTurnedNPL'].isna())&
                                        (df['DateClientTurnedNPL']>=pd.to_datetime(transfer_date_later)))&
                                        (df['PaymentDelayDays'].between(int(DPD_min), int(DPD_max))|df['PaymentDelayDays'].isna())]

# ... some lines are cut off ...

                        form_check2=True
                        if zero_val:
                            df_filtered_rev=df_filtered_rev[df_filtered_rev['GrossLoanAmount']!=0]
                        if blank_dpd:
                            df_filtered_rev['PaymentDelayDays'].fillna('No DPD', inplace=True)
                            df_filtered_rev=df_filtered_rev[df_filtered_rev['PaymentDelayDays']!="No DPD"]
                      
                        
                        for col in df_filtered_rev.select_dtypes(include=['datetime64[ns]']):
                           df_filtered_rev[col]=pd.to_datetime(df_filtered_rev[col]).dt.strftime('%d/%m/%Y')
                           
                        st.write(f"The filtered dataframe has {len(df_filtered_rev)} rows:")
                        st.dataframe(df_filtered_rev,hide_index=True)
                        
                        df_filtered_rev['ClientIDC']=df_filtered_rev['ClientIDC'].astype(str)
                        #df_filtered_rev['ContractCurrentCd']=df_filtered_rev['ContractCurrentCd'].astype(str)
                        
                        
                                                        
                        
            finished_filtering_toggle=st.toggle("Finished filtering and ready to export data:")   

            if finished_filtering_toggle:

                    if form_check2:
                            excel_file=convert_to_excel(df_filtered_rev)
                            current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            str_current_datetime = str(current_datetime)
                            file_export_name3 = "exported_data_" + str_current_datetime + ".xlsx"
                            download = st.download_button(
                                label="📊 Download data to excel",
                                data=excel_file,
                                file_name=file_export_name3,
                                mime="application/vnd.ms-excel"
                            )
                    else:
                            st.warning("Click Refresh-Submit selected filters before downloading data")

        # if (export_type=="Custom Filtering"):
        #     conditions=[
        #         (df['ContractLegalFlg']=='F'),
        #         (df['ContractLegalFlg'].isin(['B','R','N'])) | (df['ContractLegalFlg'].isna())
        #     ]
        #     choices=['FINAL DEMAND', 'NOT TERMINATED']
        #     df['Terminated Flg']=np.select(conditions,choices,default='TERMINATED')
            
        #     filtered_df=filter_dataframe(df)
                                        
