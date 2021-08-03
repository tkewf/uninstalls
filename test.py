import streamlit as st

st.sidebar.title("Features")
#Intializing
parameter_list=['Average Total Page Views (per session)','Batch Delivers Received last week','Days since Last App Visit','Days since First App Visit', 'Number of App Visits last week']
parameter_input_values=[]
parameter_default_values=['0','0','0','0','0']
values=[]

#Display
for parameter, parameter_df in zip(parameter_list, parameter_default_values):
 
 values= st.sidebar.slider(label=parameter, key=parameter,value=float(parameter_df), min_value=0.0, max_value=500, step=1)
 parameter_input_values.append(values)
 
input_variables=pd.DataFrame([parameter_input_values],columns=parameter_list,dtype=float)
st.write('\n\n')
