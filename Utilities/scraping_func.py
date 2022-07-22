#import relevant libraries
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup


# input url to extract relevant data and output dataframe
def url_to_df(url):
    page = requests.get(url)
    #print("here")
    soup = BeautifulSoup(page.text, features="html.parser")
    table = soup.find_all('table')
    df = pd.DataFrame({'Names': table})
    #print(df.shape)
    df = df.iloc[3:17].reset_index().drop(['index'],axis =1)
    
    return df

#get fixtures for the epl season
def matches_lst(df):
    fixtures_team1 = ""
    for i in df.iloc[1]:
        fixtures_team1+=str(i)

    fixture_regex = 'data-stat="date".scope="row"><a.href=".[a-z]*.[a-z]*.[a-zA-Z0-9]*.[A-Za-z0-9-]*'

    schedules = re.findall(fixture_regex, fixtures_team1)

    matches = []

    for match in schedules:
        if match[-14:]=="Premier-League":
            #print(match[39:])
            matches.append(('https://fbref.com/'+match[39:]))

    return matches



#data manipulation to ultimately output team and player/gk information
def df_to_teams(df):


    player_stats_regex = 'data-stat="[a-z_0-9]*">[a-zA-Z0-9.]*'
    player_name_regex = 'data-stat="player" scope="row">\\xa0\\xa0\\xa0<a href=".[A-Za-z0-9_-]*[:]*..[a-z.]*.[a-z]*.[a-z]*.[a-z0-9]*.[A-Za-z-]*|data-stat="player" scope="row"><a href=".[a-z]*.[a-z]*.[a-zA-Z0-9]*.[A-Za-z-.]*.[a-z]*.[a-z]'
    team_name_regex = '<caption>[a-zA-Z ]*<.caption>'


    #team 1 stats
    summary_team1 = df_to_text(df,0)      
    passing_team1 = df_to_text(df,1)      
    pass_types_team1 = df_to_text(df,2)   
    defensive_actions_team1 = df_to_text(df,3)
    possession_team1 = df_to_text(df,4)
    misc_team1 = df_to_text(df,5)
    gk_team1 = df_to_text(df,6)

    #team 2 stats
    summary_team2 = df_to_text(df,7)
    passing_team2 = df_to_text(df,8)
    pass_types_team2 = df_to_text(df,9)
    defensive_actions_team2 = df_to_text(df,10)
    possession_team2 = df_to_text(df,11)
    misc_team2 = df_to_text(df,12)
    gk_team2 = df_to_text(df,13)
    
    # player names for both teams
    names_team1 = re.findall(player_name_regex, summary_team1)
    names_team2 = re.findall(player_name_regex, summary_team2)

    players_team1 = player_list(names_team1)
    players_team2 = player_list(names_team2)


    #player stats for team1
    summary_stats_team1 = re.findall(player_stats_regex, summary_team1)
    pass_stats_team1 = re.findall(player_stats_regex, passing_team1)
    pass_types_stats_team1 = re.findall(player_stats_regex, pass_types_team1)
    defensive_actions_stats_team1 = re.findall(player_stats_regex, defensive_actions_team1)
    possession_stats_team1 = re.findall(player_stats_regex, possession_team1)
    misc_stats_team1 = re.findall(player_stats_regex, misc_team1)
    gk_stats_team1 = re.findall(player_stats_regex, gk_team1)
    team1_name = re.findall(team_name_regex,summary_team1)
    team1_name = team1_name[0].split('>')[1].split('Player')[0][0:-1]
    
    #player stats for team2
    summary_stats_team2 = re.findall(player_stats_regex, summary_team2)
    pass_stats_team2 = re.findall(player_stats_regex, passing_team2)
    pass_types_stats_team2 = re.findall(player_stats_regex, pass_types_team2)
    defensive_actions_stats_team2 = re.findall(player_stats_regex, defensive_actions_team2)
    possession_stats_team2 = re.findall(player_stats_regex, possession_team2)
    misc_stats_team2 = re.findall(player_stats_regex, misc_team2)
    gk_stats_team2 = re.findall(player_stats_regex, gk_team2)
    team2_name = re.findall(team_name_regex,summary_team2)
    team2_name = team2_name[0].split('>')[1].split('Player')[0][0:-1]
    
    player_team1_summary = player_stats(players_team1,30,summary_stats_team1[7:len(players_team1)*30+7])
    player_team1_passing = player_stats(players_team1,25,pass_stats_team1[6:len(players_team1)*25+6])
    player_team1_pass_types = player_stats(players_team1,29,pass_types_stats_team1[6:len(players_team1)*29+6])
    player_team1_defensive_actions = player_stats(players_team1,27,defensive_actions_stats_team1[6:len(players_team1)*27+6])
    player_team1_possesion = player_stats(players_team1,28,possession_stats_team1[5:len(players_team1)*28+5])
    player_team1_misc = player_stats(players_team1,20,misc_stats_team1[3:len(players_team1)*20+3])
    player_team1_gk = goalk_stats(players_team1,22,gk_stats_team1[7:29])

    player_team2_summary = player_stats(players_team2,30,summary_stats_team2[7:len(players_team2)*30+7])
    player_team2_passing = player_stats(players_team2,25,pass_stats_team2[6:len(players_team2)*25+6])
    player_team2_pass_types = player_stats(players_team2,29,pass_types_stats_team2[6:len(players_team2)*29+6])
    player_team2_defensive_actions = player_stats(players_team2,27,defensive_actions_stats_team2[6:len(players_team2)*27+6])
    player_team2_possesion = player_stats(players_team2,28,possession_stats_team2[5:len(players_team2)*28+5])
    player_team2_misc = player_stats(players_team2,20,misc_stats_team2[3:len(players_team2)*20+3])
    player_team2_gk = goalk_stats(players_team2,22,gk_stats_team2[7:29])
    
    
    team1_df_summary = dict_to_df(player_team1_summary,players_team1[0])
    team1_df_passing = dict_to_df(player_team1_passing,players_team1[0])
    team1_df_pass_types = dict_to_df(player_team1_pass_types,players_team1[0])
    team1_df_defensive_actions = dict_to_df(player_team1_defensive_actions,players_team1[0])
    team1_df_possesion = dict_to_df(player_team1_possesion,players_team1[0])
    team1_df_misc = dict_to_df(player_team1_misc,players_team1[0])
    team1_df_gk = dict_to_df(player_team1_gk,players_team1[-1])

    team1_df_passing = team1_df_passing.drop(columns = ['position','age','minutes'],axis = 1)
    team1_df_pass_types = team1_df_pass_types.drop(columns = ['position','age','minutes'],axis = 1)
    team1_df_defensive_actions = team1_df_defensive_actions.drop(columns = ['position','age','minutes'],axis = 1)
    team1_df_possesion = team1_df_possesion.drop(columns = ['position','age','minutes'],axis = 1)
    team1_df_misc = team1_df_misc.drop(columns = ['position','age','minutes'],axis = 1)

    team1_temp1 = team1_df_summary.merge(team1_df_passing,how = "inner",on = ['name','shirtnumber','passes','passes_completed','passes_pct','progressive_passes','xa','assists'])
    team1_temp2 = team1_temp1.merge(team1_df_pass_types,how = "inner",on = ['name','shirtnumber','passes','passes_completed'])
    team1_temp3 = team1_temp2.merge(team1_df_defensive_actions,how = "inner",on = ['name','shirtnumber','pressures','tackles','interceptions','blocks'])
    team1_temp4 = team1_temp3.merge(team1_df_possesion,how = "inner",on = ['name','shirtnumber','touches','carries','progressive_carries','dribbles_completed','dribbles'])
    team1 = team1_temp4.merge(team1_df_misc,how = "inner",on = ['name','shirtnumber','cards_yellow','cards_red','interceptions','tackles_won','crosses'])


    team2_df_summary = dict_to_df(player_team2_summary,players_team2[0])
    team2_df_passing = dict_to_df(player_team2_passing,players_team2[0])
    team2_df_pass_types = dict_to_df(player_team2_pass_types,players_team2[0])
    team2_df_defensive_actions = dict_to_df(player_team2_defensive_actions,players_team2[0])
    team2_df_possesion = dict_to_df(player_team2_possesion,players_team2[0])
    team2_df_misc = dict_to_df(player_team2_misc,players_team2[0])
    team2_df_gk = dict_to_df(player_team2_gk,players_team2[-1])

    team2_df_passing = team2_df_passing.drop(columns = ['position','age','minutes'],axis = 1)
    team2_df_pass_types = team2_df_pass_types.drop(columns = ['position','age','minutes'],axis = 1)
    team2_df_defensive_actions = team2_df_defensive_actions.drop(columns = ['position','age','minutes'],axis = 1)
    team2_df_possesion = team2_df_possesion.drop(columns = ['position','age','minutes'],axis = 1)
    team2_df_misc = team2_df_misc.drop(columns = ['position','age','minutes'],axis = 1)

    team2_temp1 = team2_df_summary.merge(team2_df_passing,how = "inner",on = ['name','shirtnumber','passes','passes_completed','passes_pct','progressive_passes','xa','assists'])
    team2_temp2 = team2_temp1.merge(team2_df_pass_types,how = "inner",on = ['name','shirtnumber','passes','passes_completed'])
    team2_temp3 = team2_temp2.merge(team2_df_defensive_actions,how = "inner",on = ['name','shirtnumber','pressures','tackles','interceptions','blocks'])
    team2_temp4 = team2_temp3.merge(team2_df_possesion,how = "inner",on = ['name','shirtnumber','touches','carries','progressive_carries','dribbles_completed','dribbles'])
    team2 = team2_temp4.merge(team2_df_misc,how = "inner",on = ['name','shirtnumber','cards_yellow','cards_red','interceptions','tackles_won','crosses'])
    
    
    team1['Venue'] = 'Home'
    team2['Venue'] = 'Away'
    team1_df_gk['Venue'] = 'Home'
    team2_df_gk['Venue'] = 'Away'
    team1['TeamName'] = team1_name
    team2['TeamName'] = team2_name
    
    team1_df_gk['TeamName'] = team1_name
    team2_df_gk['TeamName'] = team2_name
    
    teams = pd.concat([team1,team2],ignore_index=True)
    gks = pd.concat([team1_df_gk,team2_df_gk],ignore_index=True)
    

    return teams,gks

