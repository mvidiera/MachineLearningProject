import os
import sys
from src.exception import CustomException #src-> exceptoion.py for custom exception
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass 

from src.components.data_trasformation import DataTransformation
from src.components.data_trasformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

#extremly important 
#decorator:dataclass is used instead of init method to initialise the values to variables within class.here i just have variables 
# to store, so I am using dataclass. As per definition, dataclass is used ONLY to hold data values. if i had other functions then
# I would use init (constructor)
@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts', 'train.csv')
    test_data_path: str=os.path.join('artifacts', 'test.csv')
    raw_data_path: str=os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()  #this has 3 values train, test, raw data path. 
#As soon as I call dataingestion class-> control goes to DataIngestionConfig and 3 things takes place 

# basic data ingestion 
    def initiate_data_ingestion(self):
        logging.info("Enter the data ingestion method or component")
        try:
            df= pd.read_csv('notebook/data/stud.csv') # basic data reading which is in csv format. to read it from mongo, I need to make changes here alone 
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok= True)
#os.path.dirname checks if train_data-path exist, if yes then it leaves as it is exist_ok=True, if it doesn't exist then
#create new directory called train_data_path using makdirs
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("train test split initiated")
            #splitting data
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            # saving train and test data into train_data_path and test_data_path variable in ingestion config class
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            #returning trainin and testing data path to next step which is transformation
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )


        except Exception as e:
            raise CustomException(e,sys)

if __name__== "__main__":
    obj= DataIngestion()
    train_data, test_data= obj.initiate_data_ingestion()

    data_transformation= DataTransformation()
    train_arr, test_arr, _= data_transformation.initiate_data_transformation(train_data, test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr)) # this prints r2 score