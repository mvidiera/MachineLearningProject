import sys
import logging
#from src.logger import logging

#it is common in entire project. That is, whereever I use try catch this will be executed
# whenever exception is raised this message is printed
#exc_info(): If the current thread is handling an exception, exc_info returns a tuple whose three items are the class, object,
# and traceback for the exception. I do not want 1st and 2nd variable, 3rd (which file, line execption has occured) store in exc_tb(traceback)
def error_message_detail(error, error_detail:sys):
    _,_,exc_tb= error_detail.exc_info()
    file_name= exc_tb.tb_frame.f_code.co_filename
    error_message= "Error occured in python script name[{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error) )

    return error_message

    
    #customised error message. 3 place holders 0,1,2. file name will be saved in traceback[frame[code[filename]]]


class CustomException(Exception):

    def __init__(self, error_message, error_detail:sys): #constructor
        super().__init__(error_message) 
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message



