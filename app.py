import streamlit as st
import pandas as pd

st.set_page_config(page_title="Billet Dashboard", layout="wide")
st.title("Billet Inventory Dashboard")

stock=pd.read_excel('Billet Dashboard Test.xlsx',sheet_name='Billet Stock & Cost Oct 2026')
usage=pd.read_excel('Billet Dashboard Test.xlsx',sheet_name='Billet Useage Oct 2026')
stillage=pd.read_excel('Billet Dashboard Test.xlsx',sheet_name='Billets Per Stillage')

usage=usage[['Product Code','Average']]
stock=stock.rename(columns={'Product':'Product Code','On Hand':'Stock'})
merged=stock.merge(usage,on='Product Code').merge(stillage,on='Product Code')
merged['Weeks Cover']=merged['Stock']/merged['Average']
merged['Stillages Used']=merged['Stock']/merged['Billets Per Stillage']
merged['Reorder?']=merged['Weeks Cover'].apply(lambda x:'🔴 YES' if x<8 else ('🟠 Monitor' if x<12 else '🟢 No'))

c1,c2,c3,c4=st.columns(4)
c1.metric('Total Billets',f"{merged['Stock'].sum():,.0f}")
c2.metric('Avg Weeks Cover',f"{merged['Weeks Cover'].mean():.1f}")
c3.metric('Reorder Items',int((merged['Weeks Cover']<8).sum()))
c4.metric('Inventory Value (£)',f"{stock['Total'].sum():,.0f}")

st.subheader('Billet Summary')
st.dataframe(merged[['Product Code','Product Description','Stock','Average','Weeks Cover','Billets Per Stillage','Stillages Used','Reorder?']],use_container_width=True)

st.subheader('Items Requiring Reorder (<8 weeks cover)')
st.dataframe(merged[merged['Weeks Cover']<8][['Product Code','Product Description','Stock','Average','Weeks Cover']],use_container_width=True)
