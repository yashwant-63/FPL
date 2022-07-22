#Importing the libraries
import pandas as pd
import numpy as np
import pickle
import streamlit as st
from Utilities.model_func import*
from Utilities.scraping_func import*

import os


pickle_lr = open('Models/linear_regression.pkl', 'rb')
model_lr = pickle.load(pickle_lr)


pickle_xgb = open('Models/xgb.pkl', 'rb')
model_xgb = pickle.load(pickle_xgb)


avg_stats_last5_gws = pd.read_csv('Data/avg_stats_last5_gameweeks.csv',delimiter=',')
player_season_stats = pd.read_csv('Data/player_level_season_stats.csv',delimiter=',')

player_list = avg_stats_last5_gws['name'].to_list()
model_list = ['Linear Regression','XGBoost']
lst = ['2','3','4','5']

def welcome():
    return 'welcome all'

# this is the main function in which we define our webpage
def main():
    # giving the webpage a title
    
    # here we define some of the front end elements of the web page like
    # the font and background color, the padding and the text to be displayed
    html_temp = """
    <div style ="background-color:blue;padding:13px">
    <h2 style ="color:white;text-align:center;">Fantasy Premier League Dashboard</h2>
    </div>
    """

    choices = ['Predict FPL points','Player Comaparison']
    ticker = st.sidebar.selectbox('Choose a Page',choices)
    st.markdown(html_temp, unsafe_allow_html = True)
    
    if (ticker=='Predict FPL points'):
            # this line allows us to display a drop list to choose the player 
            
            st.header('FPL point prediction page')
            player_name = ''
            selected_model = st.selectbox('Model',model_list)

            if selected_model == 'Linear Regression':
                model_name = 'Models/linear_regression.pkl'
            elif selected_model == 'XGBoost':
                model_name = 'Models/xgb.pkl'

            # the below line ensures that when the button called 'Predict' is clicked,
            # the prediction function defined above is called to make the prediction
            # and store it in the variable result
            player_name = st.selectbox('Player Name', np.array(player_list))

            # CSS to inject contained in a string
            hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """
            
            if st.button("Predict "):
                if False:
                    st.text('Please select different teams')
                else:
                    
                    #print(avg_stats_last5_gws)
                    predicted_points,top10_predicted_players = predict_fpl_points(player_name,model_name,avg_stats_last5_gws)
                    # Inject CSS with Markdown
                    st.markdown(hide_table_row_index, unsafe_allow_html=True)

                    
                    st.subheader('Point Prediction')

                    st.text("Predicted points for the next gameweek for {player_name} is {predicted_points}.".format(player_name = player_name,predicted_points = round(predicted_points,2)))
                    st.text("The table below gives the top 10 players for the upcoming week")

                    col1,col2 = st.columns(2)
                    col1.markdown("Top 10 players")
                    col1.dataframe(top10_predicted_players[['name','predicted_points']])
                    

    else:
        st.header('Player Comparison')
                
        players = st.sidebar.selectbox('Number of players',lst)


        if players == '2':
            player_1 = st.selectbox('Player 1 Name',player_list)
            player_2 = st.selectbox('Player 2 Name',player_list)
            player_names = [player_1,player_2]
        elif players == '3':
            player_1 = st.selectbox('Player 1 Name',player_list)
            player_2 = st.selectbox('Player 2 Name',player_list)
            player_3 = st.selectbox('Player 3 Name',player_list)
            player_names = [player_1,player_2,player_3]
        elif players == '4':
            player_1 = st.selectbox('Player 1 Name',player_list)
            player_2 = st.selectbox('Player 2 Name',player_list)
            player_3 = st.selectbox('Player 3 Name',player_list)
            player_4 = st.selectbox('Player 4 Name',player_list)
            player_names = [player_1,player_2,player_3,player_4]
        else :    
            player_1 = st.selectbox('Player 1 Name',player_list)
            player_2 = st.selectbox('Player 2 Name',player_list)
            player_3 = st.selectbox('Player 3 Name',player_list)
            player_4 = st.selectbox('Player 4 Name',player_list)
            player_5 = st.selectbox('Player 5 Name',player_list)
            player_names = [player_1,player_2,player_3,player_4,player_5]




        if st.button("Compare "):
            

            fig = compare_players(player_names,player_season_stats)
            


            st.pyplot(fig)

            
                
    
if __name__=='__main__':
    main()

