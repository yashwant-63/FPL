# FPL

This project is dedicated to my eternal love for FPL - [Fantasy Premier League](https://fantasy.premierleague.com/). The game requires you to select 15 players for a budget of $100 from the 20 English Premier League teams with some constraints. 
The initial version is a very basic dashboard which has two features:
1) Future gameweek point prediction
2) Player comparison

The app is hosted on [streamlit](https://yashwant-63-fpl-fpl-app-klvq2s.streamlitapp.com/)

## Future gameweek point prediction
I built models using linear regression and XGBoost to figure out the players who are likely to score the most points in the upcoming gameweeks. The tool gives you an option to select the model and player of your choice, after which it returns the predicted points for the selected player. It also outputs the top 10 players who are likely to score the most fpl points. The current version is static, meaning the points predicted for each player is constant as their statistics are constant. I plan to change this in a future version wherein you can input the stats for a player (e.g - xg, shots on target, touches, etc) and the tool would give you an estimate of fpl points based on these stats. 

## Player comparison
This tool lets you compare upto players to get a sense of which players are performing well on stats like goals, assists, xg, xa and npxg. The output is a barplot of the accumulated season statistics for the variables mentioned previously.



# Data Source

The player level statistics have been collected from [this](https://fbref.com/en/) website. I scraped the 21-22 English Premier League player level statistics using Beautiful Soup in python. The process has been further described in this [jupyter notebook](https://github.com/yashwant-63/FPL/blob/main/Final_Scraping.ipynb)

#### The main prediction features used are:
- Age: Players age in years at the time of the match
- shots_total : Number of shots by a player
- shots_on_target: Number of shots on target i.e the goal
- touches: Number of times a player touches the ball
- pressures: Number of times applying pressure to opponent
- tackles: Number of players tackled (a player can be tackled more than once)
- interceptions: Number of times ball intercepted
- blocks: Number of times ball blocked while standing in its path
- xg: Expected goals
- npxg: Non-penalty expected goals
- xa: Excepted Assists
- sca: Shot Creating Actions - The two offensive actions directly leading to a shot such as passes, dribbles
- gca: Goal Creating Actions - The two offensive actions directly leading to a goal such as passes, dribbles
- passes_completed: Number of succesful passes
- passes: Number of attempted passes
- progressive_passes: Completed passes that move towards the opponent's goal
- carries: Number of times the player controlled the ball with their feet
- progressive_carries: Carries that move the ball towards the opponent's goal

# Model building
Simple data manipulation takes us from game level statistics to season level statistics for a player. The features mentioned above are then used to model points prediction using linear regression and XGBoost regression. After hyperparameter tuning, XGBoost model turns out to be the best with an accuracy of ~59% whereas the best linear regression model has an accuracy of ~49%. A detailed version of data manipulation, eda and model building can be found [here](https://github.com/yashwant-63/FPL/blob/main/FPL%20Analysis.ipynb).

# Future work
The current app is a very basic version of what I have in mind. I plan to make a much more detailed dashboard including:
1) Performance for the selected FPL team
2) Transfer recommendations for your team for gaining maximum points in the future n gameweeks
3) Wildcard/ Free-Hit drafts
