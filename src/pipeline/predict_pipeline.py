import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self): #empty constructor
        pass

# model pickle file is provided(which has best model)-> preprocessing pkl file is provided-> 
# load best model and pass file path.(load obj is in utils) -> transformation is done (scaling)-> prediction is made and returned.
    def predict(self, features):
        try:
        
            model_path= 'artifacts/model.pkl'
            preprocessor_path= 'artifacts/preprocessor.pkl'

            #load best model-> scale (preprocessing)-> predict
            model= load_object(file_path= model_path)
            preprocessor= load_object(file_path= preprocessor_path)
            data_scale= preprocessor.transform(features)
            #predictions
            preds= model.predict(data_scale)
            return preds

        except Exception as e:
            raise CustomException(e,sys)

#custom dataclass maps all inputs provided by user in html page to backend
# this has all input feilds or independant features
class CustomData:
    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education, 
        lunch:str, 
        test_preparation_course:str,
        reading_score:int,
        writing_score:int,
    ):#assigning all the arguments passed. that is in html page, I select gender as female, that value is mapped here. 
    
        self.gender = gender

        self.race_ethnicity = race_ethnicity

        self.parental_level_of_education = parental_level_of_education

        self.lunch = lunch

        self.test_preparation_course = test_preparation_course

        self.reading_score = reading_score

        self.writing_score = writing_score

#return all input in form of dataframe: return pd.dataframe. from web app the inputs are mapped with this as datafframe. 
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)