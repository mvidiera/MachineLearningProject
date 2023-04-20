import logging
import os
from datetime import datetime
#any execution and all info will be logged and tracked. Anything and everything will be logged

LOG_FILE= f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #file is created and date time which is in string format will be logged. 
logs_path= os.path.join(os.getcwd(), "logs", LOG_FILE) #getcwd get current working directory
os.makedirs(logs_path, exist_ok= True)


LOG_FILE_PATH= os.path.join(logs_path, LOG_FILE)


logging.basicConfig(
    filename= LOG_FILE_PATH, 
    format= "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO,

)