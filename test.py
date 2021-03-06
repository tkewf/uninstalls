import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import requests
import matplotlib.pyplot as plt
import seaborn
import statistics

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_book = load_lottieurl('https://assets9.lottiefiles.com/packages/lf20_bfcbo83f.json')
st_lottie(lottie_book, speed=0.6, height=200, key="initial")

##st.sidebar.image(background, width=50)
st.sidebar.title("Features")
#Intializing
parameter_list_slider=['Days since Last App Visit','Days since First App Visit']
parameter_list_num=['Average Total Page Views (per session)','Batch Delivers Received last week','Number of App Visits last week']
parameter_default_values_slider=['0','0']
parameter_default_values_num=['0','0','0']
parameter_input_values=[]
values=[]

#Display

values_slides_lastappvisit = st.sidebar.slider(label='Days since Last App Visit',value=int(0), min_value=0, max_value=1000, step=1, key = 'a')
parameter_input_values.append(values_slides_lastappvisit)


values_slides_firstappvisit = st.sidebar.slider(label='Days since First App Visit',value=int(0), min_value=int(values_slides_lastappvisit), max_value=1000, step=1, key = 'b')
if values_slides_firstappvisit < values_slides_lastappvisit:
    st.write('Your first app visit should be earlier than your last app visit!')
else: 
    parameter_input_values.append(values_slides_firstappvisit)
 
values_num_avgpages= st.sidebar.number_input(label='Average Total Page Views (per session)', key='c',value=float(0), min_value=0.0, max_value=500.0, step=0.1,format="%.1f")
parameter_input_values.append(values_num_avgpages)

values_num_batch= st.sidebar.number_input(label='Batch Delivers Received last week', key='d',value=int(0), min_value=0, max_value=250, step=1)
parameter_input_values.append(values_num_batch)
    
values_num_apppvisits= st.sidebar.number_input(label='Number of App Visits last week', key='e',value=int(0), min_value=0, max_value=250, step=1)
parameter_input_values.append(values_num_apppvisits)


 
#input_variables=pd.DataFrame([parameter_input_values],columns=parameter_list,dtype=int)
#st.write('\n\n')

def tree_new(input_variables): #max depth = 8, features = 5
  days_since_lastappvisit = input_variables[0]
  days_since_firstappvisit = input_variables[1]  
  AvgTotalPageViews = input_variables[2]
  batch_delivers = input_variables[3]
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
     
#if __name__ == "__main__":
 
