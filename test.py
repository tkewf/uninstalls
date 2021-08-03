import streamlit as st
import pandas as pd

st.sidebar.title("Features")
st.sidebar.image('wayfairapp.png', width=100, height=100)
#Intializing
parameter_list_slider=['Days since Last App Visit','Days since First App Visit']
parameter_list_num=['Average Total Page Views (per session)','Batch Delivers Received last week','Number of App Visits last week']
parameter_default_values_slider=['0','0']
parameter_default_values_num=['0','0','0']
parameter_input_values=[]
values=[]

#Display
for parameter, parameter_df in zip(parameter_list_slider, parameter_default_values_slider):
 values_slider= st.sidebar.slider(label=parameter, key=parameter,value=int(parameter_df), min_value=0, max_value=1000, step=1)
 parameter_input_values.append(values_slider)
 
for parameter, parameter_df in zip(parameter_list_num, parameter_default_values_num): 
 values_num= st.sidebar.number_input(label=parameter, key=parameter,value=float(parameter_df), min_value=0.0, max_value=500.0, step=0.1,format="%.1f")
 parameter_input_values.append(values_num)
 
#input_variables=pd.DataFrame([parameter_input_values],columns=parameter_list,dtype=int)
#st.write('\n\n')

def tree_new(input_variables): #max depth = 8, features = 5
  AvgTotalPageViews = input_variables[0]
  batch_delivers = input_variables[1]
  days_since_lastappvisit = input_variables[2]
  days_since_firstappvisit = input_variables[3]
  num_app_visits = input_variables[4]

  if AvgTotalPageViews <= 0.5:
     return (1)
  elif AvgTotalPageViews > 0.5:
    if batch_delivers <= 0.5:
      if days_since_lastappvisit <= 7.5:
        if days_since_firstappvisit <= 0.5:
          if num_app_visits <= 1.5:
             return (0)
          elif num_app_visits > 1.5:
            if num_app_visits <= 2.5:
              if AvgTotalPageViews <= 12.75:
                if AvgTotalPageViews <= 1.25:
                   return (0)
                elif AvgTotalPageViews > 1.25:
                   return (1)
              elif AvgTotalPageViews > 12.75:
                if AvgTotalPageViews <= 48.5:
                   return (0)
                elif AvgTotalPageViews > 48.5:
                   return (1)
            elif num_app_visits > 2.5:
                   return (0)
        elif days_since_firstappvisit > 0.5:
          if num_app_visits <= 2.5:
             return (1)
          elif num_app_visits > 2.5:
            if num_app_visits <= 7.5:
              if days_since_lastappvisit <= 4.5:
                   return (1)
              elif days_since_lastappvisit > 4.5:
                   return (0)
            elif num_app_visits > 7.5:
              if days_since_lastappvisit <= 1.5:
                if num_app_visits <= 16.5:
                   return (1)
                elif num_app_visits > 16.5:
                   return (0)
              elif days_since_lastappvisit > 1.5:
                   return (0)
      elif days_since_lastappvisit > 7.5:
         return (0)
    elif batch_delivers > 0.5:
       return (0)
     
if __name__ == "__main__":
 if st.button("Click Here to Classify"):
    prediction = tree_new(parameter_input_values)
    if prediction == 0 :
     st.title("There is a 93% chance that this person has not uninstalled the WFUS App.") 
    else:
     st.title("There is a 93% chance that this person has uninstalled the WFUS App.")

  
  
  
  
  
  
