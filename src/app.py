from flask import Flask, request, render_template
import numpy as np 
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline


application= Flask(__name__) #app name, whihc is entry point

app= application

# route for home page

@app.route('/')
def index():
    return render_template('index.html') # when control goes to render_template, this looks for templates (name is imp) folder. 
    #create template folder under the main project file. in templates, index.html is considered

#GET requests are intended to retrieve data from a server and do not modify the server's state. 
#On the other hand, POST requests are used to send data to the server for processing and may modify the server's state.
#The POST method transfers information via HTTP headers
@app.route('/predictdata',methods=["GET", "POST"]) #predictdata is html extension, which uses GET and POST method.
def predict_datapoint():
    if request.method=="GET":
        return render_template('home.html') 
# when user click on predict, she has to input the data so that op can be predicted, so control takes to home.html which has 
# input feild to enter. this is GET method where input has been gotten from user

    #if method is not get then it is post,so this method is written in else block. 
    #else block does the same thing of getting input info same as home.html, if post then flask app is used to get info. 
    # that is, request.form.get fro custom data in predict_pipeline.py
    else:
        data=CustomData( 
            gender= request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score')),

        )
#once I get input data from flask app, then I need to convert it into DF. This is done by get_data_as_data_frame() in predictpipeline.py
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        # actual prediction: initialise predictpipleline to predict_pipeline obj, call predict() using this object
        # pass DF prepared above and store in rresult. print result
        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=results[0]) # show this output in home.html page, this is done by render_template


# to run app.py 
if __name__== "__main__":
    app.run(host="0.0.0.0", debug= True)

# to run this: terminal: python app.py. then go to browser-: 127.0.0.1:5000 (default port: 5000)