import streamlit as st

st.sidebar.title("Features")
#Intializing
parameter_list=['Average Total Page Views (per session)','Batch Delivers Received last week','Days since Last App Visit','Days since First App Visit', 'Number of App Visits last week']
parameter_input_values=[]
parameter_default_values=['0','0','0','0','0']
values=[]

#Display
for parameter, parameter_df in zip(parameter_list, parameter_default_values):
 
 values= st.sidebar.slider(label=parameter, key=parameter,value=int(parameter_df), min_value=0, max_value=500, step=1)
 parameter_input_values.append(values)
 
input_variables=pd.DataFrame([parameter_input_values],columns=parameter_list,dtype=int)
st.write('\n\n')

def tree_new(input_variables): #max depth = 8, features = 5
  AvgTotalPageViews = input_variables.iloc[1]
  batch_delivers = input_variables.iloc[2]
  days_since_lastappvisit = input_variables.iloc[3]
  days_since_firstappvisit = input_variables.iloc[4]
  num_app_visits = input_variables.iloc[5]

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
    prediction = tree_new(input_variables)
    if prediction == 0 :
     st.title("0") 
    else:
     st.title("1")

  
  
  
  
  
  
