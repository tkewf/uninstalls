WARNING: This app is strictly for visualization and educational purposes and should not be used for commercial or other uses.

## Android App Uninstall Prediction
[![App Link here](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/tkewf/uninstalls/main/test.py)

This app provides a simple interface for users to test different features and see the associated changes to the prediction of an Android user uninstalling the app tomorrow (with a **_~92%_** accuracy). 
The 5 features include: 
- Days since installation
- Days since last visited the app
- Batch pushes delivered (for the past week)
- Average total page views per app session (for the past week)
- Number of app visits (for the past week)


To view the decision tree rules, please see `tree_new` function located in `test.py`. 
Data used to make graphs have been anonymized to protect user privacy and can be found in `data_for_graph (1).csv`. 

This app was made possible by Streamlit. 
