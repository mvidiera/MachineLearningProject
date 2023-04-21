import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer # for OHE, standard scalar, for pipline
from sklearn.impute import SimpleImputer # for missing data
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
#pickle files for transforming like: caategorical into numerical etc

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path= os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config= DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''

        try:
            numerical_columns= ['writing_score',"reading_score"]
            categorical_columns=[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

#pipleline creation for numerical features. for all numnerical features, check if there is missing data.  
# If yes, fill with median using simpleimputer. next step is to scale the numerical data

            num_pipeline= Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )
            cat_pipeline= Pipeline(

                steps=[
                    ("imputer", SimpleImputer(strategy= "most_frequent")),
                    ("One hot Encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))

                ]
            )
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"numerical columns: {numerical_columns}")
            
#columntransformer is a transformer for all columns. This is nothing but combination of numerical and categorical columns
            preprocessor= ColumnTransformer(
                [
                    ("num_pipelines", num_pipeline, numerical_columns), # pipeline name, what pipeline it is and the columns/data where I need to apply this transformation(pipeline)
                    ("cat_pipelines", cat_pipeline, categorical_columns)              
                ]
            )

            return preprocessor


        except Exception as e:
            raise CustomException(e,sys)


# now definition of data transformation initiation (it will be under Dataclass). Arg are output from data ingestion
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df= pd.read_csv(train_path)
            test_df= pd.read_csv(test_path)

            logging.info("The train and test data reading is completed")

            logging.info("Obtaining preprocessing object") #preprocessor objects are the obj which I have created above

            preprocessing_obj= self.get_data_transformer_object()

            target_column_name= "math_score"
            numerical_columns= ['writing_score',"reading_score"]

            input_feature_train_df= train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df= train_df[target_column_name]

            input_feature_test_df= test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df= test_df[target_column_name]

            logging.info(f"applying preprocessing object on training dataframe and testing dataframe")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

        # c_ : join two matrices by row, left and right. here, dataframe is joined whch has both Independant and predcition data(math score)
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            #applying same to test data. 
            test_arr= np.c_[
                input_feature_test_arr,np.array(target_feature_test_df)

            ]

            logging.info("Saved preprocessng object")

            #saving as pkl file. utils holds common things which I use.. go to utils and 
            save_object(
                file_path= self.data_transformation_config.preprocessor_obj_file_path,
                obj= preprocessing_obj
            )
            return(
                train_arr, 
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path, #pkl file

            )


        except Exception as e:
            raise CustomException(e,sys)

        
