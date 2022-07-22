
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle






def predict_fpl_points(player_name,model_name,input_data):


    pickle_input = open(model_name,'rb')
    model = pickle.load(pickle_input)

    if model_name == 'Models/linear_regression.pkl':
        X_predict = input_data.loc[:,~input_data.columns.isin(['Unnamed: 0','fpl_position','fpl_points','Venue','rank','name','passes','passes_completed','touches'])]
    elif model_name == 'Models/xgb.pkl':
        X_predict = input_data.loc[:,~input_data.columns.isin(['Unnamed: 0','fpl_position','fpl_points','Venue','rank','name'])]
    
    
    
    y_predict = model.predict(X_predict)
    
    y_test_new  = pd.DataFrame(y_predict,columns = ['predicted_points']).round(1)
    df_with_predictions  = pd.concat([input_data,y_test_new],axis = 1)
    
    predicted_points = df_with_predictions.loc[df_with_predictions['name']==player_name]
    top10_predicted_players = df_with_predictions[['name','predicted_points']].sort_values(by = ('predicted_points'),ascending=False).head(10)
    return float(predicted_points['predicted_points']), top10_predicted_players.reset_index()


def compare_players(player_names,input_data):
    num_players = len(player_names)
    df_stats = input_data[input_data['name'].isin(player_names)]


    dfm = df_stats[['name','goals','assists','xg','npxg','xa']].melt('name',var_name = "cols",value_name = "vals")
    
    sz = (num_players*2,5)
    
    fig = plt.figure(figsize=sz)
    sns.barplot(x = "name",y= "vals",hue = "cols",data = dfm)
    
    return fig
    