# CMPT 383 Final Project

# IMPORTANT VAGRANT INSTRUCTIONS
1. vagrant up 
2. vagrant ssh 
3. cd project 
4. bash run.sh 
5. Access at http://localhost:8085/

# What is the project about? 
A web app for simulating NBA games and predict the winner based on individual team's stats.

# Where is the data coming from?
All the data is coming from NBA stats via API calls (using python). Currently using 2019 season stats to simulate the games. For future iterations, I will implement having the choice to choose the season.

# How are the games simulated?
There are three different models for simulating the games. Model 1 is a simple model (Monte Carlo simulation), it is based on mean points scored by the team, and mean points scored by the opponent's team (calculated in C++). Model 2 is also based on Monte Carlo simulation; however, for model 2, team points and opponent team points are calculated using advanced stats. Model 3 is a slightly more advanced model, model 3 is a naive bayes classifier trained on advanced stats data (win/lose is the class, and advanced stats are the features). \
Model 1 & model 2 simulate 10,000 'games', and model 3 predicts the winner based on 200 'games'.

# How are the languages connected?
Python calls C++ code (where the calculation happens) via SWIG (tried to implement via ctypes & CDLL; however, I had a lot of difficulty with making it work). \
JavaScript calls python code (which fetches the data & calls C++ code to make calculations) via AJAX (jQuery) requests to NodeJS server.

# What did I learned from this project?
I learned that combining different languages in one project is harder than expected.\
I learned that vagrant can be a pain in the butt to set up - especially if the ubuntu mirrors are not defective. \
I learned how to make calls to the server using jQuery! 

# Next steps for the project
Implement Logisitc regression in C++ (instead of simply using scipy library).\
Implement better statistical models for 'simulating' games between teams.