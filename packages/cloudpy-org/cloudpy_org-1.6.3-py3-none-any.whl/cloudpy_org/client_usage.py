"""
███████████████████████████client_usage of cloudpy_org███████████████████████████
Copyright © 2023-2024 Cloudpy.org

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Find documentation at https://www.cloudpy.org
"""
from cloudpy_org import aws_framework_manager_client,processing_tools,cloudpy_org_customizable_chatbot,subscription_url,msh
import os
import awswrangler as wr
import pandas as pd
import re
import random as rand
from flask import Flask,render_template,request,jsonify,make_response,redirect
import json
import requests
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from multiprocessing import Process, Queue
import time
import pytz
default_timezone = "US/Central"
scheduler = BackgroundScheduler(timezone=pytz.timezone(default_timezone))
from tqdm import tqdm
import sys
from werkzeug.utils import secure_filename
import PyPDF2
from io import BytesIO
secure_cloudpy_org='https://secure.cloudpy.org'
www_cloudpy_org= 'https://www.cloudpy.org'
default_app = """
app = aws.flask.app
aws.web_portal_id = "@web_portal_id"
aws.set_web_portal_variables()
aws.create_basic_templates()

#***********************LLM related*********************************
@app.route('/co_set_chatbot_context',methods=['POST'])
def co_set_chatbot_context():
    return aws.co_set_chatbot_context()
    
#***********************secure-ttk-auth*********************************
@app.route('/secure',methods=['POST'])
def secure():
    return aws.secure()
@app.route('/ttk',methods=['GET'])
def ttk():
    return aws.ttk()
@app.route('/auth',methods=['GET'])
def auth():
    return aws.auth()
#***********************data interaction*********************************
#______________________________________________________________

@app.route('/send_confirmation_email',methods=['POST'])
def send_confirmation_email():
    return aws.send_confirmation_email()
#______________________________________________________________
@app.route('/confirm_email',methods=['GET'])
def confirm_email():
    return aws.validate_email_confirmation_link()
#______________________________________________________________
@app.route('/store',methods=['POST'])
def store():
    return aws.secure_save_form_data(redirect=False)
#______________________________________________________________
@app.route('/obtain',methods=['POST'])
def obtain():
    return aws.obtain()
#***********************dynamic sites*********************************
@app.route('/register')
def registry():
    return aws.dynamic_site()
@app.route('/register_new_user',methods=['GET'])
def register_new_user():
    return aws.register_new_user()
#______________________________________________________________
@app.route('/resend_confirmation_email')
def resend_confirmation_email():
    return aws.dynamic_site()
#______________________________________________________________
#______________________________________________________________
@app.route('/')
def default():
    return aws.flask.redirect(aws.default_redirect_if_not_authenticated)
#______________________________________________________________
@app.route('/login')
def access():
    return aws.dynamic_site()
@construct_pages
#***********************schedule cron jobs capability*********************************
aws.some_queue = aws.Queue()
def restart_base(restart_pass_phrase:str=None):
    m = "no action taken"
    try:
        if restart_pass_phrase == aws.restart_pass_phrase:
            try:
                aws.some_queue.put("something")
                m = "successfully restarted at " + aws.current_datetime_str()
            except Exception as e:
                print('Error: ',str(e))
        else:
            m = "invalid pwd value"
    except Exception as e: 
        m = "Failed in restart: " + str(e)
    aws.last_restart_message = m
#__________________________________________
@app.route('/restart', methods=['POST'])
def restart():
    json_data = aws.flask.request.json
    if "pwd" in set(json_data.keys()) and json_data["pwd"] != None:
        pwd = json_data["pwd"]
        restart_base(pwd)
        return aws.last_restart_message
    else:
        m = "No pwd provided"
        #aws.logging_it('error',m)
        return m
#__________________________________________
def start_flaskapp(queue):
    aws.some_queue = queue
    restart_schedules = {}
    triggers_list = []
    for k,v in restart_schedules.items():
        triggers_list.append(aws.CronTrigger.from_crontab(v, timezone=conf["default_timezone"]))
    trigger = aws.OrTrigger(triggers_list)
    aws.scheduler.add_job(restart_base, trigger)
    aws.scheduler.start()
    app.run(host='@flask_host',port=@flask_port,debug=@flask_debug)
#__________________________________________
def initiate():
    q = aws.Queue()
    p = aws.Process(target=start_flaskapp, args=(q,))
    p.start()
    while True:
        if q.empty(): 
            aws.time.sleep(1)
        else:
            break
    p.terminate()
    args = [sys.executable] + [sys.argv[0]]
    aws.subprocess.call(args)
"""

this_dict = {}
#___________________________________________________
k = 'select'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label for="@id" class="sensation" id="@id_label" style="@custom_style02">@label_title</label>
<br>
<select action_id="@action_id" action_item="@action_item" k="@k" obj="" isidentifier="@isidentifier" order="@order" enter_key='@enter_key' labelkey="@label_title" id="@id" class="sensation inx" onchange="temp_input(this,'@k','');" onload="">
@options
</select>
<br>
""".replace('@k',k)
this_dict[k]['object'] = "<option style='font-size:15px;padding:5px;'>@object</option>"
this_dict[k]['params'] = ['@id','@label_title','@options']
#___________________________________________________
k = 'radios_horizontal'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<h2 id="@id_radios_title" class="sensation" style="@custom_style02">@label_title</h2>
<br>
<br>
<div>
<a>
@options
</a>
</div>
<br>
""".replace('@k',k)
this_dict[k]['object'] = """&nbsp;&nbsp;&nbsp;
<span style="padding-right:10px;">
<input action_id="@action_id" action_item="@action_item" k="@k" isidentifier="@isidentifier" order="@order" obj="@object" enter_key='@enter_key' labelkey="@label_title" type="radio" name="radio_@id" id="@id_@n" onchecked="temp_input(this,'@k','@object');" onload="">
<label for="@id_@n" class ="sensation" id="@id_@n_label">@object</label>
</span>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@option_1','@option_2']
#___________________________________________________
k = 'radios_vertical'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<h2 id="@id_radios_title" class="sensation" style="@custom_style02">@label_title</h2>
<a>@subtitle</a>
<br>
<br>
<div>
<a>
@options
</a>
</div>
<br>
""".replace('@k',k)
this_dict[k]['object'] = """&nbsp;&nbsp;&nbsp;
<div style="padding-right:10px;">
<input action_id="@action_id" action_item="@action_item" k="@k" isidentifier="@isidentifier" order="@order" obj="@object" labelkey="@label_title" type="radio" name="radio_@id" id="@id_@n" onchecked="temp_input(this,'@k','@object');" onload="">
<label for="@id_@n" class ="sensation" id="@id_@n_label">@object</label>
</div>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@option_1','@option_2']
#___________________________________________________
k = 'num_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation" for="@id" id="@id_label" style="@custom_style02">@label_title</label>
<a>@subtitle</a>
<br>
<input action_id="@action_id" action_item="@action_item" k="@k" obj="" isidentifier="@isidentifier" order="@order" enter_key='@enter_key' labelkey="@label_title" id="@id" class="sensation" us="@us" type="number" value="@text_content" style="border-bottom-width:1px;@custom_style01" oninput="temp_input(this,'@k','');" onload="">
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@text_content']
#___________________________________________________
k = 'text_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation" for="@id" id="@id_label" style="@custom_style02">@label_title</label>
<a>@subtitle</a>
<input action_id="@action_id" action_item="@action_item" k="@k" obj="" isidentifier="@isidentifier" order="@order" enter_key='@enter_key' labelkey="@label_title" id="@id" class="sensation" us="@us" type="text" value="@text_content" style="border-bottom-width:1px;@custom_style01" oninput="temp_input(this,'@k','');" onload="">
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@text_content']
#___________________________________________________
k = 'pwd_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation" for="@id" id="@id_label" style="@custom_style02">@label_title</label>
<a>@subtitle</a>
<input action_id="@action_id" action_item="@action_item" k="@k" obj="" isidentifier="@isidentifier" order="@order" enter_key='@enter_key' labelkey="@label_title" id="@id" class="sensation" type="password" autocomplete="off" cpw="@cpw" cpwconf="@cpwconf" value="@text_content" style="border-bottom-width:1px;@custom_style01" oninput="temp_input(this,'@k','');" onload="" >
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@text_content']
#___________________________________________________
k = 'btn_input'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<br>
<br>
<a class="sensation" id="@id_label" style="display:none;font-size:16px;color:gray;"><a/>
<button action_id="@action_id" action_item="@action_item" id="@id" class="@custom_btn_input_class" event_type='@event_type' style="width:100%;@custom_style01" onclick="temp_input(this,'@k','');" onload="">@label_title</button>
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@text_content']
#___________________________________________________
k = 'text_area'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<label class="sensation" for="@id" id="@id_label" style="@custom_style02">@label_title</label>
<a>@subtitle</a>
<br>
<textarea action_id="@action_id" action_item="@action_item" k="@k" obj="" isidentifier="@isidentifier" order="@order" enter_key='@enter_key' labelkey="@label_title" id="@id" class="sensation inx" rows="@rowsnum" oninput="temp_input(this,'@k','');" onload="" style="@custom_style01">@text_content</textarea>
<br>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@rowsnum']
#___________________________________________________
k = 'acc_checkboxes'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<div action_id="@action_id" action_item="@action_item" class='accordion' id='acc_@id'>
<div class="accordion-item" style="font-size:14px;">
<h2 class="accordion-header" id="@id">
<button class="accordion-button collapsed sensation" style="font-size:14px;padding:7px;" type="button" data-bs-toggle="collapse" 
data-bs-target="#collapse_@id" aria-expanded="false" aria-controls="collapseOne">
<a id="@id_checkboxes_title" style="@custom_style02">@label_title</a>
<a>@subtitle</a>
<a id="@id_counter_container" style="position:absolute;left:@counter_leftpx;color:#252F3E;display:none;"><span id="@id_counter" 
style="padding-right:10px;">0</span><span>selected</span></a>
</button>
</h2>
<div id="collapse_@id" class="accordion-collapse collapse" aria-labelledby="@id" 
data-bs-parent="#acc_@id" style="">
<div id='acc_@id_body' class="accordion-body" style="@custom_style01">
@options
</div></div></div>
</div>
<br>
""".replace('@k',k)
this_dict[k]['object'] = """<div style="padding:7px;"><input isidentifier="@isidentifier" order="@order" labelkey="@label_title" type="checkbox" id="@id_checkbox_@n" onclick="temp_input(this,'@k','');service_counter(this,'@id');" onload=""><label class="sensation" for="@id_checkbox_@n" id="@id_@n_label">@object</label></div>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@options','@n','@counter_left']
#___________________________________________________
k = 'multi_checkboxes'
this_dict[k] = {}
this_dict[k]['html'] = """
<br>
<div action_id="@action_id" action_item="@action_item" class='accordion' id='acc_@id'>
<div class="" style="font-size:14px;">
<h2 class="accordion-header" id="@id">
<div class="sensation" style="font-size:14px;padding:7px;">
<a id="@id_checkboxes_title" style="@custom_style02">@label_title</a>
<a>@subtitle</a>
<a id="@id_counter_container" style="position:absolute;left:@counter_leftpx;color:#252F3E;display:none;"><span id="@id_counter" 
style="padding-right:10px;">0</span><span>selected</span></a>
</div>
</h2>
<div id="collapse_@id" class="accordion-collapse collapse show" aria-labelledby="@id" 
data-bs-parent="#acc_@id" style="">
<div id='acc_@id_body' class="accordion-body" style="@custom_style01">
@options
</div></div></div>
</div>
<br>
""".replace('@k',k)
this_dict[k]['object'] = """<div style="padding:7px;"><input isidentifier="@isidentifier" order="@order" labelkey="@label_title" type="checkbox" id="@id_checkbox_@n" onclick="temp_input(this,'@k','');service_counter(this,'@id');" onload=""><label class="sensation" for="@id_checkbox_@n" id="@id_@n_label">@object</label></div>
""".replace('@k',k)
this_dict[k]['params'] = ['@id','@label_title','@options','@n','@counter_left']
#*******************************sections
this_sections = {}
section_template = """
<div name="section" sectionname="@section_title" id="@section_id" class="col-md-@n animated fadeInUp" data-animate="fadeInUp" data-delay="1.25" style="@section_borders;visibility: visible; animation-delay: 1.25s;@section_style">
<div style="display: flex; justify-content: center; align-items: center; height: 100vh; flex-direction: column; text-align: left;">
<div>@section_custom_top_content</div>
<h5 class="sensation" style="color:#252F3E;font-weight:800;">
<a id="title_@section_id" style="@sec_title_style">@section_title</a>
@custom_title_html
<a id="@section_id_a" class="sensation"  style="position:relative;left:0px;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:@editvisibility;float:right;" 
 onclick="save_load_edit_undo('@section_id','edit');">edit</a> 
