import os
import sys
import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train,y_train, X_test, y_test, models, param):
    try:
        report= {}

        for i in range(len(list(models))):
            model= list(models.values())[i]
            #hyper parameter tuning
            para= param[list(models.keys())[i]]
            #applying gridsearch cv
            gs= GridSearchCV(model,para,cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred= model.predict(X_train)
            y_test_pred= model.predict(X_test)

            train_model_score=r2_score(y_train, y_train_pred)
            test_model_score= r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)


#this function takes file_path and open it in read byte mode as the file is pickle forma(byte), then store in file_obj var
# this object file_obj is then loaded using dill. (as pkl file is byte stream, dill is used to send python object across the network
# as byte stream)
    def load_obj(file_path):
        try:
            with open(file_path, "rb") as file_obj:
                return dill.load(file_obj)

        except Exception as e:
            raise CustomException(e, sys)
