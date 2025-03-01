from flask import Flask,session, render_template,url_for,redirect,flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a secret key"

import pandas as pd
from pymongo import MongoClient
from tkinter import filedialog as fd
import os
import random
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MultiLabelBinarizer
from skmultilearn.adapt import MLkNN
from pymongo import MongoClient

class TeacherLoginForm(FlaskForm):
    teachername=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"Enter your name"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"password"})
    submit=SubmitField("Enter")
    
class FindStudentRecommendation(FlaskForm):
    classname=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"Class Name"})
    course_id=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"Course Id"})
    roll_no=IntegerField(validators=[InputRequired()],render_kw={'placeholder':"Roll No"})
    submit=SubmitField("Search")

class StudentAnalysisForm(FlaskForm):
    course_id = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': "Course Id"})
    course_file = FileField("Choose Course File", validators=[FileAllowed(['csv', 'xlsx'], 'CSV or Excel files only!')])
    student_file = FileField("Choose Students File", validators=[FileAllowed(['csv', 'xlsx'], 'CSV or Excel files only!')])
    submit = SubmitField("Analysis")
    
class ClassAnalysisForm(FlaskForm):
    classname=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"Class Name"})
    course_id=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':"Course Id"})
    submit=SubmitField("Search")
    
    
@app.route('/')
def login():
    return render_template("login.html")


@app.route('/teacherlogin',methods=['GET','POST'])
def teacherlogin():
    
    form = TeacherLoginForm()
   
    mongo_client = MongoClient('mongodb+srv://Upgrade:19Cse357@upgrade.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000')  # Adjust the URI as needed
    db = mongo_client['Upgrade'] 

    if form.validate_on_submit():
        print("hello")
        name = form.teachername.data
        pas = form.password.data
        # Query the database directly for the teacher matching the provided name and password
        teacher = db['Teachers'].find_one({'name': name, 'password': pas})
        
        if teacher:
            session['teacher_name'] = name 
            return redirect(url_for('teacher_dashboard'))
        
        flash("Wrong Username or Password", 'error')
        print("Flash message set") 

    return render_template('teacherlogin.html', form=form)


@app.route('/teacher_dashboard',methods=['GET','POST'])
def teacher_dashboard():
    teacher_name = session.get('teacher_name')
    return render_template('teacher_dashboard.html', teacher_name=teacher_name)


@app.route('/find_student_recommendation',methods=['GET','POST'])
def find_student_recommendation():
    
    mongo_client = MongoClient('mongodb+srv://Upgrade:19Cse357@upgrade.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000')  # Adjust the URI as needed
    db = mongo_client['Upgrade']

    form=FindStudentRecommendation()
    
    if form.validate_on_submit():
        course_id = form.course_id.data
        cls = form.classname.data
        rollno = form.roll_no.data

        students_collection_name = f'Students_{course_id}'

        if students_collection_name not in db.list_collection_names():
            flash(f"Student data for {course_id} does not exist.",'error')
        else:
            df_students = pd.DataFrame(list(db[students_collection_name].find({'Class': cls, 'Student Id': rollno})))
            mark_list = ""
            for index, row in df_students.iterrows():
                for col in df_students.columns:
                    if col != '_id':
                        mark_list += f"{col} : {row[col]}<br>"
                flash(f"{mark_list}",'success')
    return render_template('find_student_recommendation.html',form=form)


@app.route('/find_student_recommendation1',methods=['GET','POST'])
def find_student_recommendation1():
    
    mongo_client = MongoClient('mongodb+srv://Upgrade:19Cse357@upgrade.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000')  # Adjust the URI as needed
    db = mongo_client['Upgrade']
    
    form=FindStudentRecommendation()
    
    if form.validate_on_submit():
        course_id = form.course_id.data
        cls = form.classname.data
        rollno = form.roll_no.data

        students_collection_name = f'Students_{course_id}'

        if students_collection_name not in db.list_collection_names():
            flash(f"Student data for {course_id} does not exist.",'error')
        else:
            df_students = pd.DataFrame(list(db[students_collection_name].find({'Class': cls, 'Student Id': rollno})))
            mark_list = ""
            for index, row in df_students.iterrows():
                for col in df_students.columns:
                    if col != '_id':
                        mark_list += f"{col} : {row[col]}<br>"
                flash(f"{mark_list}",'success')
    return render_template('find_student_recommendation1.html',form=form)


@app.route('/student_dashboard',methods=['GET','POST'])
def student_dashboard():
    return render_template('student_dashboard.html')