if st.sidebar.button("Click Here to Classify"):
    prediction = tree_new(parameter_input_values)
    if prediction == 0 :
        st.markdown("# :blush: There is a 93% chance that this person has **_not_** uninstalled the WFUS App.")
        st.write('')
        st.write('')
        st.markdown('## How does this person compare to the typical Wayfair Android App User?')
        st.write('')

        # Plots
        df = pd.read_csv('data_for_graph (1).csv')
        df_uninstalled_sample = df[df['uninstalled']==1]
        df_persisting_sample = df[df['uninstalled']==0]

        st.write('')
        st.write('')    
        # First graph: Days since first visit
        st.markdown('### Days since first app visit')
        fig, ax = plt.subplots(1,2)# figsize=(10,12))

        #fig.suptitle('Days since Install', fontsize=20)

        ax[0].hist(df_uninstalled_sample['days_since_firstappvisit'],range=[0,500],bins=40,color = 'darksalmon')
        ax[0].set_title('Uninstalled users')
        ax[0].set_ylim(top=10000)
        ax[0].set_xlabel('Days')
        ax[0].set_ylabel('Number of Users')
        

        ax[1].hist(df_persisting_sample['days_since_firstappvisit'],range=[0,500],bins=40, color='skyblue')
        ax[1].set_title('Persisting users')
        ax[1].set_ylim(top=10000)
        ax[1].set_xlabel('Days')
        ax[1].axvline(parameter_input_values[1], 0, 10000, label='User value', color = 'purple')

        plt.style.use('seaborn')
        fig.set_figheight(5)
        fig.set_figwidth(12) 
        fig.legend()
        st.pyplot(fig)

        days_input = parameter_input_values[1]
        median_days_input = statistics.median(df_persisting_sample.days_since_firstappvisit)
        st.markdown("It has been **{} days** since this user installed the app,"
                    "compared to the median number of days (**{}**) for **persisting** users.".format(days_input, median_days_input))
        st.write('') 
        st.write('')    
        # Second graph: Days since last app visit
        st.markdown('### Days since last app visit')
        fig, ax = plt.subplots(1,2)# figsize=(10,12))

        #fig.suptitle('Days since Last App Visit', fontsize=20)

        ax[0].hist(df_uninstalled_sample['days_since_lastappvisit'],range=[0,500],bins=40,color = 'darksalmon')
        ax[0].set_title('Uninstalled users')
        ax[0].set_ylim(top=10000)
        ax[0].set_xlabel('Days')
        ax[0].set_ylabel('Number of Users')
        

        ax[1].hist(df_persisting_sample['days_since_lastappvisit'],range=[0,500],bins=40, color='skyblue')
        ax[1].set_title('Persisting users')
        ax[1].set_ylim(top=10000)
        ax[1].set_xlabel('Days')
        ax[1].axvline(parameter_input_values[0], 0, 10000, label='User value', color = 'purple')

        plt.style.use('seaborn')
        fig.set_figheight(5)
        fig.set_figwidth(12) 
        fig.legend()
        st.pyplot(fig)
     
        last_days_input = parameter_input_values[0]
        median_last_days_input = statistics.median(df_persisting_sample.days_since_lastappvisit)
        st.markdown("It has been **{} days** since this user last visited the app,"
                    "compared to the median number of days (**{}**) for **persisting** users.".format(last_days_input, median_last_days_input))
        st.write('') 
        st.write('')

        # Third graph: Avg page views per session
        st.markdown('### Average Page Views per session')
        fig, ax = plt.subplots(1,2)# figsize=(10,12))

        #fig.suptitle('Average Page Views per session', fontsize=20)

        ax[0].hist(df_uninstalled_sample['AvgTotalPageViews'],range=[0,80],bins=40,color = 'darksalmon')
        ax[0].set_title('Uninstalled users')
        ax[0].set_ylim(top=15000)
        ax[0].set_xlabel('Page Views')
        ax[0].set_ylabel('Number of Users')
        

        ax[1].hist(df_persisting_sample['AvgTotalPageViews'],range=[0,80],bins=40, color='skyblue')
        ax[1].set_title('Persisting users')
        ax[1].set_ylim(top=15000)
        ax[1].set_xlabel('Page Views')
        ax[1].axvline(parameter_input_values[2], 0, 10000, label='User value', color = 'purple')

        plt.style.use('seaborn')
        fig.set_figheight(5)
        fig.set_figwidth(12) 
        fig.legend()
        st.pyplot(fig)

        avg_page_views = parameter_input_values[2]
        median_avg_page_views = statistics.median(df_persisting_sample.AvgTotalPageViews)
        st.markdown("The average number of pages viewed during the past week for this user is **{}**, "
                    "compared to the median number of pages (**{}**) for **persisting** users.".format(avg_page_views, median_avg_page_views))
        st.write('') 
        st.write('')  
        # Fourth graph: Avg page views per session
        st.markdown('### Number of app visits since last week')
        fig, ax = plt.subplots(1,2)# figsize=(10,12))

        #fig.suptitle('Number of app visits since last week', fontsize=20)

        ax[0].hist(df_uninstalled_sample['num_app_visits'],range=[0,20],bins=21,color = 'darksalmon')
        ax[0].set_title('Uninstalled users')
        ax[0].set_ylim(top=20000)
        ax[0].set_xlabel('Page Views')
        ax[0].set_ylabel('Number of Users')
        

        ax[1].hist(df_persisting_sample['num_app_visits'],range=[0,20],bins=21, color='skyblue')
        ax[1].set_title('Persisting users')
        ax[1].set_ylim(top=20000)
        ax[1].set_xlabel('Page Views')
        ax[1].axvline(parameter_input_values[4], 0, 10000, label='User value', color = 'purple')

        plt.style.use('seaborn')
        fig.set_figheight(5)
        fig.set_figwidth(12) 
        fig.legend()
        st.pyplot(fig)
        
        num_visits = parameter_input_values[3]
        median_num_visits = statistics.median(df_persisting_sample.num_app_visits)
        st.markdown("The number of app visits during the past week for this user is **{}**, "
                    "compared to the median number of visits (**{}**) for **persisting** users.".format(num_visits, median_num_visits))

    else:
        st.markdown("# :fearful: There is a 93% chance that this person has **_uninstalled_** the WFUS App.")
    
        st.write('')
        st.write('')
        st.markdown('## How does this person compare to the typical Wayfair Android App User?')
        st.write('')

        # Plots
        df = pd.read_csv('data_for_graph (1).csv')
        df_uninstalled_sample = df[df['uninstalled']==1]
        df_persisting_sample = df[df['uninstalled']==0]

        st.write('')
        st.write('')    
        # First graph: Days since first visit
        st.markdown('### Days since first app visit')
        fig, ax = plt.subplots(1,2)# figsize=(10,12))

        #fig.suptitle('Days since Install', fontsize=20)

        ax[0].hist(df_uninstalled_sample['days_since_firstappvisit'],range=[0,500],bins=40,color = 'darksalmon')
        ax[0].set_title('Uninstalled users')
        ax[0].set_ylim(top=10000)
        ax[0].set_xlabel('Days')
        ax[0].set_ylabel('Number of Users')
        ax[0].axvline(parameter_input_values[1], 0, 10000, label='User value', color = 'purple')

        ax[1].hist(df_persisting_sample['days_since_firstappvisit'],range=[0,500],bins=40, color='skyblue')
        ax[1].set_title('Persisting users')
        ax[1].set_ylim(top=10000)
        ax[1].set_xlabel('Days')

        plt.style.use('seaborn')
        fig.set_figheight(5)
        fig.set_figwidth(12) 
        fig.legend()
        st.pyplot(fig)
 
        days_input = parameter_input_values[1]
        median_days_input = statistics.median(df_uninstalled_sample.days_since_firstappvisit)
        st.markdown("It has been **{} days** since this user installed the app,"
                    "compared to the median number of days (**{}**) for **uninstalled** users.".format(days_input, median_days_input))
        st.write('')
        st.write('')  
        # Second graph: Days since last app visit
        st.markdown('### Days since last app visit')
        fig, ax = plt.subplots(1,2)# figsize=(10,12))

        #fig.suptitle('Days since Last App Visit', fontsize=20)

        ax[0].hist(df_uninstalled_sample['days_since_lastappvisit'],range=[0,500],bins=40,color = 'darksalmon')
        ax[0].set_title('Uninstalled users')
        ax[0].set_ylim(top=10000)
        ax[0].set_xlabel('Days')
        ax[0].set_ylabel('Number of Users')
        ax[0].axvline(parameter_input_values[0], 0, 10000, label='User value', color = 'purple')

        ax[1].hist(df_persisting_sample['days_since_lastappvisit'],range=[0,500],bins=40, color='skyblue')
        ax[1].set_title('Persisting users')
        ax[1].set_ylim(top=10000)
        ax[1].set_xlabel('Days')

        plt.style.use('seaborn')
        fig.set_figheight(5)
        fig.set_figwidth(12) 
        fig.legend()
        st.pyplot(fig)

        last_days_input = parameter_input_values[0]
        median_last_days_input = statistics.median(df_uninstalled_sample.days_since_lastappvisit)
        st.markdown("It has been **{} days** since this user last visited the app,"
                    "compared to the median number of days (**{}**) for **uninstalled** users.".format(last_days_input, median_last_days_input))
        
        st.write('')
        st.write('')  
        # Third graph: Avg page views per session
        st.markdown('### Average Page Views per session')
        fig, ax = plt.subplots(1,2)# figsize=(10,12))

        #fig.suptitle('Average Page Views per session', fontsize=20)

        ax[0].hist(df_uninstalled_sample['AvgTotalPageViews'],range=[0,80],bins=40,color = 'darksalmon')
        ax[0].set_title('Uninstalled users')
        ax[0].set_ylim(top=15000)
        ax[0].set_xlabel('Page Views')
        ax[0].set_ylabel('Number of Users')
        ax[0].axvline(parameter_input_values[2], 0, 10000, label='User value', color = 'purple')

        ax[1].hist(df_persisting_sample['AvgTotalPageViews'],range=[0,80],bins=40, color='skyblue')
        ax[1].set_title('Persisting users')
        ax[1].set_ylim(top=15000)
        ax[1].set_xlabel('Page Views')

        plt.style.use('seaborn')
        fig.set_figheight(5)
        fig.set_figwidth(12) 
        fig.legend()
        st.pyplot(fig)

        avg_page_views = parameter_input_values[2]
        median_avg_page_views = statistics.median(df_uninstalled_sample.AvgTotalPageViews)
        st.markdown("The average number of pages viewed during the past week for this user is **{}**, "
                    "compared to the median number of pages (**{}**) for **uninstalled** users.".format(avg_page_views, median_avg_page_views))
        
        st.write('')
        st.write('')  
        # Fourth graph: Avg page views per session
        st.markdown('### Number of app visits since last week')
        fig, ax = plt.subplots(1,2)# figsize=(10,12))

        #fig.suptitle('Number of app visits since last week', fontsize=20)

        ax[0].hist(df_uninstalled_sample['num_app_visits'],range=[0,20],bins=21,color = 'darksalmon')
        ax[0].set_title('Uninstalled users')
        ax[0].set_ylim(top=20000)
        ax[0].set_xlabel('Page Views')
        ax[0].set_ylabel('Number of Users')
        ax[0].axvline(parameter_input_values[4], 0, 10000, label='User value', color = 'purple')

        ax[1].hist(df_persisting_sample['num_app_visits'],range=[0,20],bins=21, color='skyblue')
        ax[1].set_title('Persisting users')
        ax[1].set_ylim(top=20000)
        ax[1].set_xlabel('Page Views')

        plt.style.use('seaborn')
        fig.set_figheight(5)
        fig.set_figwidth(12) 
        fig.legend()
        st.pyplot(fig)

        num_visits = parameter_input_values[3]
        median_num_visits = statistics.median(df_uninstalled_sample.num_app_visits)
        st.markdown("The number of app visits during the past week for this user is **{}**, "
                    "compared to the median number of visits (**{}**) for **uninstalled** users.".format(num_visits, median_num_visits))

