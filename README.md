# Games Success Prediction

## Overview

### Application link: http://3.91.207.237:8501/

The Game Success Prediction Application is designed to predict the potential success of video games based on various features and characteristics. 
This application utilizes machine learning techniques, specifically a Multi-Layer Perceptron Classifier (MLPClassifier), 
to analyze historical game data ([steam-games.csv](https://www.kaggle.com/datasets/amanbarthwal/steam-store-data/data) from Kaggle.com) and provide insights into future game performance.

### Dependencies:
Python 3.11, Altair, Joblib, Pandas, Streamlit, and Scikit-learn.

### Screenshot:
![main](https://github.com/hoan-swe/game-success-prediction/assets/152995318/42f5a1f2-7a83-4079-b121-a3064cbd036c)

## User Guide
To use the application, follow these steps:

### Web app:
1. Open a web browser
2. Go to http://3.91.207.237:8501/
3. Select/toggle features, genres and platforms the potential game will be in
4. Click ‘Predict’ button to see the result
5. Click on ‘Details’ expander to see more information
6. Click ‘Clear’ button in the top right corner to un-select all options
	
### Host the app locally:
1. Fork the repository
2. Clone the repository to your local machine
3. Run the command `streamlit run SuccessPrediction.py`
4. A web browser should open automatically and direct to the app. If not, open a web browser and go to http://localhost:8501 or http://{your_ip_address}:8501