@app.route('/student_analysis',methods=['GET','POST'])
def student_analysis():
    form=StudentAnalysisForm()
    if form.validate_on_submit():
        course_id = form.course_id.data
        course_file = form.course_file.data
        student_file = form.student_file.data
        
        print(course_file)
        global course_excell_path, Students_excell_path
        mongo_client = MongoClient('mongodb+srv://Upgrade:19Cse357@upgrade.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000')  # Adjust the URI as needed
        db = mongo_client['Upgrade'] 
        
        UPLOAD_FOLDER = './/Sheets'

        # Ensure the directory exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Save the files
        course_filename = secure_filename(course_file.filename)
        student_filename = secure_filename(student_file.filename)

        course_excell_path = os.path.join(UPLOAD_FOLDER, course_filename).replace("\\","//")
        Students_excell_path = os.path.join(UPLOAD_FOLDER, student_filename).replace("\\","//")
        print(course_excell_path)
        print(Students_excell_path)
        

        course_file.save(course_excell_path)
        student_file.save(Students_excell_path)
        
        
        
        # Send course data ========================================+===========================================================================
        
        file_truth = 0
        
        collection_name = f'Course_{course_id}'
        if collection_name in db.list_collection_names():
            flash(f"The course collection '{collection_name}' already exists.", 'info')
            file_truth = 1
            
        else:        
            xls = pd.ExcelFile(course_excell_path)
            
            if course_id in xls.sheet_names:
                data = pd.read_excel(course_excell_path, sheet_name=course_id)
                collection_course = db[f'Course_{course_id}']
                data_dict = data.to_dict('records')
                result = collection_course.insert_many(data_dict)
                flash(f'Documents inserted: {len(result.inserted_ids)}', 'success')
                file_truth = 1
                
            else: 
                flash(f"No such Course details {course_id} in the given excell sheet",'error')
        
        # Send course data ===================================================================================================================
        
        if file_truth == 1:
            collection_name = f'Students_{course_id}'
            if collection_name in db.list_collection_names():
                flash(f"The students collection '{collection_name}' already exists.", 'info')
            else:
                xls = pd.ExcelFile(Students_excell_path)
                
                if course_id in xls.sheet_names:
                    
                    def dataprep(course_id):
                        global Converted_Assessments_name
                        
                        df_courses = pd.read_excel(course_excell_path, sheet_name=course_id)
                        df_test = pd.read_excel(Students_excell_path, sheet_name=course_id)

                        Assessments = df_courses['Assessments']
                        for i in Assessments:
                            df_test[i].fillna(int(0), inplace=True)
                            df_test[i] = df_test[i]
                        
                        df_test.to_excel(Students_excell_path, sheet_name=course_id, index=False)
                        
                        Total_Marks = list(df_courses['Total Marks'].values)
                        Converted_Marks = list(df_courses['Converted Marks'].values)
                        
                        Converted_Assessments_name = []
                        
                        for i,j in enumerate(Assessments):
                            converted_column_name = j + ' Converted'
                            Converted_Assessments_name.append(converted_column_name)
                            df_test[converted_column_name] = round((df_test[j] * Converted_Marks[i])/ Total_Marks[i])
                            df_test[converted_column_name] = df_test[converted_column_name].astype(int)

                        for i,j in enumerate(Assessments):
                            df_test['Total'] = df_test[Converted_Assessments_name].sum(axis=1)
                            
                        df_test.to_excel(Students_excell_path, sheet_name=course_id, index=False)

                    dataprep(course_id)

                    data = pd.read_excel(Students_excell_path, sheet_name=course_id)
                    collection_Students = db[f'Students_{course_id}']
                    data_dict = data.to_dict('records')
                    result = collection_Students.insert_many(data_dict)
                    flash(f'Documents inserted: {len(result.inserted_ids)}', 'success')
                    
                    
                    #===================================================================================================================================
                    #Generate Dataset

                    def generate_data(course_id):
                            
                        Train_Dataset_Path = course_id + "_train_dataset.xlsx"
                        
                        df_courses = pd.read_excel(course_excell_path,sheet_name=course_id)
                        
                        Assessments = list(df_courses['Assessments'])
                        Converted_Marks = list(df_courses['Converted Marks'].values)
                        
                        max_scores = dict(zip(Assessments, Converted_Marks))
                        total_max_score = sum(max_scores.values())
                        threshold_score = 0.75 * total_max_score
                        
                        Strategies = list(df_courses['Strategies'])
                        Assessments_strategy = dict(zip(Assessments, Strategies))
                        
                        def generate_synthetic_data(row_count):
                            data = []
                            for i in range(row_count):
                                row = {
                                    'Student Id': 22000 + i,  # Generate student IDs incrementally
                                    'Class': 'CSE A',  # Assuming class is the same for all
                                }
                                for assessment in max_scores.keys():
                                    row[assessment] = random.randint(0, max_scores[assessment])
                                data.append(row)
                            return pd.DataFrame(data)

                        row_count = 100000
                        df = generate_synthetic_data(row_count)
                        df.to_excel(Train_Dataset_Path, index=False)
                        
                        def generate_recommendations_based_on_total(row):
                            total_score = 0
                            for _ , mark in row.items():
                                if _ not in ['Student Id', 'Class']:
                                    total_score += mark
                            
                            if total_score < threshold_score:
                                recommendations = []
                                for assessment, con_marks in max_scores.items():
                                    if row[assessment] < 0.75 * con_marks:
                                        recommendations.append(Assessments_strategy[assessment])
                                
                                return "; ".join(recommendations) if recommendations else "Improve performance"
                            
                            elif (total_score >= threshold_score) and (total_score < 0.85 * total_max_score):
                                recommendations = ["Good performance overall"]
                                for assessment, con_marks in max_scores.items():
                                    if row[assessment] < 0.75 * con_marks:
                                        recommendations.append(Assessments_strategy[assessment])
                                
                                return "; ".join(recommendations) if recommendations else "Improve performance"
                            
                            elif (total_score >= 0.85 * total_max_score) and (total_score < 0.9 * total_max_score):
                                recommendations = ["Excelent performance overall"]
                                for assessment, con_marks in max_scores.items():
                                    if row[assessment] < 0.75 * con_marks:
                                        recommendations.append(Assessments_strategy[assessment])
                                
                                return "; ".join(recommendations) if recommendations else "Improve performance"
                            
                            elif (total_score >= 0.9 * total_max_score):
                                return "Outstanding performance overall"

                        df['Recommendation'] = df.apply(generate_recommendations_based_on_total, axis=1)
                        df.to_excel(Train_Dataset_Path, index=False)
                        flash(f"Dataset created successfully.", 'success')
                        

                    #====================================================================================================================================
                    #Train Dataset

                    def training_data(course_id):
                        
                        model_file_path = course_id + "_dataset_model.joblib"
                        mlb_file_path = course_id + '_dataset_mlb.joblib'

                        if os.path.isfile(model_file_path):
                            #print(f"{model_file_path} exists.")
                            pass
                        else:
                            #print(f"{model_file_path} does not exist. So creating the model")
                            
                            Train_Dataset_Path = course_id + "_train_dataset.xlsx"
                            
                            df_courses = pd.read_excel(course_excell_path,sheet_name=course_id)
                            Assessments = list(df_courses['Assessments'])
                        
                            df = pd.read_excel(Train_Dataset_Path)

                            X = df[Assessments]

                            df['Recommendation'] = df['Recommendation'].fillna("")
                            df['Recommendation'] = df['Recommendation'].apply(lambda x: x.split("; ") if x else [])

                            mlb = MultiLabelBinarizer()
                            Y = mlb.fit_transform(df['Recommendation'])

                            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

                            mlknn = MLkNN(k=30)

                            mlknn.fit(X_train, Y_train)

                            Y_pred = mlknn.predict(X_test)

                            accuracy = accuracy_score(Y_test, Y_pred.toarray())
                            print("Accuracy: {:.2f}%".format(accuracy * 100))
                            flash("Accuracy: {:.2f}%".format(accuracy * 100), 'info')
                            
                            joblib.dump(mlknn, model_file_path)
                            flash(f"Model saved as {model_file_path}", 'success')
                            joblib.dump(mlb, mlb_file_path)
                            flash(f"MLB saved as {mlb_file_path}", 'success')
                            os.remove(Train_Dataset_Path)


                    #==================================================================================================================================== 
                    #Student Analysis

                    def student_recommendation(course_id):
                        
                        model_file_path = course_id + "_dataset_model.joblib"
                        mlb_file_path = course_id + '_dataset_mlb.joblib'
                        loaded_model = joblib.load(model_file_path)
                        mlb = joblib.load(mlb_file_path)

                        student_collection_name = f'Students_{course_id}'
                        df_students = pd.DataFrame(list(db[student_collection_name].find()))

                        if df_students.empty:
                            print(f"No student data found in the {student_collection_name} collection.")
                            return

                        course_collection_name = f'Course_{course_id}'
                        df_courses = pd.DataFrame(list(db[course_collection_name].find()))

                        if df_courses.empty:
                            print(f"No course data found in the {course_collection_name} collection.")
                            return

                        Converted_Assessments_name = list(df_courses['Assessments'])
                        
                        recommendations_list = []

                        for index, row in df_students.iterrows():
                            test_data = {assessment: [row[assessment]] for assessment in Converted_Assessments_name if assessment in row}
                            test_df = pd.DataFrame(test_data)
                            
                            predictions = loaded_model.predict(test_df)
                            predicted_labels = mlb.inverse_transform(predictions.toarray())

                            recommendation = ""
                            for labels in predicted_labels:
                                if labels:
                                    recommendation += f"{', '.join(labels)}; "
                                else:
                                    recommendation += "No Recommendations; "
                            recommendations_list.append(recommendation)

                        df_students['Recommendation'] = recommendations_list

                        for index, row in df_students.iterrows():
                            db[student_collection_name].update_one({'_id': row['_id']}, {'$set': {'Recommendation': row['Recommendation']}})

                        flash(f"Recommendation complete for Course ID {course_id}",'success')


                    #==================================================================================================================================== 
                    #Class Analysis

                    def class_analysis_recommendation(course_id):
                        students_collection_name = f'Students_{course_id}'
                        class_collection_name = f'Class_{course_id}'

                        if students_collection_name not in db.list_collection_names():
                            print(f"Student data for {course_id} does not exist.")
                            return

                        df_students = pd.DataFrame(list(db[students_collection_name].find()))

                        df_courses = pd.DataFrame(list(db[f'Course_{course_id}'].find()))
                        Assessments = list(df_courses['Assessments'])

                        class_avg = df_students.groupby('Class')[Assessments].mean().reset_index().round(2)

                        model_file_path = f"{course_id}_dataset_model.joblib"
                        mlb_file_path = f"{course_id}_dataset_mlb.joblib"
                        loaded_model = joblib.load(model_file_path)
                        mlb = joblib.load(mlb_file_path)

                        recommendations_list = []

                        for index, row in class_avg.iterrows():
                            class_name = row['Class']
                            
                            test_data = {assessment: [row[assessment]] for assessment in Assessments}
                            test_df = pd.DataFrame(test_data)

                            predictions = loaded_model.predict(test_df)
                            predicted_labels = mlb.inverse_transform(predictions.toarray())

                            recommendation = ""
                            for labels in predicted_labels:
                                if labels:
                                    recommendation += f"{', '.join(labels)}; "
                                else:
                                    recommendation += "No Recommendations; "

                            class_data = {'Class': class_name, 'Recommendation': recommendation}

                            for assessment in Assessments:
                                class_data[assessment] = row[assessment]

                            recommendations_list.append(class_data)

                        db[class_collection_name].insert_many(recommendations_list)

                        flash(f"Class analysis stored successfully in the collection {class_collection_name}.", 'success')
                    
                    
                    generate_data(course_id)
                    training_data(course_id)
                    student_recommendation(course_id)
                    class_analysis_recommendation(course_id)
                    model_file_path = f"{course_id}_dataset_model.joblib"
                    mlb_file_path = f"{course_id}_dataset_mlb.joblib"
                    os.remove(model_file_path)
                    os.remove(mlb_file_path)
                else: 
                    flash(f"No such Students Marks of the course {course_id} in the given excell sheet", 'error')

                
    return render_template('student_analysis.html',form=form)


@app.route('/class_analysis',methods=['GET','POST'])
def class_analysis():
    mongo_client = MongoClient('mongodb+srv://Upgrade:19Cse357@upgrade.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000')  # Adjust the URI as needed
    db = mongo_client['Upgrade']
    
    form=ClassAnalysisForm()
    
    if form.validate_on_submit():
        course_id = form.course_id.data
        cls = form.classname.data

        class_collection_name = f'Class_{course_id}'

        if class_collection_name not in db.list_collection_names():
            flash(f"Class data for {course_id} does not exist.",'error')
        else:
            df_class = pd.DataFrame(list(db[class_collection_name].find({'Class': cls})))
            mark_list = ""
            
            for index, row in df_class.iterrows():
                for col in df_class.columns:
                    if col != '_id':
                        mark_list += f"{col} : {row[col]}<br>"
                flash(f"{mark_list}",'success')
    return render_template('class_analysis.html',form=form)

if __name__ == "__main__":
    app.run(debug=True)
