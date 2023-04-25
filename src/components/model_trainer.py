import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path= os.path.join("artifacts", "model.pkl")
# create model.pkl file in artifacts folder once the model is trained. trained_model_file_path is variable 

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config= ModelTrainerConfig()

# step 1: 
# create a dictioanry of all models 
# evaluate_model is function in utils, take all models-> fit X_train and y_train, predction on x_train and x_test-> calculate r2
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info('splitting training and test input data')
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1], # apart from last column, store everythingin train array 
                train_array[:, -1],
                test_array[:,:-1],
                test_array[:,-1],
            )

            models= {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            model_report:dict=evaluate_models(X_train=X_train, y_train= y_train, X_test= X_test, y_test= y_test, models=models)

            #evalaute_model returns the list of models. sort the scores of all model, get the best using max(). value is the model score
            best_model_score = max(sorted(model_report.values()))

            #in last line, I got score, now let me get the model name as well from the dictionary. key is the model name
            best_model_name= list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model= models[best_model_name]

            #setting up treshold for the model accuracy. If accuracy of all models are less than 60% then dont consider any
            if best_model_score<0.6:
                raise CustomException("No best model found")

            logging.info("best model found on both training and testing dataset.")

            # to save model path as pkl file
            save_object(
                file_path= self.model_trainer_config.trained_model_file_path,
                obj= best_model
            )
            
            predicted= best_model.predict(X_test)
            r2_square= r2_score(y_test,predicted)
            return r2_square

            
        except Exception as e:
            raise CustomException(e,sys)

