# -*- coding: utf-8 -*-
from datetime import timedelta
from flask import Flask,session
from flask import render_template,request,redirect,url_for,jsonify
import os
from engine import *
from config.system_info import SystemInfoUtil
from settings import host,port


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(days=7)


@app.route('/')
def index_info():
    process = select_all_process()
    if not process:process=[["","没有在运行的任务","",""]]
    disk_usage = SystemInfoUtil.get_disk_usage()
    virtual_memory = SystemInfoUtil.get_virtual_memory()
    return render_template('index.html',process=process,disk_usage=disk_usage,virtual_memory=virtual_memory)


@app.route('/create',methods=['POST'])
def browser_start():
    url = request.form.get("url")
    name = request.form.get("name")
    try:
        create_browser(url,name)
        session_id, process_name, process_url, datetime,base_url = select_process_name(name)
        result = {'session_id': session_id, 'process_name': process_name,
                  'process_url': process_url, 'datetime': datetime}
        return jsonify(result)
    except:
        return jsonify({"result":0,"detail":"驱动配置错误或任务名已存在"})


@app.route('/xhr',methods=['POST'])
def browser_xhr():
    session_id = request.form.get("session_id")
    process_url = request.form.get("process_url")
    request_url = request.form.get("request_url")
    request_type = request.form.get("request_type")
    formdata = request.form.get("formdata")
    result = carry_browser(session_id,process_url,request_url,request_type,formdata)
    return jsonify({"result":result})


@app.route('/close',methods=['POST'])
def browser_close():
    session_id = request.form.get("session_id")
    process_url = request.form.get("process_url")
    process_name = request.form.get("process_name")
    try:
        close_browser(session_id,process_url,process_name)
        return jsonify({"result":1})
    except:
        return jsonify({"result":0,"detail":"驱动窗口已自动关闭"})


@app.route('/delete/<process_name>',methods=['GET'])
def delete_process_name(process_name):
    try:
        process = select_process_name(process_name)
        close_browser(session_id=process[0],process_url=process[2],process_name=process_name)
    except:
        delete_process(process_name)
        print("delete except: line 70")
    return redirect('/')


if __name__ == '__main__':
    app.run(host=host,port=port,use_reloader=False,debug=True)