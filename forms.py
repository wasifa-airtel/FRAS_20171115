from flask_wtf import FlaskForm
from wtforms import  FieldList ,StringField,validators, FormField, SubmitField,IntegerField,ValidationError,SelectField,TextField,TextAreaField,PasswordField
from wtforms.validators import DataRequired
from wtforms_components import DateRange
from datetime import datetime, date
from model import *
from wtforms.fields.html5 import DateField


class RegistrationForm(FlaskForm):
    dt = DateField("Registration Date",format="%Y-%m-%d",
        default=datetime.today, 
        validators=[DataRequired()]
    )
    name =StringField('Name', validators=[DataRequired()])
    service_id =StringField('Service id', validators=[DataRequired()])
    unit =StringField('Unit', validators=[DataRequired()])
    brig =StringField('Brigade', validators=[DataRequired()])
    submit = SubmitField('Save')

class BulkRegistrationForm(FlaskForm):
    dt = DateField("Registration Date",format="%Y-%m-%d",
        default=datetime.today, 
        validators=[DataRequired()]
    )
class GroupEditForm(FlaskForm):
    date =  DateField("Date",format="%Y-%m-%d",
        default=datetime.today, 
        validators=[DataRequired()]
    )
    group_no=StringField('Group No', validators=[DataRequired()])
    target_1_army=StringField('Target 1')
    target_2_army=StringField('Target 2')
    target_3_army=StringField('Target 3')
    target_4_army=StringField('Target 4')
    target_5_army=StringField('Target 5')
    target_6_army=StringField('Target 6')
    target_7_army=StringField('Target 7')
    target_8_army=StringField('Target 8')
    submit = SubmitField('Save')
    
class MonthlyReportForm(FlaskForm):
    start_time = DateField('Date :',  format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Report')
    
    
class RegistrationFormBulk(FlaskForm):
    addresses = FieldList(FormField(RegistrationForm), min_entries=3)
    
class RegistrationEditForm(FlaskForm):
    date =  DateField("Registration Date",format="%Y-%m-%d",
        default=datetime.today, 
        validators=[DataRequired()]
    )
    name =StringField('Name', validators=[DataRequired()])
    service_id =StringField('Serice id', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    div =StringField('Division', validators=[DataRequired()])
    cantonment =StringField('Cantonment', validators=[DataRequired()])
    brigade =StringField('Brigade', validators=[DataRequired()])
    unit =StringField('Unit', validators=[DataRequired()])
    rank = StringField('Rank', validators=[DataRequired()])
    submit = SubmitField('Save')


class TargetOne(FlaskForm):
    session_no = StringField('Session No')
    detail_no=IntegerField('Detail No')
    paper_reference =IntegerField('Paper No')
    set_no =IntegerField('Set No')
    target_1_id=StringField('Service No')
    submit = SubmitField('Save')
    
    
class DetailEditForm(FlaskForm):
    date =  DateField("Date",validators=[DataRequired()])
    session_id =StringField('Session No', validators=[DataRequired()])
    detail_no =IntegerField('Detail No', validators=[DataRequired()])
    paper_ref =IntegerField('Paper Reference No', validators=[DataRequired()])
    set_no =IntegerField('Set No', validators=[DataRequired()])
    target_1_service =StringField('Target 1 service_id', validators=[DataRequired()])
    target_2_service =StringField('Target 2 service_id', validators=[DataRequired()])
    target_3_service =StringField('Target 3 service_id', validators=[DataRequired()])
    target_4_service =StringField('Target 4 service_id', validators=[DataRequired()])
    target_5_service =StringField('Target 5 service_id', validators=[DataRequired()])
    target_6_service =StringField('Target 6 service_id', validators=[DataRequired()])
    target_7_service =StringField('Target 7 service_id', validators=[DataRequired()])
    target_8_service =StringField('Target 8 service_id', validators=[DataRequired()])
    submit = SubmitField('Save')
    

class SessionForm(FlaskForm):
    date = DateField('Date',format="%Y-%m-%d",default=datetime.today, validators=[DataRequired()])
    session_no = StringField('Session No', validators=[DataRequired()])
    target_distance=IntegerField('Target Distance', default =100)   
    occ =StringField('Occassion')
    weather_notes = TextAreaField('Weather Notes' ,validators=[DataRequired()])
    comments = TextAreaField('Comments' ,validators=[DataRequired()])  
    submit = SubmitField('Save')



class SessionEditForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d')
    session_no = StringField('Session ID', validators=[DataRequired()])
    target_distance = IntegerField('Target Distance' ,validators=[DataRequired()])
    ammunation_name=TextField('Ammunation' ,validators=[DataRequired()])
    firerarms_name=TextField('Firerarms' ,validators=[DataRequired()])
    range_name=TextField('Firing Range' ,validators=[DataRequired()])
    occ=StringField('Occasion')
    weather_notes = TextAreaField('Weather Notes')
    comments = TextAreaField('Comments')
    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])




    
    
        