<a id="@section_id_b1" edition="@section_id" edition_type="undo" style="width:20px;float:right;color:transparent;display:none;">-</a>
<a id="@section_id_b2" edition="@section_id" edition_type="undo" class="sensation" 
style="position:relative;;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:visible;float:right;display:none;" 
onclick="save_load_edit_undo('@section_id','undo');">undo</a>
<a id="@section_id_c1" edition="@section_id" edition_type="save" style="width:20px;float:right;color:transparent;display:none;">-</a>
<a id="@section_id_c2" edition="@section_id" edition_type="save" class="sensation" 
style="position:relative;;cursor:pointer;font-size:16px;color:rgb(40,143,235);visibility:visible;float:right;display:none;" 
onclick="save_load_edit_undo('@section_id','save');">save</a>
</h5>
@content
</div>
</div>
"""
section_borders = {}
section_borders["right_border"] = "border-right:solid 1px orange;"
section_borders["left_border"] = "border-left:solid 1px orange;"
section_borders["no_border"] = "none;"
for k in set(section_borders.keys()):
    this_sections[k] = {}
    this_sections[k]['html'] = section_template\
    .replace("@section_borders",section_borders[k])\
    .replace('@k',k)
    this_sections[k]['params'] = ['@section_title','@n','@content']

this_sections[k]['params'] = ['@section_title','@n','@content']
#****************************************************
this_common_menu = {}
k = 'menubar'
this_common_menu[k] = {}
this_common_menu[k]['html_legacy'] = """
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="padding:0px;height:37px;background-color:@menu_background_color;color:@menu_font_color;">
<div class="container-fluid">
<a class="navbar-brand" href="#"><img src="static/img/@menu_left_img" alt="" style="@img_style"></a>
<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#main_nav">
<span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse sensation" id="main_nav">
<ul class="navbar-nav ms-auto" style="right:53px;position:absolute;">
@items
</ul>
</div> <!-- navbar-collapse.// -->
</div> <!-- container-fluid.// -->
</nav>
"""
this_common_menu[k]['default_img_style_legacy']='max-width:175px;top:-30px;position:absolute;left:53px;'
k1 = 'items_legacy'
this_common_menu[k][k1] = {}
k2 = 'single_legacy'
this_common_menu[k][k1][k2] = """<li class="nav-item"><a class="nav-link" href="@href" onclick="@onclick" style="color:inherit;">@item_name</a></li>"""
k2 = 'multiple_legacy'
this_common_menu[k][k1][k2] = {}
this_common_menu[k][k1][k2]['dropdown_list'] = """
<li class="nav-item dropdown">
<a class="nav-link  dropdown-toggle" href="#" data-bs-toggle="dropdown" style="color:inherit;">@item_name</a>
<ul class="dropdown-menu dropdown-menu-right" style="top:33px;background-color:@menu_background_color;color:@menu_font_color;">
@objects
</ul>
</li>
"""
this_common_menu[k][k1][k2]['object_legacy'] = """
<li><a class="dropdown-item" href="@href" onclick="@onclick" style="color:inherit;font-size:14px;">@object</a></li>
"""
#************************************************
this_common_menu[k]['html'] ="""
<div class="header-main">
<div class="header-container container">
<div class="header-wrap">
<!-- Logo @s -->
<div class="header-logo logo animated fadeInDown" data-animate="fadeInDown" data-delay=".85" style="visibility: visible; animation-delay: 0.85s;">
<a href="./" class="logo-link">
<img class="logo-light" src="{{ secure_cloudpy_org | safe }}/static/img/@menu_left_img" alt="logo" style="@img_style">
</a>
</div>
<!-- Menu Toogle @s -->
<div class="header-nav-toggle">
<a href="#" class="navbar-toggle" data-menu-toggle="example-menu-04">
<div class="toggle-line">
<span></span>
</div>
</a>
</div>
<!-- Menu @s -->
<div class="header-navbar header-navbar-s1">
<nav class="header-menu" id="example-menu-04">
<ul class="menu menu-s2 animated fadeInDown" data-animate="fadeInDown" data-delay=".75" style="visibility: visible; animation-delay: 0.75s;">
@items
</ul>
</nav>
<div class="header-navbar-overlay"></div>
<div class="header-navbar-overlay"></div>
</div><!-- .header-navbar @e -->
</div>
</div>
</div>
"""

this_common_menu[k]['default_img_style']='left:0px;position:relative;width:97.1px;height:60px;top:0px;'
k1 = 'items'
this_common_menu[k][k1] = {}
k2 = 'single'
this_common_menu[k][k1][k2] = """<li class="menu-item active" style="font-family:sensationLight;">
<a class="nav-link menu-toggle" style="color:@menu_font_color;padding-bottom:5px;padding-top:10px;padding-left:10px;padding-right:10px;font-family:sensationLight;width:auto;cursor:pointer;background-color:@menu_background_color;" href="@href" onclick="@onclick">
@item_name
</a></li>"""
k2 = 'multiple'
this_common_menu[k][k1][k2] = {}
this_common_menu[k][k1][k2]['dropdown_list'] = """
<li class="menu-item active" style="font-family:sensationLight;">
<a class="nav-link menu-toggle" style = "padding-bottom:5px;padding-top:10px;padding-left:10px;padding-right:10px;font-family:sensationLight;width:auto;cursor:pointer;">@item_name</a>
<ul class="menu-sub menu-drop" style="background-color:@menu_background_color;color:@menu_font_color;">
@objects
</ul>
</li>
"""
this_common_menu[k][k1][k2]['object'] = """
<li class="menu-item active"><a class="menu-link nav-link" href="@href" style="font-family:sensationLight;width:auto;padding-right:15px;" onclick="@onclick">@object</a></li>
"""


this_common_menu[k]['params'] = ['@menu_background_color','@menu_font_color','@menu_left_img','@item_name','@object','@href']
main_dict = {}
main_dict['sections'] = this_sections
main_dict['inputs'] = this_dict
main_dict['common_menu'] = this_common_menu

dynamic_js = {}
dynamic_js['load_data_dynamic_code'] = "@dynamic_js"
dynamic_js['load_data_dynamic_routine'] = """
oridat["@k"] = @v;
"""

class cloudpy_org_web_client:
    def __init__(self, **kwargs):
        self.main_dict = main_dict
        self.dynamic_js = dynamic_js
        self.pt = processing_tools()
        self.current_path = os.getcwd() + '/'
        #with open (self.current_path + 'dynamic_html.json', 'r') as f:
        #    self.main_dict = json.loads(f.read())
    #___________________________________________________
    def create_section(self,
                       section_title:str
                       ,section_type:str='right_border'
                       ,section_style:str=''
                       ,size:int=2
                       ,section_custom_top_content:str=''):
        a = self.pt.camel_to_snake(section_title).replace('?','').replace('.','_').replace(',','')
        section_id = a[0:6] + a[::-1][0:6][::-1]
        section_id = section_id.replace("'","").replace('"','')
        rslt = self.main_dict['sections'][section_type]['html']\
        .replace('@section_id',section_id)\
        .replace('@section_title',section_title)\
        .replace('@section_style',section_style)\
        .replace('@n',str(size))\
        .replace('@section_custom_top_content',section_custom_top_content)
        
        return rslt.replace('\n','')
    #___________________________________________________
    def create_menu_item(self
                         ,item_name:str
                         ,options:object
                         ,menu_background_color:str='black'
                         ,menu_font_color:str='white'
                        ):
        if type(options) != list:
            options = [options]
        lo = len(options)
        menu_background_color = menu_background_color.lower().replace(' ','')
        menu_font_color = menu_font_color.lower().replace(' ','')
        if lo < 1:
            return ''
        else:
            if lo == 1:
                item_type = 'single'
                onclick = ''
                if 'onclick' in set(options[0].keys()):
                    onclick = options[0]['onclick']
                rslt = self.main_dict['common_menu']['menubar']['items'][item_type]\
                .replace('@href',options[0]['href'])\
                .replace('@onclick',onclick)

            else:
                item_type = 'multiple'
                rslt = self.main_dict['common_menu']['menubar']['items'][item_type]['dropdown_list']\
                .replace('@menu_background_color',menu_background_color)\
                .replace('@menu_font_color',menu_font_color)
                objects = ''
                obj = self.main_dict['common_menu']['menubar']['items'][item_type]['object']
                for i in options:
                    onclick = ''
                    if 'onclick' in set(i.keys()):
                        onclick = i['onclick']
                    objects += obj.replace('@object',i['name'])\
                    .replace('@href',i['href'])\
                    .replace('@onclick',onclick)
                rslt = rslt.replace('@objects',objects)    
            rslt = rslt.replace('@item_name',item_name)
            return rslt.replace('\n','')
    #___________________________________________________
    def create_common_menu(self,menu_structure:dict,auth:bool=False,username:str=''):
        menu_background_color = menu_structure['menu_background_color']
        menu_font_color = menu_structure['menu_font_color']
        menu_left_img = menu_structure['menu_left_img']
        keys = set(menu_structure.keys())
        if 'img_style' in keys and menu_structure['img_style'].lower().replace(' ','') != 'default':
            img_style = menu_structure['img_style']
        else:
            img_style = self.main_dict['common_menu']['menubar']['default_img_style']
            
        rslt = self.main_dict['common_menu']['menubar']['html']\
        .replace('@menu_background_color',menu_background_color)\
        .replace('@menu_font_color',menu_font_color)\
        .replace('@menu_left_img',menu_left_img)\
        .replace('@img_style',img_style)\
        .replace('{{ secure_cloudpy_org | safe }}',subscription_url)\
        .replace('{{ www_cloudpy_org | safe }}',subscription_url.replace('w'*3,msh))

        items = ''
        items_nums = list(menu_structure['items'].keys())
        items_nums.sort()
        for i in items_nums:
            if 'after_authentication' in set(menu_structure['items'][i].keys()) and auth == True:
                w = 'after_authentication'
                items += self.create_menu_item(
                    item_name=menu_structure['items'][i][w]['item_name'].replace('@username',username)
                    ,options=menu_structure['items'][i][w]['options']
                    ,menu_background_color=menu_background_color
                    ,menu_font_color=menu_font_color
            )
            else:
                items += self.create_menu_item(
                    item_name=menu_structure['items'][i]['item_name']
                    ,options=menu_structure['items'][i]['options']
                    ,menu_background_color=menu_background_color
                    ,menu_font_color=menu_font_color
                )
        
        rslt = rslt.replace('@items',items)
        return rslt.replace('\n','')
        
    #___________________________________________________
    def create_input(self
                     ,input_type:str
                     ,label_title:str
                     ,options:list=[]
                     ,text_content:str=''
                     ,rowsnum:int=3
                     ,section_size:int=3
                     ,event_type:str='save'
                     ,us:str='no'
                     ,cpw:str='no'
                     ,cpwconf:str='no'
                     ,enter_key:str='no'
                     ,action_id:str=''
                     ,action_item:str=''
                     ,subtitle:str=''
                     ,custom_style01:str=''
                     ,custom_style02:str=''
                     ,custom_style03:str=''
                     ,order:str=''
                     ,isidentifier:str=''
                     ,custom_btn_input_class:str='submitrequest'):
        counter_left = (section_size-1)*120 + 20
        a = self.pt.camel_to_snake(label_title)[0:12].replace('?','').replace('.','_').replace(',','')
        this_id = a[0:6] + a[::-1][0:6][::-1]
        this_id = this_id.replace("'","").replace('"','')
        rslt = self.main_dict['inputs'][input_type]['html']\
        .replace('@id',this_id)\
        .replace('@label_title',label_title)\
        .replace('@us',us)\
        .replace('@cpwconf',cpwconf)\
        .replace('@cpw',cpw)\
        .replace('@enter_key',enter_key)\
        .replace('@action_id',action_id)\
        .replace('@action_item',action_item)\
        .replace('@subtitle',subtitle)\
        .replace('@custom_style01',custom_style01)\
        .replace('@custom_style02',custom_style02)\
        .replace('@custom_style03',custom_style03)\
        .replace('@order',str(order))\
        .replace('@isidentifier',isidentifier)
        if input_type in ['select','radios_horizontal','radios_vertical','acc_checkboxes','multi_checkboxes']:
            opti = ''
            obj = self.main_dict['inputs'][input_type]['object']
            n = 0
            for this_option in options:
                n+=1
                opti += obj.replace('@object',this_option)\
                .replace('@n',str(n))\
                .replace('@id',this_id)\
                .replace('@label_title',label_title)\
                .replace('@action_id',action_id)\
                .replace('@action_item',action_item)\
                .replace('@order',str(order))\
                .replace('@isidentifier',isidentifier)
            rslt = rslt.replace('@options',opti).replace('@counter_left',str(counter_left))
        elif input_type in['text_input','num_input','pwd_input','text_area']:
            rslt = rslt.replace('@text_content',text_content)
            if input_type == 'text_area':
                rslt = rslt.replace('@rowsnum',str(rowsnum))
        elif input_type in ['btn_input']:
            rslt = rslt.replace('@event_type',event_type)\
            .replace('@custom_btn_input_class',custom_btn_input_class)
        return rslt.replace('\n','')
    #___________________________________________________
    def complete_dynamic_form(self,dynamic_form:dict):
        
        custom_title_html = ''
        if 'custom_title_html' in set(dynamic_form.keys()):
            if len(dynamic_form['custom_title_html']) > 0:
                custom_title_html = dynamic_form['custom_title_html']
        row_style = ''
        if 'row_style' in set(dynamic_form.keys()):
            if len(dynamic_form['row_style']) > 0:
                row_style = dynamic_form['row_style']
        sections = ''
        section_nums = list(dynamic_form['sections'].keys())
        section_nums.sort()
        for i in section_nums:
            ts = dynamic_form['sections'][i]
            tskeys = set(ts.keys())  
            inputs = ts['inputs']
            section_size = ts['size']
            section_style = ''
            if 'section_style' in tskeys:
                section_style = ts['section_style']
            section_custom_top_content = ''
            if 'section_custom_top_content' in tskeys:
                section_custom_top_content = ts['section_custom_top_content']
            section = self.create_section(
                section_title=ts['section_title']
                ,section_type=ts['section_type']
                ,section_style=section_style
                ,size=section_size
                ,section_custom_top_content=section_custom_top_content)
             
            editvisibility = 'hidden'
            if 'edit_enabled' in tskeys:
                if len(ts['section_title']) > 0 and ts['edit_enabled'].lower().replace(' ','') == 'yes':
                    editvisibility = 'visible'
            
            sec_title_style = 'float:left;'
            if 'sec_title_style' in tskeys and ts['sec_title_style'].lower().replace(' ','') != 'default':
                sec_title_style=ts['sec_title_style']
            section = section.replace('@editvisibility',editvisibility).replace('@sec_title_style',sec_title_style)
            content = ""
            for j in inputs:
                jkeys = set(j.keys())
                
                custom_style01=''
                if 'custom_style01' in jkeys:
                    custom_style01=j['custom_style01']
                
                custom_style02=''
                if 'custom_style02' in jkeys:
                    custom_style02=j['custom_style02']
                
                custom_style03=''
                if 'custom_style03' in jkeys:
                    custom_style03=j['custom_style03']
                    
                custom_btn_input_class = 'submitrequest'
                if 'custom_btn_input_class' in jkeys:
                    custom_btn_input_class=j['custom_btn_input_class']
                
                order=''
                if 'order' in jkeys:
                    order=j['order']
                
                isidentifier='no'
                if 'isidentifier' in jkeys:
                    if str(j['isidentifier']).lower().replace(' ','') == 'yes':
                        isidentifier = 'yes'
                
                subtitle = ''
                if 'subtitle' in jkeys:
                    subtitle=j['subtitle']
                action_id = ''
                if 'action_id' in jkeys:
                    action_id=j['action_id'].lower().replace(' ','')
                action_item= ''
                if 'action_item' in jkeys:
                    action_item=j['action_item'].lower().replace(' ','')
                
                if 'custom_content' in jkeys:
                    content += j['custom_content']
                elif j['input_type'] in ['text_input','pwd_input','text_area']:
                    enter_key = 'no'
                    if 'enter_key' in jkeys:
                        enter_key = j['enter_key'].lower().replace(' ','')
                            
                    text_content = ''
                    if 'text_content' in jkeys:
                        text_content=j['text_content']
                    if j['input_type'] == 'text_area':
                        rowsnum = j['rowsnum']
                        content += self.create_input(
                            input_type=j['input_type']
                            ,label_title=j['label_title']
                            ,text_content=text_content
                            ,rowsnum=rowsnum
                            ,section_size=section_size
                            ,enter_key=enter_key
                            ,action_id=action_id
                            ,action_item=action_item
                            ,subtitle=subtitle
                            ,custom_style01=custom_style01
                            ,custom_style02=custom_style02
                            ,custom_style03=custom_style03
                            ,order=order
                            ,isidentifier=isidentifier
                            ,custom_btn_input_class=custom_btn_input_class)
                    elif j['input_type'] == 'text_input':
                        us = 'no'
                        if 'us' in jkeys:
                            us=j['us'].lower().replace(' ','')
                        content += self.create_input(
                            input_type=j['input_type']
                            ,label_title=j['label_title']
                            ,text_content=text_content
                            ,section_size=section_size
                            ,us=us
                            ,enter_key=enter_key
                            ,action_id=action_id
                            ,action_item=action_item
                            ,subtitle=subtitle
                            ,custom_style01=custom_style01
                            ,custom_style02=custom_style02
                            ,custom_style03=custom_style03
                            ,order=order
                            ,isidentifier=isidentifier
                            ,custom_btn_input_class=custom_btn_input_class
                        )
                    elif j['input_type'] == 'pwd_input':
                        cpw = 'no'
                        if 'cpw' in jkeys:
                            cpw=j['cpw'].lower().replace(' ','')
                        cpwconf = 'no'
                        if 'cpwconf' in jkeys:
                            cpwconf=j['cpwconf'].lower().replace(' ','')
                        content += self.create_input(
                            input_type=j['input_type']
                            ,label_title=j['label_title']
                            ,text_content=text_content
                            ,section_size=section_size
                            ,cpw=cpw
                            ,cpwconf=cpwconf
                            ,enter_key=enter_key
                            ,action_id=action_id
                            ,action_item=action_item
                            ,subtitle=subtitle
                            ,custom_style01=custom_style01
                            ,custom_style02=custom_style02
                            ,custom_style03=custom_style03
                            ,order=order
                            ,isidentifier=isidentifier
                            ,custom_btn_input_class=custom_btn_input_class
                        )
                    else:
                        content += self.create_input(
                            input_type=j['input_type']
                            ,label_title=j['label_title']
                            ,text_content=text_content
                            ,section_size=section_size
                            ,action_id=action_id
                            ,action_item=action_item
                            ,subtitle=subtitle
                            ,custom_style01=custom_style01
                            ,custom_style02=custom_style02
                            ,custom_style03=custom_style03
                            ,order=order
                            ,isidentifier=isidentifier
                            ,custom_btn_input_class=custom_btn_input_class
                        )
                elif j['input_type'] in ['btn_input']:
                    event_type = None
                    if 'event_type' in jkeys:
                        event_type=j['event_type']
                    content += self.create_input(
                        input_type=j['input_type']
                        ,label_title=j['label_title']
                        ,section_size=section_size
                        ,event_type=str(event_type)
                        ,action_id=action_id
                        ,action_item=action_item
                        ,subtitle=subtitle
                        ,custom_style01=custom_style01
                        ,custom_style02=custom_style02
                        ,custom_style03=custom_style03
                        ,order=order
                        ,isidentifier=isidentifier
                        ,custom_btn_input_class=custom_btn_input_class
                    )
                else:
                    options = []
                    if 'options' in jkeys:
                        options=j['options']
                    content += self.create_input(
                        input_type=j['input_type']
                        ,label_title=j['label_title']
                        ,options=options
                        ,section_size=section_size
                        ,action_id=action_id
                        ,action_item=action_item
                        ,subtitle=subtitle
                        ,custom_style01=custom_style01
                        ,custom_style02=custom_style02
                        ,custom_style03=custom_style03
                        ,order=order
                        ,isidentifier=isidentifier
                        ,custom_btn_input_class=custom_btn_input_class
                    )
            sections += section.replace('@content',content)
        
        complete_form = """<div id="main_row" class="row" style="@row_style">
        <div class="col-md-2"></div>
        @sections
        <div class="col-md-2"></div>
        </div>"""
        
        complete_form =complete_form.replace('@sections',sections)\
        .replace('@row_style',row_style)\
        .replace('@custom_title_html',custom_title_html)
        dynamic_form_keys = set(dynamic_form.keys())
        
        if 'display_banner' in dynamic_form_keys and dynamic_form['display_banner'].lower().replace(' ','') == 'no':
            display_banner = 'none'
        else:
            display_banner = 'block'
        
        if 'body_class' in dynamic_form_keys and dynamic_form['body_class'].lower().replace(' ','') != 'default':
            body_class=dynamic_form['body_class']
        else:
            body_class = ''
            
        if 'body_style' in dynamic_form_keys and dynamic_form['body_style'].lower().replace(' ','') != 'default':
            body_style=dynamic_form['body_style']
        elif 'body_background_color' in dynamic_form_keys and len(dynamic_form['body_background_color']) > 0:
            body_style="padding:0px;background-color:" + dynamic_form['body_background_color'].lower().replace(' ','') + ";"
        else:
            body_style="padding:0px;"
        bannertitle,banner_subtitle,bannerbackground,topcontent = '','','',''
        requires_authentication = True
        if 'bannertitle' in dynamic_form_keys:
            bannertitle = dynamic_form['bannertitle']
        if 'banner_subtitle' in dynamic_form_keys:
            banner_subtitle = dynamic_form['banner_subtitle']
        if 'bannerbackground' in dynamic_form_keys:
            bannerbackground = dynamic_form['bannerbackground']
        if 'topcontent' in dynamic_form_keys:
            topcontent = dynamic_form['topcontent']
        if 'requires_authentication' in dynamic_form_keys:
            requires_authentication = dynamic_form['requires_authentication']
        return complete_form,body_style,body_class,display_banner,bannertitle,banner_subtitle,bannerbackground,topcontent,requires_authentication
class cloudpy_flask():
    def __init__(self,name:str):
        self.app = Flask(name)
        self.render_template = render_template
        self.request = request
        self.jsonify = jsonify
        self.make_response = make_response
        self.redirect = redirect

class cloudpy_org_aws_framework_client:
    def __init__(self
                 ,aws_namespace:str=None
                 ,env:str='dev'
                 ,region_name:str="us-east-2"
                 ,token_path:str=None
                 ,enable_flask:bool=False
                 ,main_name:str='__main__'
                 ,config:dict=None
                ):
        self.cloudpy_org_chatbot = None
        if config != None and config != {}:
            aws_namespace=config["aws_namespace"]
            region_name=config["region_name"]
            env=config["env"]
            self.config = config
        else:
            self.config = {}
        if aws_namespace == None:
            return 'aws_namespace is required.'
        else:
            self.OrTrigger = OrTrigger
            self.CronTrigger = CronTrigger
            self.BackgroundScheduler = BackgroundScheduler
            self.time = time
            self.pytz = pytz
            self.scheduler = scheduler
            self.Queue = Queue
            self.Process = Process
            self.subprocess = subprocess
            self.web = cloudpy_org_web_client()
            self.aws_namespace = aws_namespace
            self.sufix = env
            self.region_name = region_name
            self.token_path = token_path
            self.__define_constants()
            self.set_user_authentication_minutes_to_expire(30,print_res=False)
            self.aws_framework_called = False
            self.aws_framework()
            self.main_name = main_name
            if enable_flask:
                self._enable_flask()
    def _enable_flask(self):
        self.flask = cloudpy_flask(self.main_name)
        self.web_app_type = 'flask'
    
    #_________________________________________________________________________
    def create_basic_templates(self,refresh_templates:bool=False):
        templates_path = self.current_path + '/templates/'
        if os.path.exists(templates_path) == False:
            os.mkdir(templates_path)
        files_in_folder = os.listdir(templates_path)
        basic_templates = ['common_base','canvas']
        url_base = self.aws.msh + "/static/@bs.html"
        file_name_base = "@bs.html"
        for bs in basic_templates:
            url = url_base.replace("@bs",bs)
            file_name = file_name_base.replace("@bs",bs)
            if file_name in files_in_folder:
                if refresh_templates:
                    x = requests.get(url=url,verify=True).text
                    with open(templates_path + file_name,'w', encoding='utf-8') as f:
                        f.write(x)
            else:
                x = requests.get(url=url,verify=True).text
                with open(templates_path + file_name,'w', encoding='utf-8') as f:
                    f.write(x)
    #_________________________________________________________________________
    def create_flask_app(self
                         ,web_portal_id:str=None
                         ,my_globals:object=None
                         ,my_locals:object=None
                         ,host:str='0.0.0.0'
                         ,port:int=None
                         ,debug:bool=False
                         ,login_capability:bool=True
                        ):
        if self.config != None and self.config != {}:
            self.flask_host = self.config["host"]
            self.flask_port = self.config["port"]
            self.flask_debug = self.config["debug"]
            self.web_portal_id = self.config["web_portal_id"]
        else:
            self.flask_host = host
            self.flask_port = port
            self.flask_debug = debug
            self.web_portal_id = web_portal_id
        self.flask_globals = my_globals
        self.flask_locals = my_locals
        dc = default_app.replace('@web_portal_id',self.web_portal_id)\
        .replace('@construct_pages',self.construct_pages())\
        .replace('@flask_host',self.flask_host)\
        .replace('@flask_port',str(self.flask_port))\
        .replace('@flask_debug',str(self.flask_debug))
        exec(dc, self.flask_globals, self.flask_locals)
        return self.flask_locals['app']
    #_________________________________________________________________________
    def initiate_webapp(self,app:object=None):
        dc = "initiate()"
        exec(dc, self.flask_globals, self.flask_locals)
        
        
        
    #_________________________________________________________________________
    def restart_base(self,restart_pass_phrase:str=None):
        m = "no action taken"
        try:
            if restart_pass_phrase == self.restart_pass_phrase:
                self.some_queue.put("something")
                m = "successfully restarted at " + self.current_datetime_str()
            else:
                m = "invalid pwd value"
        except Exception as e: 
            m = "Failed in restart: " + str(e)
        self.last_restart_message = m
    #_________________________________________________________________________
    def start_flaskapp(self,queue):
        self.some_queue = queue
        restart_schedules = {}
        triggers_list = []
        for k,v in restart_schedules.items():
            triggers_list.append(self.CronTrigger.from_crontab(v, timezone=default_timezone))
        trigger = self.OrTrigger(triggers_list)
        self.scheduler.add_job(self.restart_base, trigger)
        self.scheduler.start()
        self.app.run(host=self.host,port=self.port,debug=self.debug)
    #_________________________________________________________________________
    def __define_constants(self):
        self._reserved_endpoints =['secure'
                                   ,'ttk'
                                   ,'auth'
                                   ,'send_confirmation_email'
                                   ,'confirm_email'
                                   ,'store'
                                   ,'obtain'
                                   ,'register'
                                   ,'register_new_user'
                                   ,'resend_confirmation_email'
                                   ,'login'
                                   ,''
                                   ]
        self._update_pages_registry_warning = """
        Warning: The data provided should have the following structure according to your desired case:
        1. For custom pages:
           {"<desired page name>":{"page_type":"custom","request_type":"<get or post>","active":<bool>,"custom_code":"<custom Python code>"}}

           Example:
           {"my_custom_page":{"page_type":"custom","request_type":"get","active":True,"custom_code":"return 'Hello, World!'"}}
        _____________________________________

        2. For well defined dynamic site that require previous authentication:
           {"<desired page name>":{"page_type":"authenticated_endpoint","active":<bool>}}

           Example:
           {"my_authenticated_page":{"page_type":"authenticated_endpoint","active":True}}
        _____________________________________

        3. For well defined dynamic site that will load data (this implies authentication required):
           {"<desired page name>":{"page_type":"secure_read_form_data","active":<bool>}}

           Example:
           {"my_secure_data_page":{"page_type":"secure_read_form_data","active":True}}
        _____________________________________

        4. For well defined dynamic site that does not require authentication:
           {"<desired page name>":{"page_type":"dynamic_site","active":<bool>}}

           Example:
           {"my_dynamic_page":{"page_type":"dynamic_site","active":True}}

        Please ensure your data adheres to one of these structures to optimize compatibility with the desired functionality.
        """
        self.domain_to_restrict_access_to = ''
        self.email_banner_img = ''
        self.favicon_ico = 'cloudpy_org_favicon.ico'
        self.notifications_email = ''
        self.default_redirect_if_not_authenticated ='/login'
        self.default_redirect_when_logged ='/home'
        
        self.web_portal_title = ''
        self.auth_token_max_age_minutes = 30
        self.__jscode={}
        self.__jscode["after_saving_data"] = """
        function after_saving_data(){
        document.getElementById("@savebtn").style.display = "None";
        document.getElementById("@savebtn_label").style.display = "block";
        document.getElementById("@savebtn_label").innerHTML = "Data successfully saved.";
        }
        setTimeout(after_saving_data,300);
        """
        self.__jscode["after_editing_data"] = """
        document.getElementById("@savebtn").style.display = "block";
        document.getElementById("@savebtn_label").style.display = "None";
        document.getElementById("@savebtn_label").innerHTML = "";
        """
        self.current_path = os.getcwd() + '/'
        if self.token_path == None:
            self.token_path = self.current_path + self.aws_namespace + '.txt'
        self.aws = None
        self.errors = {}
        self.errors[1] = 'Invalid service token.'
        self.errors[2] = 'No aws framework client has been initialized yet.'
        self.errors[3] = 'Provided data format cannot be converted to json.'
        self._catalog_base_description = """GLUE Data Catalog '@catalog_name'.
        Created programmatically with cloudpy_org_aws_framework_client under the following criteria:
        cloudpy.org_aws_namespace = '@namespace', cloudpy.org_aws_env = '@env', region = '@region', creation_date='@creation_date'.
        Visit https://www.cloudpy.org/documentation.
        Additional custom description:@desc"""
        self.__letters = list('abcdefghijklmnopqrstuvwxyz0123456789')
        self.__letters.append('_')
        self.__letters.append('-')
        
    #_________________________________________________________________________
    def set_user_authentication_minutes_to_expire(self,minutes:int,print_res:bool=True):
        self.user_authentication_minutes_to_expire = minutes
        if print_res:
            print('Temporal authentication token expiration for framework users has been set to ' + str(minutes) + ' minutes.')
    #_________________________________________________________________________
    def get_full_path(self,relative_path:str):
        relative_path = relative_path.replace('\\','/').replace('//','/').replace('//','')
        l = len(relative_path)
        if relative_path[l-1:l] == '/':
            relative_path = relative_path[0:l-1]
            l = len(relative_path)
        if relative_path[0:1] == '/':
            relative_path = relative_path[1:l]
        return self.s3_root_path + relative_path + '/'
    #_________________________________________________________________________
    def ofuscate(self,str_input:str):
        rslt = ''
        u = list(self.aws.ypt.decrypt(self._unique_of,self.__gen_key))
        for i in str_input:
            if i in self.__letters:
                rslt += u[self.__letters.index(i)]
            else:
                rslt += i
        return rslt
    #_________________________________________________________________________
    def deofuscate(self,str_input:str):
        rslt = ''
        u = list(self.aws.ypt.decrypt(self._unique_of,self.__gen_key))
        for i in str_input:
            if i in u:
                rslt += self.__letters[u.index(i)]
            else:
                rslt += i
        return rslt
    #_________________________________________________________________________
    def _suok(self):
        file_name = self.aws_namespace + '_o_key.txt'
        x = self.get_s3_file_content(file_name=file_name,relative_path=self._secrets_relative_path)
        if x != None and len(x) > 1:
            self._unique_of = x
            print('Security was previously set. Security in place.')
        else:
            try:
                random_numbers,b,l=[],'',len(self.__letters)
                while len(random_numbers) < l:
                    this_rn = rand.randint(0,l-1)
                    if this_rn not in random_numbers:
                        random_numbers.append(this_rn)
                for i in range(l):
                    b += self.__letters[random_numbers[i]]
                self._unique_of = self.aws.ypt.encrypt(b,self.__gen_key)
                self.write_in_s3_folder(
                    data=self._unique_of
                    ,file_name=file_name
                    ,relative_path=self._secrets_relative_path,print_res=False)
                print('Security in place.')
            except Exception as e:
                print(str(e))
                self._unique_of = None
                print('Could not set unique file ofuscation.')
        
    #_________________________________________________________________________
    def aws_framework(self):
        if self.aws_framework_called == False:
            cont = False
            try:
                with open(self.token_path, 'r') as f:
                    service_token=f.read()
                    self.aws = aws_framework_manager_client(
                        service_token=service_token
                        ,aws_namespace=self.aws_namespace
                        ,region_name=self.region_name)
                try:
                    self.bucket_name = self.aws.get_bucket_name(sufix=self.sufix,region=self.region_name)
                    self.s3_root_path = 's3://' + self.bucket_name + '/'
                    self._secrets_relative_path = '/settings/secrets/'
                    self._users_relative_path = self._secrets_relative_path + 'users'
                    self.__gen_key = self.get_s3_file_content(file_name='general_key.txt',relative_path=self._secrets_relative_path)
                    self.athena = self.aws.ypt.b3session.client('athena',region_name=self.region_name)
                    self.ses = self.aws.ypt.b3session.client('ses',region_name=self.region_name)
                    self.data_catalog_sufix = self.bucket_name.replace('cloudpy.org-','')
                    banned_relative_paths = ['settings/','settings/secrets/users/','metadata/']
                    self.banned_paths = [self.get_full_path(i) for i in banned_relative_paths]
                    cont = True
                except Exception as e:
                    cont = False
                    print('Error AFW01:',str(e))
            except Exception as e:
                cont = False
                print('Error AFW02:', self.errors[1])
            if cont:
                self._suok()
                self.aws_framework_called = True
        else:
            print('second time?')
    #_________________________________________________________________________
    def get_s3_file_content(self,file_name:str,relative_path:str):
        if self.aws != None:
            file_name,ext = self.__treat_file_name(file_name)
            s3FullFolderPath = self.get_full_path(relative_path)
            rslt = None
            if ext == 'json':
                try:
                    rslt = self.aws.ypt.get_s3_file_content(referenceName=file_name,s3FullFolderPath=s3FullFolderPath,exceptionCase=False)
                except:
                    try:
                        rslt = self.aws.ypt.get_s3_file_content(referenceName=file_name,s3FullFolderPath=s3FullFolderPath,exceptionCase=True)
                    except Exception as e:
                        print(str(e))
            else:
                rslt = self.aws.ypt.get_s3_file_content(referenceName=file_name,s3FullFolderPath=s3FullFolderPath,exceptionCase=True)
            return rslt
        else:
            print(self.errors[2])
            return None
    #_________________________________________________________________________
    def __treat_file_name(self,file_name:str):
        file_name = file_name.lower()\
        .replace('  ',' ')\
        .replace('  ',' ')\
        .replace('  ','')\
        .replace(' ','_')\
        .replace('__','_')\
        .replace('__','_')\
        .replace('__','')
        ext = file_name[::-1].split('.')[0][::-1]
        file_name = file_name.replace('.' + file_name[::-1].split('.')[0][::-1],'') + '.' + ext
        return file_name,ext
    #_________________________________________________________________________    
    def write_in_s3_folder(self,data:object,file_name:str,relative_path:str,print_res:bool=True):
        if self.aws != None:
            file_name,ext = self.__treat_file_name(file_name)
            s3FullFolderPath = self.get_full_path(relative_path)
            if ext != 'json':
                if type(data) != str:
                    data = str(data)
                self.aws.ypt.store_str_as_file_in_s3_folder(
                    strInput=data
                    ,fileName=file_name
                    ,s3FullFolderPath=s3FullFolderPath
                    ,region_name=self.region_name
                    ,print_res=print_res)
            elif ext == 'json':
                cont = True
                if type(data) != dict:
                    data = str(data)
                    try:
                        data = self.aws.dictstr_to_dict(data)
                    except:
                        cont = False
                        print(self.errors[3])
                if cont:
                    try:
                        self.aws.ypt.standard_dict_to_json(jsonOrDictionary=data,fileName=file_name,folderPath=s3FullFolderPath,print_res=print_res)
                    except Exception as e:
                        print(str(e))
        else:
            print(self.errors[2])
    #_________________________________________________________________________        
    def create_user(self,username:str,email:str,pwd:str):
        rslt = self.aws.create_new_user(sufix=self.sufix,region=self.region_name,username=username,email=email,pwd=pwd)
        return rslt
    #_________________________________________________________________________
    def check_user(self,username_or_email:str='not_authenticated_person'):
        if username_or_email != None:
            rslt = self.aws.check_if_user_exists_and_was_confirmed(
                username_or_email=username_or_email
                ,bucket_name=self.bucket_name
                ,sufix=self.sufix
                ,region=self.region_name
            )
        else:
            rslt = 'Invalid username_or_email input.'
        return rslt
    #_________________________________________________________________________
    def confirm_user(self,username_or_email:str):
        user_check = self.check_user(username_or_email)
        uck = set(user_check.keys())
        if 'exists' in uck and 'confirmed' in uck and 'file_name' in uck:
            if user_check['confirmed'] == 0:
                rslt = self.get_s3_file_content(file_name=user_check['file_name'],relative_path=self._users_relative_path)
                rslt['confirmed_email'] = 1
                self.write_in_s3_folder(data=rslt,file_name=user_check['file_name'],relative_path=self._users_relative_path,print_res=False)
    #_________________________________________________________________________            
    def get_user_temp_token(self,username_or_email:str,pwd:str=None,email_notification:bool=False,temp_token:str=None):
        if email_notification:
            return self._gut(username_or_email=username_or_email,email_notification=email_notification,temp_token=temp_token)
        else:
            return self._gut(username_or_email=username_or_email,pwd=pwd)
    #_________________________________________________________________________
    def co_set_chatbot_context(self):
        try:
            enc_api_creds = request.cookies.get('enc_api_creds')
            api_creds == self.aws.ypt.decrypt(enc_api_creds,self.__gen_key).split('***')
            self.cloudpy_org_chatbot = cloudpy_org_customizable_chatbot(api_key=api_creds[0],api_organization=api_creds[1])
            return {"co_data":"success"}
        except:
            return {"co_data":"Invalid credentials, could not set the chatbot context."}
    #_________________________________________________________________________
    def train_ai_chatbot(self):
        enc_api_creds = request.cookies.get('enc_api_creds');
        json_data = request.json
        file_name = json_data['file_name']
        #file_name = request.cookies.get('file_name');
        us = request.cookies.get('us');
        api_creds == self.aws.ypt.decrypt(enc_api_creds,self.__gen_key).split('***')
        self.cloudpy_org_chatbot = cloudpy_org_customizable_chatbot(api_key=api_creds[0],api_organization=api_creds[1])
        page_name = request.base_url[::-1].split('/')[0][::-1]
        inputStr = self.extract_text_from_file(page_name=page_name,file_name=file_name,username=us)
        print('inputStr:',inputStr)
        return {"co_data":inputStr}
        
        
    #_________________________________________________________________________
    def _gut(self,username_or_email:str,pwd:str=None,email_notification:bool=False,temp_token:str=None):
        user_check = self.check_user(username_or_email)
        uck = set()
        if type(user_check) == dict:
            uck = set(user_check.keys())
        if 'exists' in uck and 'confirmed' in uck and 'file_name' in uck:
            if user_check['exists']:
                if user_check['confirmed'] == 1:
                    f = user_check['file_name']
                    r = self._users_relative_path
                    data = self.get_s3_file_content(file_name=f,relative_path=r)
                    this_key = 'temp_token'
                    minutes_to_expire = self.user_authentication_minutes_to_expire
                    cont = False
                    if email_notification:
                        this_key = 'email_notification_token'
                        minutes_to_expire = 30
                        if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token,email_notification=False):
                            cont = True
                    elif pwd == self.aws.ypt.decrypt(data['encrypted_pwd'],self.__gen_key):
                        cont = True
                    if cont:
                        temp_token = self.aws.ypt.encrypt(f,self.aws.ypt.gen_enc_key())
                        data[this_key] = self.aws.ypt.gen_encrypted_data_with_expiration(original_message=temp_token,minutes_to_expire=minutes_to_expire)
                        self.write_in_s3_folder(data=data,file_name=f,relative_path=r,print_res=False)
                        return temp_token
                    else:
                        return 'Wrong password.'
                else:
                    return 'User has not been confirmed.'
            else:
                return 'User does not exist.'
    #_________________________________________________________________________        
    def user_token_authentication(self,username_or_email:str,temp_token:str,email_notification:bool=False):
        return self.__uta(username_or_email=username_or_email,temp_token=temp_token,email_notification=email_notification)
    #_________________________________________________________________________
    def __uta(self,username_or_email:str,temp_token:str,email_notification:bool=False):
        user_check = self.check_user(username_or_email)
        uck = set()
        if type(user_check) == dict:
            uck = set(user_check.keys())
        if 'exists' in uck and 'confirmed' in uck and 'file_name' in uck:
            if user_check['exists']:
                if user_check['confirmed'] == 1:
                    f = user_check['file_name']
                    r = self._users_relative_path
                    data = self.get_s3_file_content(file_name=f,relative_path=r)
                    this_key = 'temp_token'
                    what = 'Token'
                    minutes_to_expire = self.user_authentication_minutes_to_expire
                    if email_notification:
                        this_key = 'email_notification_token'
                        what = 'Link'
                        minutes_to_expire = 30
                    try:
                        enc_data = data[this_key]
                        stored_token = self.aws.ypt.decrypt_before_expiration(data=enc_data)
                        if stored_token.lower().replace('.','').strip() == 'encryption expired':
                            print(what + ' expired.')
                    except Exception as e:
                        stored_token = None
                    if temp_token == stored_token:
                        return True
                    else:
                        new_temp_token = self.aws.ypt.encrypt(f,self.aws.ypt.gen_enc_key())
                        new_enc_data = self.aws.ypt.gen_encrypted_data_with_expiration(original_message=new_temp_token,minutes_to_expire=minutes_to_expire)
                        data[this_key] = new_enc_data
                        self.write_in_s3_folder(data=data,file_name=f,relative_path=r,print_res=False)
                        return False
                else:
                    return 'User has not been confirmed.'
            else:
                return 'User does not exist.'
    #__________________________________________________________________________
    def update_user_password(self,username_or_email:str,email_temp_token:str,new_pwd:str):
        self.__up(username_or_email=username_or_email,email_temp_token=email_temp_token,new_pwd=new_pwd)
    #__________________________________________________________________________
    def __up(self,username_or_email:str,email_temp_token:str,new_pwd:str):
        if self.user_token_authentication(username_or_email=username_or_email,temp_token=email_temp_token,email_notification=True):
            try:
                user_check = self.check_user(username_or_email)
                f = user_check['file_name']
                r = self._users_relative_path
                data = self.get_s3_file_content(file_name=f,relative_path=r)
                data['encrypted_pwd'] = self.aws.ypt.encrypt(new_pwd,self.__gen_key)
                self.write_in_s3_folder(data=data,file_name=f,relative_path=r,print_res=False)
                print('Password successfully updated')
                return True
            except:
                print('Error while trying to modify password.')
                return False
        else:
            print('Could not modify password.')
            return  False
    #__________________________________________________________________________
    def df_to_big_data_hive(self,df_input:pd.DataFrame,table_name:str,sink_relative_path:str='sinks',partition_cols:list=None):
        path = self.get_full_path(relative_path=sink_relative_path + table_name)
        wr.s3.to_parquet(
            df=df_input
            ,dataset=True
            ,path=path
            ,boto3_session=aws.aws.ypt.b3session
            ,partition_cols=partition_cols
        )
    #__________________________________________________________________________
    def create_data_catalog(self,catalog_name:str=None,description:str='',include_environment_tag:bool=True,catalog_id:str=None):
        if catalog_name == None:
            catalog_name = self.data_catalog_sufix + '-data-catalog'
        else:
            catalog_name = self._treat_name(catalog_name)
            if include_environment_tag:
                catalog_name = self.data_catalog_sufix + '-' + catalog_name
        
        date_id,time_id = self.aws.ypt.date_time_id(local=True)
        creation_date = self.aws.ypt.date_time_str(date_id,time_id)
        new_description = self._catalog_base_description\
        .replace('@catalog_name',catalog_name)\
        .replace('@namespace',self.aws_namespace)\
        .replace('@env',self.sufix)\
        .replace('@region',self.region_name)\
        .replace('@creation_date',creation_date)\
        .replace('@desc',description)
        try:
            if catalog_id == None:
                account_id = wr.sts.get_account_id(boto3_session=self.aws.ypt.b3session)
                catalog_id = account_id
            self.athena.create_data_catalog(
                Name=catalog_name
                ,Type='GLUE'
                ,Description=new_description
                ,Parameters={'catalog-id': catalog_id}
            )
            print('catalog_name: ',catalog_name)
            print('description: ',new_description)
        except Exception as e:
            r = str(e)
            if ': DataCatalog' in r:
                r = 'DataCatalog' + r.split(': DataCatalog')[1]
            print(r)
    #__________________________________________________________________________
    def _treat_name(self,name:str):
        name = name.lower().strip()\
        .replace('  ',' ')\
        .replace('  ',' ')\
        .replace('  ','')\
        .replace(' ','_')\
        .replace('__','_')\
        .replace('__','_')\
        .replace('__','')\
        .replace('--','-')\
        .replace('--','-')\
        .replace('--','')
        return name
    #__________________________________________________________________________
    def create_big_data_db(self,db_name:str,description:str):
        db_name = self._treat_name(db_name)
        try:
            wr.catalog.create_database(name=db_name,description=description,boto3_session=self.aws.ypt.b3session)
            return 'Database ' + db_name + ' succesfully created.'
        except Exception as e:
            return str(e).split('already exists')[0] + 'already exists.'
    #__________________________________________________________________________   
    def _update_get_datasources_schemas(self):
        catalogs = self.athena.list_data_catalogs()
        cats = {}
        for this_cat in [i['CatalogName'] for i in catalogs['DataCatalogsSummary']]:
            d = self.athena.list_databases(CatalogName=this_cat)
            cats[this_cat] = {}
            databases = {j['Name'] for j in d['DatabaseList']}
            for this_db in databases:
                cats[this_cat][this_db] = {}
                dd = self.athena.list_table_metadata(CatalogName=this_cat,DatabaseName=this_db)
                these_tables = [i['Name'] for i in dd['TableMetadataList']]
                for this_table in these_tables:
                    cats[this_cat][this_db][this_table] = {}
                    for m in dd['TableMetadataList']:
                        if m['Name'] == this_table:
                            this_metadata = m
                            these_keys = [x for x in set(this_metadata.keys()) if x != 'Name']
                            for this_key in these_keys:
                                cats[this_cat][this_db][this_table][self.aws.ypt.camel_to_snake(this_key)] = this_metadata[this_key]
                            break
        rslt = {}
        rslt['simple'] = {}
        rslt['complete'] = {}
        version = ['simple','complete']
        for a,b in cats.items():
            for u in version:
                rslt[u][a] = {}
            for c,d in b.items():
                for u in version:
                    rslt[u][a][c] = {}
                for e,f in d.items():
                    for u in version:
                        rslt[u][a][c][e] = {}
                    for g,h in f.items():
                        if g == 'columns':
                            for u in version:
                                rslt[u][a][c][e][g] = {hh['Name']:hh['Type'] for hh in h}
                        else:
                            rslt['complete'][a][c][e][g] = h
        self._datasources_schemas = rslt
    def show_datasources_schemas(self,version:bool='simple'):
        self._update_get_datasources_schemas()
        rslt = {}
        for k,v in self._datasources_schemas[version].items():
            if self.data_catalog_sufix in k:
                rslt[k] = v
        return rslt
    #__________________________________________________________________________    
    def create_athena_table(self,sink_path:str,db_name:str,table_name,columns_schema:dict,partition_cols:list):
        wr.athena.create_table(
            database=db_name,
            table=table_name,
            path=sink_path,
            columns_types=columns_schema,
            partition_cols=partition_cols
        )
    #__________________________________________________________________________
    def list_s3_object(self,relative_path:str=''):
        try:
            fp = self.get_full_path(relative_path)
            l = wr.s3.list_objects(path=fp,boto3_session=self.aws.ypt.b3session)
            rslt = [i.replace(fp,'') for i in l if '/' not in i.replace(fp,'')]
            rslt = set(rslt)
            rslt = list(rslt)
            rslt.sort()
        except Exception as e:
            print(str(e))
            rslt = []
        return rslt
    #__________________________________________________________________________
    def delete_s3_objects(self,relative_path:str,file_names:list=[],clear_all_directory:bool=False):
        folder_path = self.get_full_path(relative_path)
        if folder_path not in self.banned_paths:
            existing_files = self.list_s3_object(relative_path)
            if clear_all_directory:
                file_names = [folder_path + i for i in existing_files]
            else:
                file_names = [folder_path + i for i in file_names if i in existing_files]
            try:
                wr.s3.delete_objects(file_names,boto3_session=self.aws.ypt.b3session)
                print(str(len(file_names)) + ' objects deleted.')
            except Exception as e:
                print(str(e))
        else:
            m = "The directory path: '@folder_path' \n"\
            "constitutes an integral component of the foundational framework structure, thus precluding direct programmatic deletion.\n"\
            "While manual removal of objects within this directory is feasible within your AWS account, we strongly advise against such "\
            "action, as it may compromise the functionalities of your cloudpy.org environment framework.\n"\
            "For comprehensive guidelines on the proper deletion procedure for a cloudpy.org framework, we "\
            "recommend consulting our documentation at https://www.cloudpy.org/documentation."
            m = m.replace('@folder_path',folder_path)
            print(m)  
    #__________________________________________________________________________        
    def delete_user(self,username_or_email:str):
        folder_path = self.get_full_path(self._users_relative_path)
        this_check = self.check_user(username_or_email=username_or_email)
        if 'file_name' in set(this_check.keys()):
            file_names = [folder_path + this_check['file_name']]
            try:
                wr.s3.delete_objects(file_names,boto3_session=self.aws.ypt.b3session)
                print(this_check, ' objects deleted.')
            except Exception as e:
                print(str(e))
        else:
            print(this_check)
    #__________________________________________________________________________
    def user_ref(self,username_or_email:str):
        c = self.check_user(username_or_email)
        if 'file_name' in c:
            return c['file_name'].replace('.json','')
        else:
            return 'Invalid username or email.'
    #__________________________________________________________________________
    def store_json_data(self,username_or_email:str,temp_token:str,form_name:str,json_data:dict):
        if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token):
            try:
                a = self.user_ref(username_or_email)
                b = self.ofuscate(a)
                if len(b) > 1:
                    self.write_in_s3_folder(
                        data=json_data
                        ,file_name= b + '.json'
                        ,relative_path=self._secrets_relative_path + self.ofuscate(self._treat_name(form_name))
                        ,print_res=False)
                    return {"stored":True}
                else:
                    return {"stored":False,"error_message":"Invalid username or email."}
            except Exception as e:
                print(str(e))
        else:
            return {"stored":False,"error_message":"Invalid token."}
        
        #__________________________________________________________________________
    def store_web_portal_json_data(self
                                   ,username_or_email:str
                                   ,folder_reference:str
                                   ,json_data:dict
                                   ,requires_auth:bool=True
                                   ,temp_token:str=None
                                   ,redirect:bool=False
                                  ):
        if self.web_portal_id != None and type(self.web_portal_id) == str and len(self.web_portal_id) > 0:
            if requires_auth:
                if temp_token == None:
                    x = False
                    return {"error_message":"Temporal token not created. Prior authentication is required."}
                else:
                    x = self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token)
            else:
                x = True
            #print('x:',x)
            if x:
                try:
                    a = self.user_ref(username_or_email)
                    b = self.ofuscate(a)
                    form_name = request.cookies.get('form_name')
                    if len(b) > 1:
                        relative_path=self._secrets_relative_path + self.web_portal_id + '/' + self.ofuscate(self._treat_name(folder_reference))
                        #print('relative_path:',relative_path)
                        self.write_in_s3_folder(
                            data=json_data
                            ,file_name= b + '.json'
                            ,relative_path=relative_path
                            ,print_res=False)
                        #jscode = self.__jscode["after_saving_data"].replace('@savebtn',savebtn)
                        if redirect:
                            return self.dynamic_site(page_name=form_name)
                        else:
                            return {"stored":True}
                    else:
                        return {"stored":False,"error_message":"Invalid username or email."}
                except Exception as e:
                    print(str(e))
                    return {"stored":False,"error_message":str(e)}
            else:
                return {"stored":False,"error_message":"Invalid token."}
        else:
            return {"error_message":"'cloudpy_org_aws_framework_client.web_portal_id has not been set.'"}
            
    #__________________________________________________________________________
    def read_form_data(self,username_or_email:str,temp_token:str,form_name:str):
        if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token):
            try:
                a = self.user_ref(username_or_email)
                b = self.ofuscate(a)
                if len(b) > 1:
                    rslt = self.get_s3_file_content(
                        file_name=b + '.json'
                        ,relative_path=self._secrets_relative_path + self.ofuscate(self._treat_name(form_name))
                    )
                    return rslt
                else:
                    return {"error_message":"Invalid username or email."}
            except Exception as e:
                print(str(e))
        else:
            return {"error_message":"Invalid token."}
    #__________________________________________________________________________
    def read_web_portal_json_data(self,username_or_email:str,temp_token:str,folder_reference:str):
        if self.web_portal_id != None and type(self.web_portal_id) == str and len(self.web_portal_id) > 0:
            if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token):
                try:
                    a = self.user_ref(username_or_email)
                    b = self.ofuscate(a)
                    if len(b) > 1:
                        rslt = self.get_s3_file_content(
                            file_name=b + '.json'
                            ,relative_path=self._secrets_relative_path + self.web_portal_id + '/' + self.ofuscate(self._treat_name(folder_reference))
                        )
                        return rslt
                    else:
                        return {"error_message":"Invalid username or email."}
                except Exception as e:
                    print(str(e))
            else:
                return {"error_message":"Invalid token."}
        else:
            return {"error_message":"'cloudpy_org_aws_framework_client.web_portal_id has not been set.'"}    
    #__________________________________________________________________________
    def set_web_portal_variables(self
                                 ,web_portal_title:str=None
                                 ,auth_token_max_age_minutes:int=None
                                 ,default_redirect_if_not_authenticated:str=None
                                 ,default_redirect_when_logged:str=None
                                 ,notifications_email:str=None
                                 ,email_banner_img:str=None
                                 ,favicon_ico:str=None
                                 ,domain_to_restrict_access_to:str=None
                                 ,restart_pass_phrase:str=None
                                ):
        new_data = {}
        if web_portal_title != None:
            new_data["web_portal_title"] = web_portal_title
        if auth_token_max_age_minutes != None:
            new_data["auth_token_max_age_minutes"] = auth_token_max_age_minutes
        if default_redirect_if_not_authenticated != None:
            new_data["default_redirect_if_not_authenticated"] = default_redirect_if_not_authenticated
        if default_redirect_when_logged != None:
            new_data["default_redirect_when_logged"] = default_redirect_when_logged
        if notifications_email != None:
            new_data["notifications_email"] = notifications_email
        if email_banner_img != None:
            new_data["email_banner_img"] = email_banner_img
        if favicon_ico != None:
            new_data["favicon_ico"] = favicon_ico
        if domain_to_restrict_access_to != None:
            new_data["domain_to_restrict_access_to"] = domain_to_restrict_access_to
        if restart_pass_phrase != None:
            new_data["restart_pass_phrase"] = restart_pass_phrase
        rslt = self._pre_stud(
            storage_label = 'portal_metadata'
            ,structure_name = 'web_portal_variables'
            ,structured_data = new_data
            ,storage_type='merge'
            ,within_web_portal=True)
        web_portal_variables = self.get_web_portal_variables()
        dc = ''
        for i in [i for i in set(web_portal_variables.keys()) if i != 'co_updates_log']:
            if type(web_portal_variables[i]) == str:
                dc += 'self.' + i + ' = "' + web_portal_variables[i] + '"\n'
            else:
                dc += 'self.' + i + ' = ' + str(web_portal_variables[i]) + '\n'
        exec(dc)
    
    #__________________________________________________________________________
    def get_web_portal_variables(self):
        return self._gds(structure_name='web_portal_variables',storage_label='portal_metadata',within_web_portal=True)
    #__________________________________________________________________________
    def write_in_web_portal_s3_folder(self,data:object,file_name:str,relative_path:str,success_message:str=None):
        if self.web_portal_id != None and self.web_portal_id != '':
            relative_path = self.ofuscate(self._treat_name(relative_path))
            relative_path = self._secrets_relative_path + self.web_portal_id + '/' + relative_path
            self.write_in_s3_folder(data=data,file_name=file_name,relative_path=relative_path)
            if success_message != None and success_message != '':
                print(success_message)
        else:
            print('cloudpy_org_aws_framework_client.web_portal_id has not been set.')
    #__________________________________________________________________________
    def read_from_web_portal_s3_folder(self,file_name:str,relative_path:str):
        if self.web_portal_id != None and self.web_portal_id != '':
            relative_path = self.ofuscate(self._treat_name(relative_path))
            relative_path = self._secrets_relative_path + self.web_portal_id + '/' + relative_path
            return self.get_s3_file_content(file_name=file_name,relative_path=relative_path)
        else:
            print('cloudpy_org_aws_framework_client.web_portal_id has not been set.')
    #__________________________________________________________________________
    def current_datetime_str(self,local:bool=True):
        date_id,time_id = self.aws.ypt.date_time_id(local=local)
        return self.aws.ypt.date_time_str(date_id,time_id)
    #__________________________________________________________________________
    def _pre_stud(self
                  ,storage_label:str=None
                  ,structure_name:str=None
                  ,structured_data:dict=None
                  ,storage_type:str=None
                  ,within_web_portal:bool=False
                  ,username_or_email:str=None
                 ):
        if storage_label != None and structure_name != None and structured_data != None and storage_type != None:
            if username_or_email == None or username_or_email == '':
                username_or_email = self.aws_namespace + '_' + 'admin'
            storage_type = storage_type.lower().replace(' ','')
            try:
                a = structure_name
                b = self.ofuscate(a)
                if len(b) > 1:
                    ofsl = self.ofuscate(storage_label)
                    if within_web_portal:
                        relative_path = self._secrets_relative_path + self.web_portal_id + '/' + ofsl
                    else:
                        relative_path = self._secrets_relative_path + ofsl
                    file_name=b + '.json'
                    co_updates_log = [] 
                    if storage_type in ['append_keep_all_version','append_keep_last_version','replace','merge']:
                        structured_data.pop('co_updates_log', None)
                        if storage_type in ['append_keep_all_version','append_keep_last_version','merge']:
                            previous_version = self.get_s3_file_content(file_name=file_name,relative_path=relative_path)
                            co_updates_log = []
                            if type(previous_version) == dict:
                                if 'co_updates_log' in set(previous_version.keys()) and storage_type == 'all_versions':
                                    co_updates_log = previous_version['co_updates_log']
                                previous_version.pop('co_updates_log', None)
                            else:
                                previous_version = {}
                            date_id,time_id = self.aws.ypt.date_time_id(local=True)
                            creation_date = self.aws.ypt.date_time_str(date_id,time_id)
                            co_updates_log.append({creation_date:{'username_or_email':username_or_email,'previous_version':previous_version}})
                            if storage_type == 'merge':
                                #print('merging...\n')
                                #print('structured_data:',structured_data,'\n______________\n')
                                #print('previous_version:',previous_version,'\n______________\n')
                                data = self.aws.ypt.high_level_dict_merge(dict_new=structured_data,dict_old=previous_version)
                                #print('merged data:',data,'\n******************************\n')
                            else:
                                data = structured_data.copy()
                            data['co_updates_log'] = co_updates_log
                        else:
                            data = structured_data.copy()
                        self.write_in_s3_folder(
                            data=data
                            ,file_name=file_name
                            ,relative_path=relative_path
                            ,print_res=False)
                        return {"stored":True}
                else:
                    return {"stored":False,"error_message":"Invalid page name."}
            except Exception as e:
                print(str(e))
                return {"stored":False,"error_message":str(e)}
        else:
            return {"stored":False,"error_message":"missing input."}
    #__________________________________________________________________________
    def _stud(self
              ,storage_label:str=None
              ,username_or_email:str=None
              ,temp_token:str=None
              ,page_name:str=None
              ,structured_data:dict=None
              ,storage_type:str=None
              ,within_web_portal:bool=False):
        if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token):
            return self._pre_stud(
                storage_label=storage_label
                ,structure_name=page_name
                ,structured_data=structured_data
                ,storage_type=storage_type
                ,within_web_portal=within_web_portal
                ,username_or_email=username_or_email
            )

        else:
            return {"stored":False,"error_message":"Invalid username or email."}

    #__________________________________________________________________________
    def list_namespace_s3_content(self,reference_name:str):
        reference_name = self._treat_name(reference_name.replace('/',''))
        return self.list_s3_object(
            relative_path=self._secrets_relative_path + self.ofuscate(reference_name)
        )
    #__________________________________________________________________________
    def update_dynamic_page(self,username_or_email:str,temp_token:str,page_name:str,data:dict):
        self.update_web_portal_json(
            username_or_email = username_or_email
            ,temp_token = temp_token
            ,structure_name = page_name
            ,storage_label = 'dynamic_pages'
            ,data = data
            ,within_web_portal=True
        )
        
    #__________________________________________________________________________
    def update_web_portal_json(self
                               ,username_or_email:str
                               ,temp_token:str
                               ,structure_name:str
                               ,storage_label:str
                               ,data:dict
                               ,within_web_portal:bool=True
                              ):
        this_page_structure = data.copy()
        return self._stud(
            storage_label=storage_label
            ,username_or_email=username_or_email
            ,temp_token=temp_token
            ,page_name=structure_name
            ,structured_data=this_page_structure
            ,storage_type='merge'
            ,within_web_portal=within_web_portal
        )
    #_______________________________________________________ 
    def validate_data_for_pages_registry(self,data:dict):
        for page_name, page_data in data.items():
            if not isinstance(page_data, dict):
                return False
            page_type = page_data.get('page_type')
            active = page_data.get('active')
            if page_type == "custom":
                if not isinstance(active, bool):
                    return False
                if 'request_type' not in page_data or 'custom_code' not in page_data:
                    return False
                if not isinstance(page_data['request_type'], str) or not isinstance(page_data['custom_code'], str):
                    return False
            elif page_type == "authenticated_endpoint":
                if not isinstance(active, bool):
                    return False
            elif page_type == "secure_read_form_data":
                if not isinstance(active, bool):
                    return False
            elif page_type == "dynamic_site":
                if not isinstance(active, bool):
                    return False
            else:
                return False
        return True

    #_______________________________________________________   
    def update_pages_registry(self,data:dict,username_or_email:str=None):
        if self.validate_data_for_pages_registry(data=data) == False:
            print(self._update_pages_registry_warning)
        else:
            reference_name = "dynamic_pages"
            pre_files = [self.deofuscate(i.replace('.json','')) for i in self.list_namespace_s3_content(reference_name=reference_name)]
            scope_keys = set(data.keys())
            files = [i for i in pre_files if i not in self._reserved_endpoints and i in scope_keys]
            attributes = ["page_type","request_type","custom_code","active"]
            lp = len(files)
            for k in tqdm(range(lp),desc="Registering pages"):
                this_page_name = files[k]
                if this_page_name not in scope_keys:
                    data[this_page_name] = {}
                    page_structure = self.get_dynamic_page_structure(this_page_name)
                    if type(page_structure) == dict and 'active' not in set(page_structure.keys()):
                        data[this_page_name]['active'] = False
                self._pre_stud(
                    storage_label = 'dynamic_pages'
                    ,structure_name=this_page_name
                    ,structured_data=data[this_page_name]
                    ,storage_type='merge'
                    ,within_web_portal=True
                    ,username_or_email=username_or_email
                )
            rslt = self._pre_stud(
                storage_label = 'pages_metadata'
                ,structure_name='pages_registry'
                ,structured_data=data
                ,storage_type='merge'
                ,within_web_portal=True
                ,username_or_email=username_or_email
            )
            print(rslt)
            return rslt
    #_______________________________________________________
    def define_dynamic_page_structure(self,username_or_email:str,temp_token:str,page_name:str,page_structure:dict):
        return self.define_web_portal_json(
            username_or_email=username_or_email
            ,temp_token=temp_token
            ,structure_name=page_name
            ,storage_label='dynamic_pages'
            ,data=page_structure
        )
    #__________________________________________________________________________
    def define_web_portal_json(self,username_or_email:str,temp_token:str,structure_name:str,storage_label:str,data:dict):
        this_page_structure = data.copy()
        return self._stud(
            storage_label=storage_label
            ,username_or_email=username_or_email
            ,temp_token=temp_token
            ,page_name=structure_name
            ,structured_data=this_page_structure
            ,storage_type='merge'
            ,within_web_portal=True
        )
    #__________________________________________________________________________
    #__________________________________________________________________________
    def extract_text_from_file(self,page_name:str=None,file_name:str=None,username:str=None):
        if page_name != None and file_name != None and page_name != '' and file_name != '':
            relative_path = self.uploaded_folder_path(page_name,username=username)
            full_path = relative_path + file_name
            file_name_ref = file_name.lower()
            if file_name_ref.endswith('.pdf'): 
                try:
                    response = self.aws.ypt.s3_client.get_object(Bucket=self.bucket_name, Key=full_path)
                    pdf_content = response['Body'].read()
                    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
                    text = ""
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text()
                    return text
                except Exception as e:
                    print("Error:", str(e))
            elif file_name_ref.endswith('.csv'):
                try:
                    response = self.aws.ypt.s3_client.get_object(Bucket=self.bucket_name, Key=full_path)
                    csv_content = response['Body'].read().decode('utf-8')
                    text = str(pd.read_csv(StringIO(csv_content)))
                    return text
                except Exception as e:
                    print("Error:", str(e))
            elif file_name_ref.endswith('.xlsx'):
                try:
                    response = self.aws.ypt.s3_client.get_object(Bucket=self.bucket_name, Key=full_path)
                    excel_content = response['Body'].read().decode('utf-8')
                    text = str(pd.read_excel(StringIO(csv_content)))
                    return text
                except Exception as e:
                    print("Error:", str(e))
            elif file_name_ref.endswith('.txt') or file_name_ref.endswith('.json'):
                try:
                    text = str(self.get_s3_file_content(file_name=file_name,relative_path=relative_path))
                    return text
                except Exception as e:
                    print("Error:", str(e))
        else:
            return 'page_name and file_name arguments are required.'
    #__________________________________________________________________________
    def uploaded_folder_path(self,page_name:str=None,username:str=None):
        a = self.ofuscate('uploaded_files')
        b = self.ofuscate(page_name)
        relative_path = self._secrets_relative_path + self.web_portal_id + '/' + a + '/'
        if page_name != None and page_name != '':
            b = self.ofuscate(page_name)
            relative_path += b +'/'
        if username != None and username != '':
            c = self.ofuscate(username)
            relative_path += c +'/'
        relative_path = relative_path.replace('/settings','settings')
        return relative_path
    #__________________________________________________________________________
    def us_files(self,page_name:str=None,email_or_username:str=None):
        us = self.user_ref(email_or_username)
        if us != None and len(us) > 6:
            relative_path = self.uploaded_folder_path(page_name=page_name,username=us)
            return self.aws.ypt.find_files_in_s3_folder(self.get_full_path(relative_path))
        else:
            return set()
    #__________________________________________________________________________
    def upload_file(self,page_name:str=None,username:str=None):
        print('request.method: ',request.method)
        if request.method == 'POST':
            img = request.files['file']
            filename = ""
            if img: 
                    filename = secure_filename(img.filename)
                    if filename.split('.')[1] in ['txt','pdf']:
                        img.save(filename)
                        relative_path = self.uploaded_folder_path(page_name=page_name,username=username)
                        full_path = relative_path + filename
                        print('full_path:',full_path)
                        self.aws.ypt.s3_client.upload_file(
                            Filename=filename
                            ,Bucket=self.bucket_name
                            ,Key=full_path
                        )
                        uploaded_message = "File succesfully uploaded to " + full_path
            if filename == "":
                uploaded_message = "Error: The file could be uploaded."
            print(uploaded_message)
            return filename, uploaded_message
        else:
            print('nothing happened')
            return '',''
        
    #__________________________________________________________________________
    def get_web_portal_chatbot_facts(self,username_or_email:str=None,temp_token:str=None):
        if username_or_email == None or username_or_email == '':
            us = request.cookies.get('us')
        else:
            us = username_or_email
        if temp_token == None or temp_token == '':
            ttk = request.cookies.get('us')
        else:
            ttk = temp_token
        if self.user_token_authentication(username_or_email=us,temp_token=ttk):
            storage_label='chatbot_facts'
            structure_name='facts_' + us.lower()
            return self._gds(structure_name=structure_name,storage_label=storage_label,within_web_portal=True)
        else:
            return 'Invalid authentication.'
    #__________________________________________________________________________
    def update_web_portal_chatbot_facts(self,content:str,username_or_email:str=None,temp_token:str=None):
        if username_or_email == None or username_or_email == '':
            us = request.cookies.get('us')
        else:
            us = username_or_email
        if temp_token == None or temp_token == '':
            ttk = request.cookies.get('us')
        else:
            ttk = temp_token
        data = {"content":content}
        return self.update_web_portal_json(
            username_or_email=us
            ,temp_token=ttk
            ,structure_name='facts_' + us.lower()
            ,storage_label='chatbot_facts'
            ,data=data
            ,within_web_portal=True
        )
    
    #__________________________________________________________________________
    def form_data_display(self,username:str,page_name:str,label_title:str=''):
        """
        ***
        Displays the details of stored data for a given page name for a given username
        ***
        """
        this_id = ''
        if label_title != None and len(label_title) > 3:
            this_id = label_title.lower().replace(' ','')[0:3]
        this_id += '_' + page_name.lower().replace(' ','')[0:3] 
        this_id +='_' + page_name.lower().replace(' ','')[::-1][0:3]
        users = []
        users.append(username)
        tdct = {}
        #___________________________________________________
        k0 = 'select'
        tdct[k0] = {}
        tdct[k0]['html'] = """
        <br>
        <script>
        let custom_select_data_str = '@custom_select_data';
        let custom_select_data = JSON.parse(custom_select_data_str);
        function details(that)
        { 
        var this_option_value = that.options[that.selectedIndex].innerHTML;
        var selected_data = custom_select_data["@username"]["@page_name"][this_option_value];
        alert(JSON.stringify(selected_data));
        }
        </script>
        <label for="@id" class="sensation" id="@id_label" style="@custom_style02">@label_title</label>
        <br>
        <select id="@id" class="sensation inx" onchange="details(this);" onload="">
        @options
        </select>
        <br>
        """.replace('@k',k0)
        tdct[k0]['object'] = "<option style='font-size:15px;padding:5px;'>@object</option>"
        tdct[k0]['params'] = ['@id','@label_title','@options']
        options = ''
        custom_select_data = self.web_portal_insights(just_these_usernames = users,just_these_pages =[page_name])
        for k,v in custom_select_data.items():
            for k1,v1 in v.items():
                for k2,v2 in v1.items():
                    if 'co_' not in k2:
                        options += tdct[k0]['object'].replace('@object',k2)
        html_code = tdct[k0]['html'].replace('@id',this_id)\
        .replace('@label_title',label_title)\
        .replace('@options',options)\
        .replace('@username',username)\
        .replace('@page_name',page_name)\
        .replace('@custom_select_data',str(custom_select_data).replace('&nbsp;','').replace('\n','').replace("'",'"'))
        return html_code
    #__________________________________________________________________________
    def web_portal_users(self):
        rslt = {}
        users = self.aws.ypt.find_files_in_s3_folder(self.get_full_path(self._users_relative_path))
        for i in users:
            a = i.split('.')[0]
            b = self.ofuscate(a)
            us = a.split('-0-')[0]
            if len(b) > 1 and len(us) > 1:
                rslt[us] = {}
                profile = self.get_s3_file_content(
                    file_name=i + '.json'
                    ,relative_path=self._users_relative_path)
                profile.pop('temp_token', None)
                profile.pop('keystr_with_expiration', None)
                profile.pop('email_notification_token', None)
                profile.pop('encrypted_pwd', None)
                rslt[us] = profile
        return rslt
    #__________________________________________________________________________
    def update_web_portal_roles(self,roles_and_policies:dict,full_refresh:bool=False):
        users = [self.user_ref(i) for i in set(roles_and_policies.keys())]
        for i in users:
            a = i.split('.')[0]
            us = a.split('-0-')[0]
            if len(us) > 1:
                profile = self.get_s3_file_content(
                    file_name=i + '.json'
                    ,relative_path=self._users_relative_path)
                roles = profile['roles']
                policies = profile['policies']
                if policies == {}:
                    policies = []
                policies_names = [list(set(x.keys()))[0] for x in policies if type(x) == dict and x!= {}]
                #________________________________________
                these_keys = set(roles_and_policies[us].keys())
                new_policies,new_roles = [],[]
                if 'roles' in these_keys:
                    new_roles = [x.lower().replace(' ','') for x in set(roles_and_policies[us]['roles'])]
                    if full_refresh:
                        roles = new_roles
                    else:
                        for new_role in new_roles:
                            if new_role not in roles:
                                roles.append(new_role)
                if 'policies' in these_keys:
                    new_policies = roles_and_policies[us]['policies']
                    if full_refresh:
                        policies = new_policies
                    else:
                        for new_policy in new_policies:
                            u = [list(set(i.keys()))[0] for x in new_policy if type(x) == dict and x!= {}]
                            if len(u) > 0 and u[0] not in policies_names:
                                this_new_policy = {u[0].lower().replace(' ',''):new_policy[u[0]]}
                                policies.append(this_new_policy)
                profile['roles'] = roles
                profile['policies'] = policies
                try:
                    self.aws.ypt.store_str_as_file_in_s3_folder(
                            strInput=profile
                            ,fileName=i + '.json'
                            ,s3FullFolderPath=self.get_full_path(self._users_relative_path)
                            ,region_name=self.region_name
                            ,print_res=False)
                    return 'success'
                except Exception as e:
                    return 'error: could not update the policies.'
                    
        
    #__________________________________________________________________________
    def web_portal_insights(self,just_these_usernames:list=[],just_these_pages:list=[],include_profile:bool=False):
        rslt = {}
        folder_references = []
        pages = self._gds(structure_name='pages_registry',storage_label='pages_metadata',within_web_portal=True)
        if len(just_these_pages) > 0 and type(just_these_pages) == list:
            folder_references = just_these_pages
        else:
            for k,v in pages.items():
                if type(v) == dict:
                    keys = set(v.keys())
                    if 'page_type' in keys and 'active' in keys:
                        if v['page_type'] in ['secure_read_form_data','authenticated_endpoint'] and v['active'] == True:
                            folder_references.append(k)
        users = []
        if len(just_these_usernames) > 0 and type(just_these_usernames) == list:
            for i in just_these_usernames:
                users.append(self.user_ref(i))
        else:
            users = self.aws.ypt.find_files_in_s3_folder(self.get_full_path(self._users_relative_path))
        for i in users:
            a = i.split('.')[0]
            b = self.ofuscate(a)
            us = a.split('-0-')[0]
            if len(b) > 1 and len(us) > 1:
                rslt[us] = {}
                if include_profile:
                    profile = self.get_s3_file_content(
                        file_name=i + '.json'
                        ,relative_path=self._users_relative_path)
                    profile.pop('temp_token', None)
                    profile.pop('keystr_with_expiration', None)
                    profile.pop('email_notification_token', None)
                    rslt[us]['profile'] = profile
                for folder_reference in folder_references:
                    relative_path=self._secrets_relative_path + self.web_portal_id + '/' + self.ofuscate(self._treat_name(folder_reference))
                    rslt[us][folder_reference] = self.get_s3_file_content(
                        file_name=b + '.json'
                        ,relative_path=relative_path)
        return rslt
    #__________________________________________________________________________
    def get_web_portal_json(self,username_or_email:str,temp_token:str,structure_name:str,storage_label:str):
        if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token):
            return self._gds(structure_name=structure_name,storage_label=storage_label,within_web_portal=True)
        else:
            return 'Invalid authentication.'
    #__________________________________________________________________________
    def define_common_menu(self,username_or_email:str,temp_token:str,menu_structure:dict):
        if self.web_portal_id != None and self.web_portal_id != '':
            return self._stud(
                storage_label='common_menus'
                ,username_or_email=username_or_email
                ,temp_token=temp_token
                ,page_name=self.web_portal_id
                ,structured_data=menu_structure
                ,storage_type='merge'
                ,within_web_portal=True
            )
        else:
            return 'cloudpy_org_aws_framework_client.web_portal_id has not been set.'
    #_________________________________________________________________________
    def construct_pages(self):
        pages_registry = self._gds(structure_name='pages_registry',storage_label='pages_metadata',within_web_portal=True)
        ptemp = "#______________________________________________________________\n"\
        "@app.route('/@endpoint_name'@methods)\n"\
        "def co_@endpoint_name():\n"\
        "@dynamic_code\n"
        allowed_page_types = ['dynamic_site','authenticated_endpoint','secure_read_form_data','custom']
        pages = ''
        pages_registry.pop('updates_log', None)
        pages_registry.pop('co_updates_log', None)
        for k,v in pages_registry.items():
            page = ptemp.replace('@endpoint_name',k)
            page_type = v['page_type']
            if page_type in allowed_page_types:
                active = v['active']
                if active:
                    if page_type != 'custom':
                        dynamic_code = '\treturn aws.' + page_type + '()'
                    else:
                        cus = v['custom_code'].split('\n')
                        custom_code = ''
                        w = 0
                        for i in cus:
                            if len(i) > 0:
                                w+= 1
                                if w > 1:
                                    custom_code += '\n'
                                custom_code += '\t' + i

                        dynamic_code = custom_code
                else:
                    dynamic_code = '\treturn "The requested page is not active."'  
            page = page.replace('@dynamic_code',dynamic_code)
            methods = ''
            if 'request_type' in set(v.keys()):
                request_type = v['request_type']
                if type(request_type) == str:
                    a = request_type.upper().replace(' ','').split(',')
                    methods_list = [i.upper() for i in a if i in ['POST','GET']]
                elif type(request_type) == list:
                    methods_list = [i.upper() for i in request_type if i in ['POST','GET']]
                else:
                    methods_list = [] 
                if len(methods_list) > 0:
                    methods = ',' + 'methods=' + str(methods_list)
            page = page.replace('@methods',methods)
            pages += page + '\n'
            if k == 'custom_ai_chatbot':
                print(page)
        if len(pages) > 0:
            pages = '\n' + pages
        return pages    
    #__________________________________________________________________________
    def _gds(self,structure_name:str=None,storage_label:str=None,within_web_portal:bool=False):
        if structure_name != None and storage_label != None:
            try:
                a = structure_name
                b = self.ofuscate(a)
                if len(b) > 1:
                    ofsl = self.ofuscate(storage_label)
                    if within_web_portal:
                        relative_path = self._secrets_relative_path + self.web_portal_id + '/' + ofsl
                    else:
                        relative_path = self._secrets_relative_path + ofsl
                    file_name= b + '.json'
                    page_structure = self.get_s3_file_content(
                        file_name=file_name
                        ,relative_path=relative_path
                    )
                    return page_structure
                else:
                    return {"error_message":"Structure definition not found."}
            except Exception as e:
                print(str(e))
                return {"error_message":"Structure definition not found."}
    #__________________________________________________________________________
    def get_dynamic_page_structure(self,page_name:str,within_web_portal:bool=True):
        return self._gds(structure_name=page_name,storage_label='dynamic_pages',within_web_portal=within_web_portal)
        #__________________________________________________________________________
    def get_common_menu(self,web_portal_id:str):
        return self._gds(structure_name=web_portal_id,storage_label='common_menus',within_web_portal=True)
        
    #___________________________________________________
    def dynamic_site(self
                     ,bannertitle:str=''
                     ,banner_subtitle:str=''
                     ,bannerbackground:str=''
                     ,topcontent:str=''
                     ,cookie_max_age_minutes:int=30,jscode:str='',page_name:str=None):
        if page_name == None or page_name == '':
            page_name = request.base_url[::-1].split('/')[0][::-1]
        dynamic_form = self.get_dynamic_page_structure(page_name)
        menu_structure = self.get_common_menu(web_portal_id=self.web_portal_id)
        maincontent,body_style,body_class,display_banner,bannertitle_x,banner_subtitle_x,bannerbackground_x,topcontent_x,requires_authentication = self.web.complete_dynamic_form(dynamic_form)
        always_editable = False
        if 'always_editable' in set(dynamic_form.keys()):
            if dynamic_form['always_editable'].lower().replace(' ','') == 'yes':
                always_editable = True
        section_ids = list(dynamic_form['sections'].keys());
        section_load_base = """
        setTimeout(function(){ load_section_by_name("@section_title","load"); },300);
        setTimeout(function(){ load_section_by_name("@section_title","undox"); },2100);
        """
        
        jscode2 = "";
        k = 'sections'
        for i in section_ids:
            isrt = str(i)
            edit_enabled = 'no'
            if 'edit_enabled' in set(dynamic_form[k][isrt].keys()):
                edit_enabled = dynamic_form[k][isrt]['edit_enabled']
            if edit_enabled == 'yes':
                section_title = dynamic_form[k][isrt]['section_title']
                #print('section_title:',section_title)
                jscode2 += section_load_base.replace('@section_title',section_title)
            
        jscode2 += """
        """
        if bannertitle == None or bannertitle == '':
            bannertitle = bannertitle_x
            
        if banner_subtitle == None or banner_subtitle == '':
            banner_subtitle = banner_subtitle_x
            
        if bannerbackground == None or bannerbackground == '':
            bannerbackground = bannerbackground_x
            
        if topcontent == None or topcontent == '':
            topcontent = topcontent_x
        us = request.cookies.get('us')
        ttk = request.cookies.get('ttk')
        auth = self.user_token_authentication(username_or_email=us,temp_token=ttk)
        try:
            username = us.split('@')[0]
        except:
            username = us
        common_menu = self.web.create_common_menu(menu_structure,auth=auth,username=username)
        root_url = self.get_root_url()
        filename, uploaded_message = self.upload_file(page_name=page_name,username=self.user_ref(us))
        resp = make_response(
            render_template(
                'canvas.html'
                ,web_portal_title=self.web_portal_title
                ,favicon_ico = self.favicon_ico
                ,bannerbackground=bannerbackground
                ,bannertitle=bannertitle
                ,banner_subtitle=banner_subtitle
                ,topcontent=topcontent
                ,common_menu = common_menu
                ,maincontent = maincontent
                ,body_style=body_style
                ,body_class=body_class
                ,display_banner=display_banner
                ,jscode=jscode
                ,jscode2=jscode2
                ,root_url=root_url
                ,secure_cloudpy_org=subscription_url.replace('w'*3,msh)
                ,www_cloudpy_org=subscription_url
                ,filename=filename
                ,uploaded_message=uploaded_message 
            ))
        resp.headers['Access-Control-Allow-Origin'] = root_url
        #print('page_name: *' + page_name + '*')
        max_age = cookie_max_age_minutes*60
        resp.set_cookie('form_name',page_name,max_age=max_age)
        resp.set_cookie('requires_authentication',str(requires_authentication),max_age=max_age)
        return resp
    #___________________________________________________
    def secure(self):
        json_data = request.json
        if 'data' in set(json_data.keys()):
            try:
                rslt = self.aws.ypt.encrypt(json_data['data'],self.__gen_key)
                print('Secure ok.')
                print(rslt)
            except:
                rslt = 'Wrong input.'
        else:
            rslt = 'Key not found.'
        return {"co_data":rslt}
    #___________________________________________________
    def ttk(self):
        resp = make_response(redirect('/auth'))
        root_url = self.get_root_url()
        resp.headers['Access-Control-Allow-Origin'] = root_url
        try:
            us = request.cookies.get('us')
            cpw = request.cookies.get('cpw')
            ttk = self.get_user_temp_token(username_or_email=us,pwd=cpw)
            #print('us:',us)
            #print('cpw:',cpw)
            #print('ttk:',ttk)
            max_age = self.auth_token_max_age_minutes*60
            resp.set_cookie('ttk',ttk,max_age=max_age)
            resp.set_cookie('cpw','')
        except Exception as e:
            print('Error:',str(e))
            resp.set_cookie('ttk','')
            resp.set_cookie('cpw','')
        return resp
    def auth(self,if_authenticated:str=None,if_not_authenticated:str=None):
        if if_authenticated == None:
            if_authenticated = self.default_redirect_when_logged
        if if_not_authenticated == None:
            if_not_authenticated = self.default_redirect_if_not_authenticated
        us = request.cookies.get('us')
        ttk = request.cookies.get('ttk')
        auth = self.user_token_authentication(username_or_email=us,temp_token=ttk)
        if auth == True:
            resp = make_response(redirect(if_authenticated))
        else:
            resp = make_response(redirect(if_not_authenticated))
        root_url = self.get_root_url()
        resp.headers['Access-Control-Allow-Origin'] = root_url
        return resp
    #___________________________________________________
    def authenticated_endpoint(self
                               ,bannertitle:str=''
                               ,banner_subtitle:str=''
                               ,bannerbackground:str=''
                               ,topcontent:str=''
                               ,redirect_if_not_authenticated:str=None):
        if redirect_if_not_authenticated == None:
            redirect_if_not_authenticated = self.default_redirect_if_not_authenticated
            
        us = request.cookies.get('us')
        ttk = request.cookies.get('ttk')
        auth = self.user_token_authentication(username_or_email=us,temp_token=ttk)
        if auth == True:
            return self.dynamic_site(
                bannertitle=bannertitle
                ,banner_subtitle=banner_subtitle
                ,bannerbackground=bannerbackground
                ,topcontent=topcontent)
        else:
            resp = make_response(redirect(redirect_if_not_authenticated))
            root_url = self.get_root_url()
            resp.headers['Access-Control-Allow-Origin'] = root_url
            return resp
    #___________________________________________________
    def obtain(self):
        json_data = request.json
        if 'data' in set(json_data.keys()):
            us = request.cookies.get('us')
            ttk = request.cookies.get('ttk')
            folder_reference = json_data['data']
            co_data = self.read_web_portal_json_data(username_or_email=us,temp_token=ttk,folder_reference=folder_reference)
            return {"co_data":co_data}
        else:
            return {"co_data":{"Error:":"Post request not allowed."}}
    #___________________________________________________
    def secure_read_form_data(self,redirect_if_not_authenticated:str=None):
        if redirect_if_not_authenticated == None:
            redirect_if_not_authenticated = self.default_redirect_if_not_authenticated
        if redirect_if_not_authenticated[0:1] == '/':
            l = len(redirect_if_not_authenticated)
            redirect_if_not_authenticated = redirect_if_not_authenticated[1:l]
        us = request.cookies.get('us')
        ttk = request.cookies.get('ttk')
        form_name = request.base_url[::-1].split('/')[0][::-1]
        if form_name != None or len(form_name) > 0:
            if ttk != None and ttk != '':
                data = self.read_web_portal_json_data(
                    username_or_email=us
                    ,temp_token=ttk
                    ,folder_reference=form_name
                )
                dynamic_js = ''
                base_code = self.web.dynamic_js['load_data_dynamic_routine']
                jscode = ''
                #print('loaded data:',data)
                if type(data) == dict:
                    for k,v in data.items():
                        if type(v) == str:
                            dynamic_js += base_code.replace('@k',k).replace('@v','"' + str(v) + '"')
                        elif type(v) ==  list:
                            dynamic_js += base_code.replace('@k',k).replace('@v','[]')
                            dj = ''
                            for i in v:
                                dj += base_code.replace('@k',k).replace(' = @v;','.push("' + i + '");')
                            dynamic_js += dj
                    jscode = self.web.dynamic_js['load_data_dynamic_code'].replace('@dynamic_js',dynamic_js)
                    #print('jscode:',jscode)
                return self.dynamic_site(jscode=jscode,page_name=form_name)
            else:
                return self.dynamic_site(page_name=redirect_if_not_authenticated)
        else:
            return 'Page name not defined.'
    #___________________________________________________
    def secure_save_form_data(self,redirect:bool=False):
        json_data = request.json
        us = request.cookies.get('us')
        form_name = request.cookies.get('form_name')
        requires_auth = request.cookies.get('requires_authentication')
        if requires_auth.lower().replace(' ','') == 'false':
            temp_token = None
            requires_auth = False
        else:
            temp_token = request.cookies.get('ttk')
            requires_auth = True
        if form_name == 'register':
            requires_auth = False
        #print('us:',us)
        #print('form_name:',form_name)
        #print('requires_auth:',requires_auth)
        #print('************************************')
        date_id,time_id = self.aws.ypt.date_time_id(local=True)
        last_update = self.aws.ypt.date_time_str(date_id,time_id)
        if json_data != None and json_data != {}:
            #print('json_data:',json_data)
            json_data_keys = set(json_data.keys())
            if 'co_main_identifier' in json_data_keys and json_data['co_main_identifier'] in json_data_keys:
                sub_json_data = json_data
                sub_json_data['co_last_update'] = last_update
                co_main_identifier = json_data[json_data['co_main_identifier']]
                sub_json_data.pop('co_main_identifier', None)
                co_sort_order = {}
                if 'co_sort_order' in json_data_keys:
                    co_sort_order = json_data['co_sort_order']
                    sub_json_data.pop('co_sort_order', None)
                us = request.cookies.get('us')
                ttk = request.cookies.get('ttk')
                co_data = {}
                co_data = self.read_web_portal_json_data(username_or_email=us,temp_token=ttk,folder_reference=form_name)
                co_data.pop('co_main_identifier', None)
                co_data.pop('co_sort_order', None)
                co_data[co_main_identifier] = sub_json_data
                co_data['co_sort_order'] = co_sort_order
            else:
                co_data = json_data
                co_data['co_last_update'] = last_update
            #print('co_data:',co_data)
            #print('folder_reference (where data is being saved):',form_name)
            return self.store_web_portal_json_data(
                username_or_email=us
                ,folder_reference=form_name
                ,json_data=co_data
                ,requires_auth=requires_auth
                ,temp_token=temp_token
                ,redirect=redirect
            )
        else:
            return 'Error SFD01: No storage took place.'
    def get_root_url(self,local:bool=False):
        if local:
            root_url = 'http://localhost'
        else:
            form_name = request.base_url[::-1].split('/')[0][::-1]
            root_url = request.base_url.replace('/' + form_name + '/','').replace('/' + form_name,'') 
        return root_url
    #___________________________________________________
    def generate_confirmation_link(self,username_or_email:str,local:bool=False):
        #print('root_url:',self.get_root_url())
        root_url = self.get_root_url(local=local)
        confirmartion_url = root_url + '/confirm_email?email_confirmation_token='
        dictstr = str(self.aws.ypt.gen_encrypted_data_with_expiration(original_message=username_or_email,minutes_to_expire=60))
        encdat = self.aws.ypt.encrypt(dictstr,self.__gen_key)
        return confirmartion_url + encdat
    #___________________________________________________
    def validate_email_confirmation_link(self):
        try:
            encdat = str(request.args.get("email_confirmation_token"))
            try:
                decdat = self.aws.ypt.decrypt(encdat,self.__gen_key)
                data = self.aws.dictstr_to_dict(decdat)
                username_or_email = self.aws.ypt.decrypt_before_expiration(data)
                response_message = ''
            except:
                response_message = 'Invalid confirmation link.'
            if 'encryption expired' in username_or_email:
                response_message = 'The confirmation link has expired.'
            elif response_message == '' and len(username_or_email) > 4:
                try:
                    self.confirm_user(username_or_email=username_or_email)
                    ch = self.check_user(username_or_email=username_or_email)
                    if str(ch['exists']).lower().replace(' ','') == 'true':
                        if str(ch['confirmed']) == '1':
                            match_type = ch['match_type']
                            what = match_type[0:1].upper() + match_type[1:len(match_type)]
                            response_message = '<h2>' + what + '<br>' + username_or_email + ''\
                            '<br>has been confirmed.<br><p><a style="font-size:20px;color:rgb(19,25,33);" href="/login">'\
                            'Click here to go to login.</a></p></h2>'
                        else:
                            response_message = 'Error CE01: Could not confirm user.'
                    else:
                        response_message = "User does not exist."
                except:
                    response_message = 'Error CE02: Could not confirm user.'
        except:
            response_message = 'Error CE03: email_confirmation_token not provided.'
            
        response_message = response_message.replace('\n','')
        modal_jscode = "setTimeout(pop_content('@response_message'),200);"
        modal_jscode = modal_jscode.replace('@response_message',response_message)
        root_url = self.get_root_url()
        resp = make_response(
            render_template(
                'canvas.html'
                ,web_portal_title=self.web_portal_title
                ,favicon_ico = self.favicon_ico
                ,modal_jscode=modal_jscode
                ,root_url=root_url
                ,secure_cloudpy_org=subscription_url.replace('w'*3,msh)
                ,www_cloudpy_org=subscription_url
            ))
        resp.headers['Access-Control-Allow-Origin'] = root_url

        return resp
    #___________________________________________________
    def send_confirmation_email(self):
        local = False
        if 'localhost' in request.base_url.lower().replace(' ',''):
            local = True
        json_data = request.json
        email_banner_img = self.email_banner_img
        if 'email' not in set(json_data.keys()):
            return {'error_message':'email not provided.'}
        else:
            email = json_data['email']
            email_notification_sender = self.notifications_email
            if email_notification_sender == None or email_notification_sender == '':
                return {'error_message':'cloudpy_org_aws_framework_client.notifications_email not set yet.'}
            else:
                confirmation_link = self.generate_confirmation_link(username_or_email=email,local=local)
                #print('root_url:',self.get_root_url())
                root_url = self.get_root_url(local=local)
                SENDER = email_notification_sender
                RECIPIENT = email
                #AWS_REGION = self.region_name
                SUBJECT = self.web_portal_title + " - Email Confirmation"
                BODY_TEXT = ("")
                BODY_HTML = """<html>
                <head>
                <style>
                @font-face {
                  font-family: sensationLight;
                  src: url("@root_url/static/fonts/sansation_light.woff");
                }
                </style>
                </head>
                <body>
                <div class="text-center" style="width:800px;">
                  <img src="@root_url/static/img/@email_banner_img" alt="" style="max-width:800px;">
                  <br>
                  <h3 style="color:gray;font-family:sensationLight;">Thank you for registering!</h3>
                  <br>
                  <h2 style="color:black;font-family:sensationLight;">Please click 
                  <a href="@confirmation_link" style="color:blue;font-family:sensationLight;">
                  HERE
                  </a> to confirm your email.</h2>
                  </div>
                </body>
                </html>
                """
                BODY_HTML = BODY_HTML.replace("@root_url",root_url)\
                .replace("@confirmation_link",confirmation_link)\
                .replace("@email_banner_img",email_banner_img)
                CHARSET = "UTF-8"
                client = self.ses
                try:
                    response = client.send_email(
                        Destination={
                            'ToAddresses': [
                                RECIPIENT,
                            ],
                        },
                        Message={
                            'Body': {
                                'Html': {
                                    'Charset': CHARSET,
                                    'Data': BODY_HTML,
                                },
                                'Text': {
                                    'Charset': CHARSET,
                                    'Data': BODY_TEXT,
                                },
                            },
                            'Subject': {
                                'Charset': CHARSET,
                                'Data': SUBJECT,
                            },
                        },
                        Source=SENDER,
                        #ConfigurationSetName=CONFIGURATION_SET,
                    )
                    return {'success':'email sent'}
                except Exception as e:
                    return {'error_message':str(e)}
                
    #___________________________________________________
    def register_new_user(self):
        rslt_template = '<textarea class="sensation" onclick="pop_off();" style="cursor:default;font-size:16px;width:500px;height:200px;border:none" rowsnum=5>@rslt</textarea>'
        try:
            email = request.cookies.get('us').lower().strip()
            pwd = request.cookies.get('cpw').strip()
            cpwconf = request.cookies.get('cpwconf').strip()
        except Exception as e:
            email = ''
            pwd = ''
            cpwconf = ''
        rslt = ''
        if email != None and email != '' and pwd != None and pwd != '' and cpwconf != None and cpwconf != '': 
            if self.aws.ypt.validate_str_as_email(email):
                username = email.split('@')[0]
                if self.domain_to_restrict_access_to != None and self.domain_to_restrict_access_to != '':
                    if self.domain_to_restrict_access_to in email:
                        if email.split('@')[1] != self.domain_to_restrict_access_to:
                            rslt = 'The email provided does not belong to the "' + self.domain_to_restrict_access_to + '" domain.'
                    else:
                        rslt = 'The email provided does not belong to the "' + self.domain_to_restrict_access_to + '" domain.'
                if rslt == '':
                    pwd_validation = self.aws.ypt.validate_password_format(pwd)
                    if  pwd_validation.lower().replace(' ','') == 'ok':
                        print('pwd validated')
                        if pwd == cpwconf:
                            rslt = self.create_user(username=username,email=email,pwd=pwd)
                            json_data={}
                            json_data['email'] = email
                            local = False
                            if 'localhost' in request.base_url.lower().replace(' ',''):
                                local = True
                            #print('root_url:',self.get_root_url())
                            root_url = self.get_root_url(local=local)
                            url = root_url + '/send_confirmation_email'
                            confirmation_rslt = requests.post(url=url,json=json_data ,verify=False).json()
                            #print('confirmation_rslt:',confirmation_rslt)

                        else:
                            rslt = 'Password and password confirmation must match.'
                    else:
                        rslt = pwd_validation
                        #print(rslt)
            else:
                rslt = 'Invalid email input. Please make sure you typed a valid email address.'
        else:
            rslt = 'Missing input.'
        rslt = rslt_template.replace('@rslt',rslt)
        return {"co_data":rslt}