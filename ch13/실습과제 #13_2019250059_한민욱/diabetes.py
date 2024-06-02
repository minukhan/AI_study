import numpy as np 
import pandas as pd
from sklearn.preprocessing import MinMaxScaler 
import googleapiclient.discovery
import os
from flask import Flask, render_template
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired

bootstrap5 = Bootstrap5(app)

class LabForm(FlaskForm):
    preg=StringField('# Pregnancies', validators=[DataRequired()]) 
    glucose=StringField('Glucose', validators=[DataRequired()]) 
    blood = StringField('Blood pressure', validators=[DataRequired()]) 
    skin = StringField('Skin thickness', validators=[DataRequired()]) 
    insulin = StringField('Insulin', validators=[DataRequired()])
    bmi = StringField('BMI', validators=[DataRequired()])
    dpf = StringField('DPF Score', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()]) 
    submit = SubmitField('Submit')

@app.route('/')
@app.route('/index') 
def index():
    return render_template('index.html')


@app.route('/prediction', methods=['GET', 'POST'])
def lab():
    form=LabForm()
    if form.validate_on_submit():
    # get the dorm data for the patient data and put into a form for the 
        X_test = np.array([[float(form.preg.data),
                            float(form.glucose.data),
                            float(form.blood.data),
                            float(form.skin.data),
                            float(form. insulin.data),
                            float(form.bmi.data),
                            float(form.dpf.data),
                            float(form.age.data)]])
        print(X_test.shape)
        print(X_test)
        # get the data for the diabetes data.   
        data = pd.read_csv('./diabetes.csv', sep=',')

        # extract the x and y from the imported data 
        X = data.values[:, 0:8]
        y = data.values[:, 8]

        # use MinMaxScaler to fit a scaler object 
        scaler=MinMaxScaler()
        scaler.fit(X)
        # min max scale the data for the prediction 
        X_test = scaler.transform(X_test)

        # create the resource to the model web api on GCP
        
        
        
        project_id = 'bustling-day-420206' 
        model_id = "my_pima_model"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="bustling-day-420206-19b5e74e4749.json"
        model_path = "projects/{}/models/{}".format(project_id, model_id) 
        model_path += "/versions/v0001/"
        ml_resource = googleapiclient.discovery.build("ml", "v1").projects()

        # format the data as a json to send to the web api
        input_data_json={"signature_name": "serving_default", "instances": X_test.tolist()}
        # make the prediction
        request = ml_resource.predict(name=model_path, body=input_data_json) 
        response = request.execute()
        print("\nresponse: \n", response)

        if "error" in response:
            raise RuntimeError(response["error"])
        # 모델 생성 시 model.summary()-> 마지막 레이어 참조!!
        predD=np.array([pred['dense_2'] for pred in response["predictions"]])

        print(predD[0][0]) 
        res = predD[0][0]
        res = np.round(res, 2)
        res = (float)(np.round(res * 100))
        return render_template('result.html', res=res) 
    return render_template('prediction.html', form=form)

if __name__ =='__main__':
    app.run()