#convert df to text
def df_to_text(df,i):
    txt = ""
    for i in df.iloc[i]:
        txt+=str(i)
    return txt

#convert dictionary to dataframe
def dict_to_df(dct,player):
    column_names = list(dct[player].keys())
    df = pd.DataFrame(columns = column_names)
    
    for k1,v1 in dct.items():
        v1['name'] = k1
        df = df.append(v1,ignore_index = True)
    return df
#get list of players 
def player_list(names):
    players = []
    
    for i,stat in enumerate(names):
        stat = stat.split('/')
    
        if i == len(names):
            players.append(stat[-1][:-1])
        else:    
            players.append(stat[-1])
    return players
#get player stats
def player_stats(player_list,n,regex_stat):
    player_dict = {}
    
    for i,player in enumerate(player_list):
        player_individual_stats = {}
        for j in range(i,i*n+n):
            stat = regex_stat[j].split('>')
            player_individual_stats[stat[0][11:-1]]=stat[1] 
        player_dict[player] = player_individual_stats
    
    return player_dict
#get goalkeeper stats
def goalk_stats(player_list,n,regex_stat):
    player_dict = {}
    player_individual_stats = {}
    for j in range(0,n):
        stat = regex_stat[j].split('>')
        if stat[1]=='':
            stat[1]=0.0
        player_individual_stats[stat[0][11:-1]]=stat[1] 
    player_dict[player_list[-1]] = player_individual_stats 
    return player_dict