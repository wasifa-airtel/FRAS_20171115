#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:16:47 2017

@author: wasifaahmed
"""

from flask import Flask, flash,render_template, request, Response, redirect, url_for, send_from_directory,jsonify,session
import json as json
from datetime import datetime,timedelta,date
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image
from flask.ext.sqlalchemy import SQLAlchemy
import matplotlib.image as mpimg
from io import StringIO
from skimage import data, exposure, img_as_float ,io,color
import scipy
from scipy import ndimage
import time
import tensorflow as tf
import os , sys
import shutil
import numpy as np
import pandas as pd
from PIL import Image
from model import *
from sqlalchemy.sql import text
from sqlalchemy import *
from forms import *
import math
from io import StringIO
import csv
from sqlalchemy.orm import load_only
from datetime import datetime,date
from numpy import genfromtxt
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_bootstrap import Bootstrap



graph = tf.Graph()
with graph.as_default():    
    sess = tf.Session(graph=graph)
    init_op = tf.global_variables_initializer()
    pointsarray=[]
    
    def load_model():
        sess.run(init_op)
        saver = tf.train.import_meta_graph('E:/FRAS Windows/FRAS_production/Simulation/FRAS_20170726/FRAS_20170727.meta')
        #saver = tf.train.import_meta_graph('/Users/wasifaahmed/Documents/FRAS/Fras_production_v.0.1/FRAS Windows/FRAS Windows/FRAS_production/Simulation/FRAS_20170726/FRAS_20170727.meta')
        print('The model is loading...')
        #saver.restore(sess, "/Users/wasifaahmed/Documents/FRAS/Fras_production_v.0.1/FRAS Windows/FRAS Windows/FRAS_production/Simulation/FRAS_20170726/FRAS_20170727")
        saver.restore(sess, 'E:/FRAS Windows/FRAS_production/Simulation/FRAS_20170726/FRAS_20170727')
        print('loaded...')
        pass
        
    engine =create_engine('postgresql://postgres:user@localhost/postgres')
    Session = scoped_session(sessionmaker(bind=engine))
    mysession = Session()
    app = Flask(__name__)
    app.config.update(
    DEBUG=True,
    SECRET_KEY='\xa9\xc2\xc6\xfa|\x82\x1a\xfa\x1b#~\xd6ppR=\x1e4\xfb`-\xc0\xad\xc9')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:user@localhost/fras_production'
    db.init_app(app)
    Bootstrap(app)
    
    @app.after_request
    def add_header(response):    
         response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
         response.headers['Cache-Control'] = 'public, max-age=0'
         return response

    
    @app.route('/',methods=['GET', 'POST']) 
    def login():
        form = LoginForm()
        return render_template('forms/login.html', form=form)
    
    
    @app.route('/home',methods=['GET', 'POST']) 
    def index():
        return render_template('pages/home.html')
    
    
    
    @app.route('/detail_setup/') 
    def Detail_Setup():
        curdate=time.strftime("%Y-%m-%d")
        selection=Shooting_Session.query.filter(Shooting_Session.date>=curdate).order_by(Shooting_Session.datetimestamp.desc()).all()
        firer_1 = [row.service_id for row in Shooter.query.all()]
        return render_template('pages/detail_setup.html',
                               data=selection,
                               firer_1=firer_1)
        
    @app.route('/auto_setup/') 
    def auto_setup():
        drop=[]
        curdate=time.strftime("%Y-%m-%d")
        form=BulkRegistrationForm()
        selection_2=Shooting_Session.query.filter(Shooting_Session.date>=curdate).order_by(Shooting_Session.datetimestamp.desc()).all()
        selection=TGroup.query.distinct(TGroup.group_no).filter(TGroup.date==curdate).all()
        return render_template('pages/auto_setup.html',
                               data=selection, data_2=selection_2,form=form) 
        
    @app.route('/auto_setup_1/') 
    def auto_setup_1():
        drop=[]
        curdate=time.strftime("%Y-%m-%d")
        form=BulkRegistrationForm()
        selection_2=Shooting_Session.query.filter(Shooting_Session.date>=curdate).order_by(Shooting_Session.datetimestamp.desc()).all()
        selection=TGroup.query.distinct(TGroup.group_no).all()
        return render_template('pages/auto_setup_1.html',
                               data=selection, data_2=selection_2,form=form)     
    @app.route('/group_gen/',methods=['GET', 'POST'])
    def group_gen():
        da_1=None
        da_2=None
        da_3=None
        da_4=None
        da_5=None
        da_6=None
        da_7=None
        da_8=None
        
        if request.method == "POST":
            data = request.get_json()
            group=data['data']
            session['group']=group
            data=TGroup.query.filter(TGroup.group_no==group).scalar()
            da_1=data.target_1_no
            da_2=data.target_2_no
            da_3=data.target_3_no
            da_4=data.target_4_no
            da_5=data.target_5_no
            da_6=data.target_6_no
            da_7=data.target_7_no
            da_8=data.target_8_no
        return jsonify(data1=da_1,
                       data2=da_2,
                       data3=da_3,
                       data4=da_4,
                       data5=da_5,
                       data6=da_6,
                       data7=da_7,
                       data8=da_8
                       
                       
                       )
        
        
    @app.route('/detail_exitence_1/',methods=['GET', 'POST'])
    def detail_exitence_1():
            ra_1=None
            da_1=None
            detail=None
            service_id_1=None
            session=None
            paper=None
            set_no=None
            cant=None
            
            if request.method == "POST":
                data = request.get_json()
                detail=data['data']
                dt=time.strftime("%Y-%m-%d")
                data=db.session.query(Session_Detail).filter(Session_Detail.detail_no==detail).scalar()
                db.session.query(TShooting).delete()
                db.session.commit()
                Tdetail_shots =TShooting(
                                            date=datetime.now(),
                                            datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                            session_id=data.session_id,
                                            detail_no=data.detail_no,
                                            target_1_id=data.target_1_id,
                                            target_2_id=data.target_2_id,
                                            target_3_id=data.target_3_id,
                                            target_4_id=data.target_4_id,
                                            target_5_id=data.target_5_id,
                                            target_6_id=data.target_6_id,
                                            target_7_id=data.target_7_id,
                                            target_8_id=data.target_8_id,
                                            paper_ref=data.paper_ref,
                                            set_no=data.set_no,
                                            save_flag=0
                                            )
                db.session.add(Tdetail_shots)
                db.session.commit()
                res=[]
                ten=[]
                gp_len=[]
                tten=db.session.query(MPI.tendency_code).filter(MPI.firer_id==data.target_1_id).order_by(MPI.datetimestamp.desc()).limit(5).all()[::-1]
                tres = db.session.query(Grouping.result).filter(Grouping.firer_id==data.target_1_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]
                tgp = db.session.query(Grouping.grouping_length_f).filter(Grouping.firer_id==data.target_1_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]
                for ele in tres:
                    for ele2 in ele:
                        res.append(ele2)
                
                for ele3 in tten:
                    for ele4 in ele3:
                        
                        ten.append(ele4)
                        
                for ele5 in tgp:
                    for ele6 in ele5:
                        gp_len.append(ele6)  
                        
                da_1=db.session.query(Shooter.name).filter(Shooter.id==data.target_1_id).scalar()
                cant_id=db.session.query(Shooter.cantonment_id).filter(Shooter.id==data.target_1_id).scalar()
                cant=db.session.query(Cantonment.cantonment).filter(Cantonment.id==cant_id).scalar()
                ra_1_id=db.session.query(Shooter.rank_id).filter(Shooter.id==data.target_1_id).scalar()
                ra_1 = db.session.query(Rank.name).filter(Rank.id==ra_1_id).scalar()
                session=db.session.query(TShooting.session_id).scalar()
                paper=db.session.query(TShooting.paper_ref).scalar()
                set_no=db.session.query(TShooting.set_no).scalar()
                service_id_1 = db.session.query(Shooter.service_id).filter(Shooter.id==data.target_1_id).scalar()
                
                
            return jsonify(
                       data1=da_1,
                       ra_1=ra_1,
                       detail=detail,
                       service_id_1=service_id_1,
                       session=session,
                       paper=paper,
                       set_no=set_no,
                       cant=cant,
                       res=res,
                       ten=ten,
                       gp_len=gp_len
                       )
    


    
    @app.route('/generate_ref/' ,methods=['GET', 'POST'])
    def generate_ref():
        g=None
        
        if request.method == "POST":
            data = request.get_json()
            paper_ref =data['data']
            
            if (paper_ref == 'New'):
                
                g=0              
            else:
                obj=TPaper_ref.query.scalar()
                g= obj.paper_ref
                
        return jsonify(gen=int(g))
    

    @app.route('/create_detail_target_2/', methods=['GET', 'POST'])    
    def create_detail_target_2():
        curdate=time.strftime("%Y-%m-%d")
        firer_1 = [row.service_id for row in Shooter.query.all()]
        detail_data=TShooting.query.scalar()
        return render_template('pages/create_detail_target_2.html',
                               detail_data=detail_data,
                               firer_1=firer_1
                               )
    @app.route('/save_target_2/', methods=['GET', 'POST'])
    def save_target_2():
        r=request.form['tag']
        r_object=Shooter.query.filter(Shooter.service_id==r).scalar()
        r_id=r_object.id
        ses=Session_Detail.query.first()
        ses.target_2_id=r_id
        db.session.commit()
        temp =TShooting.query.first()
        temp.target_2_id=r_id
        db.session.commit()
        return redirect(url_for('individual_score_target_2'))
    
    @app.route('/create_detail_target_1/', methods=['GET', 'POST'])    
    def create_detail_target_1():
        curdate=time.strftime("%Y-%m-%d")
        selection=Shooting_Session.query.filter(Shooting_Session.date==curdate).all()
        firer_1 = [row.service_id for row in Shooter.query.all()]
        return render_template('pages/create_detail_target_1.html',
                               data=selection,
                               firer_1=firer_1
                               )
    

    @app.route('/create_session/', methods=['GET', 'POST'])
    def create_session():
        try:
            data = Shooter.query.all()
            rang= Range.query.all()
            firearms = Firearms.query.all()
            ammunation = Ammunation.query.all()
            rang_name = request.form.get('comp_select_4')
            fire_name = request.form.get('comp_select_5')
            ammu_name = request.form.get('comp_select_6')
            form=SessionForm()
            
            if(rang_name is None):
                range_id=999
                fire_id=999
                ammu_id=999
            else:
                range_id = db.session.query(Range.id).filter(Range.name==rang_name).scalar()
                fire_id = db.session.query(Firearms.id).filter(Firearms.name==fire_name).scalar()
                ammu_id = db.session.query(Ammunation.id).filter(Ammunation.name==ammu_name).scalar()
        
                
                if form.validate_on_submit():
                    shooting=Shooting_Session(
                                    date=form.date.data.strftime('%Y-%m-%d'),
                                    datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                    shooting_range_id=range_id,
                                    firearms_id=fire_id,
                                    ammunation_id=ammu_id,
                                    target_distance = form.target_distance.data,
                                    weather_notes = form.weather_notes.data,
                                    comments = form.comments.data,
                                    session_no=form.session_no.data,
                                    occasion=form.occ.data
                                      )
                    
                    db.session.add(shooting)
                    db.session.commit()
                    return redirect(url_for('create_detail_target_1'))
        except Exception as e:
            return redirect(url_for('error5_505.html'))
        return render_template('forms/shooting_form.html', form=form, data =data ,rang=rang , firearmns=firearms, ammunation = ammunation)
    
    
    @app.route('/monthly_report/',methods=['GET','POST'])
    def monthly_report():
        year=None
        month=None
        date_start=None
        try:
            if request.method=='POST':
                month=request.form.get('comp_select')
                year = datetime.now().year
                if (month == 'October'):
                    dt_start='-10-01'
                    dt_end ='-10-31'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                elif(month=='January'):
                    dt_start='-01-01'
                    dt_end ='-01-31'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                elif(month=='February'):
                    dt_start='-02-01'
                    dt_end ='-02-28'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                elif(month=='March'):
                    dt_start='-03-01'
                    dt_end ='-03-31'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                elif(month=='April'):
                    dt_start='-04-01'
                    dt_end ='-04-30'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                elif(month=='May'):
                    dt_start='-05-01'
                    dt_end ='-05-31'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                elif(month=='June'):
                    dt_start='-06-01'
                    dt_end ='-06-30'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                elif(month=='July'):
                    dt_start='-07-01'
                    dt_end ='-07-31'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                elif(month=='August'):
                    dt_start='-08-01'
                    dt_end ='-08-31'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                elif(month=='September'):
                    dt_start='-09-01'
                    dt_end ='-09-30'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                elif(month=='November'):
                    dt_start='-11-01'
                    dt_end ='-11-30'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                else:
                    dt_start='-12-01'
                    dt_end ='-12-31'
                    str_date_start = str(year)+dt_start
                    date_start=datetime.strptime(str_date_start, "%Y-%m-%d")
                    str_date_end  = str(year)+dt_end
                    date_end=datetime.strptime(str_date_end, "%Y-%m-%d")
                    dat1=db.session.query(Grouping.date,Shooter.service_id,Rank.name,Shooter.name.label('firer'),Shooter.unit,Shooter.brigade,Grouping.detail_no,Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.date.between(date_start,date_end), Grouping.firer_id==Shooter.id,Shooter.rank_id==Rank.id and Grouping.date==MPI.date, Grouping.session_id==MPI.session_id,Grouping.firer_id==MPI.firer_id,Grouping.detail_no==MPI.detail_no,Grouping.target_no==MPI.target_no,Grouping.spell_no==MPI.spell_no,Grouping.paper_ref==MPI.paper_ref).all()
                    
                return render_template('pages/monthly_report.html', dat1=dat1 ,month=month)
                
        except Exception as e:
                return render_template('errors/month_session.html')    
        return render_template('pages/monthly_report.html')
    
    
    @app.route('/save_target_1/', methods=['GET', 'POST'])
    def save_target_1():
        ref_1=None
        try:
            if request.method == 'POST':
                     detail_no = request.form['game_id_1']
                     r=request.form['tag']
                     r_object=Shooter.query.filter(Shooter.service_id==r).scalar()
                     r_id=r_object.id
                     r2_id=999
                     r3_id=999
                     r4_id=999
                     r5_id=999
                     r6_id=999
                     r7_id=999
                     r8_id=999
                     ref=request.form['business']
                     set_no = request.form.get('comp_select_6')
                     shots = request.form['tag_8']
                     sess=request.form.get('comp_select')
                     ref_1 = None
                     paper=db.session.query(TPaper_ref).scalar()
                     if(ref == ""):
                         ref_1=paper.paper_ref
                     else:
                         ref_1=ref
                     temp_shooting=db.session.query(TShooting).scalar()
                     
                     if(temp_shooting is None):
                         
                         
                         detail_shots =Session_Detail(
                                    date=datetime.now(),
                                    datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                    session_id=sess,
                                    detail_no=detail_no,
                                    target_1_id=r_id,
                                    target_2_id=r2_id,
                                    target_3_id=r3_id,
                                    target_4_id=r4_id,
                                    target_5_id=r5_id,
                                    target_6_id=r6_id,
                                    target_7_id=r7_id,
                                    target_8_id=r8_id,
                                    paper_ref=ref_1,
                                    set_no=set_no,
                                    save_flag=0
                                   
                                    )
                         db.session.add(detail_shots)
                         db.session.commit()
                     
                         db.session.query(TPaper_ref).delete()
                         db.session.commit()
                                
                         ref_db = TPaper_ref(
                                        paper_ref=ref_1,
                                        detail_no=detail_no,
                                        session_no=sess
                                        )
                         db.session.add(ref_db)
                         db.session.commit()
                                
                         Tdetail_shots =TShooting(
                                        date=datetime.now(),
                                        datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                        session_id=sess,
                                        detail_no=detail_no,
                                        target_1_id=r_id,
                                        target_2_id=r2_id,
                                        target_3_id=r3_id,
                                        target_4_id=r4_id,
                                        target_5_id=r5_id,
                                        target_6_id=r6_id,
                                        target_7_id=r7_id,
                                        target_8_id=r8_id,
                                        paper_ref=ref_1,
                                        set_no=set_no,
                                        save_flag=0
                                        )
                         db.session.add(Tdetail_shots)
                         db.session.commit()
                         
                     else:
                         
                         db.session.query(TShooting).delete()
                         
                         
                         db.session.commit()
                         
                         
                         db.session.query(TPaper_ref).delete()
                         db.session.commit()
                                
                         ref_db = TPaper_ref(
                                        paper_ref=ref_1,
                                        detail_no=detail_no,
                                        session_no=sess
                                        )
                         db.session.add(ref_db)
                         db.session.commit()
                         
                         detail_shots =Session_Detail(
                                    date=datetime.now(),
                                    datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                    session_id=sess,
                                    detail_no=detail_no,
                                    target_1_id=r_id,
                                    target_2_id=r2_id,
                                    target_3_id=r3_id,
                                    target_4_id=r4_id,
                                    target_5_id=r5_id,
                                    target_6_id=r6_id,
                                    target_7_id=r7_id,
                                    target_8_id=r8_id,
                                    paper_ref=ref_1,
                                    set_no=set_no,
                                    save_flag=0
                                   
                                    )
                         db.session.add(detail_shots)
                         db.session.commit()
                                
                         Tdetail_shots =TShooting(
                                        date=datetime.now(),
                                        datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                        session_id=sess,
                                        detail_no=detail_no,
                                        target_1_id=r_id,
                                        target_2_id=r2_id,
                                        target_3_id=r3_id,
                                        target_4_id=r4_id,
                                        target_5_id=r5_id,
                                        target_6_id=r6_id,
                                        target_7_id=r7_id,
                                        target_8_id=r8_id,
                                        paper_ref=ref_1,
                                        set_no=set_no,
                                        save_flag=0
                                        )
                         db.session.add(Tdetail_shots)
                         db.session.commit()
        except Exception as e:
            
            return redirect(url_for('error_target_1')) 
        return redirect(url_for('individual_score_target_1'))
        
    @app.route('/FRAS/', methods=['GET', 'POST'])
    def load ():
        try:
            
            ref_1=None
            
            if request.method == 'POST':
               
                detail_no = request.form['game_id_1']            
                tmp_list = []
                duplicate = False
                r=request.form['tag']
                if (r== ""):
                    r_id = 999
                else:
                    r_object=Shooter.query.filter(Shooter.service_id==r).scalar()
                    r_id=r_object.id
                r1=request.form['tag_1']
                if(r1== ""):
                    r1_id=999
                else:
                    r1_object=Shooter.query.filter(Shooter.service_id==r1).scalar()
                    r1_id=r1_object.id
                r2=request.form['tag_2'] 
                if (r2==""):
                    r2_id=999
                else:
                    r2_object=Shooter.query.filter(Shooter.service_id==r2).scalar()
                    r2_id=r2_object.id
    
                    
                r3=request.form['tag_3']
                if(r3==""):
                    r3_id=999
                else:
                    r3_object=Shooter.query.filter(Shooter.service_id==r3).scalar()
                    r3_id=r3_object.id
                    
                r4=request.form['tag_4']
                if(r4==""):
                    r4_id=999
                else:
                    r4_object=Shooter.query.filter(Shooter.service_id==r4).scalar()
                    r4_id=r4_object.id
    
                r5=request.form['tag_5']
                
                if(r5==""):
                    r5_id=999
                else:
                    r5_object=Shooter.query.filter(Shooter.service_id==r5).scalar()
                    r5_id=r5_object.id
    
            
                r6=request.form['tag_6']
                
                if(r6==""):
                    r6_id=999
                else:
                    r6_object=Shooter.query.filter(Shooter.service_id==r6).scalar()
                    r6_id=r6_object.id
               
                r7=request.form['tag_7']
                
                if(r7== ""):
                    r7_id=999
                else:
                    r7_object=Shooter.query.filter(Shooter.service_id==r7).scalar()
                    r7_id=r7_object.id
                    
                ref=request.form['business']
                
                set_no = request.form.get('comp_select_6')
                shots = request.form['tag_8']
                sess=request.form.get('comp_select')
                
                tmp_list.append(r_id)
                tmp_list.append(r1_id)
                tmp_list.append(r2_id)
                tmp_list.append(r3_id)
                tmp_list.append(r4_id)
                tmp_list.append(r5_id)
                tmp_list.append(r6_id)
                tmp_list.append(r7_id)
                
               
                
                if ref == None or ref =="":
                    
                    ref_obj=TPaper_ref.query.scalar()
                    ref_1=ref_obj.paper_ref
                    
                
                else :
                    print("Inside ref _4 else")
                    ref_1=ref
                    print(ref_1)
                    
                    print("Inside ref _4 else 1")
                    if(int(set_no)>5):
                        print("Inside ref _5 else")
                        return redirect(url_for('paper_duplicate_error'))
                    
                    else:
                        print("Inside TPaper_ref")
                        db.session.query(TPaper_ref).delete()
                        print("Inside TPaper_ref")
                        db.session.commit()
                        
                        ref_db = TPaper_ref(
                                paper_ref=ref_1,
                                detail_no=detail_no,
                                session_no=sess
                                )
                        db.session.add(ref_db)
                        db.session.commit()
           
            
                print("Inside load 3")
                for i in range(len(tmp_list)):
                    for j in range(len(tmp_list)):
                        if(tmp_list[i]== 999 and tmp_list[j]==999):
                            duplicate = False
                        elif(i!=j and tmp_list[i]==tmp_list[j]):
                            duplicate = True
                           
                print("temp1")
                if(duplicate):
                    return redirect(url_for('duplicate_firer_error'))
                else: 
                    print("temp")
                    temp=db.session.query(TShooting.save_flag).scalar()
                    print(temp)
                    if(temp is None):
                        print("Inside the temp if")
                        print(sess)
                        print(detail_no)
                        Tdetail_shots =TShooting(
                                        date=datetime.now(),
                                        datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                        session_id=sess,
                                        detail_no=detail_no,
                                        target_1_id=r_id,
                                        target_2_id=r1_id,
                                        target_3_id=r2_id,
                                        target_4_id=r3_id,
                                        target_5_id=r4_id,
                                        target_6_id=r5_id,
                                        target_7_id=r6_id,
                                        target_8_id=r7_id,
                                        paper_ref=ref_1,
                                        set_no=set_no,
                                        save_flag=0
                                        )
                        print(Tdetail_shots)
                        print("Tdetail_shots")
                        db.session.add(Tdetail_shots)
                        db.session.commit()
                        print(""
                              )
                        detail_shots =Session_Detail(
                            date=datetime.now(),
                            datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                            session_id=sess,
                            detail_no=detail_no,
                            target_1_id=r_id,
                            target_2_id=r1_id,
                            target_3_id=r2_id,
                            target_4_id=r3_id,
                            target_5_id=r4_id,
                            target_6_id=r5_id,
                            target_7_id=r6_id,
                            target_8_id=r7_id,
                            paper_ref=ref_1,
                            set_no=set_no,
                            save_flag=0
                            )
                        db.session.add(detail_shots)
                        db.session.commit()
                    else:
                        db.session.query(TShooting).filter(TShooting.id != 999).delete()
                        db.session.commit()
                        
                        Tdetail_shots =TShooting(
                                date=datetime.now(),
                                datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                session_id=sess,
                                detail_no=detail_no,
                                target_1_id=r_id,
                                target_2_id=r1_id,
                                target_3_id=r2_id,
                                target_4_id=r3_id,
                                target_5_id=r4_id,
                                target_6_id=r5_id,
                                target_7_id=r6_id,
                                target_8_id=r7_id,
                                paper_ref=ref_1,
                                set_no=set_no,
                                save_flag=0
                                )
                        db.session.add(Tdetail_shots)
                        db.session.commit()
                        detail_shots =Session_Detail(
                            date=datetime.now(),
                            datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                            session_id=sess,
                            detail_no=detail_no,
                            target_1_id=r_id,
                            target_2_id=r1_id,
                            target_3_id=r2_id,
                            target_4_id=r3_id,
                            target_5_id=r4_id,
                            target_6_id=r5_id,
                            target_7_id=r6_id,
                            target_8_id=r7_id,
                            paper_ref=ref_1,
                            set_no=set_no,
                            save_flag=0
                            )
                        db.session.add(detail_shots)
                        db.session.commit()
                    
        except Exception as e:
             print(e)
             return redirect(url_for('error_2'))
        return redirect(url_for('image_process'))
    
    
    @app.route('/FRAS_1/', methods=['GET', 'POST'])
    def load_1 ():
        ref_1=None
        try:
            if request.method == 'POST':
                print("This is inside Post")
                
                detail_no = request.form['game_id_1']  
                print("this is detail_no")
                print(detail_no)
                tmp_list = []
                duplicate = False
                gr=session.get('group',None)
                data=TGroup.query.filter(TGroup.group_no==gr).scalar()
                da_1=data.target_1_no
                da_2=data.target_2_no
                da_3=data.target_3_no
                da_4=data.target_4_no
                da_5=data.target_5_no
                da_6=data.target_6_no
                da_7=data.target_7_no
                da_8=data.target_8_no
                if(da_1==""):
                    r_id=999
                else:
                    r=Shooter.query.filter(Shooter.service_id==da_1).scalar()
                    r_id=r.id
                if(da_2==""):
                    r1_id=999
                else:
                    r1=Shooter.query.filter(Shooter.service_id==da_2).scalar()
                    r1_id=r1.id
                if(da_3==""):
                    r2_id=999
                else:
                    
                    r2=Shooter.query.filter(Shooter.service_id==da_3).scalar()
                    r2_id=r2.id
                
                
                if(da_4==""):
                    r3_id=999
                else:
                    r3=Shooter.query.filter(Shooter.service_id==da_4).scalar()
                    r3_id=r3.id
                    
               
                if(da_5==""):
                    r4_id=999
                else:
                    r4=Shooter.query.filter(Shooter.service_id==da_5).scalar()
                    r4_id=r4.id
                
                
                
                if(da_6==""):
                    r5_id=999
                else:
                    r5=Shooter.query.filter(Shooter.service_id==da_6).scalar()
                    r5_id=r5.id
               
                
                if(da_7==""):
                    r6_id=999
                else:
                    r6=Shooter.query.filter(Shooter.service_id==da_7).scalar()
                    r6_id=r6.id
                
                
                if(da_8==""):
                    r7_id=999
                else:
                    r7=Shooter.query.filter(Shooter.service_id==da_8).scalar()
                    r7_id=r7.id
                ref=request.form['business']
                set_no = request.form.get('comp_select_6')
                shots = request.form['tag_8']
                sess=request.form.get('comp_select')
                
                tmp_list.append(r_id)
                tmp_list.append(r1_id)
                tmp_list.append(r2_id)
                tmp_list.append(r3_id)
                tmp_list.append(r4_id)
                tmp_list.append(r5_id)
                tmp_list.append(r6_id)
                tmp_list.append(r7_id)
                
                print(tmp_list)
                
                if ref == None or ref =="":
                    ref_obj=TPaper_ref.query.scalar()
                    ref_1=ref_obj.paper_ref
                    
                
                else :
                    ref_1=ref
                    check=TPaper_ref.query.scalar()
                    
                    cses=check.session_no
                    det=check.detail_no
                    
                    
                    if(int(set_no)>5):
                        return redirect(url_for('paper_duplicate_error'))
                    else:
                        db.session.query(TPaper_ref).delete()
                        db.session.commit()
                        
                        ref_db = TPaper_ref(
                                paper_ref=ref_1,
                                detail_no=detail_no,
                                session_no=sess
                                )
                        db.session.add(ref_db)
                        db.session.commit()
           
            
    
                for i in range(len(tmp_list)):
                    for j in range(len(tmp_list)):
                        if(tmp_list[i]== 999 and tmp_list[j]==999):
                            duplicate = False
                        elif(i!=j and tmp_list[i]==tmp_list[j]):
                            duplicate = True
                           
                
                if(duplicate):
                    return redirect(url_for('duplicate_firer_error'))
                else:
                    
                    
                    temp_shooting=db.session.query(TShooting).scalar()
                    if(temp_shooting is None):
                        detail_shots =Session_Detail(
                            date=datetime.now(),
                            datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                            session_id=sess,
                            detail_no=detail_no,
                            target_1_id=r_id,
                            target_2_id=r1_id,
                            target_3_id=r2_id,
                            target_4_id=r3_id,
                            target_5_id=r4_id,
                            target_6_id=r5_id,
                            target_7_id=r6_id,
                            target_8_id=r7_id,
                            paper_ref=ref_1,
                            set_no=set_no,
                            save_flag=0
                            )
                        db.session.add(detail_shots)
                        db.session.commit()
                        Tdetail_shots =TShooting(
                                        date=datetime.now(),
                                        datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                        session_id=sess,
                                        detail_no=detail_no,
                                        target_1_id=r_id,
                                        target_2_id=r1_id,
                                        target_3_id=r2_id,
                                        target_4_id=r3_id,
                                        target_5_id=r4_id,
                                        target_6_id=r5_id,
                                        target_7_id=r6_id,
                                        target_8_id=r7_id,
                                        paper_ref=ref_1,
                                        set_no=set_no,
                                        save_flag=0
                                        )
                        db.session.add(Tdetail_shots)
                        db.session.commit()
                
                    else:
                        db.session.query(TShooting).filter(TShooting.id != 999).delete()
                        db.session.commit()
                        
                        Tdetail_shots =TShooting(
                                date=datetime.now(),
                                datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                session_id=sess,
                                detail_no=detail_no,
                                target_1_id=r_id,
                                target_2_id=r1_id,
                                target_3_id=r2_id,
                                target_4_id=r3_id,
                                target_5_id=r4_id,
                                target_6_id=r5_id,
                                target_7_id=r6_id,
                                target_8_id=r7_id,
                                paper_ref=ref_1,
                                set_no=set_no,
                                save_flag=0
                                )
                        db.session.add(Tdetail_shots)
                        db.session.commit()
                        
                        detail_shots =Session_Detail(
                            date=datetime.now(),
                            datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                            session_id=sess,
                            detail_no=detail_no,
                            target_1_id=r_id,
                            target_2_id=r1_id,
                            target_3_id=r2_id,
                            target_4_id=r3_id,
                            target_5_id=r4_id,
                            target_6_id=r5_id,
                            target_7_id=r6_id,
                            target_8_id=r7_id,
                            paper_ref=ref_1,
                            set_no=set_no,
                            save_flag=0
                            )
                        db.session.add(detail_shots)
                        db.session.commit()
        except Exception as e:
            return redirect(url_for('error_102'))                
        return redirect(url_for('detail_view'))
    
    @app.route('/FRAS_2/', methods=['GET', 'POST'])
    def load_2 ():
        ref_1=None
        try:
            if request.method == 'POST':
                print("This is inside Post")
                
                detail_no = request.form['game_id_1']  
                print("this is detail_no")
                print(detail_no)
                tmp_list = []
                duplicate = False
                gr=session.get('group',None)
                data=TGroup.query.filter(TGroup.group_no==gr).scalar()
                da_1=data.target_1_no
                da_2=data.target_2_no
                da_3=data.target_3_no
                da_4=data.target_4_no
                da_5=data.target_5_no
                da_6=data.target_6_no
                da_7=data.target_7_no
                da_8=data.target_8_no
                if(da_1==""):
                    r_id=999
                else:
                    r=Shooter.query.filter(Shooter.service_id==da_1).scalar()
                    r_id=r.id
                if(da_2==""):
                    r1_id=999
                else:
                    r1=Shooter.query.filter(Shooter.service_id==da_2).scalar()
                    r1_id=r1.id
                if(da_3==""):
                    r2_id=999
                else:
                    
                    r2=Shooter.query.filter(Shooter.service_id==da_3).scalar()
                    r2_id=r2.id
                
                
                if(da_4==""):
                    r3_id=999
                else:
                    r3=Shooter.query.filter(Shooter.service_id==da_4).scalar()
                    r3_id=r3.id
                    
               
                if(da_5==""):
                    r4_id=999
                else:
                    r4=Shooter.query.filter(Shooter.service_id==da_5).scalar()
                    r4_id=r4.id
                
                
                
                if(da_6==""):
                    r5_id=999
                else:
                    r5=Shooter.query.filter(Shooter.service_id==da_6).scalar()
                    r5_id=r5.id
               
                
                if(da_7==""):
                    r6_id=999
                else:
                    r6=Shooter.query.filter(Shooter.service_id==da_7).scalar()
                    r6_id=r6.id
                
                
                if(da_8==""):
                    r7_id=999
                else:
                    r7=Shooter.query.filter(Shooter.service_id==da_8).scalar()
                    r7_id=r7.id
                ref=request.form['business']
                set_no = request.form.get('comp_select_6')
                shots = request.form['tag_8']
                sess=request.form.get('comp_select')
                
                tmp_list.append(r_id)
                tmp_list.append(r1_id)
                tmp_list.append(r2_id)
                tmp_list.append(r3_id)
                tmp_list.append(r4_id)
                tmp_list.append(r5_id)
                tmp_list.append(r6_id)
                tmp_list.append(r7_id)
                
                print(tmp_list)
                
                if ref == None or ref =="":
                    ref_obj=TPaper_ref.query.scalar()
                    ref_1=ref_obj.paper_ref
                    
                
                else :
                    ref_1=ref
                    check=TPaper_ref.query.scalar()
                    
                    cses=check.session_no
                    det=check.detail_no
                    
                    
                    if(int(set_no)>5):
                        return redirect(url_for('paper_duplicate_error'))
                    else:
                        db.session.query(TPaper_ref).delete()
                        db.session.commit()
                        
                        ref_db = TPaper_ref(
                                paper_ref=ref_1,
                                detail_no=detail_no,
                                session_no=sess
                                )
                        db.session.add(ref_db)
                        db.session.commit()
           
            
    
                for i in range(len(tmp_list)):
                    for j in range(len(tmp_list)):
                        if(tmp_list[i]== 999 and tmp_list[j]==999):
                            duplicate = False
                        elif(i!=j and tmp_list[i]==tmp_list[j]):
                            duplicate = True
                           
                
                if(duplicate):
                    return redirect(url_for('duplicate_firer_error'))
                else:
                    temp_shooting=db.session.query(TShooting).scalar()
                    if(temp_shooting is None):
                         detail_shots =Session_Detail(
                            date=datetime.now(),
                            datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                            session_id=sess,
                            detail_no=detail_no,
                            target_1_id=r_id,
                            target_2_id=r1_id,
                            target_3_id=r2_id,
                            target_4_id=r3_id,
                            target_5_id=r4_id,
                            target_6_id=r5_id,
                            target_7_id=r6_id,
                            target_8_id=r7_id,
                            paper_ref=ref_1,
                            set_no=set_no,
                            save_flag=0
                            
                            )
                         db.session.add(detail_shots)
                         db.session.commit()
                         
                         Tdetail_shots =TShooting(
                                        date=datetime.now(),
                                        datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                        session_id=sess,
                                        detail_no=detail_no,
                                        target_1_id=r_id,
                                        target_2_id=r1_id,
                                        target_3_id=r2_id,
                                        target_4_id=r3_id,
                                        target_5_id=r4_id,
                                        target_6_id=r5_id,
                                        target_7_id=r6_id,
                                        target_8_id=r7_id,
                                        paper_ref=ref_1,
                                        set_no=set_no,
                                        save_flag=0
                                        )
                         db.session.add(Tdetail_shots)
                         db.session.commit()
                         
                    else:
                         db.session.query(TShooting).filter(TShooting.id != 999).delete()
                         db.session.commit()
                         Tdetail_shots =TShooting(
                                date=datetime.now(),
                                datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                session_id=sess,
                                detail_no=detail_no,
                                target_1_id=r_id,
                                target_2_id=r1_id,
                                target_3_id=r2_id,
                                target_4_id=r3_id,
                                target_5_id=r4_id,
                                target_6_id=r5_id,
                                target_7_id=r6_id,
                                target_8_id=r7_id,
                                paper_ref=ref_1,
                                set_no=set_no,
                                save_flag=0
                                )
                         db.session.add(Tdetail_shots)
                         db.session.commit()
                         
                         detail_shots =Session_Detail(
                            date=datetime.now(),
                            datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                            session_id=sess,
                            detail_no=detail_no,
                            target_1_id=r_id,
                            target_2_id=r1_id,
                            target_3_id=r2_id,
                            target_4_id=r3_id,
                            target_5_id=r4_id,
                            target_6_id=r5_id,
                            target_7_id=r6_id,
                            target_8_id=r7_id,
                            paper_ref=ref_1,
                            set_no=set_no,
                            save_flag=0
                            )
                         db.session.add(detail_shots)
                         db.session.commit()
        except Exception as e:
            print(e)
            return redirect(url_for('error'))
                
        return redirect(url_for('image_process'))
    
    @app.route('/detail_view/', methods=['GET', 'POST'])
    def detail_view():
        detail = Session_Detail.query.all()
        for details in detail:
            details.target_1=Shooter.query.filter(Shooter.id==details.target_1_id).scalar()
            details.target_2=Shooter.query.filter(Shooter.id==details.target_2_id).scalar()
            details.target_3=Shooter.query.filter(Shooter.id==details.target_3_id).scalar()
            details.target_4=Shooter.query.filter(Shooter.id==details.target_4_id).scalar()
            details.target_5=Shooter.query.filter(Shooter.id==details.target_5_id).scalar()
            details.target_6=Shooter.query.filter(Shooter.id==details.target_6_id).scalar()
            details.target_7=Shooter.query.filter(Shooter.id==details.target_7_id).scalar()
            details.target_8=Shooter.query.filter(Shooter.id==details.target_8_id).scalar()
        return render_template('pages/detail_view.html',detail=detail)
    
    @app.route('/detail_view/detail/<id>', methods=['GET', 'POST'])
    def view_detail(id):
        detail=Session_Detail.query.filter(Session_Detail.id == id)
        for details in detail:
            details.target_1=Shooter.query.filter(Shooter.id==details.target_1_id).scalar()
            details.target_2=Shooter.query.filter(Shooter.id==details.target_2_id).scalar()
            details.target_3=Shooter.query.filter(Shooter.id==details.target_3_id).scalar()
            details.target_4=Shooter.query.filter(Shooter.id==details.target_4_id).scalar()
            details.target_5=Shooter.query.filter(Shooter.id==details.target_5_id).scalar()
            details.target_6=Shooter.query.filter(Shooter.id==details.target_6_id).scalar()
            details.target_7=Shooter.query.filter(Shooter.id==details.target_7_id).scalar()
            details.target_8=Shooter.query.filter(Shooter.id==details.target_8_id).scalar()
        return render_template('pages/detail_view_id.html',data=detail)
    
    @app.route('/detail_view/edit/<id>', methods=['GET', 'POST'])
    def view_detail_edit(id):
        try:
            detail=Session_Detail.query.filter(Session_Detail.id == id).first()
            form=DetailEditForm(obj=detail)
            if form.validate_on_submit():
                tmp_list = []
                target_1=Shooter.query.filter(Shooter.service_id == form.target_1_service.data).scalar()
                tmp_list.append(target_1.id)
                target_2=Shooter.query.filter(Shooter.service_id == form.target_2_service.data).scalar()
                tmp_list.append(target_2.id)
                target_3=Shooter.query.filter(Shooter.service_id == form.target_3_service.data).scalar()
                tmp_list.append(target_3.id)
                target_4=Shooter.query.filter(Shooter.service_id == form.target_4_service.data).scalar()
                tmp_list.append(target_4.id)
                target_5=Shooter.query.filter(Shooter.service_id == form.target_5_service.data).scalar()
                tmp_list.append(target_5.id)
                target_6=Shooter.query.filter(Shooter.service_id == form.target_6_service.data).scalar()
                tmp_list.append(target_6.id)
                target_7=Shooter.query.filter(Shooter.service_id == form.target_7_service.data).scalar()
                tmp_list.append(target_7.id)
                target_8=Shooter.query.filter(Shooter.service_id == form.target_8_service.data).scalar()
                tmp_list.append(target_8.id)
                duplicate = False
                
                for i in range(len(tmp_list)):
                    for j in range(len(tmp_list)):
                        if(tmp_list[i]== 999  and tmp_list[j]==999):
                            duplicate = False
                        elif(i!=j and tmp_list[i]==tmp_list[j]):
                            duplicate = True
                            
                if(duplicate):
                    return redirect(url_for('duplicate_firer_error'))
                
                else:
                    detail.date=form.date.data
                    detail.session_id=form.session_id.data
                    detail.detail_no=form.detail_no.data
                    detail.paper_ref=form.paper_ref.data
                    detail.set_no=form.set_no.data
                    target_1_obj=Shooter.query.filter(Shooter.service_id == form.target_1_service.data).scalar()
                    detail.target_1_id=target_1_obj.id
                    target_2_obj=Shooter.query.filter(Shooter.service_id == form.target_2_service.data).scalar()
                    detail.target_2_id=target_2_obj.id
                    target_3_obj=Shooter.query.filter(Shooter.service_id == form.target_3_service.data).scalar()
                    detail.target_3_id=target_3_obj.id
                    target_4_obj=Shooter.query.filter(Shooter.service_id == form.target_4_service.data).scalar()
                    detail.target_4_id=target_4_obj.id
                    target_5_obj=Shooter.query.filter(Shooter.service_id == form.target_5_service.data).scalar()
                    detail.target_5_id=target_5_obj.id
                    target_6_obj=Shooter.query.filter(Shooter.service_id == form.target_6_service.data).scalar()
                    detail.target_6_id=target_6_obj.id
                    target_7_obj=Shooter.query.filter(Shooter.service_id == form.target_7_service.data).scalar()
                    detail.target_7_id=target_7_obj.id
                    target_8_obj=Shooter.query.filter(Shooter.service_id == form.target_8_service.data).scalar()
                    detail.target_8_id=target_8_obj.id
    
                    db.session.commit()
                    
                    db.session.query(TPaper_ref).delete()
                    db.session.commit()
                    ref_edit = TPaper_ref(
                                    paper_ref=form.paper_ref.data,
                                    detail_no=form.detail_no.data,
                                    session_no=form.session_id.data
                                    )
                    db.session.add(ref_edit)
                    db.session.commit()
                    
                    
                    
                    target_1_obj=Shooter.query.filter(Shooter.service_id == form.target_1_service.data).scalar()
                    target_2_obj=Shooter.query.filter(Shooter.service_id == form.target_2_service.data).scalar()
                    target_3_obj=Shooter.query.filter(Shooter.service_id == form.target_3_service.data).scalar()
                    target_4_obj=Shooter.query.filter(Shooter.service_id == form.target_4_service.data).scalar()
                    target_5_obj=Shooter.query.filter(Shooter.service_id == form.target_5_service.data).scalar()
                    target_6_obj=Shooter.query.filter(Shooter.service_id == form.target_6_service.data).scalar()
                    target_7_obj=Shooter.query.filter(Shooter.service_id == form.target_7_service.data).scalar()
                    target_8_obj=Shooter.query.filter(Shooter.service_id == form.target_8_service.data).scalar()
                    temp_shooting=db.session.query(TShooting).scalar()
    
                    if(temp_shooting.save_flag==1):
                        return redirect(url_for('data_save'))
                    else:
                        db.session.query(TShooting).filter(TShooting.id != 999).delete()
                        db.session.commit()
                        Tdetail_edit =TShooting(
                                    date=form.date.data,
                                    datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                    session_id=form.session_id.data,
                                    detail_no=form.detail_no.data,
                                    target_1_id=target_1_obj.id,
                                    target_2_id=target_2_obj.id,
                                    target_3_id=target_3_obj.id,
                                    target_4_id=target_4_obj.id,
                                    target_5_id=target_5_obj.id,
                                    target_6_id=target_6_obj.id,
                                    target_7_id=target_7_obj.id,
                                    target_8_id=target_8_obj.id,	
                                    paper_ref=form.paper_ref.data,
                                    set_no=form.set_no.data,
                                    save_flag=0
                                    )
                        db.session.add(Tdetail_edit)
                        db.session.commit()
                        return redirect(url_for('detail_view'))
                
            form.date.data=detail.date
            form.session_id.data=detail.session_id
            form.detail_no.data=detail.detail_no
            form.paper_ref.data=detail.paper_ref
            form.set_no.data=detail.set_no
            
            name_1=	Shooter.query.filter(Shooter.id==detail.target_1_id).scalar()	
            form.target_1_service.data=data=name_1.service_id
            
            
            name_2=	Shooter.query.filter(Shooter.id==detail.target_2_id).scalar()	
            form.target_2_service.data=data=name_2.service_id
            
            name_3=	Shooter.query.filter(Shooter.id==detail.target_3_id).scalar()	
            form.target_3_service.data=data=name_3.service_id
            
            name_4=	Shooter.query.filter(Shooter.id==detail.target_4_id).scalar()	
            form.target_4_service.data=data=name_4.service_id
            
            name_5=Shooter.query.filter(Shooter.id==detail.target_5_id).scalar()	
            form.target_5_service.data=data=name_5.service_id
            
            
            name_6=Shooter.query.filter(Shooter.id==detail.target_6_id).scalar()	
            form.target_6_service.data=data=name_6.service_id
            
            name_7=Shooter.query.filter(Shooter.id==detail.target_7_id).scalar()	
            form.target_7_service.data=data=name_7.service_id
            
            name_8=Shooter.query.filter(Shooter.id==detail.target_8_id).scalar()	
            form.target_8_service.data=data=name_8.service_id
        except Exception as e:
            return render_template('errors/detail_view.html')
        return render_template('pages/detail_view_edit.html' , detail=detail,form=form)
    
    @app.route('/data_save', methods=['GET', 'POST'])
    def data_save():
        return render_template('pages/data_save.html')
    
    
    
    @app.route('/target_registration/', methods=['GET', 'POST']) 
    def target_registration():
        result=None
        if request.method=="POST":
            data1 = request.get_json()
            print(data1)
            cant=data1['cant']
            div=data1['div']
            rank=data1['rank']
            gen=data1['gender']
            dt=data1['date']
            name=data1['name']
            army_no=data1['service']
            unit=data1['unit']
            brigade=data1['brig']
            gender_id=db.session.query(Gender.id).filter(Gender.name==gen).scalar()
            rank_id=db.session.query(Rank.id).filter(Rank.name==rank).scalar()
            cant_id=db.session.query(Cantonment.id).filter(Cantonment.cantonment==cant ,Cantonment.division==div).scalar()
            print("cant_id")
            print(cant_id)
            shooter = Shooter(
                        name=name,
                        service_id = army_no,
                        registration_date = dt,
                        gender_id=gender_id,
                        cantonment_id = cant_id,
                        rank_id =rank_id,
                        unit=unit,
                        brigade=brigade
                        )
            db.session.add(shooter)
            db.session.commit()
            
            result="Data Saved Sucessfully"

        return jsonify(result=result)

    @app.route('/shooter_registration/', methods=['GET', 'POST']) 
    def registration():
        try:
            cantonment=Cantonment.query.distinct(Cantonment.cantonment)
            gender =Gender.query.all()
            rank = Rank.query.all()
            ran = request.form.get('comp_select4') 
            cant = request.form.get('comp_select')
            gen = request.form.get('comp_select5')
            brig = request.form.get('comp_select1')
            form = RegistrationForm(request.form)
            if(ran is None):
                pass
            else:
                ran_object=Rank.query.filter(Rank.name==ran).scalar()
                rank_id =  ran_object.id
                cant_object = Cantonment.query.filter(Cantonment.cantonment==cant,Cantonment.division==brig).scalar()
                cant_id = cant_object.id
                gen_obj=Gender.query.filter(Gender.name==gen).scalar()
                gender_id = gen_obj.id
                
                
                
                if form.validate_on_submit():
                    shooter = Shooter(
                                 name=form.name.data,
                                 service_id = form.service_id.data,
                                 registration_date = form.dt.data.strftime('%Y-%m-%d'),
                                 gender_id=gender_id,
                                 cantonment_id = cant_id,
                                 rank_id =rank_id,
                                 unit=form.unit.data,
                                 brigade=form.brig.data
                                 )
                    db.session.add(shooter)
                    db.session.commit()
                    new_form = RegistrationForm(request.form)
                    
                    return redirect(url_for('firer_details'))
        
        except Exception as e:
            return redirect(url_for('error_4'))
        
        return render_template('forms/registration.html',
                               cantonment =  cantonment ,
                               form=form ,
                               rank = rank,
                               gender=gender)
    
    @app.route('/get_brigade/')
    def get_brigade():
        cant = request.args.get('customer')
        da = da = Cantonment.query.filter(Cantonment.cantonment==cant).distinct(Cantonment.division)
        data = [{"name": x.division} for x in da]
        return jsonify(data)
    
   
    
    @app.route('/firer_details/', methods=['GET', 'POST'])
    def firer_details():
        firer = Shooter.query.all()
        for firers in firer:
            firers.cantonment_name= Cantonment.query.filter(Cantonment.id==firers.cantonment_id).scalar()
            firers.division = Cantonment.query.filter(Cantonment.id==firers.cantonment_id).scalar()
            firers.rank = Rank.query.filter(Rank.id==firers.rank_id).scalar()
            firers.gender_name = Gender.query.filter(Gender.id==firers.gender_id).scalar()
        return render_template('pages/firer_details.html' , firer = firer)
    
    @app.route('/bulk_registration_group')
    def bulk_registration_group():
        form=BulkRegistrationForm(request.form)
        return render_template('pages/bulk_registration_group.html',form=form)
    
    
    
    @app.route('/bulk_registration')
    def bulk_registration():
        cantonment=db.session.query(Cantonment).distinct(Cantonment.cantonment)
        form=RegistrationForm(request.form)
         
        return render_template('pages/bulk_registration.html',cantonment=cantonment,form=form)
    

    @app.route('/upload', methods=['POST'])
    def upload():
        try:
            
            f = request.files['data_file']
            cant = request.form.get('comp_select')
            div = request.form.get('comp_select1')
    
            form=RegistrationForm(request.form) 
            unit = request.form['game_id_1']  
            brig = request.form['game_id_2']  
            
            cant_id = db.session.query(Cantonment.id).filter(Cantonment.cantonment==cant,
                                                             Cantonment.division==div
                                         
                                                    ).scalar()
            
            if form.is_submitted():
                stream = StringIO(f.stream.read().decode("UTF8"))
                csv_input = csv.reader(stream)  
                lis =list(csv_input)
                
                
                for i in range(len(lis)):
                    if (i==0):
                        
                        pass
                    else:
                        shooters = Shooter(
                                name  = lis[i][0],
                                service_id=lis[i][3],
                                registration_date=datetime.now(),
                                gender_id=db.session.query(Gender.id).filter(Gender.name==lis[i][2]).scalar(),
                                cantonment_id = cant_id,
                                rank_id = db.session.query(Rank.id).filter(Rank.name==lis[i][1]).scalar(),
                                unit=unit,
                                brigade=brig
                                
                                )
                        
                        
                        db.session.add(shooters)
                        db.session.commit()
                        
        except Exception as e:
            return redirect(url_for('error_3'))
        
        return redirect(url_for('firer_details'))         
        
    
    @app.route('/uploadgroup', methods=['POST'])
    def uploadgroup():
        try:
            
            f = request.files['data_file']
            form=BulkRegistrationForm(request.form)
            
            if form.is_submitted():
                curdate_p=(date.today())- timedelta(1)
    
                if(db.session.query(db.exists().where(TGroup.date <= curdate_p)).scalar()):
                    db.session.query(TGroup).delete()
                    db.session.commit()
                    stream = StringIO(f.stream.read().decode("UTF8"))
                    csv_input = csv.reader(stream)  
                    lis =list(csv_input)
                    for i in range(len(lis)):
                        
                        if (i==0):
                            
                            
                            
                            pass
                        else:
                            group = TGroup(
                                    date=datetime.now(),
                                    group_no=lis[i][0],
                                    target_1_no=lis[i][1],
                                    target_2_no=lis[i][2],
                                    target_3_no=lis[i][3],
                                    target_4_no=lis[i][4],
                                    target_5_no=lis[i][5],
                                    target_6_no=lis[i][6],
                                    target_7_no=lis[i][7],
                                    target_8_no=lis[i][8]
                                    
                                    
                                    
                                    )
                            db.session.add(group)
                            db.session.commit()
        
                else:
                    
                    stream = StringIO(f.stream.read().decode("UTF8"))
                    csv_input = csv.reader(stream)  
                    lis =list(csv_input)  
                    for i in range(len(lis)):
                        if (i==0):
                            
                            
                            pass
                        else:
                            group = TGroup(
                                    date=datetime.now(),
                                    group_no=lis[i][0],
                                    target_1_no=lis[i][1],
                                    target_2_no=lis[i][2],
                                    target_3_no=lis[i][3],
                                    target_4_no=lis[i][4],
                                    target_5_no=lis[i][5],
                                    target_6_no=lis[i][6],
                                    target_7_no=lis[i][7],
                                    target_8_no=lis[i][8]
                                    
                                    
                                    
                                    )
                            db.session.add(group)
                            db.session.commit()   
        
        except Exception as e:
            return redirect(url_for('error_duplicate'))
        
        return redirect(url_for('group_view')) 
    
    
    @app.route('/new_group')
    def new_group():
        firer = [row.service_id for row in Shooter.query.all()]
        return render_template('pages/new_group.html',firer_1=firer)
    
    @app.route('/individual_group/', methods=['GET', 'POST'])
    def individual_group():
        try:
            curdate_p=(date.today())- timedelta(1)
            #check=mysession.query(TGroup).filter(date==curdate_p).all()
            if request.method=="POST":
                
                grp = request.form['game_id_1']
                
                tmp_list = []
                duplicate = False
                r=request.form['tag']
                if (r== ""):
                    r_id = 999
                else:
                    r_object=Shooter.query.filter(Shooter.service_id==r).scalar()
                    r_id=r_object.id
                r1=request.form['tag_1']
                if(r1== ""):
                    r1_id=999
                else:
                    r1_object=Shooter.query.filter(Shooter.service_id==r1).scalar()
                    r1_id=r1_object.id
                r2=request.form['tag_2'] 
                if (r2==""):
                    r2_id=999
                else:
                    r2_object=Shooter.query.filter(Shooter.service_id==r2).scalar()
                    r2_id=r2_object.id
    
                    
                r3=request.form['tag_3']
                if(r3==""):
                    r3_id=999
                else:
                    r3_object=Shooter.query.filter(Shooter.service_id==r3).scalar()
                    r3_id=r3_object.id
                    
                r4=request.form['tag_4']
                if(r4==""):
                    r4_id=999
                else:
                    r4_object=Shooter.query.filter(Shooter.service_id==r4).scalar()
                    r4_id=r4_object.id
    
                r5=request.form['tag_5']
                
                if(r5==""):
                    r5_id=999
                else:
                    r5_object=Shooter.query.filter(Shooter.service_id==r5).scalar()
                    r5_id=r5_object.id
    
            
                r6=request.form['tag_6']
                
                if(r6==""):
                    r6_id=999
                else:
                    r6_object=Shooter.query.filter(Shooter.service_id==r6).scalar()
                    r6_id=r6_object.id
               
                r7=request.form['tag_7']
                
                if(r7== ""):
                    r7_id=999
                else:
                    r7_object=Shooter.query.filter(Shooter.service_id==r7).scalar()
                    r7_id=r7_object.id
                
                tmp_list.append(r_id)
                tmp_list.append(r1_id)
                tmp_list.append(r2_id)
                tmp_list.append(r3_id)
                tmp_list.append(r4_id)
                tmp_list.append(r5_id)
                tmp_list.append(r6_id)
                tmp_list.append(r7_id)
                
                
                for i in range(len(tmp_list)):
                    for j in range(len(tmp_list)):
                        if(tmp_list[i]== 999 and tmp_list[j]==999):
                            duplicate = False
                        elif(i!=j and tmp_list[i]==tmp_list[j]):
                            duplicate = True
                            
                            
             
                if(db.session.query(db.exists().where(TGroup.date == curdate_p)).scalar()):
                    db.session.query(TGroup).delete()
                    db.session.commit()
                    if(duplicate):
                        return redirect(url_for('duplicate_firer_error'))
                    else:
                    
                        gr=TGroup(
                                date=datetime.now(),
                                group_no=grp,
                                target_1_no=r,
                                target_2_no=r1,
                                target_3_no=r2,
                                target_4_no=r3,
                                target_5_no=r4,
                                target_6_no=r5,
                                target_7_no=r6,
                                target_8_no=r7
                                )
                        db.session.add(gr)
                        db.session.commit()
                else:
                    if(duplicate):
                        return redirect(url_for('duplicate_firer_error'))
                    else:
                    
                        gr=TGroup(
                                date=datetime.now(),
                                group_no=grp,
                                target_1_no=r,
                                target_2_no=r1,
                                target_3_no=r2,
                                target_4_no=r3,
                                target_5_no=r4,
                                target_6_no=r5,
                                target_7_no=r6,
                                target_8_no=r7
                                )
                        db.session.add(gr)
                        db.session.commit()
        except Exception as e:
            return render_template('errors/group_view_error.html')
        return redirect(url_for('group_view'))
    
    @app.route('/group_view/', methods=['GET', 'POST'])
    def group_view():
        detail = TGroup.query.all()
        return render_template('pages/group_detail_view.html',detail=detail)
    
    @app.route('/group_view/detail/<id>', methods=['GET', 'POST'])
    def group_detail_view(id):
        view = TGroup.query.filter(TGroup.group_no == id)
        return render_template('pages/group_detail_view_id.html' , data = view)
    
    
    @app.route('/group_details/edit/<id>', methods=['GET', 'POST'])  
    def group_detail_edit(id):
         firer = TGroup.query.filter(TGroup.group_no == id).first()
         form=GroupEditForm(obj=firer)
         
         if form.validate_on_submit():
             
             firer.date=form.date.data
             firer.target_1_no=form.target_1_army.data
             firer.target_2_no=form.target_2_army.data
             firer.target_3_no=form.target_3_army.data
             firer.target_4_no=form.target_4_army.data
             firer.target_5_no=form.target_5_army.data
             firer.target_6_no=form.target_6_army.data
             firer.target_7_no=form.target_7_army.data
             firer.target_8_no=form.target_8_army.data
             firer.group_no=form.group_no.data
             db.session.commit()
             return redirect(url_for('group_view'))
             
         form.group_no.data=firer.group_no    
         form.target_1_army.data=firer.target_1_no
         form.target_2_army.data=firer.target_2_no
         form.target_3_army.data=firer.target_3_no
         form.target_4_army.data=firer.target_4_no
         form.target_5_army.data=firer.target_5_no
         form.target_6_army.data=firer.target_6_no
         form.target_7_army.data=firer.target_7_no
         form.target_8_army.data=firer.target_8_no
         
         return render_template('pages/group_edit.html' , firer = firer , form=form)
    
    @app.route('/firer_details/detail/<id>', methods=['GET', 'POST'])
    def firer_detail_view(id):
        firer = Shooter.query.filter(Shooter.service_id == id)
        for firers in firer:
            firers.cantonment_name= Cantonment.query.filter(Cantonment.id==firers.cantonment_id).scalar()
            firers.division = Cantonment.query.filter(Cantonment.id==firers.cantonment_id).scalar()
            firers.rank = Rank.query.filter(Rank.id==firers.rank_id).scalar()
            firers.gender_name = Gender.query.filter(Gender.id==firers.gender_id).scalar()
        return render_template('pages/firer_detail_view.html' , data = firer)
     
    @app.route('/firer_details/edit/<id>', methods=['GET', 'POST'])  
    def firer_detail_edit(id):
         firer = Shooter.query.filter(Shooter.service_id == id).first()
         form=RegistrationEditForm(obj=firer)
         try:
             if form.validate_on_submit():
                 firer.name = form.name.data
                 firer.service_id=form.service_id.data
                 firer.registration_date=form.date.data
                 gender_obj=Gender.query.filter(Gender.name==form.gender.data).scalar()
                 firer.gender_id=gender_obj.id
                 cantonment_obj=Cantonment.query.filter(Cantonment.cantonment==form.cantonment.data ,Cantonment.division==form.div.data).scalar()
                 firer.cantonment_id=cantonment_obj.id
                 rank_obj=Range.query.filter(Rank.name==form.rank.data).distinct(Rank.id).scalar()
                 firer.rank_id=rank_obj.id
                 firer.unit=form.unit.data
                 firer.brigade=form.brigade.data
                 db.session.commit()
                 return redirect(url_for('firer_details'))
             
             form.name.data=firer.name
             form.service_id.data=firer.service_id
             form.date.data=firer.registration_date
             gender_name=Gender.query.filter(Gender.id==firer.gender_id).scalar()
             form.gender.data=gender_name.name
             cantonment_name=Cantonment.query.filter(Cantonment.id==firer.cantonment_id).scalar()
             form.cantonment.data=cantonment_name.cantonment
             form.div.data=cantonment_name.division 
             unit_data=Shooter.query.filter(Shooter.service_id==firer.service_id).scalar()
             form.unit.data=unit_data.unit
             form.brigade.data=unit_data.brigade
             rank_name=Rank.query.filter(Rank.id==firer.rank_id).distinct(Rank.name).scalar()
             form.rank.data=rank_name.name
         except Exception as e:
             return redirect(url_for('error_7'))
         return render_template('pages/firer_detail_edit.html' , firer = firer , form=form)
     
    @app.route('/live/')
    def live():
        T1_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_rank = mysession.query(Rank.name).filter(Rank.id==T1_r_id).scalar()
        
        T2_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_rank = mysession.query(Rank.name).filter(Rank.id==T2_r_id).scalar()
        
        
        
        T3_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_rank = mysession.query(Rank.name).filter(Rank.id==T3_r_id).scalar()
        
        T4_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_rank = mysession.query(Rank.name).filter(Rank.id==T4_r_id).scalar()
        
        T5_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_5_id).scalar()
        T5_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_5_id).scalar()
        T5_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_5_id).scalar()
        T5_rank = mysession.query(Rank.name).filter(Rank.id==T5_r_id).scalar()
        
        T6_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_6_id).scalar()
        T6_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_6_id).scalar()
        T6_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_6_id).scalar()
        T6_rank = mysession.query(Rank.name).filter(Rank.id==T6_r_id).scalar()
        
        T7_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_7_id).scalar()
        T7_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_7_id).scalar()
        T7_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_7_id).scalar()
        T7_rank = mysession.query(Rank.name).filter(Rank.id==T7_r_id).scalar()
        
        T8_name = mysession.query(Shooter.name).filter(Shooter.id==TShooting.target_8_id).scalar()
        T8_service = mysession.query(Shooter.service_id).filter(Shooter.id==TShooting.target_8_id).scalar()
        T8_r_id = mysession.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_8_id).scalar()
        T8_rank = mysession.query(Rank.name).filter(Rank.id==T8_r_id).scalar()
        
        return render_template('pages/live.html' ,
                               T1_name=T1_name,
                               T1_service=T1_service,
                               T2_name=T2_name,
                               T2_service=T2_service,
                               T3_name=T3_name,
                               T3_service=T3_service,
                               T4_name=T4_name,
                               T4_service=T4_service,
                               T5_name=T5_name,
                               T5_service=T5_service,
                               T6_name=T6_name,
                               T6_service=T6_service,
                               T7_name=T7_name,
                               T7_service=T7_service,
                               T8_name=T8_name,
                               T8_service=T8_service,
                               T1_rank=T1_rank,
                               T2_rank=T2_rank,
                               T3_rank=T3_rank,
                               T4_rank=T4_rank,
                               T5_rank=T5_rank,
                               T6_rank=T6_rank,
                               T7_rank=T7_rank,
                               T8_rank=T8_rank
                               
                               )
    
    @app.route('/cam_detail_2/', methods=['GET', 'POST'])
    def cam_detail_2():
        return render_template('pages/cam_detail_1.html')
    
    @app.route('/cam_detail_4/', methods=['GET', 'POST'])
    def cam_detail_4():
        return render_template('pages/cam_detail_2.html')
    
    @app.route('/cam_detail_1/', methods=['GET', 'POST'])
    def cam_detail_1():
        return render_template('pages/cam_detail_3.html')
    
    
    @app.route('/cam_detail_3/', methods=['GET', 'POST'])
    def cam_detail_3():
        return render_template('pages/cam_detail_4.html')
    
    @app.route('/cam_detail_6/', methods=['GET', 'POST'])
    def cam_detail_6():
        return render_template('pages/cam_detail_5.html')
    
    @app.route('/cam_detail_8/', methods=['GET', 'POST'])
    def cam_detail_8():
        return render_template('pages/cam_detail_6.html')
    
    @app.route('/cam_detail_7/', methods=['GET', 'POST'])
    def cam_detail_7():
        return render_template('pages/cam_detail_7.html')
    
    @app.route('/cam_detail_5/', methods=['GET', 'POST'])
    def cam_detail_5():
        return render_template('pages/cam_detail_8.html')
    
    @app.route('/session_setup/', methods=['GET', 'POST'])
    def session_setup():
        try:
            data = Shooter.query.all()
            rang= Range.query.all()
            firearms = Firearms.query.all()
            ammunation = Ammunation.query.all()
            rang_name = request.form.get('comp_select_4')
            fire_name = request.form.get('comp_select_5')
            ammu_name = request.form.get('comp_select_6')
            form=SessionForm()
            
            if(rang_name is None):
                range_id=999
                fire_id=999
                ammu_id=999
            else:
                range_id = db.session.query(Range.id).filter(Range.name==rang_name).scalar()
                fire_id = db.session.query(Firearms.id).filter(Firearms.name==fire_name).scalar()
                ammu_id = db.session.query(Ammunation.id).filter(Ammunation.name==ammu_name).scalar()
        
                
                if form.validate_on_submit():
                    shooting=Shooting_Session(
                                    date=form.date.data.strftime('%Y-%m-%d'),
                                    datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                                    shooting_range_id=range_id,
                                    firearms_id=fire_id,
                                    ammunation_id=ammu_id,
                                    target_distance = form.target_distance.data,
                                    weather_notes = form.weather_notes.data,
                                    comments = form.comments.data,
                                    session_no=form.session_no.data,
                                    occasion=form.occ.data
                                      )
                    
                    db.session.add(shooting)
                    db.session.commit()
                    return redirect(url_for('session_config'))
        except Exception as e:
            return redirect(url_for('error5_505.html'))
        return render_template('forms/shooting_form.html', form=form, data =data ,rang=rang , firearmns=firearms, ammunation = ammunation)
    
    @app.route('/configuration/', methods=['GET', 'POST'])
    def session_config():
        config = Shooting_Session.query.all()
        for con in config:  
            con.range_name =  Range.query.filter(Range.id==con.shooting_range_id).scalar()
            con.firerarms_name = Firearms.query.filter(Firearms.id==con.firearms_id).scalar()
            con.ammunation_name = Ammunation.query.filter(Ammunation.id==con.ammunation_id).scalar()
        return render_template('pages/shooting_configuration_detail.html',con=config)
    
    @app.route('/image_process/')
    def image_process():
        dt=time.strftime("%Y-%m-%d")
        detail_data=db.session.query(Session_Detail).filter(Session_Detail.date==dt,Session_Detail.save_flag==0).all()
        data =TShooting.query.scalar()
        if(data is None):
            T1_name ="NA"
            T1_service ="NA"
            T1_rank="NA"
            
            T2_name ="NA"
            T2_service ="NA"
            T2_rank="NA"
            
            T3_name ="NA"
            T3_service ="NA"
            T3_rank="NA"
            
            T4_name ="NA"
            T4_service ="NA"
            T4_rank="NA"
            
            T5_name ="NA"
            T5_service ="NA"
            T5_rank="NA"
            
            T6_name ="NA"
            T6_service ="NA"
            T6_rank="NA"
            
            T7_name ="NA"
            T7_service ="NA"
            T7_rank="NA"
            
            T8_name ="NA"
            T8_service ="NA"
            T8_rank="NA"
        elif(data.save_flag == 1 ):
            db.session.query(TShooting).delete()
            db.session.commit()
            T1_name ="NA"
            T1_service ="NA"
            T1_rank="NA"
            
            T2_name ="NA"
            T2_service ="NA"
            T2_rank="NA"
            
            T3_name ="NA"
            T3_service ="NA"
            T3_rank="NA"
            
            T4_name ="NA"
            T4_service ="NA"
            T4_rank="NA"
            
            T5_name ="NA"
            T5_service ="NA"
            T5_rank="NA"
            
            T6_name ="NA"
            T6_service ="NA"
            T6_rank="NA"
            
            T7_name ="NA"
            T7_service ="NA"
            T7_rank="NA"
            
            T8_name ="NA"
            T8_service ="NA"
            T8_rank="NA"
            
       
        else:
            T1=Shooter.query.filter(Shooter.id==TShooting.target_1_id).scalar()
            
            if(T1 is None):
                T1_name ="NA"
                T1_service ="NA"
                T1_rank="NA"
            else:
                T1_name = T1.name
                T1_service = T1.service_id
                T1_r_id = T1.rank_id
                T1_rank_id = Rank.query.filter(Rank.id==T1_r_id).scalar()
                T1_rank=T1_rank_id.name
                
            
            T2=Shooter.query.filter(Shooter.id==TShooting.target_2_id).scalar()
            if(T2 is None):
                T2_name ="NA"
                T2_service ="NA"
                T2_rank="NA"
                
            else:
                T2_name = T2.name
                T2_service = T2.service_id
                T2_r_id = T2.rank_id
                T2_rank_id = Rank.query.filter(Rank.id==T2_r_id).scalar()
                T2_rank=T2_rank_id.name
                
            T3=Shooter.query.filter(Shooter.id==TShooting.target_3_id,TShooting.target_3_id!=999).scalar()		
            if(T3 is None):
                T3_name ="NA"
                T3_service ="NA"
                T3_rank="NA"
            else:
                T3_name = T3.name
                T3_service = T3.service_id
                T3_r_id = T3.rank_id
                T3_rank_id = Rank.query.filter(Rank.id==T3_r_id).scalar()
                T3_rank=T3_rank_id.name
               
            T4=Shooter.query.filter(Shooter.id==TShooting.target_4_id,TShooting.target_4_id!=999).scalar()		
            if(T4 is None):
                T4_name ="NA"
                T4_service ="NA"
                T4_rank="NA"
            else:
                T4_name = T4.name
                T4_service = T4.service_id
                T4_r_id = T4.rank_id
                T4_rank_id = Rank.query.filter(Rank.id==T4_r_id).scalar()
                T4_rank=T4_rank_id.name
               
            T5=Shooter.query.filter(Shooter.id==TShooting.target_5_id).scalar()		
            
            if(T5 is None):
                T5_name ="NA"
                T5_service ="NA"
                T5_rank="NA"
            else:
                T5_name = T5.name
                T5_service = T5.service_id
                T5_r_id = T5.rank_id
                T5_rank_id = Rank.query.filter(Rank.id==T5_r_id).scalar()
                T5_rank=T5_rank_id.name
                
            T6=Shooter.query.filter(Shooter.id==TShooting.target_6_id).scalar()		
            if(T6 is None):
                T6_name ="NA"
                T6_service ="NA"
                T6_rank="NA"
            else:
                T6_name = T6.name
                T6_service = T6.service_id
                T6_r_id = T6.rank_id
                T6_rank_id = Rank.query.filter(Rank.id==T6_r_id).scalar()
                T6_rank=T6_rank_id.name
                
            T7=Shooter.query.filter(Shooter.id==TShooting.target_7_id).scalar()		
            
            if(T7 is None):
                T7_name ="NA"
                T7_service ="NA"
                T7_rank="NA"
            else:
                T7_name = T7.name
                T7_service = T7.service_id
                T7_r_id = T7.rank_id
                T7_rank_id = Rank.query.filter(Rank.id==T7_r_id).scalar()
                T7_rank=T7_rank_id.name
                
            T8=Shooter.query.filter(Shooter.id==TShooting.target_8_id).scalar()		
            
            if(T8 is None):
                T8_name ="NA"
                T8_service ="NA"
                T8_rank="NA"
            else:
                T8_name = T8.name
                T8_service = T8.service_id
                T8_r_id = T8.rank_id
                T8_rank_id = Rank.query.filter(Rank.id==T8_r_id).scalar()
                T8_rank=T8_rank_id.name
               
        return render_template('pages/image_process.html' ,
                               T1_name=T1_name,
                               detail_data=detail_data,
                               T1_service=T1_service,
                               T2_name=T2_name,
                               T2_service=T2_service,
                               T3_name=T3_name,
                               T3_service=T3_service,
                               T4_name=T4_name,
                               T4_service=T4_service,
                               T5_name=T5_name,
                               T5_service=T5_service,
                               T6_name=T6_name,
                               T6_service=T6_service,
                               T7_name=T7_name,
                               T7_service=T7_service,
                               T8_name=T8_name,
                               T8_service=T8_service,
                               T1_rank=T1_rank,
                               T2_rank=T2_rank,
                               T3_rank=T3_rank,
                               T4_rank=T4_rank,
                               T5_rank=T5_rank,
                               T6_rank=T6_rank,
                               T7_rank=T7_rank,
                               T8_rank=T8_rank
                               
                               )
    
    @app.route('/image_edit_1/', methods=['GET', 'POST'])
    def image_edit_1():
        return render_template('pages/image_edit_1.html')
    
    @app.route('/image_edit_2/', methods=['GET', 'POST'])
    def image_edit_2():
        return render_template('pages/image_edit_2.html')
    
    
    @app.route('/image_edit_3/', methods=['GET', 'POST'])
    def image_edit_3():
        return render_template('pages/image_edit_3.html')
    
    @app.route('/image_edit_4/', methods=['GET', 'POST'])
    def image_edit_4():
        return render_template('pages/image_edit_4.html')
    
    @app.route('/image_edit_5/', methods=['GET', 'POST'])
    def image_edit_5():
        return render_template('pages/image_edit_5.html')
    
    
    @app.route('/image_edit_6/', methods=['GET', 'POST'])
    def image_edit_6():
        return render_template('pages/image_edit_6.html')
    
    
    @app.route('/image_edit_7/', methods=['GET', 'POST'])
    def image_edit_7():
        return render_template('pages/image_edit_7.html')
    
    
    @app.route('/image_edit_8/', methods=['GET', 'POST'])
    def image_edit_8():
        return render_template('pages/image_edit_8.html')
    
    
    @app.route('/configuration/detail/<id>', methods=['GET', 'POST'])
    def session_config_detail(id):
        config = Shooting_Session.query.filter(Shooting_Session.id == id)
        for con in config:
            con.range_name =  Range.query.filter(Range.id==con.shooting_range_id).scalar()
            con.firerarms_name = Firearms.query.filter(Firearms.id==con.firearms_id).scalar()
            con.ammunation_name = Ammunation.query.filter(Ammunation.id==con.ammunation_id).scalar()
        return render_template('pages/shooting_configuration_detail_view.html',con=config)
    
    @app.route('/configuration/edit/<id>', methods=['GET', 'POST'])
    def shooting_config_edit(id):
        
        
        edit = Shooting_Session.query.get_or_404(id)
        form = SessionEditForm(obj=edit)
        if form.validate_on_submit():
            edit.session_no = form.session_no.data
            edit.date = form.date.data
            edit.occasion=form.occ.data
            edit.target_distance = form.target_distance.data
            ammunation_id=Ammunation.query.filter(Ammunation.name==form.ammunation_name.data).scalar()
            edit.ammunation_id=ammunation_id.id
            firearms_id=Firearms.query.filter(Firearms.name==form.firerarms_name.data).scalar()
            edit.firearms_id=firearms_id.id
            range_id=Range.query.filter(Range.name==form.range_name.data).scalar()
            edit.shooting_range_id=range_id.id
            edit.weather_notes=form.weather_notes.data
            edit.comments=form.comments.data
            db.session.commit()
            return redirect(url_for('session_config'))
        
        form.session_no.data=edit.session_no
        form.date.data=edit.date
        form.occ.data=edit.occasion
        ammunation_name=Ammunation.query.filter(Ammunation.id==edit.ammunation_id).scalar()
        form.ammunation_name.data=ammunation_name.name
        firerarms_name=Firearms.query.filter(Firearms.id==edit.firearms_id).scalar()
        form.firerarms_name.data=firerarms_name.name
        range_name=Range.query.filter(Range.id==edit.shooting_range_id).scalar()
        form.range_name.data=range_name.name
        form.weather_notes.data=edit.weather_notes
        form.comments.data=edit.comments
        return render_template('pages/shooting_configuration_edit.html',form=form,edit=edit)
    
    @app.route('/detail_dashboard/')
    def detail_dashboard():
        tshoot=db.session.query(TShooting).scalar()
        
        if(tshoot is None):
            
            T1_name = "NA"
            T1_service="NA"
            T1_rank ="NA"
            
            T2_name = "NA"
            T2_service="NA"
            T2_rank ="NA"
            
            T3_name = "NA"
            T3_service="NA"
            T3_rank ="NA"
            
            T4_name = "NA"
            T4_service="NA"
            T4_rank ="NA"
            
            T5_name = "NA"
            T5_service="NA"
            T5_rank ="NA"
            
            T6_name = "NA"
            T6_service="NA"
            T6_rank ="NA"
            
            T7_name = "NA"
            T7_service="NA"
            T7_rank ="NA"
            
            T8_name = "NA"
            T8_service="NA"
            T8_rank ="NA"
            
        else:
            T1=Shooter.query.filter(Shooter.id==TShooting.target_1_id).scalar()		
            T1_name = T1.name
            T1_service = T1.service_id
            T1_r_id = T1.rank_id
            T1_rank_id = Rank.query.filter(Rank.id==T1_r_id).scalar()
            T1_rank=T1_rank_id.name
            
            
            T2=Shooter.query.filter(Shooter.id==TShooting.target_2_id).scalar()		
            T2_name = T2.name
            T2_service = T2.service_id
            T2_r_id = T2.rank_id
            T2_rank_id = Rank.query.filter(Rank.id==T2_r_id).scalar()
            T2_rank=T2_rank_id.name
            
            T3=Shooter.query.filter(Shooter.id==TShooting.target_3_id).scalar()		
            T3_name = T3.name
            T3_service = T3.service_id
            T3_r_id = T3.rank_id
            T3_rank_id = Rank.query.filter(Rank.id==T3_r_id).scalar()
            T3_rank=T3_rank_id.name
           
            T4=Shooter.query.filter(Shooter.id==TShooting.target_4_id).scalar()		
            T4_name = T4.name
            T4_service = T4.service_id
            T4_r_id = T4.rank_id
            T4_rank_id = Rank.query.filter(Rank.id==T4_r_id).scalar()
            T4_rank=T4_rank_id.name
           
            T5=Shooter.query.filter(Shooter.id==TShooting.target_5_id).scalar()		
            T5_name = T5.name
            T5_service = T5.service_id
            T5_r_id = T5.rank_id
            T5_rank_id = Rank.query.filter(Rank.id==T5_r_id).scalar()
            T5_rank=T5_rank_id.name
            
            T6=Shooter.query.filter(Shooter.id==TShooting.target_6_id).scalar()		
            T6_name = T6.name
            T6_service = T6.service_id
            T6_r_id = T6.rank_id
            T6_rank_id = Rank.query.filter(Rank.id==T6_r_id).scalar()
            T6_rank=T6_rank_id.name
            
            T7=Shooter.query.filter(Shooter.id==TShooting.target_7_id).scalar()		
            T7_name = T7.name
            T7_service = T7.service_id
            T7_r_id = T7.rank_id
            T7_rank_id = Rank.query.filter(Rank.id==T7_r_id).scalar()
            T7_rank=T7_rank_id.name
            
            T8=Shooter.query.filter(Shooter.id==TShooting.target_8_id).scalar()		
            T8_name = T8.name
            T8_service = T8.service_id
            T8_r_id = T8.rank_id
            T8_rank_id = Rank.query.filter(Rank.id==T8_r_id).scalar()
            T8_rank=T8_rank_id.name
           
           
        return render_template('pages/detail_dashboard.html' ,
                               T1_name=T1_name,
                               T1_service=T1_service,
                               T2_name=T2_name,
                               T2_service=T2_service,
                               T3_name=T3_name,
                               T3_service=T3_service,
                               T4_name=T4_name,
                               T4_service=T4_service,
                               T5_name=T5_name,
                               T5_service=T5_service,
                               T6_name=T6_name,
                               T6_service=T6_service,
                               T7_name=T7_name,
                               T7_service=T7_service,
                               T8_name=T8_name,
                               T8_service=T8_service,
                               T1_rank=T1_rank,
                               T2_rank=T2_rank,
                               T3_rank=T3_rank,
                               T4_rank=T4_rank,
                               T5_rank=T5_rank,
                               T6_rank=T6_rank,
                               T7_rank=T7_rank,
                               T8_rank=T8_rank
                               
                               )
        
    @app.route('/adhoc_detail_1/', methods=['GET', 'POST'])    
    def adhoc_detail_1():
        name_1=None
        army=None
        rank=None
        cant=None
        set_1_name=None
        set_1_army=None
        set_2_name=None
        set_2_army=None
        set_3_name=None
        set_3_army=None
        set_4_name=None
        set_4_army=None
        res=[]
        ten=[]
        gp_len=[]
        if request.method == "POST":
            data1 = request.get_json()
            
            
            army=data1['usr']
        
            curdate=time.strftime("%Y-%m-%d")
         
            name_1=db.session.query(Shooter.name).filter(Shooter.service_id==army).scalar()
            target_1_id=db.session.query(Shooter.id).filter(Shooter.service_id==army).scalar()
            rank_id=db.session.query(Shooter.rank_id).filter(Shooter.service_id==army).scalar()
            cant_id=db.session.query(Shooter.cantonment_id).filter(Shooter.service_id==army).scalar()
            rank=db.session.query(Rank.name).filter(Rank.id==rank_id).scalar()
            cant=db.session.query(Cantonment.cantonment).filter(Cantonment.id==cant_id).scalar()
            
            
            tten=db.session.query(MPI.tendency_code).filter(MPI.firer_id==target_1_id).order_by(MPI.datetimestamp.desc()).limit(5).all()[::-1]
            tres = db.session.query(Grouping.result).filter(Grouping.firer_id==target_1_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]
            tgp = db.session.query(Grouping.grouping_length_f).filter(Grouping.firer_id==target_1_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]

            for ele in tres:
                for ele2 in ele:
                    res.append(ele2)
            for ele3 in tten:
                for ele4 in ele3:
                    ten.append(ele4)
                
            for ele5 in tgp:
                for ele6 in ele5:
                    gp_len.append(ele6)
            
            
            set_1_id = db.session.query(Firer_Details.firer_id).filter(Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==1                                                            
                                      ).distinct().scalar()
            
            
            set_1_name=db.session.query(Shooter.name).filter(Shooter.id==set_1_id).scalar()
            set_1_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_1_id).scalar()
            
            set_2_id = db.session.query(Firer_Details.firer_id).filter(Firer_Details.date==curdate, 
                                      Firer_Details.target_no==2, 
                                      Firer_Details.set_no==2                                                            
                                      ).distinct().scalar()
            
            
            set_2_name=db.session.query(Shooter.name).filter(Shooter.id==set_2_id).scalar()
            set_2_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_2_id).scalar()
            
            set_3_id = db.session.query(Firer_Details.firer_id).filter(Firer_Details.date==curdate, 
                                      Firer_Details.target_no==3, 
                                      Firer_Details.set_no==3                                                            
                                      ).distinct().scalar()
            
            
            set_3_name=db.session.query(Shooter.name).filter(Shooter.id==set_3_id).scalar()
            set_3_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_3_id).scalar()
            
            set_4_id = db.session.query(Firer_Details.firer_id).filter(Firer_Details.date==curdate, 
                                      Firer_Details.target_no==4, 
                                      Firer_Details.set_no==4                                                            
                                      ).distinct().scalar()
            
            
            set_4_name=db.session.query(Shooter.name).filter(Shooter.id==set_4_id).scalar()
            set_4_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_4_id).scalar()
            
            
            
        return jsonify(name_1=name_1,army=army,rank=rank,cant=cant,
                       set_1_name=set_1_name,
                       set_2_name=set_2_name,
                       set_3_name=set_3_name,
                       set_4_name=set_4_name,
                       set_1_army=set_1_army,
                       set_2_army=set_2_army,
                       set_3_army=set_3_army,
                       set_4_army=set_4_army,
                       gp_len=gp_len,
                       res=res,
                       ten=ten
                       
                       
                       )

        
    
    
    @app.route('/individual_score/target_1', methods=['GET', 'POST'])
    def individual_score_target_1():
        session.clear()
        data=TShooting.query.scalar()
        firing_set_arr=[]
        cantonment=Cantonment.query.distinct(Cantonment.cantonment)
        curdate=time.strftime("%Y-%m-%d")
        selection=Shooting_Session.query.filter(Shooting_Session.date>=curdate).order_by(Shooting_Session.datetimestamp.desc()).all()
        gender =Gender.query.all()
        rank_s = Rank.query.all()
        firing_set=db.session.query(Firer_Details.set_no).filter(Firer_Details.target_no==1).distinct().all()
        for ele in firing_set:
            for ele2 in ele:
                firing_set_arr.append(ele2)
        
       
        
        
        
        if(len(firing_set_arr)<1):
            pass
        else:
            i=len(firing_set_arr)-1
            
            if(firing_set_arr[i]==5):
                
                db.session.query(Firer_Details).filter(Firer_Details.target_no==1).delete()
                db.session.commit()
                
            else:
                
                pass
                
            
        dt=time.strftime("%Y-%m-%d")
        curdatetime=datetime.now()
        firer_1 = [row.service_id for row in Shooter.query.all()]
        detail_data=db.session.query(Session_Detail).filter(Session_Detail.date==dt,Session_Detail.save_flag==0).all()
        name = "NA"
        detail_no ="NA"
        rank ="NA"
        target_no = 1
        service_id ="NA"
        ten = []
        res = []
        selection=Shooting_Session.query.filter(Shooting_Session.date>=dt).order_by(Shooting_Session.datetimestamp.desc()).all()
        firearms = Firearms.query.all()
        rang= Range.query.all()
        ammunation = Ammunation.query.all()
        return render_template('pages/prediction_target_1.html',
                               curdatetime=curdatetime,
                               name = name,
                               firer_1=firer_1,
                               rank=rank,
                               detail_data=detail_data,
                               detail_no=detail_no,
                               target_no=target_no,
                               service_id=service_id,
                               firearms=firearms,
                               ammunation=ammunation,
                               data=selection,
                               rang=rang,
                               res=res,
                               date=dt,
                               ten=ten,
                               cantonment=cantonment,
                               gender=gender,
                               rank_s=rank_s)
     
    @app.route('/session_target_1/', methods=['GET', 'POST'])
    def session_target_1():
        
       
        if request.method == "POST":
             
             data1 = request.get_json()
             session=data1["session"]
             ran=data1["range"]
             arms=data1["arms"]
             distance=data1["dis"]
             occ=data1["occ"]
             ammu=data1["ammu"]
             weather=data1["weather"]
             comment=data1["comment"]       
             range_id=db.session.query(Range.id).filter(Range.name==ran).scalar()
             arms_id=db.session.query(Firearms.id).filter(Firearms.name==arms).scalar()
             ammu_id=db.session.query(Ammunation.id).filter(Ammunation.name==ammu).scalar()
             
             shooting=Shooting_Session(
                      date=time.strftime("%Y-%m-%d"),
                      datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                      shooting_range_id=range_id,
                      firearms_id=arms_id,
                      ammunation_id=ammu_id,
                      target_distance=distance,
                      weather_notes =weather,
                      comments =comment,
                      session_no=session,
                      occasion=occ
                      )
             db.session.add(shooting)
             db.session.commit()
                      
                      
             result="This is Successfully Saved" 
             return jsonify(result=result ,session=session)
         
            
    @app.route('/target_1_populate/', methods=['GET', 'POST'])
    def target_1_populate():
        if request.method == 'POST':
            session_id=db.session.query(TShooting.session_id).scalar()
        return jsonify(session_id=session_id)
    
    
    @app.route('/load_detail_1/', methods=['GET', 'POST'])
    def load_detail_1():
        result_1="Done"
        if request.method == 'POST':
            curdate=time.strftime("%Y-%m-%d")
            r8=None
            
            data=request.get_json()
            
            tmp_list = []
            duplicate = False
            detail =data["detail"]
            sess=data["session"]
            paper=data["paper"]
            shot=data["shot"]
            set=data["set"]
            
            if(data["r1"]==""):
                r1_id=999
            else:
                r1=data["r1"]
                r1_id=db.session.query(Shooter.id).filter(Shooter.service_id==r1).scalar()
            
            if(data["r2"]==""):
                r2_id=999
            else:
                r2=data["r2"]
                r2_id=db.session.query(Shooter.id).filter(Shooter.service_id==r2).scalar()
            
            if(data["r3"]==""):
                r3_id=999
            else:
                r3=data["r3"]
                r3_id=db.session.query(Shooter.id).filter(Shooter.service_id==r3).scalar()
                
            if(data["r4"]==""):
                r4_id=999
            else:
                r4=data["r4"]
                r4_id=db.session.query(Shooter.id).filter(Shooter.service_id==r4).scalar()
                
            if(data["r5"]==""):
                r5_id=999
            else:
                r5=data["r5"]
                r5_id=db.session.query(Shooter.id).filter(Shooter.service_id==r5).scalar()
                
            if(data["r6"]==""):
                r6_id=999
            else:
                r6=data["r6"]
                r6_id=db.session.query(Shooter.id).filter(Shooter.service_id==r6).scalar()
                
            if(data["r7"]==""):
                r7_id=999
            else:
                r7=data["r7"]
                r7_id=db.session.query(Shooter.id).filter(Shooter.service_id==r7).scalar()
                
            if(data["r8"]==""):
                r8_id=999
            else:
                r8=data["r8"]
                r8_id=db.session.query(Shooter.id).filter(Shooter.service_id==r8).scalar()
        
            
            tmp_list.append(r1_id)
            tmp_list.append(r2_id)
            tmp_list.append(r3_id)
            tmp_list.append(r4_id)
            tmp_list.append(r5_id)
            tmp_list.append(r6_id)
            tmp_list.append(r7_id)
            tmp_list.append(r8_id)
            
            db.session.query(TPaper_ref).delete()
            db.session.commit()
            ref_db = TPaper_ref(
                    date=time.strftime("%Y-%m-%d"),
                    paper_ref=paper,
                    detail_no=detail,
                    session_no=sess
                    )
            db.session.add(ref_db)
            db.session.commit()
            
            for i in range(len(tmp_list)):
                
                for j in range(len(tmp_list)):
                    
                    if(i!=j and tmp_list[i]==tmp_list[j]):
                        if(tmp_list[i]== 999 and tmp_list[j]==999):
                            duplicate = False
                        else:
                            duplicate = True
                    else:
                        
                        duplicate = False
                        
                        
                       
            if(duplicate):
                print("inside dup")
                error="dup"
              
            else:
                db.session.query(TShooting).delete()
                db.session.commit()
                tshoot=TShooting(
                        date=datetime.now(),
                        datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                        session_id=sess,
                        detail_no=detail,
                        target_1_id=r1_id,
                        target_2_id=r2_id,
                        target_3_id=r3_id,
                        target_4_id=r4_id,
                        target_5_id=r5_id,
                        target_6_id=r6_id,
                        target_7_id=r7_id,
                        target_8_id=r8_id,
                        paper_ref=paper,
                        set_no=set,
                        save_flag=0
                        )
                
                db.session.add(tshoot)
                db.session.commit()
                detail_shots =Session_Detail(
                            date=datetime.now(),
                            datetimestamp=time.strftime("%Y-%m-%d %H:%M"),
                            session_id=sess,
                            detail_no=detail,
                            target_1_id=r1_id,
                            target_2_id=r2_id,
                            target_3_id=r3_id,
                            target_4_id=r4_id,
                            target_5_id=r5_id,
                            target_6_id=r6_id,
                            target_7_id=r7_id,
                            target_8_id=r8_id,
                            paper_ref=paper,
                            set_no=set,
                            save_flag=0
                            )
                db.session.add(detail_shots)
                db.session.commit()
                error="ok"
                firer_name,cant,rank,service_id,res,tenden,gp_len,set_4_name,set_4_army,set_4_session_no,set_4_detail_no,set_3_name,set_3_army,set_3_session_no,set_3_detail_no,set_2_name,set_2_army,set_2_session_no,set_2_detail_no,set_1_name,set_1_army,set_1_session_no,set_1_detail_no,current_firer_name,current_army_no,current_session_no,current_detail_no=get_information(r1_id,sess,paper)
       
            result="The Detail is Saved Successfully"
            
            return jsonify(result=result,data1=firer_name,ra_1=rank,detail=detail,
                       service_id_1=service_id,
                       session=sess,
                       paper=paper,
                       set_no=set,
                       cant=cant,
                       gp_len=gp_len,
                       res=res,
                       ten=tenden,
                       set_4_name=set_4_name,
                       set_3_name=set_3_name,
                       set_2_name=set_2_name,
                       set_1_name=set_1_name,
                       current_firer_name=current_firer_name,
                       set_4_army=set_4_army,
                       set_3_army=set_3_army,
                       set_2_army=set_2_army,
                       set_1_army=set_1_army,
                       current_army_no=current_army_no,
                       set_4_session_no=set_4_session_no,
                       set_3_session_no=set_3_session_no,
                       set_2_session_no=set_2_session_no,
                       set_1_session_no=set_1_session_no,
                       current_session_no=current_session_no,
                       set_4_detail_no=set_4_detail_no,
                       set_3_detail_no=set_3_detail_no,
                       set_2_detail_no=set_2_detail_no,
                       set_1_detail_no=set_1_detail_no,
                       current_detail_no=current_detail_no
                                          )
        return jsonify(result_1=result_1)
    
    def get_information(target_1_id,sess,paper_ref):
        res=[]
        ten=[]
        gp_len=[]
        curdate=time.strftime("%Y-%m-%d")
        tten=db.session.query(MPI.tendency_code).filter(MPI.firer_id==target_1_id).order_by(MPI.datetimestamp.desc()).limit(5).all()[::-1]
        tres = db.session.query(Grouping.result).filter(Grouping.firer_id==target_1_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]
        tgp = db.session.query(Grouping.grouping_length_f).filter(Grouping.firer_id==target_1_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]

        for ele in tres:
            for ele2 in ele:
                res.append(ele2)
        for ele3 in tten:
            for ele4 in ele3:
                ten.append(ele4)
                
        for ele5 in tgp:
            for ele6 in ele5:
                gp_len.append(int(ele6))
                
        da_1=db.session.query(Shooter.name).filter(Shooter.id==target_1_id).scalar()
        cant_id=db.session.query(Shooter.cantonment_id).filter(Shooter.id==target_1_id).scalar()
        cant=db.session.query(Cantonment.cantonment).filter(Cantonment.id==cant_id).scalar()
        ra_1_id=db.session.query(Shooter.rank_id).filter(Shooter.id==target_1_id).scalar()
        ra_1 = db.session.query(Rank.name).filter(Rank.id==ra_1_id).scalar()
        service_id_1 = db.session.query(Shooter.service_id).filter(Shooter.id==target_1_id).scalar()
        
        set_1_id = db.session.query(Firer_Details.firer_id).filter(
                                        Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==1
                                                                                                  
                                      ).distinct().scalar()
            
            
        set_1_session_no=db.session.query(Firer_Details.session_id).filter(
                    Firer_Details.date==curdate, 
                                     Firer_Details.target_no==1, 
                                      Firer_Details.set_no==1                                                            
                                      ).distinct().scalar()
            
        set_1_detail_no=db.session.query(Firer_Details.detail_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==1
                                                                                                 
                                      ).distinct().scalar()
            
        set_1_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_1_id
                                                        ).scalar()
        set_1_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_1_id).scalar()
            
            
        set_2_id = db.session.query(Firer_Details.firer_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==2
                                                                                                  
                                      ).distinct().scalar()
            
        set_2_session_no=db.session.query(Firer_Details.session_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==2
                                                                                          
                                      ).distinct().scalar()
            
        set_2_detail_no=db.session.query(Firer_Details.detail_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==2
                                                                                          
                                      ).distinct().scalar()
            
        set_2_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_2_id
                                                        ).scalar()
            
            
        set_2_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_2_id).scalar()
            
            
        set_3_id = db.session.query(Firer_Details.firer_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==3                                                            
                                      ).distinct().scalar()
            
        set_3_session_no=db.session.query(Firer_Details.session_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==3                                                            
                                      ).distinct().scalar()
            
        set_3_detail_no=db.session.query(Firer_Details.detail_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==3
                                                                                                
                                      ).distinct().scalar()
            
        set_3_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_3_id
                                                        ).scalar()
        set_3_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_3_id).scalar()
            
            
            
        set_4_id = db.session.query(Firer_Details.firer_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==4                                                            
                                      ).distinct().scalar()
            
        set_4_session_no=db.session.query(Firer_Details.session_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==4
                                                                                                  
                                      ).distinct().scalar()
            
        set_4_detail_no=db.session.query(Firer_Details.detail_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==4                                                            
                                      ).distinct().scalar()
            
        set_4_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_4_id
                                                        ).scalar()
        set_4_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_4_id).scalar()
            
            
        current_firer_name = db.session.query(Shooter.name).filter(Shooter.id==target_1_id).scalar()
        current_army_no = db.session.query(Shooter.service_id).filter(Shooter.id==target_1_id).scalar()
        current_session_no=db.session.query(TShooting.session_id).filter(TShooting.target_1_id==target_1_id).scalar()
        current_detail_no=db.session.query(TShooting.detail_no).filter(TShooting.target_1_id==target_1_id).scalar()
        
        return(da_1,cant,ra_1,service_id_1,res,ten,gp_len,
               set_4_name,set_4_army,set_4_session_no,set_4_detail_no,
               set_3_name,set_3_army,set_3_session_no,set_3_detail_no,
               set_2_name,set_2_army,set_2_session_no,set_2_detail_no,
               set_1_name,set_1_army,set_1_session_no,set_1_detail_no,
               current_firer_name,current_army_no,current_session_no,current_detail_no
               )
    
        
    @app.route('/individual_score/target_2', methods=['GET', 'POST'])
    def individual_score_target_2():
        firer_id =db.session.query(TShooting.target_2_id).scalar()
        detail_no =db.session.query(TShooting.detail_no).scalar()
        session_no =db.session.query(TShooting.session_id).scalar()
        target_no = 2
        tres = db.session.query(Grouping.result).filter(Grouping.firer_id==firer_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]
        res=[]
        ten=[]
        tten=db.session.query(MPI.tendency_code).filter(MPI.firer_id==firer_id).order_by(MPI.datetimestamp.desc()).limit(5).all()[::-1]
        print(tres,)
        for ele in tres:
            for ele2 in ele:
                print(type(ele2))
                res.append(ele2)
                
        for ele3 in tten:
            for ele4 in ele3:
                print(type(ele4))
                ten.append(ele4)
            
            
        service_id = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
        rank_id=db.session.query(Shooter.rank_id).filter(Shooter.id==firer_id).scalar()
        rank=db.session.query(Rank.name).filter(Rank.id==rank_id).scalar()
        name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
        firer_id,sess,o,p,u,q,t1_x,t1_y,xmpi,ympi,f,gp,Tfirt_x,Tfirt_y,fin_x_1,fin_y_1,result_1,fir_tendency_1=prediction_calculation_2()
        if request.method == 'POST':
            paper_ref=db.session.query(TPaper_ref.paper_ref).scalar() 
            print("paper_ref")
            print(paper_ref)
        return render_template('pages/prediction_target_2.html',
                               name = name,
                               detail_no=detail_no,
                               session_no=session_no,
                               target_no=target_no,
                               service_id=service_id,
                               rank=rank,
                               res=res,
                               ten=ten)
        
    @app.route('/individual_score/target_3', methods=['GET', 'POST'])
    def individual_score_target_3():
        firer_id =db.session.query(TShooting.target_3_id).scalar()
        detail_no =db.session.query(TShooting.detail_no).scalar()
        session_no =db.session.query(TShooting.session_id).scalar()
        target_no = 3
        tres = db.session.query(Grouping.result).filter(Grouping.firer_id==firer_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]
        res=[]
        ten=[]
        tten=db.session.query(MPI.tendency_code).filter(MPI.firer_id==firer_id).order_by(MPI.datetimestamp.desc()).limit(5).all()[::-1]
        print(tres)
        for ele in tres:
            for ele2 in ele:
                print(type(ele2))
                res.append(ele2)
                
        for ele3 in tten:
            for ele4 in ele3:
                print(type(ele4))
                ten.append(ele4)
            
            
        service_id = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
        rank_id=db.session.query(Shooter.rank_id).filter(Shooter.id==firer_id).scalar()
        rank=db.session.query(Rank.name).filter(Rank.id==rank_id).scalar()
        name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
        return render_template('pages/prediction_target_3.html',
                               name = name,
                               detail_no=detail_no,
                               session_no=session_no,
                               target_no=target_no,
                               service_id=service_id,
                               rank=rank,
                               res=res,
                               ten=ten)
        
    @app.route('/individual_score/target_4', methods=['GET', 'POST'])
    def individual_score_target_4():
        firer_id =db.session.query(TShooting.target_4_id).scalar()
        detail_no =db.session.query(TShooting.detail_no).scalar()
        session_no =db.session.query(TShooting.session_id).scalar()
        target_no = 4
        tres = db.session.query(Grouping.result).filter(Grouping.firer_id==firer_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]
        res=[]
        ten=[]
        tten=db.session.query(MPI.tendency_code).filter(MPI.firer_id==firer_id).order_by(MPI.datetimestamp.desc()).limit(5).all()[::-1]
        print(tres)
        for ele in tres:
            for ele2 in ele:
                print(type(ele2))
                res.append(ele2)
                
        for ele3 in tten:
            for ele4 in ele3:
                print(type(ele4))
                ten.append(ele4)
            
            
        service_id = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
        rank_id=db.session.query(Shooter.rank_id).filter(Shooter.id==firer_id).scalar()
        rank=db.session.query(Rank.name).filter(Rank.id==rank_id).scalar()
        name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
        return render_template('pages/prediction_target_4.html',
                               name = name,
                               detail_no=detail_no,
                               session_no=session_no,
                               target_no=target_no,
                               service_id=service_id,
                               rank=rank,
                               res=res,
                               ten=ten)
        
        
    @app.route('/individual_score/target_5', methods=['GET', 'POST'])
    def individual_score_target_5():
        firer_id =db.session.query(TShooting.target_5_id).scalar()
        detail_no =db.session.query(TShooting.detail_no).scalar()
        session_no =db.session.query(TShooting.session_id).scalar()
        target_no = 5
        tres = db.session.query(Grouping.result).filter(Grouping.firer_id==firer_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]
        res=[]
        ten=[]
        tten=db.session.query(MPI.tendency_code).filter(MPI.firer_id==firer_id).order_by(MPI.datetimestamp.desc()).limit(5).all()[::-1]
        print(tres)
        for ele in tres:
            for ele2 in ele:
                print(type(ele2))
                res.append(ele2)
                
        for ele3 in tten:
            for ele4 in ele3:
                print(type(ele4))
                ten.append(ele4)
            
            
        service_id = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
        rank_id=db.session.query(Shooter.rank_id).filter(Shooter.id==firer_id).scalar()
        rank=db.session.query(Rank.name).filter(Rank.id==rank_id).scalar()
        name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
        return render_template('pages/prediction_target_5.html',
                               name = name,
                               detail_no=detail_no,
                               session_no=session_no,
                               target_no=target_no,
                               service_id=service_id,
                               rank=rank,
                               res=res,
                               ten=ten)
        
        
    @app.route('/individual_score/target_6', methods=['GET', 'POST'])
    def individual_score_target_6():
        firer_id =db.session.query(TShooting.target_6_id).scalar()
        detail_no =db.session.query(TShooting.detail_no).scalar()
        session_no =db.session.query(TShooting.session_id).scalar()
        target_no = 6
        tres = db.session.query(Grouping.result).filter(Grouping.firer_id==firer_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]
        res=[]
        ten=[]
        tten=db.session.query(MPI.tendency_code).filter(MPI.firer_id==firer_id).order_by(MPI.datetimestamp.desc()).limit(5).all()[::-1]
        print(tres)
        for ele in tres:
            for ele2 in ele:
                print(type(ele2))
                res.append(ele2)
                
        for ele3 in tten:
            for ele4 in ele3:
                print(type(ele4))
                ten.append(ele4)
            
            
        service_id = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
        rank_id=db.session.query(Shooter.rank_id).filter(Shooter.id==firer_id).scalar()
        rank=db.session.query(Rank.name).filter(Rank.id==rank_id).scalar()
        name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
        return render_template('pages/prediction_target_6.html',
                               name = name,
                               detail_no=detail_no,
                               session_no=session_no,
                               target_no=target_no,
                               service_id=service_id,
                               rank=rank,
                               res=res,
                               ten=ten)
        
    @app.route('/individual_score/target_7', methods=['GET', 'POST'])
    def individual_score_target_7():
        firer_id =db.session.query(TShooting.target_7_id).scalar()
        detail_no =db.session.query(TShooting.detail_no).scalar()
        session_no =db.session.query(TShooting.session_id).scalar()
        target_no = 7
        tres = db.session.query(Grouping.result).filter(Grouping.firer_id==firer_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]
        res=[]
        ten=[]
        tten=db.session.query(MPI.tendency_code).filter(MPI.firer_id==firer_id).order_by(MPI.datetimestamp.desc()).limit(5).all()[::-1]
        print(tres)
        for ele in tres:
            for ele2 in ele:
                print(type(ele2))
                res.append(ele2)
                
        for ele3 in tten:
            for ele4 in ele3:
                print(type(ele4))
                ten.append(ele4)
            
            
        service_id = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
        rank_id=db.session.query(Shooter.rank_id).filter(Shooter.id==firer_id).scalar()
        rank=db.session.query(Rank.name).filter(Rank.id==rank_id).scalar()
        name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
        return render_template('pages/prediction_target_7.html',
                               name = name,
                               detail_no=detail_no,
                               session_no=session_no,
                               target_no=target_no,
                               service_id=service_id,
                               rank=rank,
                               res=res,
                               ten=ten)
        
    @app.route('/individual_score/target_8', methods=['GET', 'POST'])
    def individual_score_target_8():
        firer_id =db.session.query(TShooting.target_8_id).scalar()
        detail_no =db.session.query(TShooting.detail_no).scalar()
        session_no =db.session.query(TShooting.session_id).scalar()
        target_no = 7
        tres = db.session.query(Grouping.result).filter(Grouping.firer_id==firer_id).order_by(Grouping.datetimestamp.desc()).limit(5).all()[::-1]
        res=[]
        ten=[]
        tten=db.session.query(MPI.tendency_code).filter(MPI.firer_id==firer_id).order_by(MPI.datetimestamp.desc()).limit(5).all()[::-1]
        print(tres)
        for ele in tres:
            for ele2 in ele:
                print(type(ele2))
                res.append(ele2)
                
        for ele3 in tten:
            for ele4 in ele3:
                print(type(ele4))
                ten.append(ele4)
            
            
        service_id = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
        rank_id=db.session.query(Shooter.rank_id).filter(Shooter.id==firer_id).scalar()
        rank=db.session.query(Rank.name).filter(Rank.id==rank_id).scalar()
        name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
        return render_template('pages/prediction_target_8.html',
                               name = name,
                               detail_no=detail_no,
                               session_no=session_no,
                               target_no=target_no,
                               service_id=service_id,
                               rank=rank,
                               res=res,
                               ten=ten)
        
        
    @app.route('/prediction_target_1/', methods=['GET', 'POST'])
    def prediction_target_1():
        t1_x=0
        t1_y=0
        xmpi_j=0
        ympi_j=0
        gp=0
        Tfirt_x_j=0
        Tfirt_y_j=0
        fin_x_1=0
        fin_y_1=0
        xmpi_inch = 0
        ympi_inch = 0
        result_1=None
        fir_tendency=None
        set_1_name = None
        set_1_army =None
        set_1_session_no = None
        set_1_detail_no=None
        set_1_id =None
        
        set_2_name = None
        set_2_army =None
        set_2_session_no = None
        set_2_detail_no=None
        set_2_id =None
        
        set_3_name = None
        set_3_army =None
        set_3_session_no = None
        set_3_detail_no=None
        set_3_id =None
        
        set_4_name = None
        set_4_army =None
        set_4_session_no = None
        set_4_detail_no=None
        set_4_id =None
        
        fir_tendency_1=None
        firer_id=None
        current_army_no=None
        current_firer_name=None
        current_session_no=None
        session_detail_no=None
        current_detail_no=None
        
        set_2_x=None
        set_2_y=None
        set_3_x=None
        set_3_y=None
        
        set_4_x=None
        set_4_y=None
        paper_ref=None
        sess=None
        res=None
        set_2_x_arr=[]
        set_2_y_arr=[]
        
        set_3_x_arr=[]
        set_3_y_arr=[]
        
        set_4_x_arr=[]
        set_4_y_arr=[]
        
        fin_x_arr_1=[]
        fin_y_arr_1=[]
        curdate=time.strftime("%Y-%m-%d")
        
        if request.method == 'POST':
            firer_id,sess,detail,p,u,q,t1_x,t1_y,xmpi,ympi,f,gp,Tfirt_x,Tfirt_y,fin_x_1,fin_y_1,result_1,fir_tendency_1=prediction_calculation_1()
            
            paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
            
            
            set_2_x=db.session.query(Firer_Details).filter(Firer_Details.date==curdate , Firer_Details.target_no==1 ,Firer_Details.set_no==2 ,  Firer_Details.session_id==sess).all()
            set_2_y=db.session.query(Firer_Details).filter(Firer_Details.date==curdate , Firer_Details.target_no==1 , Firer_Details.set_no==2 , Firer_Details.session_id==sess).all()
            
            for x_2 in set_2_x:
                set_2_x_arr.append(int(x_2.final_x))
                
            for y_2 in set_2_y:
                set_2_y_arr.append(int(y_2.final_y))
                
                
            set_3_x=db.session.query(Firer_Details).filter(Firer_Details.date==curdate , Firer_Details.target_no==1 , Firer_Details.set_no==3 , Firer_Details.session_id==sess).all()
            set_3_y=db.session.query(Firer_Details).filter(Firer_Details.date==curdate , Firer_Details.target_no==1 , Firer_Details.set_no==3 , Firer_Details.session_id==sess).all()
            
            for x_3 in set_3_x:
                set_3_x_arr.append(int(x_3.final_x))
                
            for y_3 in set_3_y:
                set_3_y_arr.append(int(y_3.final_y))
                
                
            print(set_3_x_arr)   
            set_4_x=db.session.query(Firer_Details).filter(Firer_Details.date==curdate , Firer_Details.target_no==1 , Firer_Details.set_no==4 , Firer_Details.session_id==sess).all()
            set_4_y=db.session.query(Firer_Details).filter(Firer_Details.date==curdate , Firer_Details.target_no==1 , Firer_Details.set_no==4 , Firer_Details.session_id==sess).all()
            
            for x_4 in set_4_x:
                set_4_x_arr.append(int(x_4.final_x))
                
            for y_4 in set_4_y:
                set_4_y_arr.append(int(y_4.final_y))
                
            set_1_id = db.session.query(Firer_Details.firer_id).filter(
                           Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==1
                                                                                                  
                                      ).distinct().scalar()
            
            
            set_1_session_no=db.session.query(Firer_Details.session_id).filter(
                    Firer_Details.date==curdate, 
                                     Firer_Details.target_no==1, 
                                      Firer_Details.set_no==1                                                            
                                      ).distinct().scalar()
            
            set_1_detail_no=db.session.query(Firer_Details.detail_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==1
                                                                                                 
                                      ).distinct().scalar()
            
            set_1_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_1_id
                                                        ).scalar()
            set_1_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_1_id).scalar()
            
            
            set_2_id = db.session.query(Firer_Details.firer_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==2
                                                                                                  
                                      ).distinct().scalar()
            
            set_2_session_no=db.session.query(Firer_Details.session_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==2
                                                                                          
                                      ).distinct().scalar()
            
            set_2_detail_no=db.session.query(Firer_Details.detail_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==2
                                                                                          
                                      ).distinct().scalar()
            print("set_2_detail_no")
            print(set_2_detail_no)
            print(set_2_detail_no)
            set_2_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_2_id
                                                        ).scalar()
            
            
            set_2_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_2_id).scalar()
            
            
            set_3_id = db.session.query(Firer_Details.firer_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==3                                                            
                                      ).distinct().scalar()
            
            set_3_session_no=db.session.query(Firer_Details.session_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==3                                                            
                                      ).distinct().scalar()
            
            set_3_detail_no=db.session.query(Firer_Details.detail_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==3
                                                                                                
                                      ).distinct().scalar()
            
            set_3_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_3_id
                                                        ).scalar()
            set_3_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_3_id).scalar()
            
            
            
            set_4_id = db.session.query(Firer_Details.firer_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==4                                                            
                                      ).distinct().scalar()
            
            set_4_session_no=db.session.query(Firer_Details.session_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==4
                                                                                                  
                                      ).distinct().scalar()
            
            set_4_detail_no=db.session.query(Firer_Details.detail_id).filter(
                                      Firer_Details.date==curdate, 
                                      Firer_Details.target_no==1, 
                                      Firer_Details.set_no==4                                                            
                                      ).distinct().scalar()
            
            set_4_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_4_id
                                                        ).scalar()
            set_4_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_4_id).scalar()
            
            
            current_firer_name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
            current_army_no = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
            current_session_no=db.session.query(TShooting.session_id).filter(TShooting.target_1_id==firer_id).scalar()
            current_detail_no=db.session.query(TShooting.detail_no).filter(TShooting.target_1_id==firer_id).scalar()
            
            
            xmpi_inch = pixeltoinch(xmpi)
            ympi_inch = pixeltoinch(ympi)
            xmpi_j =pd.Series(xmpi_inch).to_json(orient='values')
            ympi_j =pd.Series(ympi_inch).to_json(orient='values')
            Tfirt_x_j =pd.Series(Tfirt_x).to_json(orient='values')
            Tfirt_y_j =pd.Series(Tfirt_y).to_json(orient='values')
            
         
            
            for x_1 in fin_x_1:
                fin_x_arr_1.append(int(x_1.final_x))
            for y_1 in fin_y_1 :
                fin_y_arr_1.append(int(y_1.final_y))
                
        return jsonify(x1=t1_x ,
                       y1=t1_y ,
                       xmpi1=Tfirt_x_j ,
                       ympi1=Tfirt_y_j,
                       gp=gp,
                       txf1=Tfirt_x_j,
                       tyf1=Tfirt_y_j,
                       fx1=fin_x_arr_1,
                       fy1=fin_y_arr_1,
                       result_1=result_1,
                       fir_tendency_1=fir_tendency_1,
                       set_1_name=set_1_name,
                       current_firer_name=current_firer_name,
                       set_1_army=set_1_army,
                       current_army_no=current_army_no,
                       set_1_session_no=set_1_session_no,
                       current_session_no=current_session_no,
                       set_1_detail_no=set_1_detail_no,
                       current_detail_no=current_detail_no,
                       set_2_x=set_2_x_arr,
                       set_2_y=set_2_y_arr,
                       set_2_name=set_2_name,
                       set_2_army=set_2_army,
                       set_2_detail_no=set_2_detail_no,
                       set_2_session_no=set_2_session_no,
                       set_3_x=set_3_x_arr,
                       set_3_y=set_3_y_arr,
                       set_3_name=set_3_name,
                       set_3_army=set_3_army,
                       set_3_session_no=set_3_session_no,
                       set_3_detail_no=set_3_detail_no,
                       set_4_x=set_4_x_arr,
                       set_4_y=set_4_y_arr,
                       set_4_name=set_4_name,
                       set_4_army=set_4_army,
                       set_4_session_no=set_4_session_no,
                       set_4_detail_no=set_4_detail_no
                       )
   
    @app.route('/prediction_target_2/', methods=['GET', 'POST'])
    def prediction_target_2():
        t1_x=0
        t1_y=0
        xmpi_j=0
        ympi_j=0
        gp=0
        Tfirt_x_j=0
        Tfirt_y_j=0
        fin_x_1=0
        fin_y_1=0
        xmpi_inch = 0
        ympi_inch = 0
        result_1=None
        fir_tendency=None
        set_1_name = None
        set_1_army =None
        set_1_session_no = None
        set_1_detail_no=None
        set_1_id =None
        
        set_2_name = None
        set_2_army =None
        set_2_session_no = None
        set_2_detail_no=None
        set_2_id =None
        
        set_3_name = None
        set_3_army =None
        set_3_session_no = None
        set_3_detail_no=None
        set_3_id =None
        
        set_4_name = None
        set_4_army =None
        set_4_session_no = None
        set_4_detail_no=None
        set_4_id =None
        
        fir_tendency_1=None
        firer_id=None
        current_army_no=None
        current_firer_name=None
        current_session_no=None
        session_detail_no=None
        current_detail_no=None
        
        set_2_x=None
        set_2_y=None
        set_3_x=None
        set_3_y=None
        
        set_4_x=None
        set_4_y=None
        paper_ref=None
        sess=None
        res=None
        set_2_x_arr=[]
        set_2_y_arr=[]
        
        set_3_x_arr=[]
        set_3_y_arr=[]
        
        set_4_x_arr=[]
        set_4_y_arr=[]
        
        fin_x_arr_1=[]
        fin_y_arr_1=[]
        curdate=time.strftime("%Y-%m-%d")
        
        if request.method == 'POST':
            firer_id,sess,o,p,u,q,t1_x,t1_y,xmpi,ympi,f,gp,Tfirt_x,Tfirt_y,fin_x_1,fin_y_1,result_1,fir_tendency_1=prediction_calculation_2()
            paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
            
            
            set_2_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==2 ,T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_2_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==2 , T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_2 in set_2_x:
                set_2_x_arr.append(int(x_2.final_x))
                
            for y_2 in set_2_y:
                set_2_y_arr.append(int(y_2.final_y))
                
                
            set_3_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==2 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_3_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==2 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_3 in set_3_x:
                set_3_x_arr.append(int(x_3.final_x))
                
            for y_3 in set_3_y:
                set_3_y_arr.append(int(y_3.final_y))
                
                
                
            set_4_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==2 , T_Firer_Details.set_no==4 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_4_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==2 , T_Firer_Details.set_no==4 ,T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_4 in set_4_x:
                set_4_x_arr.append(int(x_4.final_x))
                
            for y_4 in set_4_y:
                set_4_y_arr.append(int(y_4.final_y))
                
            set_1_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref, 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            
            set_1_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_1_id
                                                        ).scalar()
            set_1_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_1_id).scalar()
            
            
            set_2_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_2_id
                                                        ).scalar()
            
            
            set_2_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_2_id).scalar()
            
            
            set_3_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_3_id
                                                        ).scalar()
            set_3_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_3_id).scalar()
            
            
            
            set_4_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==2, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_4_id
                                                        ).scalar()
            set_4_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_4_id).scalar()
            
            
            current_firer_name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
            current_army_no = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
            current_session_no=db.session.query(TShooting.session_id).filter(TShooting.target_1_id==firer_id).scalar()
            current_detail_no=db.session.query(TShooting.detail_no).filter(TShooting.target_1_id==firer_id).scalar()
            
            
            xmpi_inch = pixeltoinch(xmpi)
            ympi_inch = pixeltoinch(ympi)
            xmpi_j =pd.Series(xmpi_inch).to_json(orient='values')
            ympi_j =pd.Series(ympi_inch).to_json(orient='values')
            Tfirt_x_j =pd.Series(Tfirt_x).to_json(orient='values')
            Tfirt_y_j =pd.Series(Tfirt_y).to_json(orient='values')
            
            fin_x_arr_1=[]
            fin_y_arr_1=[]
            
            for x_1 in fin_x_1:
                fin_x_arr_1.append(int(x_1.final_x))
            for y_1 in fin_y_1 :
                fin_y_arr_1.append(int(y_1.final_y))
                
        return jsonify(x1=t1_x ,
                       y1=t1_y ,
                       xmpi1=Tfirt_x_j ,
                       ympi1=Tfirt_y_j,
                       gp=gp,
                       txf1=Tfirt_x_j,
                       tyf1=Tfirt_y_j,
                       fx1=fin_x_arr_1,
                       fy1=fin_y_arr_1,
                       result_1=result_1,
                       fir_tendency_1=fir_tendency_1,
                       set_1_name=set_1_name,
                       current_firer_name=current_firer_name,
                       set_1_army=set_1_army,
                       current_army_no=current_army_no,
                       set_1_session_no=set_1_session_no,
                       current_session_no=current_session_no,
                       set_1_detail_no=set_1_detail_no,
                       current_detail_no=current_detail_no,
                       set_2_x=set_2_x_arr,
                       set_2_y=set_2_y_arr,
                       set_2_name=set_2_name,
                       set_2_army=set_2_army,
                       set_2_detail_no=set_2_detail_no,
                       set_2_session_no=set_2_session_no,
                       set_3_x=set_3_x_arr,
                       set_3_y=set_3_y_arr,
                       set_3_name=set_3_name,
                       set_3_army=set_3_army,
                       set_3_session_no=set_3_session_no,
                       set_3_detail_no=set_3_detail_no,
                       set_4_x=set_4_x_arr,
                       set_4_y=set_4_y_arr,
                       set_4_name=set_4_name,
                       set_4_army=set_4_army,
                       set_4_session_no=set_4_session_no,
                       set_4_detail_no=set_4_detail_no
                       )
    @app.route('/prediction_target_3/', methods=['GET', 'POST'])
    def prediction_target_3():
        t1_x=0
        t1_y=0
        xmpi_j=0
        ympi_j=0
        gp=0
        Tfirt_x_j=0
        Tfirt_y_j=0
        fin_x_1=0
        fin_y_1=0
        xmpi_inch = 0
        ympi_inch = 0
        result_1=None
        fir_tendency=None
        set_1_name = None
        set_1_army =None
        set_1_session_no = None
        set_1_detail_no=None
        set_1_id =None
        
        set_2_name = None
        set_2_army =None
        set_2_session_no = None
        set_2_detail_no=None
        set_2_id =None
        
        set_3_name = None
        set_3_army =None
        set_3_session_no = None
        set_3_detail_no=None
        set_3_id =None
        
        set_4_name = None
        set_4_army =None
        set_4_session_no = None
        set_4_detail_no=None
        set_4_id =None
        
        fir_tendency_1=None
        firer_id=None
        current_army_no=None
        current_firer_name=None
        current_session_no=None
        session_detail_no=None
        current_detail_no=None
        
        set_2_x=None
        set_2_y=None
        set_3_x=None
        set_3_y=None
        
        set_4_x=None
        set_4_y=None
        paper_ref=None
        sess=None
        res=None
        set_2_x_arr=[]
        set_2_y_arr=[]
        
        set_3_x_arr=[]
        set_3_y_arr=[]
        
        set_4_x_arr=[]
        set_4_y_arr=[]
        
        fin_x_arr_1=[]
        fin_y_arr_1=[]
        curdate=time.strftime("%Y-%m-%d")
        
        if request.method == 'POST':
            firer_id,sess,o,p,u,q,t1_x,t1_y,xmpi,ympi,f,gp,Tfirt_x,Tfirt_y,fin_x_1,fin_y_1,result_1,fir_tendency_1=prediction_calculation_3()
            paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
            
            
            set_2_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==3 ,T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_2_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==3 , T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_2 in set_2_x:
                set_2_x_arr.append(int(x_2.final_x))
                
            for y_2 in set_2_y:
                set_2_y_arr.append(int(y_2.final_y))
                
                
            set_3_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==3 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_3_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==3 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_3 in set_3_x:
                set_3_x_arr.append(int(x_3.final_x))
                
            for y_2 in set_2_y:
                set_3_y_arr.append(int(y_3.final_y))
                
                
                
            set_4_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==3 , T_Firer_Details.set_no==4 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_4_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==3 , T_Firer_Details.set_no==4 ,T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_4 in set_4_x:
                set_4_x_arr.append(int(x_4.final_x))
                
            for y_2 in set_2_y:
                set_4_y_arr.append(int(y_4.final_y))
                
            set_1_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref, 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            
            set_1_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_1_id
                                                        ).scalar()
            set_1_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_1_id).scalar()
            
            
            set_2_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_2_id
                                                        ).scalar()
            
            
            set_2_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_2_id).scalar()
            
            
            set_3_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_3_id
                                                        ).scalar()
            set_3_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_3_id).scalar()
            
            
            
            set_4_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==3, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_4_id
                                                        ).scalar()
            set_4_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_4_id).scalar()
            
            
            current_firer_name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
            current_army_no = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
            current_session_no=db.session.query(TShooting.session_id).filter(TShooting.target_1_id==firer_id).scalar()
            current_detail_no=db.session.query(TShooting.detail_no).filter(TShooting.target_1_id==firer_id).scalar()
            
            
            xmpi_inch = pixeltoinch(xmpi)
            ympi_inch = pixeltoinch(ympi)
            xmpi_j =pd.Series(xmpi_inch).to_json(orient='values')
            ympi_j =pd.Series(ympi_inch).to_json(orient='values')
            Tfirt_x_j =pd.Series(Tfirt_x).to_json(orient='values')
            Tfirt_y_j =pd.Series(Tfirt_y).to_json(orient='values')
            
            fin_x_arr_1=[]
            fin_y_arr_1=[]
            
            for x_1 in fin_x_1:
                fin_x_arr_1.append(int(x_1.final_x))
            for y_1 in fin_y_1 :
                fin_y_arr_1.append(int(y_1.final_y))
                
        return jsonify(x1=t1_x ,
                       y1=t1_y ,
                       xmpi1=Tfirt_x_j ,
                       ympi1=Tfirt_y_j,
                       gp=gp,
                       txf1=Tfirt_x_j,
                       tyf1=Tfirt_y_j,
                       fx1=fin_x_arr_1,
                       fy1=fin_y_arr_1,
                       result_1=result_1,
                       fir_tendency_1=fir_tendency_1,
                       set_1_name=set_1_name,
                       current_firer_name=current_firer_name,
                       set_1_army=set_1_army,
                       current_army_no=current_army_no,
                       set_1_session_no=set_1_session_no,
                       current_session_no=current_session_no,
                       set_1_detail_no=set_1_detail_no,
                       current_detail_no=current_detail_no,
                       set_2_x=set_2_x_arr,
                       set_2_y=set_2_y_arr,
                       set_2_name=set_2_name,
                       set_2_army=set_2_army,
                       set_2_detail_no=set_2_detail_no,
                       set_2_session_no=set_2_session_no,
                       set_3_x=set_3_x_arr,
                       set_3_y=set_3_y_arr,
                       set_3_name=set_3_name,
                       set_3_army=set_3_army,
                       set_3_session_no=set_3_session_no,
                       set_3_detail_no=set_3_detail_no,
                       set_4_x=set_4_x_arr,
                       set_4_y=set_4_y_arr,
                       set_4_name=set_4_name,
                       set_4_army=set_4_army,
                       set_4_session_no=set_4_session_no,
                       set_4_detail_no=set_4_detail_no
                       )
        
        
    @app.route('/prediction_target_4/', methods=['GET', 'POST'])
    def prediction_target_4():
        t1_x=0
        t1_y=0
        xmpi_j=0
        ympi_j=0
        gp=0
        Tfirt_x_j=0
        Tfirt_y_j=0
        fin_x_1=0
        fin_y_1=0
        xmpi_inch = 0
        ympi_inch = 0
        result_1=None
        fir_tendency=None
        set_1_name = None
        set_1_army =None
        set_1_session_no = None
        set_1_detail_no=None
        set_1_id =None
        
        set_2_name = None
        set_2_army =None
        set_2_session_no = None
        set_2_detail_no=None
        set_2_id =None
        
        set_3_name = None
        set_3_army =None
        set_3_session_no = None
        set_3_detail_no=None
        set_3_id =None
        
        set_4_name = None
        set_4_army =None
        set_4_session_no = None
        set_4_detail_no=None
        set_4_id =None
        
        fir_tendency_1=None
        firer_id=None
        current_army_no=None
        current_firer_name=None
        current_session_no=None
        session_detail_no=None
        current_detail_no=None
        
        set_2_x=None
        set_2_y=None
        set_3_x=None
        set_3_y=None
        
        set_4_x=None
        set_4_y=None
        paper_ref=None
        sess=None
        res=None
        set_2_x_arr=[]
        set_2_y_arr=[]
        
        set_3_x_arr=[]
        set_3_y_arr=[]
        
        set_4_x_arr=[]
        set_4_y_arr=[]
        fin_x_arr_1=[]
        fin_y_arr_1=[]
        
        curdate=time.strftime("%Y-%m-%d")
        
        if request.method == 'POST':
            firer_id,sess,o,p,u,q,t1_x,t1_y,xmpi,ympi,f,gp,Tfirt_x,Tfirt_y,fin_x_1,fin_y_1,result_1,fir_tendency_1=prediction_calculation_4()
            paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
            
            
            set_2_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==4 ,T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_2_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==4 , T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_2 in set_2_x:
                set_2_x_arr.append(int(x_2.final_x))
                
            for y_2 in set_2_y:
                set_2_y_arr.append(int(y_2.final_y))
                
                
            set_3_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==4 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_3_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==4 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_3 in set_3_x:
                set_3_x_arr.append(int(x_3.final_x))
                
            for y_3 in set_3_y:
                set_3_y_arr.append(int(y_3.final_y))
                
                
                
            set_4_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==4 , T_Firer_Details.set_no==4 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_4_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==4 , T_Firer_Details.set_no==4 ,T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_4 in set_4_x:
                set_4_x_arr.append(int(x_4.final_x))
                
            for y_4 in set_4_y:
                set_4_y_arr.append(int(y_4.final_y))
                
            set_1_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref, 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            
            set_1_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_1_id
                                                        ).scalar()
            set_1_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_1_id).scalar()
            
            
            set_2_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_2_id
                                                        ).scalar()
            
            
            set_2_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_2_id).scalar()
            
            
            set_3_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_3_id
                                                        ).scalar()
            set_3_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_3_id).scalar()
            
            
            
            set_4_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==4, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_4_id
                                                        ).scalar()
            set_4_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_4_id).scalar()
            
            
            current_firer_name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
            current_army_no = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
            current_session_no=db.session.query(TShooting.session_id).filter(TShooting.target_1_id==firer_id).scalar()
            current_detail_no=db.session.query(TShooting.detail_no).filter(TShooting.target_1_id==firer_id).scalar()
            
            
            xmpi_inch = pixeltoinch(xmpi)
            ympi_inch = pixeltoinch(ympi)
            xmpi_j =pd.Series(xmpi_inch).to_json(orient='values')
            ympi_j =pd.Series(ympi_inch).to_json(orient='values')
            Tfirt_x_j =pd.Series(Tfirt_x).to_json(orient='values')
            Tfirt_y_j =pd.Series(Tfirt_y).to_json(orient='values')
            

            for x_1 in fin_x_1:
                fin_x_arr_1.append(int(x_1.final_x))
            for y_1 in fin_y_1 :
                fin_y_arr_1.append(int(y_1.final_y))
                
        return jsonify(x1=t1_x ,
                       y1=t1_y ,
                       xmpi1=Tfirt_x_j ,
                       ympi1=Tfirt_y_j,
                       gp=gp,
                       txf1=Tfirt_x_j,
                       tyf1=Tfirt_y_j,
                       fx1=fin_x_arr_1,
                       fy1=fin_y_arr_1,
                       result_1=result_1,
                       fir_tendency_1=fir_tendency_1,
                       set_1_name=set_1_name,
                       current_firer_name=current_firer_name,
                       set_1_army=set_1_army,
                       current_army_no=current_army_no,
                       set_1_session_no=set_1_session_no,
                       current_session_no=current_session_no,
                       set_1_detail_no=set_1_detail_no,
                       current_detail_no=current_detail_no,
                       set_2_x=set_2_x_arr,
                       set_2_y=set_2_y_arr,
                       set_2_name=set_2_name,
                       set_2_army=set_2_army,
                       set_2_detail_no=set_2_detail_no,
                       set_2_session_no=set_2_session_no,
                       set_3_x=set_3_x_arr,
                       set_3_y=set_3_y_arr,
                       set_3_name=set_3_name,
                       set_3_army=set_3_army,
                       set_3_session_no=set_3_session_no,
                       set_3_detail_no=set_3_detail_no,
                       set_4_x=set_4_x_arr,
                       set_4_y=set_4_y_arr,
                       set_4_name=set_4_name,
                       set_4_army=set_4_army,
                       set_4_session_no=set_4_session_no,
                       set_4_detail_no=set_4_detail_no
                       )
        
        
    @app.route('/prediction_target_5/', methods=['GET', 'POST'])
    def prediction_target_5():
        t1_x=0
        t1_y=0
        xmpi_j=0
        ympi_j=0
        gp=0
        Tfirt_x_j=0
        Tfirt_y_j=0
        fin_x_1=0
        fin_y_1=0
        xmpi_inch = 0
        ympi_inch = 0
        result_1=None
        fir_tendency=None
        set_1_name = None
        set_1_army =None
        set_1_session_no = None
        set_1_detail_no=None
        set_1_id =None
        
        set_2_name = None
        set_2_army =None
        set_2_session_no = None
        set_2_detail_no=None
        set_2_id =None
        
        set_3_name = None
        set_3_army =None
        set_3_session_no = None
        set_3_detail_no=None
        set_3_id =None
        
        set_4_name = None
        set_4_army =None
        set_4_session_no = None
        set_4_detail_no=None
        set_4_id =None
        
        fir_tendency_1=None
        firer_id=None
        current_army_no=None
        current_firer_name=None
        current_session_no=None
        session_detail_no=None
        current_detail_no=None
        
        set_2_x=None
        set_2_y=None
        set_3_x=None
        set_3_y=None
        
        set_4_x=None
        set_4_y=None
        paper_ref=None
        sess=None
        res=None
        set_2_x_arr=[]
        set_2_y_arr=[]
        
        set_3_x_arr=[]
        set_3_y_arr=[]
        
        set_4_x_arr=[]
        set_4_y_arr=[]
        
        fin_x_arr_1=[]
        fin_y_arr_1=[]
        
        
        curdate=time.strftime("%Y-%m-%d")
        
        if request.method == 'POST':
            firer_id,sess,o,p,u,q,t1_x,t1_y,xmpi,ympi,f,gp,Tfirt_x,Tfirt_y,fin_x_1,fin_y_1,result_1,fir_tendency_1=prediction_calculation_5()
            paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
            
            
            set_2_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==5 ,T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_2_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==5 , T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_2 in set_2_x:
                set_2_x_arr.append(int(x_2.final_x))
                
            for y_2 in set_2_y:
                set_2_y_arr.append(int(y_2.final_y))
                
                
            set_3_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==5 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_3_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==5 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_3 in set_3_x:
                set_3_x_arr.append(int(x_3.final_x))
                
            for y_3 in set_3_y:
                set_3_y_arr.append(int(y_3.final_y))
                
                
                
            set_4_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==5 , T_Firer_Details.set_no==4 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_4_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==5 , T_Firer_Details.set_no==4 ,T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_4 in set_4_x:
                set_4_x_arr.append(int(x_4.final_x))
                
            for y_4 in set_4_y:
                set_4_y_arr.append(int(y_4.final_y))
                
            set_1_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref, 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            
            set_1_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_1_id
                                                        ).scalar()
            set_1_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_1_id).scalar()
            
            
            set_2_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_2_id
                                                        ).scalar()
            
            
            set_2_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_2_id).scalar()
            
            
            set_3_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_3_id
                                                        ).scalar()
            set_3_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_3_id).scalar()
            
            
            
            set_4_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==5, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_4_id
                                                        ).scalar()
            set_4_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_4_id).scalar()
            
            
            current_firer_name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
            current_army_no = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
            current_session_no=db.session.query(TShooting.session_id).filter(TShooting.target_1_id==firer_id).scalar()
            current_detail_no=db.session.query(TShooting.detail_no).filter(TShooting.target_1_id==firer_id).scalar()
            
            
            xmpi_inch = pixeltoinch(xmpi)
            ympi_inch = pixeltoinch(ympi)
            xmpi_j =pd.Series(xmpi_inch).to_json(orient='values')
            ympi_j =pd.Series(ympi_inch).to_json(orient='values')
            Tfirt_x_j =pd.Series(Tfirt_x).to_json(orient='values')
            Tfirt_y_j =pd.Series(Tfirt_y).to_json(orient='values')
            
            
            
            for x_1 in fin_x_1:
                fin_x_arr_1.append(int(x_1.final_x))
            for y_1 in fin_y_1 :
                fin_y_arr_1.append(int(y_1.final_y))
                
        return jsonify(x1=t1_x ,
                       y1=t1_y ,
                       xmpi1=Tfirt_x_j ,
                       ympi1=Tfirt_y_j,
                       gp=gp,
                       txf1=Tfirt_x_j,
                       tyf1=Tfirt_y_j,
                       fx1=fin_x_arr_1,
                       fy1=fin_y_arr_1,
                       result_1=result_1,
                       fir_tendency_1=fir_tendency_1,
                       set_1_name=set_1_name,
                       current_firer_name=current_firer_name,
                       set_1_army=set_1_army,
                       current_army_no=current_army_no,
                       set_1_session_no=set_1_session_no,
                       current_session_no=current_session_no,
                       set_1_detail_no=set_1_detail_no,
                       current_detail_no=current_detail_no,
                       set_2_x=set_2_x_arr,
                       set_2_y=set_2_y_arr,
                       set_2_name=set_2_name,
                       set_2_army=set_2_army,
                       set_2_detail_no=set_2_detail_no,
                       set_2_session_no=set_2_session_no,
                       set_3_x=set_3_x_arr,
                       set_3_y=set_3_y_arr,
                       set_3_name=set_3_name,
                       set_3_army=set_3_army,
                       set_3_session_no=set_3_session_no,
                       set_3_detail_no=set_3_detail_no,
                       set_4_x=set_4_x_arr,
                       set_4_y=set_4_y_arr,
                       set_4_name=set_4_name,
                       set_4_army=set_4_army,
                       set_4_session_no=set_4_session_no,
                       set_4_detail_no=set_4_detail_no
                       )
        
    @app.route('/prediction_target_6/', methods=['GET', 'POST'])
    def prediction_target_6():
        t1_x=0
        t1_y=0
        xmpi_j=0
        ympi_j=0
        gp=0
        Tfirt_x_j=0
        Tfirt_y_j=0
        fin_x_1=0
        fin_y_1=0
        xmpi_inch = 0
        ympi_inch = 0
        result_1=None
        fir_tendency=None
        set_1_name = None
        set_1_army =None
        set_1_session_no = None
        set_1_detail_no=None
        set_1_id =None
        
        set_2_name = None
        set_2_army =None
        set_2_session_no = None
        set_2_detail_no=None
        set_2_id =None
        
        set_3_name = None
        set_3_army =None
        set_3_session_no = None
        set_3_detail_no=None
        set_3_id =None
        
        set_4_name = None
        set_4_army =None
        set_4_session_no = None
        set_4_detail_no=None
        set_4_id =None
        
        fir_tendency_1=None
        firer_id=None
        current_army_no=None
        current_firer_name=None
        current_session_no=None
        session_detail_no=None
        current_detail_no=None
        
        set_2_x=None
        set_2_y=None
        set_3_x=None
        set_3_y=None
        
        set_4_x=None
        set_4_y=None
        paper_ref=None
        sess=None
        res=None
        set_2_x_arr=[]
        set_2_y_arr=[]
        
        set_3_x_arr=[]
        set_3_y_arr=[]
        
        set_4_x_arr=[]
        set_4_y_arr=[]
        
        fin_x_arr_1=[]
        fin_y_arr_1=[]
        
        
        curdate=time.strftime("%Y-%m-%d")
        
        if request.method == 'POST':
            firer_id,sess,o,p,u,q,t1_x,t1_y,xmpi,ympi,f,gp,Tfirt_x,Tfirt_y,fin_x_1,fin_y_1,result_1,fir_tendency_1=prediction_calculation_6()
            paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
            
            
            set_2_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==6 ,T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_2_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==6 , T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_2 in set_2_x:
                set_2_x_arr.append(int(x_2.final_x))
                
            for y_2 in set_2_y:
                set_2_y_arr.append(int(y_2.final_y))
                
                
            set_3_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==6 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_3_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==6 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_3 in set_3_x:
                set_3_x_arr.append(int(x_3.final_x))
                
            for y_3 in set_3_y:
                set_3_y_arr.append(int(y_3.final_y))
                
                
                
            set_4_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==6 , T_Firer_Details.set_no==4 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_4_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==6 , T_Firer_Details.set_no==4 ,T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_4 in set_4_x:
                set_4_x_arr.append(int(x_4.final_x))
                
            for y_4 in set_4_y:
                set_4_y_arr.append(int(y_4.final_y))
                
            set_1_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref, 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            
            set_1_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_1_id
                                                        ).scalar()
            set_1_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_1_id).scalar()
            
            
            set_2_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_2_id
                                                        ).scalar()
            
            
            set_2_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_2_id).scalar()
            
            
            set_3_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_3_id
                                                        ).scalar()
            set_3_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_3_id).scalar()
            
            
            
            set_4_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==6, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_4_id
                                                        ).scalar()
            set_4_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_4_id).scalar()
            
            
            current_firer_name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
            current_army_no = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
            current_session_no=db.session.query(TShooting.session_id).filter(TShooting.target_1_id==firer_id).scalar()
            current_detail_no=db.session.query(TShooting.detail_no).filter(TShooting.target_1_id==firer_id).scalar()
            
            
            xmpi_inch = pixeltoinch(xmpi)
            ympi_inch = pixeltoinch(ympi)
            xmpi_j =pd.Series(xmpi_inch).to_json(orient='values')
            ympi_j =pd.Series(ympi_inch).to_json(orient='values')
            Tfirt_x_j =pd.Series(Tfirt_x).to_json(orient='values')
            Tfirt_y_j =pd.Series(Tfirt_y).to_json(orient='values')
            
            
            
            for x_1 in fin_x_1:
                fin_x_arr_1.append(int(x_1.final_x))
            for y_1 in fin_y_1 :
                fin_y_arr_1.append(int(y_1.final_y))
                
        return jsonify(x1=t1_x ,
                       y1=t1_y ,
                       xmpi1=Tfirt_x_j ,
                       ympi1=Tfirt_y_j,
                       gp=gp,
                       txf1=Tfirt_x_j,
                       tyf1=Tfirt_y_j,
                       fx1=fin_x_arr_1,
                       fy1=fin_y_arr_1,
                       result_1=result_1,
                       fir_tendency_1=fir_tendency_1,
                       set_1_name=set_1_name,
                       current_firer_name=current_firer_name,
                       set_1_army=set_1_army,
                       current_army_no=current_army_no,
                       set_1_session_no=set_1_session_no,
                       current_session_no=current_session_no,
                       set_1_detail_no=set_1_detail_no,
                       current_detail_no=current_detail_no,
                       set_2_x=set_2_x_arr,
                       set_2_y=set_2_y_arr,
                       set_2_name=set_2_name,
                       set_2_army=set_2_army,
                       set_2_detail_no=set_2_detail_no,
                       set_2_session_no=set_2_session_no,
                       set_3_x=set_3_x_arr,
                       set_3_y=set_3_y_arr,
                       set_3_name=set_3_name,
                       set_3_army=set_3_army,
                       set_3_session_no=set_3_session_no,
                       set_3_detail_no=set_3_detail_no,
                       set_4_x=set_4_x_arr,
                       set_4_y=set_4_y_arr,
                       set_4_name=set_4_name,
                       set_4_army=set_4_army,
                       set_4_session_no=set_4_session_no,
                       set_4_detail_no=set_4_detail_no
                       )
    
    @app.route('/prediction_target_7/', methods=['GET', 'POST'])
    def prediction_target_7():
        t1_x=0
        t1_y=0
        xmpi_j=0
        ympi_j=0
        gp=0
        Tfirt_x_j=0
        Tfirt_y_j=0
        fin_x_1=0
        fin_y_1=0
        xmpi_inch = 0
        ympi_inch = 0
        result_1=None
        fir_tendency=None
        set_1_name = None
        set_1_army =None
        set_1_session_no = None
        set_1_detail_no=None
        set_1_id =None
        
        set_2_name = None
        set_2_army =None
        set_2_session_no = None
        set_2_detail_no=None
        set_2_id =None
        
        set_3_name = None
        set_3_army =None
        set_3_session_no = None
        set_3_detail_no=None
        set_3_id =None
        
        set_4_name = None
        set_4_army =None
        set_4_session_no = None
        set_4_detail_no=None
        set_4_id =None
        
        fir_tendency_1=None
        firer_id=None
        current_army_no=None
        current_firer_name=None
        current_session_no=None
        session_detail_no=None
        current_detail_no=None
        
        set_2_x=None
        set_2_y=None
        set_3_x=None
        set_3_y=None
        
        set_4_x=None
        set_4_y=None
        paper_ref=None
        sess=None
        res=None
        set_2_x_arr=[]
        set_2_y_arr=[]
        
        set_3_x_arr=[]
        set_3_y_arr=[]
        
        set_4_x_arr=[]
        set_4_y_arr=[]
        
        fin_x_arr_1=[]
        fin_y_arr_1=[]
        
        
        curdate=time.strftime("%Y-%m-%d")
        
        if request.method == 'POST':
            firer_id,sess,o,p,u,q,t1_x,t1_y,xmpi,ympi,f,gp,Tfirt_x,Tfirt_y,fin_x_1,fin_y_1,result_1,fir_tendency_1=prediction_calculation_7()
            paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
            
            
            set_2_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==7,T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_2_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==7 , T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_2 in set_2_x:
                set_2_x_arr.append(int(x_2.final_x))
                
            for y_2 in set_2_y:
                set_2_y_arr.append(int(y_2.final_y))
                
                
            set_3_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==7 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_3_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==7 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_3 in set_3_x:
                set_3_x_arr.append(int(x_3.final_x))
                
            for y_3 in set_3_y:
                set_3_y_arr.append(int(y_3.final_y))
                
                
                
            set_4_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==7 , T_Firer_Details.set_no==4 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_4_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==7 , T_Firer_Details.set_no==4 ,T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_4 in set_4_x:
                set_4_x_arr.append(int(x_4.final_x))
                
            for y_4 in set_4_y:
                set_4_y_arr.append(int(y_4.final_y))
                
            set_1_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref, 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            
            set_1_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_1_id
                                                        ).scalar()
            set_1_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_1_id).scalar()
            
            
            set_2_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_2_id
                                                        ).scalar()
            
            
            set_2_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_2_id).scalar()
            
            
            set_3_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_3_id
                                                        ).scalar()
            set_3_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_3_id).scalar()
            
            
            
            set_4_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==7, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_4_id
                                                        ).scalar()
            set_4_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_4_id).scalar()
            
            
            current_firer_name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
            current_army_no = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
            current_session_no=db.session.query(TShooting.session_id).filter(TShooting.target_1_id==firer_id).scalar()
            current_detail_no=db.session.query(TShooting.detail_no).filter(TShooting.target_1_id==firer_id).scalar()
            
            
            xmpi_inch = pixeltoinch(xmpi)
            ympi_inch = pixeltoinch(ympi)
            xmpi_j =pd.Series(xmpi_inch).to_json(orient='values')
            ympi_j =pd.Series(ympi_inch).to_json(orient='values')
            Tfirt_x_j =pd.Series(Tfirt_x).to_json(orient='values')
            Tfirt_y_j =pd.Series(Tfirt_y).to_json(orient='values')
            
            
            
            for x_1 in fin_x_1:
                fin_x_arr_1.append(int(x_1.final_x))
            for y_1 in fin_y_1 :
                fin_y_arr_1.append(int(y_1.final_y))
                
        return jsonify(x1=t1_x ,
                       y1=t1_y ,
                       xmpi1=Tfirt_x_j ,
                       ympi1=Tfirt_y_j,
                       gp=gp,
                       txf1=Tfirt_x_j,
                       tyf1=Tfirt_y_j,
                       fx1=fin_x_arr_1,
                       fy1=fin_y_arr_1,
                       result_1=result_1,
                       fir_tendency_1=fir_tendency_1,
                       set_1_name=set_1_name,
                       current_firer_name=current_firer_name,
                       set_1_army=set_1_army,
                       current_army_no=current_army_no,
                       set_1_session_no=set_1_session_no,
                       current_session_no=current_session_no,
                       set_1_detail_no=set_1_detail_no,
                       current_detail_no=current_detail_no,
                       set_2_x=set_2_x_arr,
                       set_2_y=set_2_y_arr,
                       set_2_name=set_2_name,
                       set_2_army=set_2_army,
                       set_2_detail_no=set_2_detail_no,
                       set_2_session_no=set_2_session_no,
                       set_3_x=set_3_x_arr,
                       set_3_y=set_3_y_arr,
                       set_3_name=set_3_name,
                       set_3_army=set_3_army,
                       set_3_session_no=set_3_session_no,
                       set_3_detail_no=set_3_detail_no,
                       set_4_x=set_4_x_arr,
                       set_4_y=set_4_y_arr,
                       set_4_name=set_4_name,
                       set_4_army=set_4_army,
                       set_4_session_no=set_4_session_no,
                       set_4_detail_no=set_4_detail_no
                       )
        
    @app.route('/prediction_target_8/', methods=['GET', 'POST'])
    def prediction_target_8():
        t1_x=0
        t1_y=0
        xmpi_j=0
        ympi_j=0
        gp=0
        Tfirt_x_j=0
        Tfirt_y_j=0
        fin_x_1=0
        fin_y_1=0
        xmpi_inch = 0
        ympi_inch = 0
        result_1=None
        fir_tendency=None
        set_1_name = None
        set_1_army =None
        set_1_session_no = None
        set_1_detail_no=None
        set_1_id =None
        
        set_2_name = None
        set_2_army =None
        set_2_session_no = None
        set_2_detail_no=None
        set_2_id =None
        
        set_3_name = None
        set_3_army =None
        set_3_session_no = None
        set_3_detail_no=None
        set_3_id =None
        
        set_4_name = None
        set_4_army =None
        set_4_session_no = None
        set_4_detail_no=None
        set_4_id =None
        
        fir_tendency_1=None
        firer_id=None
        current_army_no=None
        current_firer_name=None
        current_session_no=None
        session_detail_no=None
        current_detail_no=None
        
        set_2_x=None
        set_2_y=None
        set_3_x=None
        set_3_y=None
        
        set_4_x=None
        set_4_y=None
        paper_ref=None
        sess=None
        res=None
        set_2_x_arr=[]
        set_2_y_arr=[]
        
        set_3_x_arr=[]
        set_3_y_arr=[]
        
        set_4_x_arr=[]
        set_4_y_arr=[]
        
        
        fin_x_arr_1=[]
        fin_y_arr_1=[]
        
        
        curdate=time.strftime("%Y-%m-%d")
        
        if request.method == 'POST':
            firer_id,sess,o,p,u,q,t1_x,t1_y,xmpi,ympi,f,gp,Tfirt_x,Tfirt_y,fin_x_1,fin_y_1,result_1,fir_tendency_1=prediction_calculation_8()
            paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
            
            
            set_2_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==8,T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_2_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==8 , T_Firer_Details.set_no==2 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_2 in set_2_x:
                set_2_x_arr.append(int(x_2.final_x))
                
            for y_2 in set_2_y:
                set_2_y_arr.append(int(y_2.final_y))
                
                
            set_3_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==8 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_3_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==8 , T_Firer_Details.set_no==3 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_3 in set_3_x:
                set_3_x_arr.append(int(x_3.final_x))
                
            for y_3 in set_3_y:
                set_3_y_arr.append(int(y_3.final_y))
                
                
                
            set_4_x=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==8 , T_Firer_Details.set_no==4 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            set_4_y=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==8 , T_Firer_Details.set_no==4 ,T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess).all()
            
            for x_4 in set_4_x:
                set_4_x_arr.append(int(x_4.final_x))
                
            for y_4 in set_4_y:
                set_4_y_arr.append(int(y_4.final_y))
                
            set_1_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref, 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            
            set_1_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==1,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_1_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_1_id
                                                        ).scalar()
            set_1_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_1_id).scalar()
            
            
            set_2_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==2,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_2_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_2_id
                                                        ).scalar()
            
            
            set_2_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_2_id).scalar()
            
            
            set_3_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==3,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_3_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_3_id
                                                        ).scalar()
            set_3_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_3_id).scalar()
            
            
            
            set_4_id = db.session.query(T_Firer_Details.firer_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_session_no=db.session.query(T_Firer_Details.session_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_detail_no=db.session.query(T_Firer_Details.detail_id).filter(T_Firer_Details.date==curdate, 
                                      T_Firer_Details.target_no==8, 
                                      T_Firer_Details.set_no==4,
                                      T_Firer_Details.paper_ref==paper_ref , 
                                      T_Firer_Details.session_id==sess                                                             
                                      ).distinct().scalar()
            
            set_4_name=db.session.query(Shooter.name).filter(
                                                        Shooter.id==set_4_id
                                                        ).scalar()
            set_4_army=db.session.query(Shooter.service_id).filter(Shooter.id==set_4_id).scalar()
            
            
            current_firer_name = db.session.query(Shooter.name).filter(Shooter.id==firer_id).scalar()
            current_army_no = db.session.query(Shooter.service_id).filter(Shooter.id==firer_id).scalar()
            current_session_no=db.session.query(TShooting.session_id).filter(TShooting.target_1_id==firer_id).scalar()
            current_detail_no=db.session.query(TShooting.detail_no).filter(TShooting.target_1_id==firer_id).scalar()
            
            
            xmpi_inch = pixeltoinch(xmpi)
            ympi_inch = pixeltoinch(ympi)
            xmpi_j =pd.Series(xmpi_inch).to_json(orient='values')
            ympi_j =pd.Series(ympi_inch).to_json(orient='values')
            Tfirt_x_j =pd.Series(Tfirt_x).to_json(orient='values')
            Tfirt_y_j =pd.Series(Tfirt_y).to_json(orient='values')
            
            
            
            for x_1 in fin_x_1:
                fin_x_arr_1.append(int(x_1.final_x))
            for y_1 in fin_y_1 :
                fin_y_arr_1.append(int(y_1.final_y))
                
        return jsonify(x1=t1_x ,
                       y1=t1_y ,
                       xmpi1=Tfirt_x_j ,
                       ympi1=Tfirt_y_j,
                       gp=gp,
                       txf1=Tfirt_x_j,
                       tyf1=Tfirt_y_j,
                       fx1=fin_x_arr_1,
                       fy1=fin_y_arr_1,
                       result_1=result_1,
                       fir_tendency_1=fir_tendency_1,
                       set_1_name=set_1_name,
                       current_firer_name=current_firer_name,
                       set_1_army=set_1_army,
                       current_army_no=current_army_no,
                       set_1_session_no=set_1_session_no,
                       current_session_no=current_session_no,
                       set_1_detail_no=set_1_detail_no,
                       current_detail_no=current_detail_no,
                       set_2_x=set_2_x_arr,
                       set_2_y=set_2_y_arr,
                       set_2_name=set_2_name,
                       set_2_army=set_2_army,
                       set_2_detail_no=set_2_detail_no,
                       set_2_session_no=set_2_session_no,
                       set_3_x=set_3_x_arr,
                       set_3_y=set_3_y_arr,
                       set_3_name=set_3_name,
                       set_3_army=set_3_army,
                       set_3_session_no=set_3_session_no,
                       set_3_detail_no=set_3_detail_no,
                       set_4_x=set_4_x_arr,
                       set_4_y=set_4_y_arr,
                       set_4_name=set_4_name,
                       set_4_army=set_4_army,
                       set_4_session_no=set_4_session_no,
                       set_4_detail_no=set_4_detail_no
                       )
    @app.route('/previous_page_target_1/', methods=['GET', 'POST'])
    def previous_page_target_1():
        T1_name = db.session.query(Shooter.name).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_service =  db.session.query(Shooter.service_id).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_r_id =  db.session.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_1_id).scalar()
        T1_rank =  db.session.query(Rank.name).filter(Rank.id==T1_r_id).scalar()
        
        T2_name =  db.session.query(Shooter.name).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_service =  db.session.query(Shooter.service_id).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_r_id =  db.session.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_2_id).scalar()
        T2_rank =  db.session.query(Rank.name).filter(Rank.id==T2_r_id).scalar()
        
        
        
        T3_name =  db.session.query(Shooter.name).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_service = db.session.query(Shooter.service_id).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_r_id =  db.session.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_3_id).scalar()
        T3_rank =  db.session.query(Rank.name).filter(Rank.id==T3_r_id).scalar()
        
        T4_name =  db.session.query(Shooter.name).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_service =  db.session.query(Shooter.service_id).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_r_id =  db.session.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_4_id).scalar()
        T4_rank = db.session.query(Rank.name).filter(Rank.id==T4_r_id).scalar()
        
        print(T1_rank)
        print(T2_rank)
        print(T3_rank)
        print(T4_rank)
        return render_template('pages/previous_page_target_1.html' ,
                               T1_name=T1_name,
                               T1_service=T1_service,
                               T2_name=T2_name,
                               T2_service=T2_service,
                               T3_name=T3_name,
                               T3_service=T3_service,
                               T4_name=T4_name,
                               T4_service=T4_service,
                               T4_rank=T4_rank,
                               T1_rank=T1_rank,
                               T2_rank=T2_rank,
                               T3_rank=T3_rank
                               
                               )
        
    @app.route('/previous_page_target_5/', methods=['GET', 'POST'])
    def previous_page_target_5():
        T5_name = db.session.query(Shooter.name).filter(Shooter.id==TShooting.target_5_id).scalar()
        T5_service = db.session.query(Shooter.service_id).filter(Shooter.id==TShooting.target_5_id).scalar()
        T5_r_id = db.session.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_5_id).scalar()
        T5_rank = db.session.query(Rank.name).filter(Rank.id==T5_r_id).scalar()
        
        T6_name = db.session.query(Shooter.name).filter(Shooter.id==TShooting.target_6_id).scalar()
        T6_service = db.session.query(Shooter.service_id).filter(Shooter.id==TShooting.target_6_id).scalar()
        T6_r_id = db.session.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_6_id).scalar()
        T6_rank = db.session.query(Rank.name).filter(Rank.id==T6_r_id).scalar()
        
        T7_name = db.session.query(Shooter.name).filter(Shooter.id==TShooting.target_7_id).scalar()
        T7_service = db.session.query(Shooter.service_id).filter(Shooter.id==TShooting.target_7_id).scalar()
        T7_r_id = db.session.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_7_id).scalar()
        T7_rank = db.session.query(Rank.name).filter(Rank.id==T7_r_id).scalar()
        
        T8_name = db.session.query(Shooter.name).filter(Shooter.id==TShooting.target_8_id).scalar()
        T8_service = db.session.query(Shooter.service_id).filter(Shooter.id==TShooting.target_8_id).scalar()
        T8_r_id = db.session.query(Shooter.rank_id).filter(Shooter.id==TShooting.target_8_id).scalar()
        T8_rank = db.session.query(Rank.name).filter(Rank.id==T8_r_id).scalar()
        
        return render_template('pages/previous_page_target_5.html' ,
                               T5_name=T5_name,
                               T5_service=T5_service,
                               T6_name=T6_name,
                               T6_service=T6_service,
                               T7_name=T7_name,
                               T7_service=T7_service,
                               T8_name=T8_name,
                               T8_service=T8_service,
                               T5_rank=T5_rank,
                               T6_rank=T6_rank,
                               T7_rank=T7_rank,
                               T8_rank=T8_rank
                               
                               )
        
    
    
    def prediction_calculation_1():
        curdate=time.strftime("%Y-%m-%d")
        X_json=0
        Y_json=0
        firer_id =db.session.query(TShooting.target_1_id).scalar()
        sess_id = db.session.query(TShooting.session_id).scalar()
        detail_id = db.session.query(TShooting.detail_no).scalar()
        target_no=1
        paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
        print(paper_ref )
        data_x_1=db.session.query(Firer_Details).filter(Firer_Details.date==curdate , Firer_Details.target_no==1 , Firer_Details.set_no==1 , Firer_Details.paper_ref==paper_ref , Firer_Details.session_id==sess_id).all()
        data_y_1=db.session.query(Firer_Details).filter(Firer_Details.date==curdate , Firer_Details.target_no==1 , Firer_Details.set_no==1 , Firer_Details.paper_ref==paper_ref , Firer_Details.session_id==sess_id).all()
        print(data_x_1)
        set_no=db.session.query(TShooting.set_no).scalar()
        paper_ref=db.session.query(TShooting.paper_ref).scalar()
        print('Old x')
        print(data_x_1)
        image=Image.open('E:/FRAS Windows/FRAS_production/static/img_dump/1.png')
        #image=Image.open('/Users/wasifaahmed/Documents/FRAS/Fras_production_v.0.1/FRAS Windows/FRAS Windows/FRAS_production/static/img_dump/1.png')
        w,h = image.size
        predictedMatrix = predictAsMatrix(image,w,h)
        g= Graph(80, 80, predictedMatrix)
        N=g.countIslands()
        points(predictedMatrix,h=80,w=80)
        centroids=kmean(N,pointsarray)
        print(centroids)
        if(centroids is None):
            x=0,
            y=0,
            mpit=0
            xmpi1=0
            ympi1=0
            f1=0,
            firt_x=0
            firt_y=0
            fir_tendency_code=""
            fir_tendency_txt=""
            gp_1=""
            result_1=""
        else:
            x= centroids [:, 1]
            y= 2000-centroids [:, 0]
            X_json=pd.Series(x).to_json(orient='values')
            Y_json = pd.Series(y).to_json(orient='values')
            mpit=mpi(1,centroids)
            xmpi1 = mpit [:, 1]
            ympi1 = 2000-mpit [:, 0]
            f1 ,firt_x,firt_y= firing_tendancy(1000, 1000 , xmpi1, ympi1)
            fir_tendency_txt,fir_tendency_code = getfiringtendencytext(f1 ,firt_x,firt_y)
            gp_1 = grouping_length(0 , 0 , x , y)
            result_1 =getresulttext(gp_1)
        return (firer_id,
                sess_id,
                detail_id,
                target_no,
                set_no,
                paper_ref,
                X_json,
                Y_json,
                xmpi1,
                ympi1,
                f1,
                gp_1,
                firt_x,
                firt_y,
                data_x_1,
                data_y_1,
                result_1,
                fir_tendency_txt
                
                )
   
    
    def prediction_calculation_2():
        curdate=time.strftime("%Y-%m-%d")
        X_json=0
        Y_json=0
        firer_id =db.session.query(TShooting.target_2_id).scalar()
        sess_id = db.session.query(TShooting.session_id).scalar()
        detail_id = db.session.query(TShooting.detail_no).scalar()
        target_no=2
        paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
        print(paper_ref )
        data_x_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==2 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        data_y_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==2 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        print(data_x_1)
        set_no=db.session.query(TShooting.set_no).scalar()
        paper_ref=db.session.query(TShooting.paper_ref).scalar()
        print('Old x' )
        print(data_x_1)
        image=Image.open('E:/FRAS Windows/FRAS_production/static/img_dump/2.png')
        w,h = image.size
        predictedMatrix = predictAsMatrix(image,w,h)
        g= Graph(80, 80, predictedMatrix)
        N=g.countIslands()
        points(predictedMatrix,h=80,w=80)
        centroids=kmean(N,pointsarray)
        if(centroids is None):
            x=0,
            y=0,
            mpit=0
            xmpi1=0
            ympi1=0
            f1=0,
            firt_x=0
            firt_y=0
            fir_tendency_code=""
            fir_tendency_txt=""
            gp_1=""
            result_1=""
        else:
            x= centroids [:, 1]
            y= 2000-centroids [:, 0]
            X_json=pd.Series(x).to_json(orient='values')
            Y_json = pd.Series(y).to_json(orient='values')
            mpit=mpi(1,centroids)
            xmpi1 = mpit [:, 1]
            ympi1 = 2000-mpit [:, 0]
            f1 ,firt_x,firt_y= firing_tendancy(1000, 1000 , xmpi1, ympi1)
            fir_tendency_txt,fir_tendency_code = getfiringtendencytext(f1 ,firt_x,firt_y)
            gp_1 = grouping_length(0 , 0 , x , y)
            result_1 =getresulttext(gp_1)
        return (firer_id,
                sess_id,
                detail_id,
                target_no,
                set_no,
                paper_ref,
                X_json,
                Y_json,
                xmpi1,
                ympi1,
                f1,
                gp_1,
                firt_x,
                firt_y,
                data_x_1,
                data_y_1,
                result_1,
                fir_tendency_txt
                
                )
        
    def prediction_calculation_3():
        X_json=0
        Y_json=0
        curdate=time.strftime("%Y-%m-%d")
        firer_id =db.session.query(TShooting.target_3_id).scalar()
        sess_id = db.session.query(TShooting.session_id).scalar()
        detail_id = db.session.query(TShooting.detail_no).scalar()
        target_no=3
        paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
        print(paper_ref)
        data_x_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==3 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        data_y_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==3 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        print(data_x_1)
        set_no=db.session.query(TShooting.set_no).scalar()
        paper_ref=db.session.query(TShooting.paper_ref).scalar()
        print('Old x' )
        print(data_x_1)
        image=Image.open('E:/FRAS Windows/FRAS_production/static/img_dump/3.png')
        w,h = image.size
        predictedMatrix = predictAsMatrix(image,w,h)
        g= Graph(80, 80, predictedMatrix)
        N=g.countIslands()
        points(predictedMatrix,h=80,w=80)
        centroids=kmean(N,pointsarray)
        if(centroids is None):
            x=0,
            y=0,
            mpit=0
            xmpi1=0
            ympi1=0
            f1=0,
            firt_x=0
            firt_y=0
            fir_tendency_code=""
            fir_tendency_txt=""
            gp_1=""
            result_1=""
            
        else:
            x= centroids [:, 1]
            y= 2000-centroids [:, 0]
            X_json=pd.Series(x).to_json(orient='values')
            Y_json = pd.Series(y).to_json(orient='values')
            mpit=mpi(1,centroids)
            xmpi1 = mpit [:, 1]
            ympi1 = 2000-mpit [:, 0]
            f1 ,firt_x,firt_y= firing_tendancy(1000, 1000 , xmpi1, ympi1)
            fir_tendency_txt,fir_tendency_code = getfiringtendencytext(f1 ,firt_x,firt_y)
            print("calling from prediction_calculation_1" )
            gp_1 = grouping_length(0 , 0 , x , y)
            result_1 =getresulttext(gp_1)
        return (firer_id,
                sess_id,
                detail_id,
                target_no,
                set_no,
                paper_ref,
                X_json,
                Y_json,
                xmpi1,
                ympi1,
                f1,
                gp_1,
                firt_x,
                firt_y,
                data_x_1,
                data_y_1,
                result_1,
                fir_tendency_txt
                
                )
        
        
    def prediction_calculation_4():
        curdate=time.strftime("%Y-%m-%d")
        firer_id =db.session.query(TShooting.target_4_id).scalar()
        sess_id = db.session.query(TShooting.session_id).scalar()
        detail_id = db.session.query(TShooting.detail_no).scalar()
        target_no=4
        paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
        print(paper_ref )
        data_x_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==4 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        data_y_1=db.session.query(T_Firer_Details.final_y).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==4 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        print(data_x_1)
        set_no=db.session.query(TShooting.set_no).scalar()
        paper_ref=db.session.query(TShooting.paper_ref).scalar()
        print('Old x' )
        print(data_x_1)
        image=Image.open('E:/FRAS Windows/FRAS_production/static/img_dump/4.png')
        w,h = image.size
        predictedMatrix = predictAsMatrix(image,w,h)
        g= Graph(80, 80, predictedMatrix)
        N=g.countIslands()
        points(predictedMatrix,h=80,w=80)
        centroids=kmean(N,pointsarray)
        if(centroids is None):
            x=0,
            y=0,
            mpit=0
            xmpi1=0
            ympi1=0
            f1=0,
            firt_x=0
            firt_y=0
            fir_tendency_code=""
            fir_tendency_txt=""
            gp_1=""
            result_1=""
            
        else:
            x= centroids [:, 1]
            y= 2000-centroids [:, 0]
            X_json=pd.Series(x).to_json(orient='values')
            Y_json = pd.Series(y).to_json(orient='values')
            mpit=mpi(1,centroids)
            xmpi1 = mpit [:, 1]
            ympi1 = 2000-mpit [:, 0]
            f1 ,firt_x,firt_y= firing_tendancy(1000, 1000 , xmpi1, ympi1)
            fir_tendency_txt,fir_tendency_code = getfiringtendencytext(f1 ,firt_x,firt_y)
            print("calling from prediction_calculation_1" )
            gp_1 = grouping_length(0 , 0 , x , y)
            result_1 =getresulttext(gp_1)
        return (firer_id,
                sess_id,
                detail_id,
                target_no,
                set_no,
                paper_ref,
                X_json,
                Y_json,
                xmpi1,
                ympi1,
                f1,
                gp_1,
                firt_x,
                firt_y,
                data_x_1,
                data_y_1,
                result_1,
                fir_tendency_txt
                
                )
        
        
    def prediction_calculation_5():
        curdate=time.strftime("%Y-%m-%d")
        firer_id =db.session.query(TShooting.target_5_id).scalar()
        sess_id = db.session.query(TShooting.session_id).scalar()
        detail_id = db.session.query(TShooting.detail_no).scalar()
        target_no=5
        paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
        print(paper_ref)
        data_x_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==5 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        data_y_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==5 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        print(data_x_1)
        set_no=db.session.query(TShooting.set_no).scalar()
        paper_ref=db.session.query(TShooting.paper_ref).scalar()
        print('Old x' )
        print(data_x_1)
        image=Image.open('E:/FRAS Windows/FRAS_production/static/img_dump/5.png')
        w,h = image.size
        predictedMatrix = predictAsMatrix(image,w,h)
        g= Graph(80, 80, predictedMatrix)
        N=g.countIslands()
        points(predictedMatrix,h=80,w=80)
        centroids=kmean(N,pointsarray)
        if(centroids is None):
            x=0,
            y=0,
            mpit=0
            xmpi1=0
            ympi1=0
            f1=0,
            firt_x=0
            firt_y=0
            fir_tendency_code=""
            fir_tendency_txt=""
            gp_1=""
            result_1=""
        else:
            x= centroids [:, 1]
            y= 2000-centroids [:, 0]
            X_json=pd.Series(x).to_json(orient='values')
            Y_json = pd.Series(y).to_json(orient='values')
            mpit=mpi(1,centroids)
            xmpi1 = mpit [:, 1]
            ympi1 = 2000-mpit [:, 0]
            f1 ,firt_x,firt_y= firing_tendancy(1000, 1000 , xmpi1, ympi1)
            fir_tendency_txt,fir_tendency_code = getfiringtendencytext(f1 ,firt_x,firt_y)
            print("calling from prediction_calculation_1" )
            gp_1 = grouping_length(0 , 0 , x , y)
            result_1 =getresulttext(gp_1)
        return (firer_id,
                sess_id,
                detail_id,
                target_no,
                set_no,
                paper_ref,
                X_json,
                Y_json,
                xmpi1,
                ympi1,
                f1,
                gp_1,
                firt_x,
                firt_y,
                data_x_1,
                data_y_1,
                result_1,
                fir_tendency_txt
                
                )
    
    def prediction_calculation_6():
        curdate=time.strftime("%Y-%m-%d")
        firer_id =db.session.query(TShooting.target_6_id).scalar()
        sess_id = db.session.query(TShooting.session_id).scalar()
        detail_id = db.session.query(TShooting.detail_no).scalar()
        target_no=6
        paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
        print(paper_ref)
        data_x_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==6 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        data_y_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==6 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        print(data_x_1)
        set_no=db.session.query(TShooting.set_no).scalar()
        paper_ref=db.session.query(TShooting.paper_ref).scalar()
        print('Old x' )
        print(data_x_1)
        image=Image.open('E:/FRAS Windows/FRAS_production/static/img_dump/6.png')
        w,h = image.size
        predictedMatrix = predictAsMatrix(image,w,h)
        g= Graph(80, 80, predictedMatrix)
        N=g.countIslands()
        points(predictedMatrix,h=80,w=80)
        centroids=kmean(N,pointsarray)
        if(centroids is None):
            x=0,
            y=0,
            mpit=0
            xmpi1=0
            ympi1=0
            f1=0,
            firt_x=0
            firt_y=0
            fir_tendency_code=""
            fir_tendency_txt=""
            gp_1=""
            result_1=""
        else:
            x= centroids [:, 1]
            y= 2000-centroids [:, 0]
            X_json=pd.Series(x).to_json(orient='values')
            Y_json = pd.Series(y).to_json(orient='values')
            mpit=mpi(1,centroids)
            xmpi1 = mpit [:, 1]
            ympi1 = 2000-mpit [:, 0]
            f1 ,firt_x,firt_y= firing_tendancy(1000, 1000 , xmpi1, ympi1)
            fir_tendency_txt,fir_tendency_code = getfiringtendencytext(f1 ,firt_x,firt_y)
            print("calling from prediction_calculation_1" )
            gp_1 = grouping_length(0 , 0 , x , y)
            result_1 =getresulttext(gp_1)
        return (firer_id,
                sess_id,
                detail_id,
                target_no,
                set_no,
                paper_ref,
                X_json,
                Y_json,
                xmpi1,
                ympi1,
                f1,
                gp_1,
                firt_x,
                firt_y,
                data_x_1,
                data_y_1,
                result_1,
                fir_tendency_txt
                
                )
        
        
    def prediction_calculation_7():
        curdate=time.strftime("%Y-%m-%d")
        firer_id =db.session.query(TShooting.target_7_id).scalar()
        sess_id = db.session.query(TShooting.session_id).scalar()
        detail_id = db.session.query(TShooting.detail_no).scalar()
        target_no=7
        paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
        print(paper_ref)
        data_x_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==7 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        data_y_1=db.session.query(T_Firer_Details.final_y).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==7 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        print(data_x_1)
        set_no=db.session.query(TShooting.set_no).scalar()
        paper_ref=db.session.query(TShooting.paper_ref).scalar()
        print('Old x' )
        print(data_x_1)
        image=Image.open('E:/FRAS Windows/FRAS_production/static/img_dump/7.png')
        w,h = image.size
        predictedMatrix = predictAsMatrix(image,w,h)
        g= Graph(80, 80, predictedMatrix)
        N=g.countIslands()
        points(predictedMatrix,h=80,w=80)
        centroids=kmean(N,pointsarray)
        if(centroids is None):
            x=0,
            y=0,
            mpit=0
            xmpi1=0
            ympi1=0
            f1=0,
            firt_x=0
            firt_y=0
            fir_tendency_code=""
            fir_tendency_txt=""
            gp_1=""
            result_1=""
        else:
            x= centroids [:, 1]
            y= 2000-centroids [:, 0]
            X_json=pd.Series(x).to_json(orient='values')
            Y_json = pd.Series(y).to_json(orient='values')
            mpit=mpi(1,centroids)
            xmpi1 = mpit [:, 1]
            ympi1 = 2000-mpit [:, 0]
            f1 ,firt_x,firt_y= firing_tendancy(1000, 1000 , xmpi1, ympi1)
            fir_tendency_txt,fir_tendency_code = getfiringtendencytext(f1 ,firt_x,firt_y)
            print("calling from prediction_calculation_1" )
            gp_1 = grouping_length(0 , 0 , x , y)
            result_1 =getresulttext(gp_1)
        return (firer_id,
                sess_id,
                detail_id,
                target_no,
                set_no,
                paper_ref,
                X_json,
                Y_json,
                xmpi1,
                ympi1,
                f1,
                gp_1,
                firt_x,
                firt_y,
                data_x_1,
                data_y_1,
                result_1,
                fir_tendency_txt
                
                )   
    def prediction_calculation_8():
        session.clear()
        curdate=time.strftime("%Y-%m-%d")
        firer_id =db.session.query(TShooting.target_8_id).scalar()
        sess_id = db.session.query(TShooting.session_id).scalar()
        detail_id = db.session.query(TShooting.detail_no).scalar()
        target_no=8
        paper_ref=db.session.query(TPaper_ref.paper_ref).scalar()
        print(paper_ref)
        data_x_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==8 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        data_y_1=db.session.query(T_Firer_Details).filter(T_Firer_Details.date==curdate , T_Firer_Details.target_no==8 , T_Firer_Details.set_no==1 , T_Firer_Details.paper_ref==paper_ref , T_Firer_Details.session_id==sess_id).all()
        print(data_x_1)
        set_no=db.session.query(TShooting.set_no).scalar()
        paper_ref=db.session.query(TShooting.paper_ref).scalar()
        print('Old x' )
        print(data_x_1)
        image=Image.open('E:/FRAS Windows/FRAS_production/static/img_dump/8.png')
        w,h = image.size
        predictedMatrix = predictAsMatrix(image,w,h)
        g= Graph(80, 80, predictedMatrix)
        N=g.countIslands()
        points(predictedMatrix,h=80,w=80)
        centroids=kmean(N,pointsarray)
        if(centroids is None):
            x=0,
            y=0,
            mpit=0
            xmpi1=0
            ympi1=0
            f1=0,
            firt_x=0
            firt_y=0
            fir_tendency_code=""
            fir_tendency_txt=""
            gp_1=""
            result_1=""
        else:
            x= centroids [:, 1]
            y= 2000-centroids [:, 0]
            X_json=pd.Series(x).to_json(orient='values')
            Y_json = pd.Series(y).to_json(orient='values')
            mpit=mpi(1,centroids)
            xmpi1 = mpit [:, 1]
            ympi1 = 2000-mpit [:, 0]
            f1 ,firt_x,firt_y= firing_tendancy(1000, 1000 , xmpi1, ympi1)
            fir_tendency_txt,fir_tendency_code = getfiringtendencytext(f1 ,firt_x,firt_y)
            print("calling from prediction_calculation_1" )
            gp_1 = grouping_length(0 , 0 , x , y)
            result_1 =getresulttext(gp_1)
        return (firer_id,
                sess_id,
                detail_id,
                target_no,
                set_no,
                paper_ref,
                X_json,
                Y_json,
                xmpi1,
                ympi1,
                f1,
                gp_1,
                firt_x,
                firt_y,
                data_x_1,
                data_y_1,
                result_1,
                fir_tendency_txt
                
                )
    
    @app.route('/save_adhoc_1/', methods=['GET', 'POST'])
    def save_adhoc_1():
        return redirect(url_for('previous_page_target_1'))
    
    
    
    @app.route('/save_1/', methods=['GET', 'POST'])
    def save_call_1():
            print("this is save_call_1",file=sys.stderr)
            final_x=[]
            final_y=[]
            tend_f_x_t = None
            tend_f_y_t = None
            x_list=None
            y_list=None
            if request.method == 'POST':
                curr_date=date.today()
                firer_id,session_id,detail_no,target_no,set_no,paper_no,x,y,mx1,my1,tendency,grouping_length,firt_x,firt_y,o,p,result,f=prediction_calculation_1()           
                t1= session.get('tmpi',None)
                Tupdate=db.session.query(TShooting).scalar()
                if(Tupdate.save_flag==1):
                    return render_template('errors/error_save.html')
                else:
              
                    print("t1",file=sys.stderr)
                    print(t1,file=sys.stderr)
                    print(f,file=sys.stderr)
                    if(t1 is None):
                        f_mpix_1=0
                    else:
                        f_mpix_1 = t1[ : 1 ] 
                        f_mpiy_1=t1[ : 0 ]
                    final_x_1  = session.get('x1', None)
                    final_y_1  = session.get('y1', None)
                    print(session.get('x1'),file=sys.stderr)
                    print("final_x_1",file=sys.stderr)
                    print(final_x_1,file=sys.stderr)
                    gp_1_f=session.get('gp_u_1', None)
                    res_u_1=session.get('res_u_1',None)
                    tend_f = session.get('tf_u_1', None)
                    tend_f_x = session.get('tfirer_x1', None)
                    tend_f_y = session.get('tfirer_y1', None)
                    tend_f_x_1 = session.get('tfirer_x1_f', None)
                    tend_f_y_1 = session.get('tfirer_y1_f', None)
                    if (x==0):
                        x=0
                        y=0
                    else:        
                        x_len=len(x)
                        y_len=len(y)
                        x_ss=x[1:x_len-1]
                        y_ss=y[1:y_len-1]
                        x_split = x_ss.split(",")
                        y_split = y_ss.split(",")
                        x_list=[]
                        y_list=[]
                        for x_t in x_split:
                            x_list.append(float(x_t))
                            
                        for y_t in y_split:
                            y_list.append(float(y_t))
                            
           
                    print(final_x_1,file=sys.stderr)
                    box = savein_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,x_list,y_list,final_x_1,final_y_1)
                    mpi=savempi_db(detail_no,target_no,paper_no,firer_id,firt_x,firt_y,tendency,session_id,set_no,tend_f,tend_f_x ,tend_f_y,tend_f_x_1,tend_f_y_1,f)
                    gp=savegp_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,grouping_length,gp_1_f,res_u_1,result)
                    Tupdate.save_flag=1
                    db.session.commit()
                    Supdate=db.session.query(Session_Detail).filter(
                                            Session_Detail.session_id==session_id,
                                            Session_Detail.detail_no==detail_no
                                            ).scalar()
                    Supdate.save_flag=1
                    print(Supdate)
                    db.session.commit()
                    image_save=save_image_1(firer_id)
                    image = image_record(
                                date=time.strftime("%Y-%m-%d"),
                                datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                                session_id=session_id,
                                detail_id=detail_no,
                                firer_id=firer_id,
                                target_no=target_no,
                                set_no=set_no,
                                paper_ref=paper_no,
                                image_name=image_save
                                )
                    db.session.add(image)
                    db.session.commit()
                    
            return redirect(url_for('previous_page_target_1'))
    
    @app.route('/save_2/', methods=['GET', 'POST'])
    def save_call_2():
        final_x_1=[]
        final_y_1=[]
        x_list=None
        y_list=None
        tend_f_x_t = None
        tend_f_y_t = None
        if request.method == 'POST':
            firer_id,session_id,detail_no,target_no,set_no,paper_no,x,y,mx1,my1,tendency,grouping_length,firt_x,firt_y,o,p,result,f=prediction_calculation_2()           
            t1= session.get('tmpi_2',None)
            f_mpix_1 = t1[ : 1 ] 
            f_mpiy_1=t1[ : 0 ]
            final_x_1  = session.get('x2', None)
            final_y_1  = session.get('y2', None)
            gp_1_f=session.get('gp_u_2', None)
            res_u_1=session.get('res_u_2',None)
            tend_f = session.get('tf_u_2', None)
            tend_f_x = session.get('tfirer_x2', None)
            tend_f_y = session.get('tfirer_y2', None)
            tend_f_x_1 = session.get('tfirer_x1_f', None)
            tend_f_y_1 = session.get('tfirer_y1_f', None)
            if (x==0):
                x=0
                y=0
            else:
                x_len=len(x)
                y_len=len(y)
                x_ss=x[1:x_len-1]
                y_ss=y[1:y_len-1]
                x_split = x_ss.split(",")
                y_split = y_ss.split(",")
                x_list=[]
                y_list=[]
                for x_t in x_split:
                    x_list.append(float(x_t))
                    
                for y_t in y_split:
                    y_list.append(float(y_t))
            
            print(x_list,file=sys.stderr)
            box = savein_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,x_list,y_list,final_x_1,final_y_1)
            mpi=savempi_db(detail_no,target_no,paper_no,firer_id,firt_x,firt_y,tendency,session_id,set_no,tend_f,tend_f_x ,tend_f_y,tend_f_x_1,tend_f_y_1)
            gp=savegp_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,grouping_length,gp_1_f,res_u_1)
            image_save=save_image_2(firer_id)
            image = image_record(
                        date=time.strftime("%x"),
                        datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                        session_id=session_id,
                        detail_id=detail_no,
                        firer_id=firer_id,
                        target_no=target_no,
                        set_no=set_no,
                        paper_ref=paper_no,
                        image_name=image_save
                        )
            db.session.add(image)
            db.session.commit()
                
        return redirect(url_for('previous_page_target_1'))
    
    @app.route('/save_3/', methods=['GET', 'POST'])
    def save_call_3():
        final_x_1=[]
        final_y_1=[]
        x_list=None
        y_list=None
        tend_f_x_t = None
        tend_f_y_t = None
        
        if request.method == 'POST':
            firer_id,session_id,detail_no,target_no,set_no,paper_no,x,y,mx1,my1,tendency,grouping_length,firt_x,firt_y,o,p,result,f=prediction_calculation_3()           
            t1= session.get('tmpi_2',None)
            f_mpix_1 = t1[ : 1 ] 
            f_mpiy_1=t1[ : 0 ]
            final_x_1  = session.get('x2', None)
            final_y_1  = session.get('y2', None)
            gp_1_f=session.get('gp_u_2', None)
            res_u_1=session.get('res_u_2',None)
            tend_f = session.get('tf_u_2', None)
            tend_f_x = session.get('tfirer_x2', None)
            tend_f_y = session.get('tfirer_y2', None)
            tend_f_x_1 = session.get('tfirer_x1_f', None)
            tend_f_y_1 = session.get('tfirer_y1_f', None)
            if (x==0):
                x=0
                y=0
            else:
                x_len=len(x)
                y_len=len(y)
                x_ss=x[1:x_len-1]
                y_ss=y[1:y_len-1]
                x_split = x_ss.split(",")
                y_split = y_ss.split(",")
                x_list=[]
                y_list=[]
                for x_t in x_split:
                    x_list.append(float(x_t))
                    
                for y_t in y_split:
                    y_list.append(float(y_t))
            
            print(x_list,file=sys.stderr)
            box = savein_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,x_list,y_list,final_x_1,final_y_1)
            mpi=savempi_db(detail_no,target_no,paper_no,firer_id,firt_x,firt_y,tendency,session_id,set_no,tend_f,tend_f_x ,tend_f_y,tend_f_x_1,tend_f_y_1)
            gp=savegp_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,grouping_length,gp_1_f,res_u_1)
            image_save=save_image_3(firer_id)
            image = image_record(
                        date=time.strftime("%x"),
                        datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                        session_id=session_id,
                        detail_id=detail_no,
                        firer_id=firer_id,
                        target_no=target_no,
                        set_no=set_no,
                        paper_ref=paper_no,
                        image_name=image_save
                        )
            db.session.add(image)
            db.session.commit()
                
        return redirect(url_for('previous_page_target_1'))
    
    @app.route('/save_4/', methods=['GET', 'POST'])
    def save_call_4():
        final_x_1=[]
        final_y_1=[]
        x_list=None
        y_list=None
        tend_f_x_t = None
        tend_f_y_t = None
        
        if request.method == 'POST':
            firer_id,session_id,detail_no,target_no,set_no,paper_no,x,y,mx1,my1,tendency,grouping_length,firt_x,firt_y,o,p,result,f=prediction_calculation_4()           
            t1= session.get('tmpi_2',None)
            f_mpix_1 = t1[ : 1 ] 
            f_mpiy_1=t1[ : 0 ]
            final_x_1  = session.get('x2', None)
            final_y_1  = session.get('y2', None)
            gp_1_f=session.get('gp_u_2', None)
            res_u_1=session.get('res_u_2',None)
            tend_f = session.get('tf_u_2', None)
            tend_f_x = session.get('tfirer_x2', None)
            tend_f_y = session.get('tfirer_y2', None)
            tend_f_x_1 = session.get('tfirer_x1_f', None)
            tend_f_y_1 = session.get('tfirer_y1_f', None)
            if (x==0):
                x=0
                y=0
            else:
                x_len=len(x)
                y_len=len(y)
                x_ss=x[1:x_len-1]
                y_ss=y[1:y_len-1]
                x_split = x_ss.split(",")
                y_split = y_ss.split(",")
                x_list=[]
                y_list=[]
                for x_t in x_split:
                    x_list.append(float(x_t))
                    
                for y_t in y_split:
                    y_list.append(float(y_t))
            
            print(x_list,file=sys.stderr)
            box = savein_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,x_list,y_list,final_x_1,final_y_1)
            mpi=savempi_db(detail_no,target_no,paper_no,firer_id,firt_x,firt_y,tendency,session_id,set_no,tend_f,tend_f_x ,tend_f_y,tend_f_x_1,tend_f_y_1)
            gp=savegp_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,grouping_length,gp_1_f,res_u_1)
            image_save=save_image_4(firer_id)
            image = image_record(
                        date=time.strftime("%x"),
                        datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                        session_id=session_id,
                        detail_id=detail_no,
                        firer_id=firer_id,
                        target_no=target_no,
                        set_no=set_no,
                        paper_ref=paper_no,
                        image_name=image_save
                        )
            db.session.add(image)
            db.session.commit()
                
        return redirect(url_for('previous_page_target_1'))
    
    @app.route('/save_5/', methods=['GET', 'POST'])
    def save_call_5():
        final_x_1=[]
        final_y_1=[]
        x_list=None
        y_list=None
        tend_f_x_t = None
        tend_f_y_t = None
        if request.method == 'POST':
            firer_id,session_id,detail_no,target_no,set_no,paper_no,x,y,mx1,my1,tendency,grouping_length,firt_x,firt_y,o,p,result,f=prediction_calculation_5()           
            t1= session.get('tmpi_2',None)
            f_mpix_1 = t1[ : 1 ] 
            f_mpiy_1=t1[ : 0 ]
            final_x_1  = session.get('x2', None)
            final_y_1  = session.get('y2', None)
            gp_1_f=session.get('gp_u_2', None)
            res_u_1=session.get('res_u_2',None)
            tend_f = session.get('tf_u_2', None)
            tend_f_x = session.get('tfirer_x2', None)
            tend_f_y = session.get('tfirer_y2', None)
            tend_f_x_1 = session.get('tfirer_x1_f', None)
            tend_f_y_1 = session.get('tfirer_y1_f', None)
            if (x==0):
                x=0
                y=0
            else:
                x_len=len(x)
                y_len=len(y)
                x_ss=x[1:x_len-1]
                y_ss=y[1:y_len-1]
                x_split = x_ss.split(",")
                y_split = y_ss.split(",")
                x_list=[]
                y_list=[]
                for x_t in x_split:
                    x_list.append(float(x_t))
                    
                for y_t in y_split:
                    y_list.append(float(y_t))
            
            print(x_list,file=sys.stderr)
            box = savein_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,x_list,y_list,final_x_1,final_y_1)
            mpi=savempi_db(detail_no,target_no,paper_no,firer_id,firt_x,firt_y,tendency,session_id,set_no,tend_f,tend_f_x ,tend_f_y,tend_f_x_1,tend_f_y_1)
            gp=savegp_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,grouping_length,gp_1_f,res_u_1)
            image_save=save_image_5(firer_id)
            image = image_record(
                        date=time.strftime("%x"),
                        datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                        session_id=session_id,
                        detail_id=detail_no,
                        firer_id=firer_id,
                        target_no=target_no,
                        set_no=set_no,
                        paper_ref=paper_no,
                        image_name=image_save
                        )
            db.session.add(image)
            db.session.commit()
                
        return redirect(url_for('previous_page_target_5'))
    
    
    
    @app.route('/save_6/', methods=['GET', 'POST'])
    def save_call_6():
        final_x_1=[]
        final_y_1=[]
        x_list=None
        y_list=None
        tend_f_x_t = None
        tend_f_y_t = None
        if request.method == 'POST':
            firer_id,session_id,detail_no,target_no,set_no,paper_no,x,y,mx1,my1,tendency,grouping_length,firt_x,firt_y,o,p,result,f=prediction_calculation_6()           
            t1= session.get('tmpi_2',None)
            f_mpix_1 = t1[ : 1 ] 
            f_mpiy_1=t1[ : 0 ]
            final_x_1  = session.get('x2', None)
            final_y_1  = session.get('y2', None)
            gp_1_f=session.get('gp_u_2', None)
            res_u_1=session.get('res_u_2',None)
            tend_f = session.get('tf_u_2', None)
            tend_f_x = session.get('tfirer_x2', None)
            tend_f_y = session.get('tfirer_y2', None)
            tend_f_x_1 = session.get('tfirer_x1_f', None)
            tend_f_y_1 = session.get('tfirer_y1_f', None)
            if (x==0):
                x=0
                y=0
            else:
                x_len=len(x)
                y_len=len(y)
                x_ss=x[1:x_len-1]
                y_ss=y[1:y_len-1]
                x_split = x_ss.split(",")
                y_split = y_ss.split(",")
                x_list=[]
                y_list=[]
                for x_t in x_split:
                    x_list.append(float(x_t))
                    
                for y_t in y_split:
                    y_list.append(float(y_t))
            
            print(x_list,file=sys.stderr)
            box = savein_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,x_list,y_list,final_x_1,final_y_1)
            mpi=savempi_db(detail_no,target_no,paper_no,firer_id,firt_x,firt_y,tendency,session_id,set_no,tend_f,tend_f_x ,tend_f_y,tend_f_x_1,tend_f_y_1)
            gp=savegp_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,grouping_length,gp_1_f,res_u_1)
            image_save=save_image_6(firer_id)
            image = image_record(
                        date=time.strftime("%x"),
                        datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                        session_id=session_id,
                        detail_id=detail_no,
                        firer_id=firer_id,
                        target_no=target_no,
                        set_no=set_no,
                        paper_ref=paper_no,
                        image_name=image_save
                        )
            db.session.add(image)
            db.session.commit()
                
        return redirect(url_for('previous_page_target_5'))
    
    @app.route('/save_7/', methods=['GET', 'POST'])
    def save_call_7():
        final_x_1=[]
        final_y_1=[]
        x_list=None
        y_list=None
        tend_f_x_t = None
        tend_f_y_t = None
        if request.method == 'POST':
            firer_id,session_id,detail_no,target_no,set_no,paper_no,x,y,mx1,my1,tendency,grouping_length,firt_x,firt_y,o,p,result,f=prediction_calculation_7()           
            t1= session.get('tmpi_2',None)
            f_mpix_1 = t1[ : 1 ] 
            f_mpiy_1=t1[ : 0 ]
            final_x_1  = session.get('x2', None)
            final_y_1  = session.get('y2', None)
            gp_1_f=session.get('gp_u_2', None)
            res_u_1=session.get('res_u_2',None)
            tend_f = session.get('tf_u_2', None)
            tend_f_x = session.get('tfirer_x2', None)
            tend_f_y = session.get('tfirer_y2', None)
            tend_f_x_1 = session.get('tfirer_x1_f', None)
            tend_f_y_1 = session.get('tfirer_y1_f', None)
            if (x==0):
                x=0
                y=0
            else:
                x_len=len(x)
                y_len=len(y)
                x_ss=x[1:x_len-1]
                y_ss=y[1:y_len-1]
                x_split = x_ss.split(",")
                y_split = y_ss.split(",")
                x_list=[]
                y_list=[]
                for x_t in x_split:
                    x_list.append(float(x_t))
                    
                for y_t in y_split:
                    y_list.append(float(y_t))
            
            print(x_list,file=sys.stderr)
            box = savein_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,x_list,y_list,final_x_1,final_y_1)
            mpi=savempi_db(detail_no,target_no,paper_no,firer_id,firt_x,firt_y,tendency,session_id,set_no,tend_f,tend_f_x ,tend_f_y,tend_f_x_1,tend_f_y_1)
            gp=savegp_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,grouping_length,gp_1_f,res_u_1)
            image_save=save_image_7(firer_id)
            image = image_record(
                        date=time.strftime("%x"),
                        datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                        session_id=session_id,
                        detail_id=detail_no,
                        firer_id=firer_id,
                        target_no=target_no,
                        set_no=set_no,
                        paper_ref=paper_no,
                        image_name=image_save
                        )
            db.session.add(image)
            db.session.commit()
                
        return redirect(url_for('previous_page_target_5'))
    
    
    @app.route('/save_8/', methods=['GET', 'POST'])
    def save_call_8():
        final_x_1=[]
        final_y_1=[]
        x_list=None
        y_list=None
        tend_f_x_t = None
        tend_f_y_t = None
        
        if request.method == 'POST':
            firer_id,session_id,detail_no,target_no,set_no,paper_no,x,y,mx1,my1,tendency,grouping_length,firt_x,firt_y,o,p,result,f=prediction_calculation_8()           
            t1= session.get('tmpi_2',None)
            f_mpix_1 = t1[ : 1 ] 
            f_mpiy_1=t1[ : 0 ]
            final_x_1  = session.get('x2', None)
            final_y_1  = session.get('y2', None)
            gp_1_f=session.get('gp_u_2', None)
            res_u_1=session.get('res_u_2',None)
            tend_f = session.get('tf_u_2', None)
            tend_f_x = session.get('tfirer_x2', None)
            tend_f_y = session.get('tfirer_y2', None)
            tend_f_x_1 = session.get('tfirer_x1_f', None)
            tend_f_y_1 = session.get('tfirer_y1_f', None)
            if (x==0):
                x=0
                y=0
            else:
                x_len=len(x)
                y_len=len(y)
                x_ss=x[1:x_len-1]
                y_ss=y[1:y_len-1]
                x_split = x_ss.split(",")
                y_split = y_ss.split(",")
                x_list=[]
                y_list=[]
                for x_t in x_split:
                    x_list.append(float(x_t))
                    
                for y_t in y_split:
                    y_list.append(float(y_t))
            
            print(x_list,file=sys.stderr)
            box = savein_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,x_list,y_list,final_x_1,final_y_1)
            mpi=savempi_db(detail_no,target_no,paper_no,firer_id,firt_x,firt_y,tendency,session_id,set_no,tend_f,tend_f_x ,tend_f_y,tend_f_x_1,tend_f_y_1)
            gp=savegp_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,grouping_length,gp_1_f,res_u_1)
            image_save=save_image_8(firer_id)
            image = image_record(
                        date=time.strftime("%x"),
                        datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                        session_id=session_id,
                        detail_id=detail_no,
                        firer_id=firer_id,
                        target_no=target_no,
                        set_no=set_no,
                        paper_ref=paper_no,
                        image_name=image_save
                        )
            db.session.add(image)
            db.session.commit()
                
        return redirect(url_for('previous_page_target_5'))
    
    def savein_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,x,y,final_x,final_y):
        try:
          print("Save in DB",file=sys.stderr)
          print("--------------",file=sys.stderr)
          print(final_x,file=sys.stderr)
          if(final_x is None):
              print("if",file=sys.stderr)
              i = 0 
              while i <len(x):
                  
                  print(x[i],file=sys.stderr)
                  detail=T_Firer_Details(
                         date=time.strftime("%Y-%m-%d"),
                         datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                         session_id=session_id,
                         detail_id=detail_no,
                         target_no=target_no,
                         set_no=set_no,
                         paper_ref=paper_no,
                         firer_id=firer_id,
                         x=x[i],
                         y=y[i],
                         final_x=x[i],
                         final_y=y[i]
                    )
                  db.session.add(detail)
                  db.session.commit()
                  
                  tdetail=Firer_Details(
                         date=time.strftime("%Y-%m-%d"),
                         datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                         session_id=session_id,
                         detail_id=detail_no,
                         target_no=target_no,
                         set_no=set_no,
                         paper_ref=paper_no,
                         firer_id=firer_id,
                         x=x[i],
                         y=y[i],
                         final_x=x[i],
                         final_y=y[i]
                    )
                  db.session.add(tdetail)
                  db.session.commit()
                  
                  i=i+1
          else:
              print("x",file=sys.stderr)
              print(x,file=sys.stderr)
              if (x is None):
                  f_x ,f_y = making_array_null(x,y , len(final_x))
                  i = 0
                  
                  while i < len(final_x):
                      detail1=T_Firer_Details(
                                date=time.strftime("%Y-%m-%d"),
                                datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                                session_id=session_id,
                                detail_id=detail_no,
                                target_no=target_no,
                                set_no=set_no,
                                paper_ref=paper_no,
                                firer_id=firer_id,
                                x=f_x[i],
                                y=f_y[i],
                                final_x=final_x[i][0],
                                final_y=final_y[i][0]
                             ) 
                      db.session.add(detail1)
                      db.session.commit()
                      
                      tdetail1=Firer_Details(
                                date=time.strftime("%Y-%m-%d"),
                                datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                                session_id=session_id,
                                detail_id=detail_no,
                                target_no=target_no,
                                set_no=set_no,
                                paper_ref=paper_no,
                                firer_id=firer_id,
                                x=f_x[i],
                                y=f_y[i],
                                final_x=final_x[i][0],
                                final_y=final_y[i][0]
                             ) 
                      db.session.add(tdetail1)
                      db.session.commit()
                      i=i+1
                      
              else:
                  if(len(final_x)<len(x)):
                      f_x_f=[]
                      f_y_f=[]
                      f_x_f ,f_y_f = making_array_del(final_x, final_y , len(x))
                      z = 0 
                      while z <len(x):
                          detail1=T_Firer_Details(
                                date=time.strftime("%Y-%m-%d"),
                                datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                                session_id=session_id,
                                detail_id=detail_no,
                                target_no=target_no,
                                set_no=set_no,
                                paper_ref=paper_no,
                                firer_id=firer_id,
                                x=x[z],
                                y=y[z],
                                final_x=f_x_f[z],
                                final_y=f_y_f[z]
                             ) 
                          db.session.add(detail1)
                          db.session.commit()
                          
                          tdetail1=Firer_Details(
                                date=time.strftime("%Y-%m-%d"),
                                datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                                session_id=session_id,
                                detail_id=detail_no,
                                target_no=target_no,
                                set_no=set_no,
                                paper_ref=paper_no,
                                firer_id=firer_id,
                                x=x[z],
                                y=y[z],
                                final_x=f_x_f[z],
                                final_y=f_y_f[z]
                             ) 
                          db.session.add(tdetail1)
                          db.session.commit()
                          z=z+1
                          
                  elif(len(x)<len(final_x)):
                      firer_x=[]
                      firer_y=[]
                      firer_x,firer_y =making_array_add(x,y ,len(final_x))
                      z=0
                      f_x_f1=[]
                      f_y_f1=[]
                      for h in range(len(final_x)):
                          f_x_f1.append(final_x[h][0])
                          f_y_f1.append(final_y[h][0])
                          
                      while z <len(f_y_f1):
                          detail2=T_Firer_Details(
                                date=time.strftime("%Y-%m-%d"),
                                datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                                session_id=session_id,
                                detail_id=detail_no,
                                target_no=target_no,
                                set_no=set_no,
                                paper_ref=paper_no,
                                firer_id=firer_id,
                                x=firer_x[z],
                                y=firer_y[z],
                                final_x=f_x_f1[z],
                                final_y=f_y_f1[z]
                             ) 
                          db.session.add(detail2)
                          db.session.commit()
                          
                          tdetail2=Firer_Details(
                                date=time.strftime("%Y-%m-%d"),
                                datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                                session_id=session_id,
                                detail_id=detail_no,
                                target_no=target_no,
                                set_no=set_no,
                                paper_ref=paper_no,
                                firer_id=firer_id,
                                x=firer_x[z],
                                y=firer_y[z],
                                final_x=f_x_f1[z],
                                final_y=f_y_f1[z]
                             ) 
                          db.session.add(tdetail2)
                          db.session.commit()
                          z=z+1       
                  else:
                      z=0
                      f_x_f1=[]
                      f_y_f1=[]
                      for h in range(len(final_x)):
                          f_x_f1.append(final_x[h][0])
                          f_y_f1.append(final_y[h][0])
                          
                      print(type(f_x_f1),f_x_f1[0],file=sys.stderr)
                      while z <len(x):
                              detail3=T_Firer_Details(
                                date=time.strftime("%Y-%m-%d"),
                                datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                                session_id=session_id,
                                detail_id=detail_no,
                                target_no=target_no,
                                set_no=set_no,
                                paper_ref=paper_no,
                                firer_id=firer_id,
                                x=x[z],
                                y=y[z],
                                final_x=int(f_x_f1[z]),
                                final_y=int(f_y_f1[z])
                               ) 
                              db.session.add(detail3)
                              db.session.commit()
                              
                              tdetail3=Firer_Details(
                                date=time.strftime("%Y-%m-%d"),
                                datetimestamp = time.strftime("%Y-%m-%d %H:%M"),
                                session_id=session_id,
                                detail_id=detail_no,
                                target_no=target_no,
                                set_no=set_no,
                                paper_ref=paper_no,
                                firer_id=firer_id,
                                x=x[z],
                                y=y[z],
                                final_x=int(f_x_f1[z]),
                                final_y=int(f_y_f1[z])
                               ) 
                              db.session.add(tdetail3)
                              db.session.commit()
                              z=z+1
        except Exception as e:
             return redirect(url_for('error_6'))
        return True

    def making_array_null(x,y,l):
        x1=[]
        y1=[]
        i=0
        for i in range(l):
            x1.append(-1)
            y1.append(-1)
        return x1 , y1
    
    
    def save_image_1(firer_id):
        srcfile = 'E:/FRAS Windows/FRAS_production/static/img_dump/1.png'
        dstdir = 'E:/FRAS Windows/FRAS_production/static/image_db'
        #srcfile = '/Users/wasifaahmed/Documents/FRAS/Fras_production_v.0.1/FRAS Windows/FRAS Windows/FRAS_production/static/img_dump/1.png'
        #dstdir = '/Users/wasifaahmed/Documents/FRAS/Fras_production_v.0.1/FRAS Windows/FRAS Windows/FRAS_production/static/image_db/'
        shutil.copy(srcfile, dstdir)     
        old_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", "1.png")
        #old_file = os.path.join('/Users/wasifaahmed/Documents/FRAS/Fras_production_v.0.1/FRAS Windows/FRAS Windows/FRAS_production/static/image_db/', "1.png")
        newfilename=""
        newfilename+=str(firer_id)
        newfilename+="_"
        newfilename+=time.strftime("%Y_%m_%d_%H_%M")
        newfilename+=".png"
        new_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", newfilename)
        #new_file = os.path.join("/Users/wasifaahmed/Documents/FRAS/Fras_production_v.0.1/FRAS Windows/FRAS Windows/FRAS_production/static/image_db/", newfilename)
        os.rename(old_file, new_file)
        return newfilename
    
    def save_image_2(firer_id):
        srcfile = 'E:/FRAS Windows/FRAS_production/static/img_dump/2.png'
        dstdir = 'E:/FRAS Windows/FRAS_production/static/image_db'
        shutil.copy(srcfile, dstdir)     
        old_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", "2.png")
        newfilename=""
        newfilename+=str(firer_id)
        newfilename+="_"
        newfilename+=time.strftime("%Y_%m_%d_%H_%M")
        newfilename+=".png"
        new_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", newfilename)
        os.rename(old_file, new_file)
        return newfilename
    
    def save_image_3(firer_id):
        srcfile = 'E:/FRAS_production/static/img_dump/3.png'
        dstdir = 'E:/FRAS Windows/FRAS_production/static/image_db'
        shutil.copy(srcfile, dstdir)     
        old_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", "3.png")
        newfilename=""
        newfilename+=str(firer_id)
        newfilename+="_"
        newfilename+=time.strftime("%Y_%m_%d_%H_%M")
        newfilename+=".png"
        new_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", newfilename)
        os.rename(old_file, new_file)
        return newfilename
    
    def save_image_4(firer_id):
        srcfile = 'E:/FRAS_production/static/img_dump/4.png'
        dstdir = 'E:/FRAS Windows/FRAS_production/static/image_db'
        shutil.copy(srcfile, dstdir)     
        old_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", "4.png")
        newfilename=""
        newfilename+=str(firer_id)
        newfilename+="_"
        newfilename+=time.strftime("%Y_%m_%d_%H_%M")
        newfilename+=".png"
        new_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", newfilename)
        os.rename(old_file, new_file)
        return newfilename
    
    def save_image_5(firer_id):
        srcfile = 'E:/FRAS_production/static/img_dump/5.png'
        dstdir = 'E:/FRAS Windows/FRAS_production/static/image_db'
        shutil.copy(srcfile, dstdir)     
        old_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", "5.png")
        newfilename=""
        newfilename+=str(firer_id)
        newfilename+="_"
        newfilename+=time.strftime("%Y_%m_%d_%H_%M")
        newfilename+=".png"
        new_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", newfilename)
        os.rename(old_file, new_file)
        return newfilename
    
    def save_image_6(firer_id):
        srcfile = 'E:/FRAS_production/static/img_dump/6.png'
        dstdir = 'E:/FRAS Windows/FRAS_production/static/image_db'
        shutil.copy(srcfile, dstdir)     
        old_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", "6.png")
        newfilename=""
        newfilename+=str(firer_id)
        newfilename+="_"
        newfilename+=time.strftime("%Y_%m_%d_%H_%M")
        newfilename+=".png"
        new_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", newfilename)
        os.rename(old_file, new_file)
        return newfilename
    
    def save_image_7(firer_id):
        srcfile = 'E:/FRAS_production/static/img_dump/7.png'
        dstdir = 'E:/FRAS Windows/FRAS_production/static/image_db'
        shutil.copy(srcfile, dstdir)     
        old_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", "7.png")
        newfilename=""
        newfilename+=str(firer_id)
        newfilename+="_"
        newfilename+=time.strftime("%Y_%m_%d_%H_%M")
        newfilename+=".png"
        new_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", newfilename)
        os.rename(old_file, new_file)
        return newfilename
    
    def save_image_8(firer_id):
        srcfile = 'E:/FRAS_production/static/img_dump/8.png'
        dstdir = 'E:/FRAS Windows/FRAS_production/static/image_db'
        shutil.copy(srcfile, dstdir)     
        old_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", "8.png")
        newfilename=""
        newfilename+=str(firer_id)
        newfilename+="_"
        newfilename+=time.strftime("%Y_%m_%d_%H_%M")
        newfilename+=".png"
        new_file = os.path.join("E:/FRAS Windows/FRAS_production/static/image_db", newfilename)
        os.rename(old_file, new_file)
        return newfilename
    
    
    def savempi_db(detail_no,target_no,paper_no,firer_id,firt_x,firt_y,tendency,session_id,set_no,tend_f,tend_f_x ,tend_f_y,tend_f_x_1,tend_f_y_1,f):
        try:
            print("this is tend_f_x",file=sys.stderr)
            print(tend_f_x_1,file=sys.stderr)
        
            if(firt_x==0):
                mpi= MPI (
                          date=time.strftime("%Y-%m-%d"),  
                          datetimestamp = time.strftime("%Y-%m-%d %H:%M"), 
                          session_id=session_id,
                          detail_no=detail_no,
                          target_no=target_no,
                          spell_no=set_no,
                          paper_ref=paper_no,
                          firer_id=firer_id,
                          mpi_x=-1,
                          mpi_y=-1,
                          f_mpi_x=tend_f_x_1,
                          f_mpi_y=tend_f_y_1,
                          tendency=-1,
                          tendency_f=int(tend_f),
                          tendency_text=tend_f_x,
                          tendency_code=tend_f_y
                         )
                db.session.add(mpi)
                db.session.commit()
            else:
                if(tend_f_x_1 is None):
                    mpi= MPI (
                          date=time.strftime("%Y-%m-%d"),  
                          datetimestamp = time.strftime("%Y-%m-%d %H:%M"), 
                          session_id=session_id,
                          detail_no=detail_no,
                          target_no=target_no,
                          spell_no=set_no,
                          paper_ref=paper_no,
                          firer_id=firer_id,
                          mpi_x=firt_x[0],
                          mpi_y=firt_y[0],
                          f_mpi_x=firt_x[0],
                          f_mpi_y=firt_y[0],
                          tendency=int(tendency),
                          tendency_f=int(tendency),
                          tendency_text=f,
                          tendency_code=f
                          
                         )
                    db.session.add(mpi)
                    db.session.commit()
                     
                else:
                    mpi= MPI (
                          date=time.strftime("%Y-%m-%d"),  
                          datetimestamp = time.strftime("%Y-%m-%d %H:%M"), 
                          session_id=session_id,
                          detail_no=detail_no,
                          target_no=target_no,
                          spell_no=set_no,
                          paper_ref=paper_no,
                          firer_id=firer_id,
                          mpi_x=firt_x[0],
                          mpi_y=firt_y[0],
                          f_mpi_x=tend_f_x_1,
                          f_mpi_y=tend_f_y_1,
                          tendency=tendency,
                          tendency_f=int(tend_f),
                          tendency_text=tend_f_x,
                          tendency_code=tend_f_y
                         )
                    db.session.add(mpi)
                    db.session.commit()
        except Exception as e:
            return redirect(url_for('error_6'))  
        return True
    
    
    
    def savegp_db(firer_id,session_id,detail_no,target_no,set_no,paper_no,gp_l,gp_f,result,result_p):
        try:
            print("gp_l",file=sys.stderr)
            print(gp_l,file=sys.stderr)
            if (gp_l==""):
                gp=Grouping(
                          date=time.strftime("%Y-%m-%d"),  
                          datetimestamp = time.strftime("%Y-%m-%d %H:%M"), 
                          session_id=session_id,
                          detail_no=detail_no,
                          target_no=target_no,
                          spell_no=set_no,
                          paper_ref=paper_no,
                          firer_id=firer_id,
                          grouping_length=-1,
                          grouping_length_f=gp_f,
                          result = result
                          )
                    
                db.session.add(gp)
                db.session.commit()
            else:
                if(gp_f is None):
                    gp=Grouping(
                          date=time.strftime("%Y-%m-%d"),  
                          datetimestamp = time.strftime("%Y-%m-%d %H:%M"), 
                          session_id=session_id,
                          detail_no=detail_no,
                          target_no=target_no,
                          spell_no=set_no,
                          paper_ref=paper_no,
                          firer_id=firer_id,
                          grouping_length=gp_l,
                          grouping_length_f=gp_l,
                          result = result_p
                          )
                    
                    db.session.add(gp)
                    db.session.commit()
                    
                else:
                    gp=Grouping(
                          date=time.strftime("%Y-%m-%d"),  
                          datetimestamp = time.strftime("%Y-%m-%d %H:%M"), 
                          session_id=session_id,
                          detail_no=detail_no,
                          target_no=target_no,
                          spell_no=set_no,
                          paper_ref=paper_no,
                          firer_id=firer_id,
                          grouping_length=gp_l,
                          grouping_length_f=gp_f,
                          result = result
                          )
                    
                    db.session.add(gp)
                    db.session.commit()
        except Exception as e:
            return redirect(url_for('error_6'))
        return True
    
    
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.route('/duplicate_firer_error/')
    def duplicate_firer_error():
        return render_template('errors/duplicate.html')
    
    @app.route('/paper_duplicate/')
    def paper_duplicate_error():
        return render_template('errors/paper_dup.html')
    
    @app.route('/error_duplicate/')
    def error_duplicate():
        return render_template('errors/error_duplicate.html')
    
    @app.route('/error/')
    def error():
        return render_template('errors/error_505.html')
    
    @app.route('/error_2/')
    def error_2():
        return render_template('errors/error2_505.html')
    
    @app.route('/error_102/')
    def error_102():
        return render_template('errors/error_102.html')
    
    
    @app.route('/error_31/')
    def error_31():
        return render_template('errors/error31.html')
    @app.route('/error_target_1/')
    def error_target_1():
        return render_template('errors/error_target_1.html')
        
    @app.route('/error_3/')
    def error_3():
        return render_template('errors/error3_505.html')
    
    
    @app.route('/error_4/')
    def error_4():
        return render_template('errors/error4_505.html')
    
    @app.route('/error_5/')
    def error_5():
        return render_template('errors/error5_505.html')
    
    @app.route('/error_6/')
    def error_6():
        return render_template('errors/error6_505.html')
    
    @app.route('/error_7/')
    def error_7():
        return render_template('errors/error7_505.html')
    
    def making_array_del(x , y , l):
        x_f=[]
        y_f=[]
        
        for i in range(len(x)):
            x_f.append(x[i][0])
            y_f.append(y[i][0])
            
        for j in range(l-len(x)):
            x_f.append(-1)
            y_f.append(-1)
        return x_f , y_f
    
    def making_array_add(x , y , l):
        x_1=[]
        y_1=[]
        for i in range(len(x)):
            x_1.append(x[i])
            y_1.append(y[i])
            
            
        for j in range(l-len(x)):
            x_1.append(-1)
            y_1.append(-1)
        
        return x_1 , y_1
        
        
        

        
    def firing_tendancy(origin_x, origin_y , x, y):
        print("x,y",file=sys.stderr)
        print(x,y,file=sys.stderr)
        x1 = origin_x-x
        y1 = origin_y-y
        xfirt=None
        yfirt=None
        deg = 0 
        h = math.sqrt(x1**2 + y1**2)
        x_dis = x-origin_x
        y_dis = y-origin_y
        theta = math.degrees(y_dis/h)
        if( x_dis > 0 and y_dis < 0 ):
            deg = 360 - theta
            xfirt=pixeltoinch(x_dis)
            yfirt=pixeltoinch(y_dis)
            
            
        elif (x_dis < 0 and y_dis < 0 ):
            deg = 270 - theta
            xfirt=pixeltoinch(x_dis)
            yfirt=pixeltoinch(y_dis)
            
        elif(x_dis < 0 and y_dis > 0 ):
            deg = 180 - theta
            xfirt=pixeltoinch(x_dis)
            yfirt=pixeltoinch(y_dis)
        else :
           deg = theta
           xfirt=pixeltoinch(x_dis)
           yfirt=pixeltoinch(y_dis)
        
        print("Sending xfirt....", file=sys.stderr)
        print(xfirt, file=sys.stderr)
        print(yfirt, file=sys.stderr)
        return (np.round(deg,0) ,xfirt ,yfirt )
    
    def getfiringtendencytext(f1 ,firt_x,firt_y):
        print("Receiving xfirt....", file=sys.stderr)
        print(firt_x, file=sys.stderr)
        print(firt_y, file=sys.stderr)
        fttext=""
        ftcode=""
        
        t1=""
        t2=""
        t1code=""
        t2code=""
        
        isbullseye=False
        
        if(abs(firt_x)<=4.5 and abs(firt_y)<=4.5):
            isbullseye=True
            
        
        if firt_x >=0 and firt_y >=0:
            t1="Top"
            t2="Right"
            t1code="T"
            t2code="R"
        elif firt_x <0 and firt_y >=0:
            t1="Top"
            t2="Left"
            t1code="T"
            t2code="L"
        elif firt_x <0 and firt_y <0:
            t1="Bottom"
            t2="Left"
            t1code="B"
            t2code="L"
        else:
            t1="Bottom"
            t2="Right"
            t1code="B"
            t2code="R"
        
        if(isbullseye):
            ftcode="Center"
            fttext = "Center "+"("+str(firt_y)+" , "+str(firt_x)+")"
        else:
            ftcode=t1code+t2code
            fttext = t1+"("+str(firt_y)+") "+t2+"("+str(firt_x)+")"
            
        return fttext,ftcode
    
    
    def grouping_length(xt,yt,x ,y):
        d = {}
        counter=0
        for i in range(len(x)):
            for j in range(len(x)):
                
                d[counter]=distance(x[j],y[j],x[i],y[i])
                counter+=1     
        maxdist = 0
        
        for key in d.keys():
            if(maxdist<d[key]):
                maxdist= d[key]
        
        maxdist_inch = pixeltoinch(maxdist)
        return maxdist_inch
            
        
        
    def distance (x1,y1,x,y):
        dist = 0 
        xdist = x1 - x
        ydist = y1 - y
        dist = math.sqrt(xdist**2 + ydist**2)
        return dist
    
    def pixeltoinch(maxdist):
        inch = (34/2000 *1.0)*maxdist
        return np.round(inch,1)
    
    def getresulttext(gpinch):
        print(type(gpinch),file=sys.stderr)
        print(gpinch,file=sys.stderr)
        if gpinch <=10:
            return "Pass"
        else:
            return "W/O"
    
    @app.route('/previous_page_edit_1/')
    def previous_page_edit_1():
        return render_template('pages/image_edit_previous_1.html')
    
    @app.route('/previous_page_edit_5/')
    def previous_page_edit_5():
        return render_template('pages/image_edit_previous_5.html')
        
    @app.route('/crop_data_1', methods=['GET', 'POST'])
    def crop_data_1():
        img = Image.open("E:/FRAS Windows/FRAS_production/static/raw_image/CAMERA1_1.JPG")
        if request.method == "POST":
            data=request.get_json()
            point_1=data['data1'][0]
            point_2=data['data2'][0]
            point_3=data['data3'][0]
            point_4=data['data4'][0]
            print(point_1,file=sys.stderr)
            print(point_2,file=sys.stderr)
            print(point_3,file=sys.stderr)
            print(point_4,file=sys.stderr)
            points=[]
            points.append(point_1)
            points.append(point_2)
            points.append(point_3)
            points.append(point_4)
            
            temp_points = []
            for p in points:
                temp_points.append(p)
                
            l=99999
            left1=None
            for p in temp_points:
                if l > p[0]:
                    l=p[0]
                    left1 = p
            
            temp_points2 = []
            for p in temp_points:
                if(p[0]!=left1[0] and p[1]!=left1[1]):
                    temp_points2.append(p)
            
            l2=99999
            left2=None
            for p in temp_points2:
                if l2 > p[0]:
                    l2=p[0]
                    left2 = p
            
            left = None
            
            print("left1,left2",file=sys.stderr)
            print(left1,left2,file=sys.stderr)
            
            if left1[1]>left2[1]:
                left = left1
            else:
                left = left2
                
            
            r=-1000
            right1=None
            for p in points:
                if r < p[0]:
                    r = p[0]
                    right1 = p
            
            temp_points3 = []
            for p in points:
                if(p[0]!=right1[0] and p[1]!=right1[1]):
                    temp_points3.append(p)
            
            r2=-1000
            right2=None
            for p in temp_points3:
                if r2 < p[0]:
                    r2=p[0]
                    right2 = p
            
            right = None
            
            if right1[1]<right2[1]:
                right = right1
            else:
                right = right2  
            
            print("right1,right2",file=sys.stderr)
            print(right1,right2,file=sys.stderr)
            
            print("left,right",file=sys.stderr)
            print(left,right,file=sys.stderr)
            x1=int(left[0])
            if(x1>5470):
                x1=5470
            
            y1=int(3648.0-(left[1]))
            if(y1<0):
                y1=0
                
            x2=int(right[0])+80
            if(x2>5470):
                x2=5470
            y2=int(3648.0-(right[1]))
            if(y2<0):
                y2=0
            
            x1=x1+50
            y1=y1+50
            x2=x2+50
            y2=y2+50
            print("x1,y1,x2, y2",file=sys.stderr)
            print(x1,y1,x2, y2,file=sys.stderr)
            img2 = img.crop((x1, y1, x2, y2))
    
            
            resize_image=img2.resize((2000, 2000), Image.ANTIALIAS)
            
            resize_image.save('E:/FRAS Windows/FRAS_production/static/img_dump/1.jpg', 'JPEG')
            image_png=Image.open('E:/FRAS Windows/FRAS_production/static/img_dump/1.jpg')
            #os.remove("E:/FRAS_production/static/img_dump/1.png")
            image_png.save('E:/FRAS Windows/FRAS_production/static/img_dump/1.png')
            sth = db.session.query(Crop).filter(Crop.target_no==1).scalar()
            if sth  is None:
                crop =Crop(
                        target_no=1,
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2
                        )
                db.session.add(crop)
                db.session.commit()
            else:
                db.session.query(Crop).filter(Crop.target_no==1).delete()
                db.session.commit()
                crop =Crop(
                        target_no=1,
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2
                        )
                db.session.add(crop)
                db.session.commit()
                
                
        return redirect(url_for('previous_page_edit_1'))
    
    
    @app.route('/calibration_1', methods=['GET', 'POST'])
    def calibration_1():
        data = db.session.query(Crop).filter_by(target_no=1).scalar()   
        print(data.target_no,file=sys.stderr)
        print(data.x1,file=sys.stderr)
        x1=data.x1
        y1=data.y1
        x2=data.x2
        y2=data.y2
        img = Image.open('E:/FRAS Windows/FRAS_production/static/raw_image/CAMERA1_1.JPG')
        img2 = img.crop((x1, y1, x2, y2))
        resize_image=img2.resize((2000, 2000), Image.ANTIALIAS)
        resize_image.save('E:/FRAS Windows/FRAS_production/static/img_dump/1.jpg', 'JPEG')
        image_png=Image.open("E:/FRAS Windows/FRAS_production/static/img_dump/1.jpg") 
        image_png.save("E:/FRAS Windows/FRAS_production/static/img_dump/1.png")
        return redirect(url_for('previous_page_edit_1'))
    
    
    @app.route('/calibration_2', methods=['GET', 'POST'])
    def calibration_2():
        data = db.session.query(Crop).filter_by(target_no=2).scalar()   
        print(data.target_no,file=sys.stderr)
        print(data.x1,file=sys.stderr)
        x1=data.x1
        y1=data.y1
        x2=data.x2
        y2=data.y2
        img = Image.open('E:/FRAS Windows/FRAS_production/static/raw_image/CAMERA2_2.JPG')
        img2 = img.crop((x1, y1, x2, y2))
        resize_image=img2.resize((2000, 2000), Image.ANTIALIAS)
        resize_image.save('E:/FRAS Windows/FRAS_production/static/img_dump/2.jpg', 'JPEG')
        image_png=Image.open("E:/FRAS Windows/FRAS_production/static/img_dump/2.jpg") 
        image_png.save("E:/FRAS Windows/FRAS_production/static/img_dump/2png")
        return redirect(url_for('previous_page_edit_1'))
    
    
    
    @app.route('/crop_data_2', methods=['GET', 'POST'])
    def crop_data_2():
        img = Image.open("E:/FRAS Windows/FRAS_production/static/raw_image/CAMERA2_2.JPG")
        if request.method == "POST":
            data=request.get_json()
            point_1=data['data1'][0]
            point_2=data['data2'][0]
            point_3=data['data3'][0]
            point_4=data['data4'][0]
            print(point_1,file=sys.stderr)
            print(point_2,file=sys.stderr)
            print(point_3,file=sys.stderr)
            print(point_4,file=sys.stderr)
            points=[]
            points.append(point_1)
            points.append(point_2)
            points.append(point_3)
            points.append(point_4)
            
            temp_points = []
            for p in points:
                temp_points.append(p)
                
            l=99999
            left1=None
            for p in temp_points:
                if l > p[0]:
                    l=p[0]
                    left1 = p
            
            temp_points2 = []
            for p in temp_points:
                if(p[0]!=left1[0] and p[1]!=left1[1]):
                    temp_points2.append(p)
            
            l2=99999
            left2=None
            for p in temp_points2:
                if l2 > p[0]:
                    l2=p[0]
                    left2 = p
            
            left = None
            
            print("left1,left2",file=sys.stderr)
            print(left1,left2,file=sys.stderr)
            
            if left1[1]>left2[1]:
                left = left1
            else:
                left = left2
                
            
            r=-1000
            right1=None
            for p in points:
                if r < p[0]:
                    r = p[0]
                    right1 = p
            
            temp_points3 = []
            for p in points:
                if(p[0]!=right1[0] and p[1]!=right1[1]):
                    temp_points3.append(p)
            
            r2=-1000
            right2=None
            for p in temp_points3:
                if r2 < p[0]:
                    r2=p[0]
                    right2 = p
            
            right = None
            
            if right1[1]<right2[1]:
                right = right1
            else:
                right = right2  
            
            print("right1,right2",file=sys.stderr)
            print(right1,right2,file=sys.stderr)
            
            print("left,right",file=sys.stderr)
            print(left,right,file=sys.stderr)
            x1=int(left[0])
            if(x1>5470):
                x1=5470
            
            y1=int(3648.0-(left[1]))
            if(y1<0):
                y1=0
                
            x2=int(right[0])+80
            if(x2>5470):
                x2=5470
            y2=int(3648.0-(right[1]))
            if(y2<0):
                y2=0
            
            x1=x1+50
            y1=y1+50
            x2=x2+50
            y2=y2+50
            print("x1,y1,x2, y2",file=sys.stderr)
            print(x1,y1,x2, y2,file=sys.stderr)
            img2 = img.crop((x1, y1, x2, y2))
    
            
            resize_image=img2.resize((2000, 2000), Image.ANTIALIAS)
            
            resize_image.save('E:/FRAS Windows/FRAS_production/static/img_dump/2.jpg', 'JPEG')
            image_png=Image.open('E:/FRAS Windows/FRAS_production/static/img_dump/2.jpg')
            #os.remove("E:/FRAS_production/static/img_dump/1.png")
            image_png.save('E:/FRAS Windows/FRAS_production/static/img_dump/2.png')
            sth = db.session.query(Crop).filter(Crop.target_no==1).scalar()
            if sth  is None:
                crop =Crop(
                        target_no=2,
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2
                        )
                db.session.add(crop)
                db.session.commit()
            else:
                db.session.query(Crop).filter(Crop.target_no==1).delete()
                db.session.commit()
                crop =Crop(
                        target_no=2,
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2
                        )
                db.session.add(crop)
                db.session.commit()
                
                
        return redirect(url_for('previous_page_edit_1'))
    
    
    @app.route('/crop_data_3', methods=['GET', 'POST'])
    def crop_data_3():
        img = Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/raw_image/CAMERA3_3.JPG")
        if request.method == "POST":
            data=request.get_json()
            point_1=data['data1'][0]
            point_2=data['data2'][0]
            point_3=data['data3'][0]
            point_4=data['data4'][0]
            print(point_1,file=sys.stderr)
            print(point_2,file=sys.stderr)
            print(point_3,file=sys.stderr)
            print(point_4,file=sys.stderr)
            points=[]
            points.append(point_1)
            points.append(point_2)
            points.append(point_3)
            points.append(point_4)
            
            temp_points = []
            for p in points:
                temp_points.append(p)
                
            l=99999
            left1=None
            for p in temp_points:
                if l > p[0]:
                    l=p[0]
                    left1 = p
            
            temp_points2 = []
            for p in temp_points:
                if(p[0]!=left1[0] and p[1]!=left1[1]):
                    temp_points2.append(p)
            
            l2=99999
            left2=None
            for p in temp_points2:
                if l2 > p[0]:
                    l2=p[0]
                    left2 = p
            
            left = None
            
            print("left1,left2",file=sys.stderr)
            print(left1,left2,file=sys.stderr)
            
            if left1[1]>left2[1]:
                left = left1
            else:
                left = left2
                
            
            r=-1000
            right1=None
            for p in points:
                if r < p[0]:
                    r = p[0]
                    right1 = p
            
            temp_points3 = []
            for p in points:
                if(p[0]!=right1[0] and p[1]!=right1[1]):
                    temp_points3.append(p)
            
            r2=-1000
            right2=None
            for p in temp_points3:
                if r2 < p[0]:
                    r2=p[0]
                    right2 = p
            
            right = None
            
            if right1[1]<right2[1]:
                right = right1
            else:
                right = right2  
            
            print("right1,right2",file=sys.stderr)
            print(right1,right2,file=sys.stderr)
            
            print("left,right",file=sys.stderr)
            print(left,right,file=sys.stderr)
            x1=int(left[0])
            if(x1>5470):
                x1=5470
            y1=int(3648.0-(left[1]))
            if(y1<0):
                y1=0
                
            x2=int(right[0])+80
            if(x2>5470):
                x2=5470
            y2=int(3648.0-(right[1]))
            if(y2<0):
                y2=0
            
            print("x1,y1,x2, y2",file=sys.stderr)
            print(x1,y1,x2, y2,file=sys.stderr)
            img2 = img.crop((x1, y1, x2, y2))
    
            
            resize_image=img2.resize((2000, 2000), Image.ANTIALIAS)
            resize_image.save('/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/3.jpg', 'JPEG')
            image_png=Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/3.jpg") 
            image_png.save("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/3.png")
        return redirect(url_for('previous_page_edit_1'))
    
    
    
    @app.route('/crop_data_4', methods=['GET', 'POST'])
    def crop_data_4():
        img = Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/raw_image/CAMERA4_4.JPG")
        if request.method == "POST":
            data=request.get_json()
            point_1=data['data1'][0]
            point_2=data['data2'][0]
            point_3=data['data3'][0]
            point_4=data['data4'][0]
            print(point_1,file=sys.stderr)
            print(point_2,file=sys.stderr)
            print(point_3,file=sys.stderr)
            print(point_4,file=sys.stderr)
            points=[]
            points.append(point_1)
            points.append(point_2)
            points.append(point_3)
            points.append(point_4)
            
            temp_points = []
            for p in points:
                temp_points.append(p)
                
            l=99999
            left1=None
            for p in temp_points:
                if l > p[0]:
                    l=p[0]
                    left1 = p
            
            temp_points2 = []
            for p in temp_points:
                if(p[0]!=left1[0] and p[1]!=left1[1]):
                    temp_points2.append(p)
            
            l2=99999
            left2=None
            for p in temp_points2:
                if l2 > p[0]:
                    l2=p[0]
                    left2 = p
            
            left = None
            
            print("left1,left2",file=sys.stderr)
            print(left1,left2,file=sys.stderr)
            
            if left1[1]>left2[1]:
                left = left1
            else:
                left = left2
                
            
            r=-1000
            right1=None
            for p in points:
                if r < p[0]:
                    r = p[0]
                    right1 = p
            
            temp_points3 = []
            for p in points:
                if(p[0]!=right1[0] and p[1]!=right1[1]):
                    temp_points3.append(p)
            
            r2=-1000
            right2=None
            for p in temp_points3:
                if r2 < p[0]:
                    r2=p[0]
                    right2 = p
            
            right = None
            
            if right1[1]<right2[1]:
                right = right1
            else:
                right = right2  
            
            print("right1,right2",file=sys.stderr)
            print(right1,right2,file=sys.stderr)
            
            print("left,right",file=sys.stderr)
            print(left,right,file=sys.stderr)
            x1=int(left[0])
            if(x1>5470):
                x1=5470
            y1=int(3648.0-(left[1]))
            if(y1<0):
                y1=0
                
            x2=int(right[0])+80
            if(x2>5470):
                x2=5470
            y2=int(3648.0-(right[1]))
            if(y2<0):
                y2=0
            
            print("x1,y1,x2, y2",file=sys.stderr)
            print(x1,y1,x2, y2,file=sys.stderr)
            img2 = img.crop((x1, y1, x2, y2))
    
            
            resize_image=img2.resize((2000, 2000), Image.ANTIALIAS)
            resize_image.save('/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/4.jpg', 'JPEG')
            image_png=Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/4.jpg") 
            image_png.save("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/4.png")
        return redirect(url_for('previous_page_edit_1'))
    
    @app.route('/crop_data_5', methods=['GET', 'POST'])
    def crop_data_5():
        img = Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/raw_image/CAMERA5_5.JPG")
        if request.method == "POST":
            data=request.get_json()
            point_1=data['data1'][0]
            point_2=data['data2'][0]
            point_3=data['data3'][0]
            point_4=data['data4'][0]
            print(point_1,file=sys.stderr)
            print(point_2,file=sys.stderr)
            print(point_3,file=sys.stderr)
            print(point_4,file=sys.stderr)
            points=[]
            points.append(point_1)
            points.append(point_2)
            points.append(point_3)
            points.append(point_4)
            
            temp_points = []
            for p in points:
                temp_points.append(p)
                
            l=99999
            left1=None
            for p in temp_points:
                if l > p[0]:
                    l=p[0]
                    left1 = p
            
            temp_points2 = []
            for p in temp_points:
                if(p[0]!=left1[0] and p[1]!=left1[1]):
                    temp_points2.append(p)
            
            l2=99999
            left2=None
            for p in temp_points2:
                if l2 > p[0]:
                    l2=p[0]
                    left2 = p
            
            left = None
            
            print("left1,left2",file=sys.stderr)
            print(left1,left2,file=sys.stderr)
            
            if left1[1]>left2[1]:
                left = left1
            else:
                left = left2
                
            
            r=-1000
            right1=None
            for p in points:
                if r < p[0]:
                    r = p[0]
                    right1 = p
            
            temp_points3 = []
            for p in points:
                if(p[0]!=right1[0] and p[1]!=right1[1]):
                    temp_points3.append(p)
            
            r2=-1000
            right2=None
            for p in temp_points3:
                if r2 < p[0]:
                    r2=p[0]
                    right2 = p
            
            right = None
            
            if right1[1]<right2[1]:
                right = right1
            else:
                right = right2  
            
            print("right1,right2",file=sys.stderr)
            print(right1,right2,file=sys.stderr)
            
            print("left,right",file=sys.stderr)
            print(left,right,file=sys.stderr)
            x1=int(left[0])
            if(x1>5470):
                x1=5470
            y1=int(3648.0-(left[1]))
            if(y1<0):
                y1=0
                
            x2=int(right[0])+80
            if(x2>5470):
                x2=5470
            y2=int(3648.0-(right[1]))
            if(y2<0):
                y2=0
            
            print("x1,y1,x2, y2",file=sys.stderr)
            print(x1,y1,x2, y2,file=sys.stderr)
            img2 = img.crop((x1, y1, x2, y2))
    
            
            resize_image=img2.resize((2000, 2000), Image.ANTIALIAS)
            resize_image.save('/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/5.jpg', 'JPEG')
            image_png=Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/5.jpg") 
            image_png.save("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/5.png")
        return redirect(url_for('previous_page_edit_2'))
    
    
    @app.route('/crop_data_6', methods=['GET', 'POST'])
    def crop_data_6():
        img = Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/raw_image/CAMERA6_6.JPG")
        if request.method == "POST":
            data=request.get_json()
            point_1=data['data1'][0]
            point_2=data['data2'][0]
            point_3=data['data3'][0]
            point_4=data['data4'][0]
            print(point_1,file=sys.stderr)
            print(point_2,file=sys.stderr)
            print(point_3,file=sys.stderr)
            print(point_4,file=sys.stderr)
            points=[]
            points.append(point_1)
            points.append(point_2)
            points.append(point_3)
            points.append(point_4)
            
            temp_points = []
            for p in points:
                temp_points.append(p)
                
            l=99999
            left1=None
            for p in temp_points:
                if l > p[0]:
                    l=p[0]
                    left1 = p
            
            temp_points2 = []
            for p in temp_points:
                if(p[0]!=left1[0] and p[1]!=left1[1]):
                    temp_points2.append(p)
            
            l2=99999
            left2=None
            for p in temp_points2:
                if l2 > p[0]:
                    l2=p[0]
                    left2 = p
            
            left = None
            
            print("left1,left2",file=sys.stderr)
            print(left1,left2,file=sys.stderr)
            
            if left1[1]>left2[1]:
                left = left1
            else:
                left = left2
                
            
            r=-1000
            right1=None
            for p in points:
                if r < p[0]:
                    r = p[0]
                    right1 = p
            
            temp_points3 = []
            for p in points:
                if(p[0]!=right1[0] and p[1]!=right1[1]):
                    temp_points3.append(p)
            
            r2=-1000
            right2=None
            for p in temp_points3:
                if r2 < p[0]:
                    r2=p[0]
                    right2 = p
            
            right = None
            
            if right1[1]<right2[1]:
                right = right1
            else:
                right = right2  
            
            print("right1,right2",file=sys.stderr)
            print(right1,right2,file=sys.stderr)
            
            print("left,right",file=sys.stderr)
            print(left,right,file=sys.stderr)
            x1=int(left[0])
            if(x1>5470):
                x1=5470
            y1=int(3648.0-(left[1]))
            if(y1<0):
                y1=0
                
            x2=int(right[0])+80
            if(x2>5470):
                x2=5470
            y2=int(3648.0-(right[1]))
            if(y2<0):
                y2=0
            
            print("x1,y1,x2, y2",file=sys.stderr)
            print(x1,y1,x2, y2,file=sys.stderr)
            img2 = img.crop((x1, y1, x2, y2))
    
            
            resize_image=img2.resize((2000, 2000), Image.ANTIALIAS)
            resize_image.save('/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/6.jpg', 'JPEG')
            image_png=Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/6.jpg") 
            image_png.save("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/6.png")
        return redirect(url_for('previous_page_edit_2'))
    
    @app.route('/crop_data_7', methods=['GET', 'POST'])
    def crop_data_7():
        img = Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/raw_image/CAMERA7_7.JPG")
        if request.method == "POST":
            data=request.get_json()
            point_1=data['data1'][0]
            point_2=data['data2'][0]
            point_3=data['data3'][0]
            point_4=data['data4'][0]
            print(point_1,file=sys.stderr)
            print(point_2,file=sys.stderr)
            print(point_3,file=sys.stderr)
            print(point_4,file=sys.stderr)
            points=[]
            points.append(point_1)
            points.append(point_2)
            points.append(point_3)
            points.append(point_4)
            
            temp_points = []
            for p in points:
                temp_points.append(p)
                
            l=99999
            left1=None
            for p in temp_points:
                if l > p[0]:
                    l=p[0]
                    left1 = p
            
            temp_points2 = []
            for p in temp_points:
                if(p[0]!=left1[0] and p[1]!=left1[1]):
                    temp_points2.append(p)
            
            l2=99999
            left2=None
            for p in temp_points2:
                if l2 > p[0]:
                    l2=p[0]
                    left2 = p
            
            left = None
            
            print("left1,left2",file=sys.stderr)
            print(left1,left2,file=sys.stderr)
            
            if left1[1]>left2[1]:
                left = left1
            else:
                left = left2
                
            
            r=-1000
            right1=None
            for p in points:
                if r < p[0]:
                    r = p[0]
                    right1 = p
            
            temp_points3 = []
            for p in points:
                if(p[0]!=right1[0] and p[1]!=right1[1]):
                    temp_points3.append(p)
            
            r2=-1000
            right2=None
            for p in temp_points3:
                if r2 < p[0]:
                    r2=p[0]
                    right2 = p
            
            right = None
            
            if right1[1]<right2[1]:
                right = right1
            else:
                right = right2  
            
            print("right1,right2",file=sys.stderr)
            print(right1,right2,file=sys.stderr)
            
            print("left,right",file=sys.stderr)
            print(left,right,file=sys.stderr)
            x1=int(left[0])
            if(x1>5470):
                x1=5470
            y1=int(3648.0-(left[1]))
            if(y1<0):
                y1=0
                
            x2=int(right[0])+80
            if(x2>5470):
                x2=5470
            y2=int(3648.0-(right[1]))
            if(y2<0):
                y2=0
            
            print("x1,y1,x2, y2",file=sys.stderr)
            print(x1,y1,x2, y2,file=sys.stderr)
            img2 = img.crop((x1, y1, x2, y2))
    
            
            resize_image=img2.resize((2000, 2000), Image.ANTIALIAS)
            resize_image.save('/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/7.jpg', 'JPEG')
            image_png=Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/7.jpg") 
            image_png.save("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/7.png")
        return redirect(url_for('previous_page_edit_2'))
    
    @app.route('/crop_data_8', methods=['GET', 'POST'])
    def crop_data_8():
        img = Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/raw_image/CAMERA8_8.JPG")
        if request.method == "POST":
            data=request.get_json()
            point_1=data['data1'][0]
            point_2=data['data2'][0]
            point_3=data['data3'][0]
            point_4=data['data4'][0]
            print(point_1,file=sys.stderr)
            print(point_2,file=sys.stderr)
            print(point_3,file=sys.stderr)
            print(point_4,file=sys.stderr)
            points=[]
            points.append(point_1)
            points.append(point_2)
            points.append(point_3)
            points.append(point_4)
            
            temp_points = []
            for p in points:
                temp_points.append(p)
                
            l=99999
            left1=None
            for p in temp_points:
                if l > p[0]:
                    l=p[0]
                    left1 = p
            
            temp_points2 = []
            for p in temp_points:
                if(p[0]!=left1[0] and p[1]!=left1[1]):
                    temp_points2.append(p)
            
            l2=99999
            left2=None
            for p in temp_points2:
                if l2 > p[0]:
                    l2=p[0]
                    left2 = p
            
            left = None
            
            print("left1,left2",file=sys.stderr)
            print(left1,left2,file=sys.stderr)
            
            if left1[1]>left2[1]:
                left = left1
            else:
                left = left2
                
            
            r=-1000
            right1=None
            for p in points:
                if r < p[0]:
                    r = p[0]
                    right1 = p
            
            temp_points3 = []
            for p in points:
                if(p[0]!=right1[0] and p[1]!=right1[1]):
                    temp_points3.append(p)
            
            r2=-1000
            right2=None
            for p in temp_points3:
                if r2 < p[0]:
                    r2=p[0]
                    right2 = p
            
            right = None
            
            if right1[1]<right2[1]:
                right = right1
            else:
                right = right2  
            
            print("right1,right2",file=sys.stderr)
            print(right1,right2,file=sys.stderr)
            
            print("left,right",file=sys.stderr)
            print(left,right,file=sys.stderr)
            x1=int(left[0])
            if(x1>5470):
                x1=5470
            y1=int(3648.0-(left[1]))
            if(y1<0):
                y1=0
                
            x2=int(right[0])+80
            if(x2>5470):
                x2=5470
            y2=int(3648.0-(right[1]))
            if(y2<0):
                y2=0
            
            print("x1,y1,x2, y2",file=sys.stderr)
            print(x1,y1,x2, y2,file=sys.stderr)
            img2 = img.crop((x1, y1, x2, y2))
    
            
            resize_image=img2.resize((2000, 2000), Image.ANTIALIAS)
            resize_image.save('/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/8.jpg', 'JPEG')
            image_png=Image.open("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/8.jpg") 
            image_png.save("/Users/wasifaahmed/Documents/FRAS/FRAS_production/static/img_dump/8.png")
        return redirect(url_for('previous_page_edit_2'))
    
    
    @app.route('/test', methods=['GET', 'POST'])       
    def update():   
         mp=0
         gp_1=0
         tyf=0
         txf=0
         f_1=0
         xmpi_1=0
         ympi_1=0
         j_x=None
         j_y=None
         j_mp=None
         up_res_1=None
         mp_inch = []
         x1=[]
         y1=[]
         u_fir_tendency_txt=None
         u_fir_tendency_code=None
         if request.method == "POST":
                            
             
             data1 = request.get_json()
             tx1 =data1['x1'] 
          
             for le in tx1:
                 x1.append(le[0])
                 
             ty1 = data1['y1']
             for le in ty1:
                 y1.append(le[0]) 
            
             points = data1['points']
             mp = mpi(1,points).tolist()
            
             
             mp_inch.append(pixeltoinch(mp[0][0]))
             mp_inch.append(pixeltoinch(mp[0][1]))
             tmpi=mpi(1,points)
             #print("Printing from UPDATE...", file=sys.stderr)
             #print(tmpi, file=sys.stderr)
             xmpi_1 = tmpi[0][0]
             ympi_1 = tmpi[0][1]
             
             session['tmpi']=mp
             f_1,txf_list,tyf_list  =firing_tendancy(1000, 1000 , xmpi_1, ympi_1)
             txf=txf_list
             tyf=tyf_list
             j_x=pd.Series(txf).to_json(orient='values')
             j_y=pd.Series(tyf).to_json(orient='values')
             print("this is inside upadate",file=sys.stderr)
             print(txf,file=sys.stderr)
             gp_1 = grouping_length(0 , 0 , x1 , y1)
             up_res_1=getresulttext(gp_1)
             u_fir_tendency_txt,u_fir_tendency_code = getfiringtendencytext(f_1,txf_list,tyf_list)
             session['x1'] = data1['x1']
             session ['y1'] = data1['y1']
             print("session.get('x1')",file=sys.stderr)
             print(session.get('x1'),file=sys.stderr)
             session['tf_u_1']=f_1
             session['gp_u_1']=gp_1
             session ['res_u_1']=up_res_1
             session ['tfirer_x1']=u_fir_tendency_txt
             session ['tfirer_y1']=u_fir_tendency_code
             session ['tfirer_x1_f']=txf
             session ['tfirer_y1_f']=tyf
             
         return jsonify(mp = mp_inch ,
                        gp_1=gp_1,
                        ten_yu=j_y,
                        ten_xu=j_x,
                        result=up_res_1,
                        u_fir_tendency=u_fir_tendency_txt
                        )
        
         
     

    @app.route('/test_2', methods=['GET', 'POST'])       
    def update_2():
         mp_2=0
         gp_2=0
         tyf_2=0
         txf_2=0
         f_2=0
         xmpi_2=0
         ympi_2=0
         j_x_2=None
         j_y_2=None
         j_mp_2=None
         up_res_2=None
         mp_inch_2 = []
         x2=[]
         y2=[]
         u_fir_tendency_txt_2=None
         u_fir_tendency_code_2=None
         if request.method == "POST":

             
             data1 = request.get_json()
             tx2 =data1['x1'] 
             

             for le in tx2:
                 x2.append(le[0])
                 
             print("x2",file=sys.stderr)
             print(x2,file=sys.stderr)
                 
             ty2 = data1['y1']
             for le in ty2:
                 y2.append(le[0]) 
            
             points = data1['points']
             mp = mpi(1,points).tolist()
            
             
             mp_inch_2.append(pixeltoinch(mp[0][0]))
             mp_inch_2.append(pixeltoinch(mp[0][1]))
             tmpi_2=mpi(1,points)
            
             #print(tmpi, file=sys.stderr)
             xmpi_1 = tmpi_2[0][0]
             ympi_1 = tmpi_2[0][1]
             
             session['tmpi_2']=mp
             f_1,txf_list,tyf_list  =firing_tendancy(1000, 1000 , xmpi_1, ympi_1)
        
        
        
             txf_2=txf_list
             tyf_2=tyf_list
             
          
             
             j_x_2=pd.Series(txf_2).to_json(orient='values')
             j_y_2=pd.Series(tyf_2).to_json(orient='values')
             
             print("calling from update_2" ,file=sys.stderr)
             print(txf_2,file=sys.stderr)
             gp_2 = grouping_length(0 , 0 , x2 , y2)
             up_res_2=getresulttext(gp_2)
             u_fir_tendency_txt_2,u_fir_tendency_code_2 = getfiringtendencytext(f_2,txf_list,tyf_list)
             session['x2'] = data1['x1']
             print(j_x_2, file=sys.stderr)
             
             session ['y2'] = data1['y1']
             session['tf_u_2']=f_1
             session['gp_u_2']=gp_2
             session ['res_u_2']=up_res_2
             session ['tfirer_x2']=u_fir_tendency_txt_2
             session ['tfirer_y2']=u_fir_tendency_code_2
             session ['tfirer_x1_f']=txf_2
             session ['tfirer_y1_f']=tyf_2

             
         return jsonify(mp = mp_inch_2 ,
                        gp_1=gp_2,
                        ten_yu=j_y_2,
                        ten_xu=j_x_2,
                        result=up_res_2,
                        u_fir_tendency=u_fir_tendency_txt_2
                        )

     
    @app.route('/test_3', methods=['GET', 'POST'])       
    def update_3():
         mp_2=0
         gp_2=0
         tyf_2=0
         txf_2=0
         f_2=0
         xmpi_2=0
         ympi_2=0
         j_x_2=None
         j_y_2=None
         j_mp_2=None
         up_res_2=None
         mp_inch_2 = []
         x2=[]
         y2=[]
         u_fir_tendency_txt_2=None
         u_fir_tendency_code_2=None
         if request.method == "POST":

             
             data1 = request.get_json()
             tx2 =data1['x1'] 
             

             for le in tx2:
                 x2.append(le[0])
                 
             print("x2",file=sys.stderr)
             print(x2,file=sys.stderr)
                 
             ty2 = data1['y1']
             for le in ty2:
                 y2.append(le[0]) 
            
             points = data1['points']
             mp = mpi(1,points).tolist()
            
             
             mp_inch_2.append(pixeltoinch(mp[0][0]))
             mp_inch_2.append(pixeltoinch(mp[0][1]))
             tmpi_2=mpi(1,points)
            
             #print(tmpi, file=sys.stderr)
             xmpi_1 = tmpi_2[0][0]
             ympi_1 = tmpi_2[0][1]
             
             session['tmpi_2']=mp
             f_1,txf_list,tyf_list  =firing_tendancy(1000, 1000 , xmpi_1, ympi_1)
        
        
        
             txf_2=txf_list
             tyf_2=tyf_list
             
          
             
             j_x_2=pd.Series(txf_2).to_json(orient='values')
             j_y_2=pd.Series(tyf_2).to_json(orient='values')
             
             print("calling from update_2" ,file=sys.stderr)
             print(txf_2,file=sys.stderr)
             gp_2 = grouping_length(0 , 0 , x2 , y2)
             up_res_2=getresulttext(gp_2)
             u_fir_tendency_txt_2,u_fir_tendency_code_2 = getfiringtendencytext(f_2,txf_list,tyf_list)
             session['x2'] = data1['x1']
             print(j_x_2, file=sys.stderr)
             
             session ['y2'] = data1['y1']
             session['tf_u_2']=f_1
             session['gp_u_2']=gp_2
             session ['res_u_2']=up_res_2
             session ['tfirer_x2']=u_fir_tendency_txt_2
             session ['tfirer_y2']=u_fir_tendency_code_2
             session ['tfirer_x1_f']=txf_2
             session ['tfirer_y1_f']=tyf_2

             
         return jsonify(mp = mp_inch_2 ,
                        gp_1=gp_2,
                        ten_yu=j_y_2,
                        ten_xu=j_x_2,
                        result=up_res_2,
                        u_fir_tendency=u_fir_tendency_txt_2
                        )
     
        
    @app.route('/test_4', methods=['GET', 'POST'])       
    def update_4():
         mp_2=0
         gp_2=0
         tyf_2=0
         txf_2=0
         f_2=0
         xmpi_2=0
         ympi_2=0
         j_x_2=None
         j_y_2=None
         j_mp_2=None
         up_res_2=None
         mp_inch_2 = []
         x2=[]
         y2=[]
         u_fir_tendency_txt_2=None
         u_fir_tendency_code_2=None
         if request.method == "POST":

             
             data1 = request.get_json()
             tx2 =data1['x1'] 
             

             for le in tx2:
                 x2.append(le[0])
                 
             print("x2",file=sys.stderr)
             print(x2,file=sys.stderr)
                 
             ty2 = data1['y1']
             for le in ty2:
                 y2.append(le[0]) 
            
             points = data1['points']
             mp = mpi(1,points).tolist()
            
             
             mp_inch_2.append(pixeltoinch(mp[0][0]))
             mp_inch_2.append(pixeltoinch(mp[0][1]))
             tmpi_2=mpi(1,points)
            
             #print(tmpi, file=sys.stderr)
             xmpi_1 = tmpi_2[0][0]
             ympi_1 = tmpi_2[0][1]
             
             session['tmpi_2']=mp
             f_1,txf_list,tyf_list  =firing_tendancy(1000, 1000 , xmpi_1, ympi_1)
        
        
        
             txf_2=txf_list
             tyf_2=tyf_list
             
          
             
             j_x_2=pd.Series(txf_2).to_json(orient='values')
             j_y_2=pd.Series(tyf_2).to_json(orient='values')
             
             print("calling from update_2" ,file=sys.stderr)
             print(txf_2,file=sys.stderr)
             gp_2 = grouping_length(0 , 0 , x2 , y2)
             up_res_2=getresulttext(gp_2)
             u_fir_tendency_txt_2,u_fir_tendency_code_2 = getfiringtendencytext(f_2,txf_list,tyf_list)
             session['x2'] = data1['x1']
             print(j_x_2, file=sys.stderr)
             
             session ['y2'] = data1['y1']
             session['tf_u_2']=f_1
             session['gp_u_2']=gp_2
             session ['res_u_2']=up_res_2
             session ['tfirer_x2']=u_fir_tendency_txt_2
             session ['tfirer_y2']=u_fir_tendency_code_2
             session ['tfirer_x1_f']=txf_2
             session ['tfirer_y1_f']=tyf_2

             
         return jsonify(mp = mp_inch_2 ,
                        gp_1=gp_2,
                        ten_yu=j_y_2,
                        ten_xu=j_x_2,
                        result=up_res_2,
                        u_fir_tendency=u_fir_tendency_txt_2
                        )
         
         
    @app.route('/test_5', methods=['GET', 'POST'])       
    def update_5():
         mp_2=0
         gp_2=0
         tyf_2=0
         txf_2=0
         f_2=0
         xmpi_2=0
         ympi_2=0
         j_x_2=None
         j_y_2=None
         j_mp_2=None
         up_res_2=None
         mp_inch_2 = []
         x2=[]
         y2=[]
         u_fir_tendency_txt_2=None
         u_fir_tendency_code_2=None
         if request.method == "POST":

             
             data1 = request.get_json()
             tx2 =data1['x1'] 
             

             for le in tx2:
                 x2.append(le[0])
                 
             print("x2",file=sys.stderr)
             print(x2,file=sys.stderr)
                 
             ty2 = data1['y1']
             for le in ty2:
                 y2.append(le[0]) 
            
             points = data1['points']
             mp = mpi(1,points).tolist()
            
             
             mp_inch_2.append(pixeltoinch(mp[0][0]))
             mp_inch_2.append(pixeltoinch(mp[0][1]))
             tmpi_2=mpi(1,points)
            
             #print(tmpi, file=sys.stderr)
             xmpi_1 = tmpi_2[0][0]
             ympi_1 = tmpi_2[0][1]
             
             session['tmpi_2']=mp
             f_1,txf_list,tyf_list  =firing_tendancy(1000, 1000 , xmpi_1, ympi_1)
        
        
        
             txf_2=txf_list
             tyf_2=tyf_list
             
          
             
             j_x_2=pd.Series(txf_2).to_json(orient='values')
             j_y_2=pd.Series(tyf_2).to_json(orient='values')
             
             print("calling from update_2" ,file=sys.stderr)
             print(txf_2,file=sys.stderr)
             gp_2 = grouping_length(0 , 0 , x2 , y2)
             up_res_2=getresulttext(gp_2)
             u_fir_tendency_txt_2,u_fir_tendency_code_2 = getfiringtendencytext(f_2,txf_list,tyf_list)
             session['x2'] = data1['x1']
             print(j_x_2, file=sys.stderr)
             
             session ['y2'] = data1['y1']
             session['tf_u_2']=f_1
             session['gp_u_2']=gp_2
             session ['res_u_2']=up_res_2
             session ['tfirer_x2']=u_fir_tendency_txt_2
             session ['tfirer_y2']=u_fir_tendency_code_2
             session ['tfirer_x1_f']=txf_2
             session ['tfirer_y1_f']=tyf_2

             
         return jsonify(mp = mp_inch_2 ,
                        gp_1=gp_2,
                        ten_yu=j_y_2,
                        ten_xu=j_x_2,
                        result=up_res_2,
                        u_fir_tendency=u_fir_tendency_txt_2
                        )
        
    @app.route('/test_6', methods=['GET', 'POST'])       
    def update_6():
         mp_2=0
         gp_2=0
         tyf_2=0
         txf_2=0
         f_2=0
         xmpi_2=0
         ympi_2=0
         j_x_2=None
         j_y_2=None
         j_mp_2=None
         up_res_2=None
         mp_inch_2 = []
         x2=[]
         y2=[]
         u_fir_tendency_txt_2=None
         u_fir_tendency_code_2=None
         if request.method == "POST":

             
             data1 = request.get_json()
             tx2 =data1['x1'] 
             

             for le in tx2:
                 x2.append(le[0])
                 
             print("x2",file=sys.stderr)
             print(x2,file=sys.stderr)
                 
             ty2 = data1['y1']
             for le in ty2:
                 y2.append(le[0]) 
            
             points = data1['points']
             mp = mpi(1,points).tolist()
            
             
             mp_inch_2.append(pixeltoinch(mp[0][0]))
             mp_inch_2.append(pixeltoinch(mp[0][1]))
             tmpi_2=mpi(1,points)
            
             #print(tmpi, file=sys.stderr)
             xmpi_1 = tmpi_2[0][0]
             ympi_1 = tmpi_2[0][1]
             
             session['tmpi_2']=mp
             f_1,txf_list,tyf_list  =firing_tendancy(1000, 1000 , xmpi_1, ympi_1)
        
        
        
             txf_2=txf_list
             tyf_2=tyf_list
             
          
             
             j_x_2=pd.Series(txf_2).to_json(orient='values')
             j_y_2=pd.Series(tyf_2).to_json(orient='values')
             
             print("calling from update_2" ,file=sys.stderr)
             print(txf_2,file=sys.stderr)
             gp_2 = grouping_length(0 , 0 , x2 , y2)
             up_res_2=getresulttext(gp_2)
             u_fir_tendency_txt_2,u_fir_tendency_code_2 = getfiringtendencytext(f_2,txf_list,tyf_list)
             session['x2'] = data1['x1']
             print(j_x_2, file=sys.stderr)
             
             session ['y2'] = data1['y1']
             session['tf_u_2']=f_1
             session['gp_u_2']=gp_2
             session ['res_u_2']=up_res_2
             session ['tfirer_x2']=u_fir_tendency_txt_2
             session ['tfirer_y2']=u_fir_tendency_code_2
             session ['tfirer_x1_f']=txf_2
             session ['tfirer_y1_f']=tyf_2

             
         return jsonify(mp = mp_inch_2 ,
                        gp_1=gp_2,
                        ten_yu=j_y_2,
                        ten_xu=j_x_2,
                        result=up_res_2,
                        u_fir_tendency=u_fir_tendency_txt_2
                        )
         
    @app.route('/test_7', methods=['GET', 'POST'])       
    def update_7():
         mp_2=0
         gp_2=0
         tyf_2=0
         txf_2=0
         f_2=0
         xmpi_2=0
         ympi_2=0
         j_x_2=None
         j_y_2=None
         j_mp_2=None
         up_res_2=None
         mp_inch_2 = []
         x2=[]
         y2=[]
         u_fir_tendency_txt_2=None
         u_fir_tendency_code_2=None
         if request.method == "POST":

             
             data1 = request.get_json()
             tx2 =data1['x1'] 
             

             for le in tx2:
                 x2.append(le[0])
                 
             print("x2",file=sys.stderr)
             print(x2,file=sys.stderr)
                 
             ty2 = data1['y1']
             for le in ty2:
                 y2.append(le[0]) 
            
             points = data1['points']
             mp = mpi(1,points).tolist()
            
             
             mp_inch_2.append(pixeltoinch(mp[0][0]))
             mp_inch_2.append(pixeltoinch(mp[0][1]))
             tmpi_2=mpi(1,points)
            
             #print(tmpi, file=sys.stderr)
             xmpi_1 = tmpi_2[0][0]
             ympi_1 = tmpi_2[0][1]
             
             session['tmpi_2']=mp
             f_1,txf_list,tyf_list  =firing_tendancy(1000, 1000 , xmpi_1, ympi_1)
        
        
        
             txf_2=txf_list
             tyf_2=tyf_list
             
          
             
             j_x_2=pd.Series(txf_2).to_json(orient='values')
             j_y_2=pd.Series(tyf_2).to_json(orient='values')
             
             print("calling from update_2" ,file=sys.stderr)
             print(txf_2,file=sys.stderr)
             gp_2 = grouping_length(0 , 0 , x2 , y2)
             up_res_2=getresulttext(gp_2)
             u_fir_tendency_txt_2,u_fir_tendency_code_2 = getfiringtendencytext(f_2,txf_list,tyf_list)
             session['x2'] = data1['x1']
             print(j_x_2, file=sys.stderr)
             
             session ['y2'] = data1['y1']
             session['tf_u_2']=f_1
             session['gp_u_2']=gp_2
             session ['res_u_2']=up_res_2
             session ['tfirer_x2']=u_fir_tendency_txt_2
             session ['tfirer_y2']=u_fir_tendency_code_2
             session ['tfirer_x1_f']=txf_2
             session ['tfirer_y1_f']=tyf_2

             
         return jsonify(mp = mp_inch_2 ,
                        gp_1=gp_2,
                        ten_yu=j_y_2,
                        ten_xu=j_x_2,
                        result=up_res_2,
                        u_fir_tendency=u_fir_tendency_txt_2
                        )
         
         
         
    @app.route('/test_8', methods=['GET', 'POST'])       
    def update_8():
         mp_2=0
         gp_2=0
         tyf_2=0
         txf_2=0
         f_2=0
         xmpi_2=0
         ympi_2=0
         j_x_2=None
         j_y_2=None
         j_mp_2=None
         up_res_2=None
         mp_inch_2 = []
         x2=[]
         y2=[]
         u_fir_tendency_txt_2=None
         u_fir_tendency_code_2=None
         if request.method == "POST":

             
             data1 = request.get_json()
             tx2 =data1['x1'] 
             

             for le in tx2:
                 x2.append(le[0])
                 
             print("x2",file=sys.stderr)
             print(x2,file=sys.stderr)
                 
             ty2 = data1['y1']
             for le in ty2:
                 y2.append(le[0]) 
            
             points = data1['points']
             mp = mpi(1,points).tolist()
            
             
             mp_inch_2.append(pixeltoinch(mp[0][0]))
             mp_inch_2.append(pixeltoinch(mp[0][1]))
             tmpi_2=mpi(1,points)
            
             #print(tmpi, file=sys.stderr)
             xmpi_1 = tmpi_2[0][0]
             ympi_1 = tmpi_2[0][1]
             
             session['tmpi_2']=mp
             f_1,txf_list,tyf_list  =firing_tendancy(1000, 1000 , xmpi_1, ympi_1)
        
        
        
             txf_2=txf_list
             tyf_2=tyf_list
             
          
             
             j_x_2=pd.Series(txf_2).to_json(orient='values')
             j_y_2=pd.Series(tyf_2).to_json(orient='values')
             
             print("calling from update_2" ,file=sys.stderr)
             print(txf_2,file=sys.stderr)
             gp_2 = grouping_length(0 , 0 , x2 , y2)
             up_res_2=getresulttext(gp_2)
             u_fir_tendency_txt_2,u_fir_tendency_code_2 = getfiringtendencytext(f_2,txf_list,tyf_list)
             session['x2'] = data1['x1']
             print(j_x_2, file=sys.stderr)
             
             session ['y2'] = data1['y1']
             session['tf_u_2']=f_1
             session['gp_u_2']=gp_2
             session ['res_u_2']=up_res_2
             session ['tfirer_x2']=u_fir_tendency_txt_2
             session ['tfirer_y2']=u_fir_tendency_code_2
             session ['tfirer_x1_f']=txf_2
             session ['tfirer_y1_f']=tyf_2

             
         return jsonify(mp = mp_inch_2 ,
                        gp_1=gp_2,
                        ten_yu=j_y_2,
                        ten_xu=j_x_2,
                        result=up_res_2,
                        u_fir_tendency=u_fir_tendency_txt_2
                        )
    
    @app.route('/detail_summary', methods=['GET', 'POST'])     
    def detail_summary():
        curdate=time.strftime("%Y-%m-%d")
        shooting_1=db.session.query(TShooting.target_1_id).scalar()
        shooting_2=db.session.query(TShooting.target_2_id).scalar()
        shooting_3=db.session.query(TShooting.target_3_id).scalar()
        shooting_4=db.session.query(TShooting.target_4_id).scalar()        
        shooting_5=db.session.query(TShooting.target_5_id).scalar()
        shooting_6=db.session.query(TShooting.target_6_id).scalar()
        shooting_7=db.session.query(TShooting.target_7_id).scalar()
        shooting_8=db.session.query(TShooting.target_8_id).scalar()
        
        
        detail_no=db.session.query(TShooting.detail_no).scalar()
        set_no=db.session.query(TShooting.set_no).scalar()
        session_no=db.session.query(TShooting.session_id).scalar()
        paper_ref=db.session.query(TShooting.paper_ref).distinct().scalar()
        
        shooter_name_1 =db.session.query(Shooter.name).filter(Shooter.id==shooting_1).scalar()
        shooter_name_1 = make_empty_string_if_needed(shooter_name_1)
        shooter_no_1 =db.session.query(Shooter.service_id).filter(Shooter.id==shooting_1).scalar()
        shooter_no_1 = make_empty_string_if_needed(str(shooter_no_1))
        result_1=db.session.query(Grouping.result).filter(
                                Grouping.firer_id==shooting_1,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref
                              
                                ).scalar()
        result_1 = make_empty_string_if_needed(result_1)
        
        gp_1=db.session.query(Grouping.grouping_length_f).filter(
                                Grouping.firer_id==shooting_1,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref
                                
                                ).scalar()
        gp_1 = make_empty_string_if_needed(str(gp_1))
        
        mpi_x_1=db.session.query(MPI.f_mpi_x).filter(
                                MPI.firer_id==shooting_1,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref
                                
                                ).scalar()
        mpi_x_1=make_empty_string_if_needed(str(mpi_x_1))
        
        mpi_y_1=db.session.query(MPI.f_mpi_y).filter(
                                MPI.firer_id==shooting_1,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref
                                
                                ).scalar()
        mpi_y_1 = make_empty_string_if_needed(str(mpi_y_1))
        
        ten_1=db.session.query(MPI.tendency_text).filter(
                                MPI.firer_id==shooting_1,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                               
                                ).scalar()
        ten_1 = make_empty_string_if_needed(ten_1)
        
        shooter_name_2 =db.session.query(Shooter.name).filter(Shooter.id==shooting_2).scalar()
        shooter_name_2 = make_empty_string_if_needed(shooter_name_2)
        shooter_no_2 =db.session.query(Shooter.service_id).filter(Shooter.id==shooting_2).scalar()
        shooter_no_2 = make_empty_string_if_needed(str(shooter_no_2))
        result_2=db.session.query(Grouping.result).filter(
                                Grouping.firer_id==shooting_2,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                               
                                ).scalar()
        result_2 = make_empty_string_if_needed(result_2)
        
        gp_2=db.session.query(Grouping.grouping_length_f).filter(
                                Grouping.firer_id==shooting_2,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                               
                                ).scalar()
        gp_2 = make_empty_string_if_needed(str(gp_2))
        
        mpi_x_2=db.session.query(MPI.f_mpi_x).filter(
                                MPI.firer_id==shooting_2,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                
                                ).scalar()
        mpi_x_2=make_empty_string_if_needed(str(mpi_x_2))
        
        mpi_y_2=db.session.query(MPI.f_mpi_y).filter(
                                MPI.firer_id==shooting_2,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                
                                ).scalar()
        mpi_y_2 = make_empty_string_if_needed(str(mpi_y_2))
        
        ten_2=db.session.query(MPI.tendency_text).filter(
                                MPI.firer_id==shooting_2,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                
                                ).scalar()
        ten_2 = make_empty_string_if_needed(ten_2)
        
        shooter_name_3 =db.session.query(Shooter.name).filter(Shooter.id==shooting_3).scalar()
        shooter_name_3 = make_empty_string_if_needed(shooter_name_3)
        shooter_no_3 =db.session.query(Shooter.service_id).filter(Shooter.id==shooting_3).scalar()
        shooter_no_3 = make_empty_string_if_needed(str(shooter_no_3))
        result_3=db.session.query(Grouping.result).filter(
                                Grouping.firer_id==shooting_3,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                
                                ).scalar()
        result_3 = make_empty_string_if_needed(result_3)
        
        gp_3=db.session.query(Grouping.grouping_length_f).filter(
                                Grouping.firer_id==shooting_3,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                
                                ).scalar()
        gp_3 = make_empty_string_if_needed(str(gp_3))
        
        mpi_x_3=db.session.query(MPI.f_mpi_x).filter(
                                MPI.firer_id==shooting_3,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                MPI.target_no==3
                                ).scalar()
        mpi_x_3=make_empty_string_if_needed(str(mpi_x_3))
        
        mpi_y_3=db.session.query(MPI.f_mpi_y).filter(
                                MPI.firer_id==shooting_3,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        mpi_y_3 = make_empty_string_if_needed(str(mpi_y_3))
        
        ten_3=db.session.query(MPI.tendency_text).filter(
                                MPI.firer_id==shooting_3,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        ten_3 = make_empty_string_if_needed(ten_3)
        
        shooter_name_4 =db.session.query(Shooter.name).filter(Shooter.id==shooting_4).scalar()
        shooter_name_4 = make_empty_string_if_needed(shooter_name_4)
        shooter_no_4 =db.session.query(Shooter.service_id).filter(Shooter.id==shooting_4).scalar()
        shooter_no_4 = make_empty_string_if_needed(str(shooter_no_4))
        result_4=db.session.query(Grouping.result).filter(
                                Grouping.firer_id==shooting_4,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                ).scalar()
        result_4 = make_empty_string_if_needed(result_4)
        
        gp_4=db.session.query(Grouping.grouping_length_f).filter(
                                Grouping.firer_id==shooting_4,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                ).scalar()
        gp_4 = make_empty_string_if_needed(str(gp_4))
        
        mpi_x_4=db.session.query(MPI.f_mpi_x).filter(
                                MPI.firer_id==shooting_4,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        mpi_x_4=make_empty_string_if_needed(str(mpi_x_4))
        
        mpi_y_4=db.session.query(MPI.f_mpi_y).filter(
                                MPI.firer_id==shooting_4,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        mpi_y_4 = make_empty_string_if_needed(str(mpi_y_4))
        
        ten_4=db.session.query(MPI.tendency_text).filter(
                                MPI.firer_id==shooting_4,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        ten_4 = make_empty_string_if_needed(ten_4)
        
        shooter_name_5 =db.session.query(Shooter.name).filter(Shooter.id==shooting_5).scalar()
        shooter_name_5 = make_empty_string_if_needed(shooter_name_5)
        shooter_no_5 =db.session.query(Shooter.service_id).filter(Shooter.id==shooting_5).scalar()
        shooter_no_5 = make_empty_string_if_needed(str(shooter_no_5))
        result_5=db.session.query(Grouping.result).filter(
                                Grouping.firer_id==shooting_5,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                ).scalar()
        result_5 = make_empty_string_if_needed(result_5)
        
        gp_5=db.session.query(Grouping.grouping_length_f).filter(
                                Grouping.firer_id==shooting_5,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                ).scalar()
        gp_5 = make_empty_string_if_needed(str(gp_5))
        
        mpi_x_5=db.session.query(MPI.f_mpi_x).filter(
                                MPI.firer_id==shooting_5,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        mpi_x_5=make_empty_string_if_needed(str(mpi_x_5))
        
        mpi_y_5=db.session.query(MPI.f_mpi_y).filter(
                                MPI.firer_id==shooting_5,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        mpi_y_5 = make_empty_string_if_needed(str(mpi_y_5))
        
        ten_5=db.session.query(MPI.tendency_text).filter(
                                MPI.firer_id==shooting_5,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        ten_5 = make_empty_string_if_needed(ten_5)
        
        
        shooter_name_6 =db.session.query(Shooter.name).filter(Shooter.id==shooting_6).scalar()
        shooter_name_6 = make_empty_string_if_needed(shooter_name_6)
        shooter_no_6 =db.session.query(Shooter.service_id).filter(Shooter.id==shooting_6).scalar()
        shooter_no_6 = make_empty_string_if_needed(str(shooter_no_6))
        result_6=db.session.query(Grouping.result).filter(
                                Grouping.firer_id==shooting_6,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                ).scalar()
        result_6 = make_empty_string_if_needed(result_6)
        
        gp_6=db.session.query(Grouping.grouping_length_f).filter(
                                Grouping.firer_id==shooting_6,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                ).scalar()
        gp_6 = make_empty_string_if_needed(str(gp_6))
        
        mpi_x_6=db.session.query(MPI.f_mpi_x).filter(
                                MPI.firer_id==shooting_6,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        mpi_x_6=make_empty_string_if_needed(str(mpi_x_6))
        
        mpi_y_6=db.session.query(MPI.f_mpi_y).filter(
                                MPI.firer_id==shooting_6,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        mpi_y_6 = make_empty_string_if_needed(str(mpi_y_6))
        
        ten_6=db.session.query(MPI.tendency_text).filter(
                                MPI.firer_id==shooting_6,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        ten_6 = make_empty_string_if_needed(ten_6)
        
        shooter_name_7 =db.session.query(Shooter.name).filter(Shooter.id==shooting_7).scalar()
        shooter_name_7 = make_empty_string_if_needed(shooter_name_7)
        shooter_no_7 =db.session.query(Shooter.service_id).filter(Shooter.id==shooting_7).scalar()
        shooter_no_7 = make_empty_string_if_needed(str(shooter_no_7))
        result_7=db.session.query(Grouping.result).filter(
                                Grouping.firer_id==shooting_7,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                ).scalar()
        result_7 = make_empty_string_if_needed(result_7)
        
        gp_7=db.session.query(Grouping.grouping_length_f).filter(
                                Grouping.firer_id==shooting_7,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                ).scalar()
        gp_7 = make_empty_string_if_needed(str(gp_7))
        
        mpi_x_7=db.session.query(MPI.f_mpi_x).filter(
                                MPI.firer_id==shooting_7,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        mpi_x_7=make_empty_string_if_needed(str(mpi_x_7))
        
        mpi_y_7=db.session.query(MPI.f_mpi_y).filter(
                                MPI.firer_id==shooting_7,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        mpi_y_7 = make_empty_string_if_needed(str(mpi_y_7))
        
        ten_7=db.session.query(MPI.tendency_text).filter(
                                MPI.firer_id==shooting_7,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        ten_7 = make_empty_string_if_needed(ten_7)
        
        shooter_name_8 =db.session.query(Shooter.name).filter(Shooter.id==shooting_8).scalar()
        shooter_name_8 = make_empty_string_if_needed(shooter_name_8)
        shooter_no_8 =db.session.query(Shooter.service_id).filter(Shooter.id==shooting_8).scalar()
        shooter_no_8 = make_empty_string_if_needed(str(shooter_no_8))
        result_8=db.session.query(Grouping.result).filter(
                                Grouping.firer_id==shooting_8,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                ).scalar()
        result_8 = make_empty_string_if_needed(result_8)
        
        gp_8=db.session.query(Grouping.grouping_length_f).filter(
                                Grouping.firer_id==shooting_8,
                                Grouping.date==curdate,
                                Grouping.session_id==session_no,
                                Grouping.detail_no==detail_no,
                                Grouping.spell_no==set_no,
                                Grouping.paper_ref==paper_ref,
                                ).scalar()
        gp_8 = make_empty_string_if_needed(str(gp_8))
        
        mpi_x_8=db.session.query(MPI.f_mpi_x).filter(
                                MPI.firer_id==shooting_8,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        mpi_x_8=make_empty_string_if_needed(str(mpi_x_8))
        
        mpi_y_8=db.session.query(MPI.f_mpi_y).filter(
                                MPI.firer_id==shooting_8,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        mpi_y_8 = make_empty_string_if_needed(str(mpi_y_8))
        
        ten_8=db.session.query(MPI.tendency_text).filter(
                                MPI.firer_id==shooting_8,
                                MPI.date==curdate,
                                MPI.session_id==session_no,
                                MPI.detail_no==detail_no,
                                MPI.spell_no==set_no,
                                MPI.paper_ref==paper_ref,
                                ).scalar()
        ten_8 = make_empty_string_if_needed(ten_8)
        
        
        return render_template('pages/detail_summary.html',
                               shooter_name_1=shooter_name_1,
                               shooter_no_1=shooter_no_1,
                               result_1=result_1,
                               gp_1=gp_1,
                               mpi_x_1=mpi_x_1,
                               mpi_y_1=mpi_y_1,
                               ten_1=ten_1,
                               
                               shooter_name_2=shooter_name_2,
                               shooter_no_2=shooter_no_2,
                               result_2=result_2,
                               gp_2=gp_2,
                               mpi_x_2=mpi_x_2,
                               mpi_y_2=mpi_y_2,
                               ten_2=ten_2,
                               
                               shooter_name_3=shooter_name_3,
                               shooter_no_3=shooter_no_3,
                               result_3=result_3,
                               gp_3=gp_3,
                               mpi_x_3=mpi_x_3,
                               mpi_y_3=mpi_y_3,
                               ten_3=ten_3,
                               
                               shooter_name_4=shooter_name_4,
                               shooter_no_4=shooter_no_4,
                               result_4=result_4,
                               gp_4=gp_4,
                               mpi_x_4=mpi_x_4,
                               mpi_y_4=mpi_y_4,
                               ten_4=ten_4,
                               
                               shooter_name_5=shooter_name_5,
                               shooter_no_5=shooter_no_5,
                               result_5=result_5,
                               gp_5=gp_5,
                               mpi_x_5=mpi_x_5,
                               mpi_y_5=mpi_y_5,
                               ten_5=ten_5,
                               
                               shooter_name_6=shooter_name_6,
                               shooter_no_6=shooter_no_6,
                               result_6=result_6,
                               gp_6=gp_6,
                               mpi_x_6=mpi_x_6,
                               mpi_y_6=mpi_y_6,
                               ten_6=ten_6,
                               
                               shooter_name_7=shooter_name_7,
                               shooter_no_7=shooter_no_7,
                               result_7=result_7,
                               gp_7=gp_7,
                               mpi_x_7=mpi_x_7,
                               mpi_y_7=mpi_y_7,
                               ten_7=ten_7,
                               
                               shooter_name_8=shooter_name_8,
                               shooter_no_8=shooter_no_8,
                               result_8=result_8,
                               gp_8=gp_8,
                               mpi_x_8=mpi_x_8,
                               mpi_y_8=mpi_y_8,
                               ten_8=ten_8
                               )
        
    
    @app.route('/firer_detail_report', methods=['GET', 'POST'])
    def firer_detail_report():
        firer = [row.service_id for row in Shooter.query.all()]
        if request.method=='POST':
            r=request.form['tag']
            firer_id=db.session.query(Shooter.id).filter(Shooter.service_id==r).scalar()
            firer_name=db.session.query(Shooter.name).filter(Shooter.service_id==r).scalar()
            firer_brigade=db.session.query(Shooter.brigade).filter(Shooter.service_id==r).scalar()
            firer_unit=db.session.query(Shooter.unit).filter(Shooter.service_id==r).scalar()
            firer_rank_id=db.session.query(Shooter.rank_id).filter(Shooter.service_id==r).scalar()
            rank=db.session.query(Rank.name).filter(Rank.id==firer_rank_id).scalar()
            cant_id = db.session.query(Shooter.cantonment_id).filter(Shooter.service_id==r).scalar()
            cant_name=db.session.query(Cantonment.cantonment).filter(Cantonment.id==cant_id).scalar()
            div_name=db.session.query(Cantonment.division).filter(Cantonment.id==cant_id).scalar()
            gp_g=db.session.query(Grouping.date,Grouping.detail_no,
                                  Grouping.result,Grouping.grouping_length_f,MPI.tendency_text).filter(Grouping.firer_id==firer_id,
                                                                                              MPI.firer_id==firer_id,
                                                                                              Grouping.firer_id==MPI.firer_id,
                                                                                              Grouping.detail_no==MPI.detail_no,
                                                                                              Grouping.target_no==MPI.target_no,
                                                                                              Grouping.spell_no==MPI.spell_no,
                                                                                              Grouping.paper_ref==MPI.paper_ref,
                                                                                              Grouping.date==MPI.date
                                                                                                  
                                                                                                    ).all()
            print(gp_g,file=sys.stderr)
            return render_template('pages/firer_detail_report.html' , firer=firer, gp_g=gp_g,rank=rank,r=r,firer_name=firer_name,firer_brigade=firer_brigade,firer_unit=firer_unit,cant_name=cant_name, div_name= div_name)
        return render_template('pages/firer_detail_report.html' , firer=firer)
    
    @app.route('/montly_session_summary', methods=['GET', 'POST'])
    def montly_session_summary():
        form=MonthlyReportForm()
        session_detail=None
        table_box=[]
        distinct_army_num_arr=[]
        distinct_detail_num_arr=[]
        try:
            if request.method == 'POST':
                date=form.start_time.data
                print("date",file=sys.stderr)
                print(date,file=sys.stderr)
                detail_no=db.session.query(Grouping.detail_no).filter(Grouping.date==date).all()
                firer_no=db.session.query(Grouping.firer_id).filter(Grouping.date==date).all()
                session_detail=db.session.query(Shooter.service_id,Shooter.name,
                                               Grouping.detail_no,
                                               Grouping.result,
                                               Grouping.grouping_length_f).filter(
                               Shooter.id==Grouping.firer_id,
                               Grouping.date==date
                               ).all()
               
                distinct_detail_num=db.session.query(Session_Detail.detail_no).filter(
                        Session_Detail.date==date ).distinct(Session_Detail.detail_no).all()
                
                for e in distinct_detail_num:
                    for e4 in e:
                        distinct_detail_num_arr.append(e4)
                
                distinct_army_num=db.session.query(Shooter.service_id).filter(
                               Shooter.id==Grouping.firer_id,
                               Session_Detail.date==date,
                               Grouping.date==date
                               ).distinct(Shooter.service_id).all()
                for e5 in distinct_army_num:
                    for e6 in e5:
                        distinct_army_num_arr.append(e6)
                
                for tarmy_no in distinct_army_num_arr:
                    box_line = []
                    box_line.append(tarmy_no)
                    tfirer_name=db.session.query(Shooter.name).filter(Shooter.service_id==tarmy_no).scalar()
                    tfirer_brigade=db.session.query(Shooter.brigade).filter(Shooter.service_id==tarmy_no).scalar()
                    tfirer_unit=db.session.query(Shooter.unit).filter(Shooter.service_id==tarmy_no).scalar()
                    cant_id=db.session.query(Shooter.cantonment_id).filter(Shooter.service_id==tarmy_no).scalar()
                    cantonment=db.session.query(Cantonment.cantonment).filter(Cantonment.id==cant_id).scalar()
                    div=db.session.query(Cantonment.division).filter(Cantonment.id==cant_id).scalar()
                    rank_id=db.session.query(Shooter.rank_id).filter(Shooter.service_id==tarmy_no).scalar()
                    tfirer_rank=db.session.query(Rank.name).filter(Rank.id==rank_id).scalar()
                    print(tfirer_rank,file=sys.stderr)
                    box_line.append(tfirer_name)
                    box_line.append(tfirer_rank)
                    box_line.append(cantonment)
                    box_line.append(div)
                    box_line.append(tfirer_brigade)
                    box_line.append(tfirer_unit)
                    for tdetail_no in distinct_detail_num_arr:
                        
                        tdetail_data = get_a_line_for_box(session_detail, tarmy_no, tdetail_no)
                        for te in tdetail_data:
                            box_line.append(te)
                    
                    table_box.append(box_line)
                    
                print("---------")
                print(table_box)    
        except Exception as e:
            return render_template('errors/monthly_session_error.html')
        return render_template('pages/monthly_session_summary.html',form=form,detail_no_f=distinct_detail_num_arr,box =table_box )
   
    @app.route('/session_summary', methods=['GET', 'POST'])
    def session_summary():
        curdate=time.strftime("%Y-%m-%d")
        s_no=db.session.query(Shooting_Session.session_no).all()
        session_detail=None
        table_box=[]
        s_arr=[]
        distinct_army_num_arr=[]
        distinct_detail_num_arr=[]

        for ele in s_no:
            for ele2 in ele:
                s_arr.append(ele2)
                     
        if request.method == 'POST':
            no = request.form.get('comp_select4')
            detail_no=db.session.query(Session_Detail.detail_no).filter(Session_Detail.session_id==no).all()
            firer_no=db.session.query(Grouping.firer_id).filter(Grouping.session_id==no).all()
            
            session_detail=db.session.query(Shooter.service_id,
                                           Shooter.name,
                                           Grouping.detail_no,
                                           Grouping.result,
                                           Grouping.grouping_length_f).filter(
                           Shooter.id==Grouping.firer_id,
                           Grouping.session_id==no
                           ).all()
                       
   
        
            distinct_detail_num=db.session.query(Session_Detail.detail_no).filter(
                           Session_Detail.session_id==no ).distinct(Session_Detail.detail_no).all()
            
            for e in distinct_detail_num:
                for e4 in e:
                    distinct_detail_num_arr.append(e4)
                
            
            distinct_army_num=db.session.query(Shooter.service_id).filter(
                           Shooter.id==Grouping.firer_id,
                           Session_Detail.session_id==no,
                           Grouping.session_id==no
                           ).distinct(Shooter.service_id).all()
            
            
            for e5 in distinct_army_num:
                for e6 in e5:
                    distinct_army_num_arr.append(e6)
            
            
            
            for tarmy_no in distinct_army_num_arr:
                box_line = []
                box_line.append(tarmy_no)
                tfirer_name=db.session.query(Shooter.name).filter(Shooter.service_id==tarmy_no).scalar()
                tfirer_brigade=db.session.query(Shooter.brigade).filter(Shooter.service_id==tarmy_no).scalar()
                tfirer_unit=db.session.query(Shooter.unit).filter(Shooter.service_id==tarmy_no).scalar()
                cant_id=db.session.query(Shooter.cantonment_id).filter(Shooter.service_id==tarmy_no).scalar()
                cantonment=db.session.query(Cantonment.cantonment).filter(Cantonment.id==cant_id).scalar()
                div=db.session.query(Cantonment.division).filter(Cantonment.id==cant_id).scalar()
                rank_id=db.session.query(Shooter.rank_id).filter(Shooter.service_id==tarmy_no).scalar()
                tfirer_rank=db.session.query(Rank.name).filter(Rank.id==rank_id).scalar()
                print(tfirer_rank)
                box_line.append(tfirer_name)
                box_line.append(tfirer_rank)
                box_line.append(cantonment)
                box_line.append(div)
                box_line.append(tfirer_brigade)
                box_line.append(tfirer_unit)
                for tdetail_no in distinct_detail_num_arr:
                    
                    tdetail_data = get_a_line_for_box(session_detail, tarmy_no, tdetail_no)
                    for te in tdetail_data:
                        box_line.append(te)
                
                table_box.append(box_line)
                    
           
            
        print("---------")
        print(table_box)
        print(distinct_detail_num_arr)
        return render_template('pages/session_summary.html',session=s_arr,detail_no_f=distinct_detail_num_arr,box =table_box )
    

    
    def get_a_line_for_box(qresult, army_no, detail_no):
        new_line = []
        found=False
        
        for line in qresult:
            if(line[2]==detail_no):
                lano = line[0]
                lname = line[1]
                ldno = line[2]
                lre = line[3]
                lgl = line[4]
                if lano == army_no:
                    new_line.append(lre)
                    new_line.append(lgl)
                    found=True
                    
        if(found == False):
            new_line.append('N/A')
            new_line.append('N/A')
 
        return new_line

    
    def predictAsMatrix(image,width,height):
        step=25
        i=0
        resized_array =np.zeros(shape=(width//25,height//25))   
        while i<=height-25:
            j=0 
            while j<=height-25:
                patch = image.crop((i, j, i+25, j+25))
                img1=np.array(patch)
                image_data=color.rgb2gray(img1)
                img_data=merge_datasets(image_data)
                test_data = reformat(img_data)
                patchp=patchIdentification(test_data)
                resized_array[j//25][i//25]=patchp
                j=j+step
            i=i+step
        return resized_array
    
    def make_empty_string_if_needed(v):
        if(v == "999" or v == "NA" or v == "None" or v is None):
            return ""
        return v

    def merge_datasets(img1):
        predict_dataset = make_arrays(1, 25, 25)
        predict_dataset[0:1, :, :] = img1
        return predict_dataset
    
    def make_arrays(nb_rows, image_height, image_width):
        if nb_rows:
            dataset = np.ndarray((nb_rows, image_height, image_width), dtype=np.float32)
        else:
            dataset = None
        return dataset
    
    
    def reformat(dataset):
        dataset = dataset.reshape((-1, 25*25)).astype(np.float32)
        return dataset
    
    
    def patchIdentification(data):
        w1 = graph.get_tensor_by_name("tf_test_image:0")
        feed_dict ={w1:data}
        op_to_restore = graph.get_tensor_by_name("test_prediction_image:0")
        predict= sess.run([op_to_restore],feed_dict=feed_dict)
        array=predict[0][0]
        if(array[0]>array[1]):
            return 0
        else :
            return 1
    
    
    class Graph:
        def __init__(self, row, col, g):
            self.ROW = row
            self.COL = col
            self.graph = g
        
        def isSafe(self, i, j, visited):
            return (i >= 0 and i < self.ROW and
                    j >= 0 and j < self.COL and
                    not visited[i][j] and self.graph[i][j])
             

        def DFS(self, i, j, visited):
            rowNbr = [-1, -1, -1,  0, 0,  1, 1, 1];
            colNbr = [-1,  0,  1, -1, 1, -1, 0, 1];
            visited[i][j] = True
        
            for k in range(8):
                if self.isSafe(i + rowNbr[k], j + colNbr[k], visited):
                    self.DFS(i + rowNbr[k], j + colNbr[k], visited)
                
        def countIslands(self):
            visited = [[False for j in range(self.COL)]for i in range(self.ROW)]
            count = 0
            for i in range(self.ROW):
                for j in range(self.COL):
                    if visited[i][j] == False and self.graph[i][j] ==1:
                        self.DFS(i, j, visited)
                        count += 1
            return count
        
        
    def points(data,h,w):
        i=0
        while (i<h):
            j=0
            while (j<w):
                if(data[i][j]==1):
                    pointsarray.append([i,j])
                j=j+1
            i=i+1
            
    def kmean(N,pointsarray):
        print("---------------------")
        print("pointsarray")
        print(pointsarray)
        n=0
        if (len(pointsarray)==0):
            centroid = 0
        else:
            while (n<=100):
                kmeans = KMeans(n_clusters=N, random_state=0).fit(pointsarray)
                center=kmeans.cluster_centers_ 
                centroid=((kmeans.cluster_centers_)*25)+12
                n=n+1
                return centroid 
        
    def mpi(N,pointsarray):
        n=0
        pointsarrayfiltered=[]
        print('This is pointsarray')
        print(pointsarray)
        
        cen_int=[]
        if(len(pointsarray)<=0):
             cen_int=[[0,0]]
            
        else:
            while (n<=100): 
                kmeans = KMeans(n_clusters=N, random_state=0).fit(pointsarray)
                center=kmeans.cluster_centers_ 
                centroid=(kmeans.cluster_centers_)
                cen_int = centroid.astype(int)
                n=n+1
        return cen_int
        
        
    if __name__ == "__main__":
        load_model()
        app.run()
        
        
    

    
    



    