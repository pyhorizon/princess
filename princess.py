#encoding:gb2312
#@author:horizon
#@version:0.2
#plotly special parameters: editable:true

from flask import Flask,jsonify,request,render_template
from multiprocessing import Process
import os
import time
import torch
import random
import numpy as np
import pickle as pkl


app = Flask(__name__)


all_datas = []
#counter = 0
'''
@app.route('/get_data')
def post_data():
    global v
    w = np.array(v[:])

    return jsonify(values = [hist(w)])
'''
@app.route('/get_data')
def post_data_by_pkl():
    try:
        with open('./temp_data.pkl','rb') as f:
            values = pkl.load(f)
    except:
        time.sleep(0.05)
        with open('./temp_data.pkl', 'rb') as f:
            values = pkl.load(f)
    #print(values[1])
    return jsonify(values=values)


@app.route('/')
def website():
    return render_template('version.html')


def histx(w):
    #return xaxis range
    return jsonify(r = [w.min(),w.max()])

def hist(w):
    group_distance = ((w.max() - w.min()) / 19).tolist() if str(type(w)) == "<class 'torch.Tensor'>"\
        else ((w.max() - w.min() )/ 19)
    x = [(i * (group_distance)) for i in range(21)]
    y = [np.where((w < (i + 1) * group_distance) & (w >= i * group_distance))[0]\
             .shape[0] for i in range(0, 21)]
    return [x,y]
class Figure:
    def __init__(self,style='darkness'):
        self.log = './temp_data.pkl'
        self.web = open('./templates/version.html','w+')
        #dict:name:{'type','data'}
        self.html = ['<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>hello,princess3!</title>\
        \n<link rel="stylesheet" href="static/layui/layui/css/layui.css"  media="all">\
        \n<script src="static/jquery.js"></script>\n<script src="static/plotly.min.js"></script>\n<script>var timer_list=[]</script>\n</head>\n<body>','\n<button onclick="stop()" class="layui-btn layui-btn-danger">stop</button><input id="inp"><script>function stop(){var i = document.getElementById("inp").value;clearInterval(timer_list[parseInt(i)]);alert("please wait a few seconds")}</script></body>','\n</html>']
        self.counter = 0
        self.row = 0
        self.widget_counter = 0
        self.data = []
        self.eyes = 0
        self.add('<script>web_root = {{ request.script_root|tojson|safe }};$(function(){})\n$.ajaxSetup({async:false});</script>')

    #add
    def add_weight(self,weight,chart_name='defaultbar',width=600,height=600,color='#4EACB6'):
        #if str(type(scalar)) == "<class 'torch.Tensor'>":
            #s = Array('f',scalar.tolist())
        width = int(width/100)
        height = int(height*0.9)
        self.insert('\n<div class="layui-col-xs{width}"><div id="{id}" style="height:{height}px"></div></div>'.format(id=chart_name,width=width,height=height))
        #length = str(len(weight))
        index = str(self.counter)
        self.add("\n<script>\nvar values=[0];\
        \nfunction get_data(){\
        $.getJSON(web_root+'/get_data',{},function(d){values = d.values;});\
        \n\n\treturn values;\n}\nfunction base"+index+"(){\
        \nvar layout={title:"+chart_name+"}\
        \ntrace = {x:get_data()["+index+"][0],y:get_data()["+index+"][1], type: 'bar',name:'t1',marker:{color:'"+color+"'}};\
        \nPlotly.plot('" + chart_name + "',[trace],{title:{text:'"+chart_name+"',font:{color:'white',size:16}},paper_bgcolor:'#00011A',plot_bgcolor:'#00011A',xaxis:{color:'white',linecolor:'white',showgrid:false},yaxis:{color:'white',linecolor:'white',showgrid:false}});\n}\nbase"+index+"();\
        \nfunction e"+index+"(){\
        Plotly.animate('"+chart_name+"',{layout:{title:{text:'"+chart_name+"',font:{color:'white',size:16}}},data:[{x:get_data()["+index+"][0],y:get_data()["+index+"][1],\
        type:'bar',name:'t1'}]})}\nvar t"+index+"=setInterval(e"+index+",200);timer_list.push(t"+index+");</script>")

        self.data.append(hist(weight))
        self.counter += 1

    def add_weights(self,weights,weight_names,chart_name='dufaultweights',width=600,height=600,colors=['#E75D2E','#DDEA78']):
        l = len(weights)
        colors_l = len(colors)
        data = '['
        update_data = ",data:["

        width = int(width / 100)
        height = int(height * 0.9)
        index = str(self.counter)
        for i in range(l):
            ii = str(i)
            if i <= colors_l-1:

                data = data + ("{ x:get_data()[" + index + "][" + ii + "][0],y:get_data()[" + index + "][" + ii + "][1], type: 'bar',name:'" +
                               weight_names[i] + "',marker:{color:'" + colors[i] + "'}},")

            else:
                data+="{ y:[get_data()[" + index + "][" + ii + "]], type: 'bar',name:'"+weight_names[i]+"'};"
            update_data += "{x:get_data()[" + index + "][" + ii + "][0],y:get_data()[" + index + "][" + ii + "][1],type:'bar'},"
        update_data = update_data[:-1]
        update_data += ']'

        data = data[:-1]
        data = data + ']'
        self.insert('\n<div class="layui-col-xs{width}"><div id="{id}" style="height:{height}px"></div></div>'.format(id=chart_name,width=width,height=height))
        self.add("\n<script>\nvar values=[0];\
                \nfunction get_data(){\
                $.getJSON(web_root+'/get_data',{},function(d){values = d.values;});\
                \n\n\treturn values;\n}\nfunction base" + index + "(){\
                \nPlotly.plot('" + chart_name + "',"+data+",{title:{text:'" + chart_name + "',font:{color:'white',size:16}},paper_bgcolor:'#00011A',plot_bgcolor:'#00011A',xaxis:{color:'white',linecolor:'white',showgrid:false},yaxis:{color:'white',linecolor:'white',showgrid:false}});\n}\nbase" + index + "();\
                \nfunction e" + index + "(){\
                Plotly.animate('" + chart_name + "',{layout:{title:{text:'" + chart_name + "',font:{color:'white',size:16}}}"+update_data+"})}\nvar t"+index+"=setInterval(e" + index + ",200);timer_list.push(t"+index+");</script>")

        self.data.append([hist(weight) for weight in weights])
        self.counter += 1
        #print(self.html)

    def add_scalar(self,scalar,chart_name='dufaultline',width=600,height=600,color='#FEAF11',fill=False):
        fill = 'fill:"tozeroy",' if fill else ''
        width = int(width/100)
        height = int(height*0.9)
        self.insert('\n<div class="layui-col-xs{width}"><div id="{id}" style="height:{height}px"></div></div>'.format(id=chart_name,width=width,height=height))
        index = str(self.counter)

        self.add("\n<script>\nvar values=[0];\
                \nfunction get_data(){\
                $.getJSON(web_root+'/get_data',{},function(d){values = d.values;});\
                \n\n\treturn values;\n}\nfunction base"+index+"(){\
                \nvar layout={title:" + chart_name + "}\
                \ntrace = {"+fill+"y:[get_data()[" + index + "]], type: 'line',name:'t1',marker:{color:'"+color+"',width:5}};\
                \nPlotly.plot('" + chart_name + "',[trace],{title:{text:'" + chart_name + "',font:{color:'white',size:16}},paper_bgcolor:'#00011A',plot_bgcolor:'#00011A',xaxis:{color:'white',showgrid:false},yaxis:{color:'white',showgrid:false}}, {scrollZoom: true});\n}\nbase"+index+"();\
                \nfunction e"+index+"(){\
                Plotly.extendTraces('" + chart_name + "',{y:[[get_data()[" + index + "]]]},[0])}\n\
                var t"+index+"=setInterval(e"+index+",400);timer_list.push(t"+index+");</script>")
        self.data.append(scalar)
        self.counter += 1
    def add_scalars(self,scalars,scalar_names,chart_name='dufaultlines',width=600,height=600,colors=['#FEAF11','#85A3E4'],fill=False):
        l = len(scalars)
        colors_l = len(colors)
        data = '['
        update_data = ",{y:["
        fill = 'fill:"tozeroy",' if fill else ''
        width = int(width / 100)
        height = int(height * 0.9)
        index = str(self.counter)
        for i in range(l):
            if i<=colors_l:
                ii = str(i)
                data = data+("{"+fill+"y:[get_data()[" + index + "]["+ii+"]], type: 'line',name:'"+scalar_names[i]+"',marker:{color:'"+colors[i]+"',width:5}},")

            else:
                data.append("{"+fill+"y:[get_data()[" + index + "]["+ii+"]], type: 'line',name:'t1',marker:{width:5}};")
            update_data += "[get_data()[" + index + "]["+ii+"]],"
        update_data = update_data[:-1]
        update_data += ']}'

        data = data[:-1]
        data = data + ']'
        #print(update_data)
        update_list = ','+str([i for i in range(l)])
        self.insert('\n<div class="layui-col-xs{width}"><div id="{id}" style="height:{height}px"></div></div>'.format(id=chart_name,width=width,height=height))

        self.add("\n<script>\nvar values=[0];\
                        \nfunction get_data(){\
                        $.getJSON(web_root+'/get_data',{},function(d){values = d.values;});\
                        \n\n\treturn values;\n}\nfunction base" + index + "(){\
                        \nPlotly.plot('" + chart_name + "',"+data+",{title:{text:'" + chart_name + "',font:{color:'white',size:16}},paper_bgcolor:'#00011A',plot_bgcolor:'#00011A',xaxis:{color:'white',showgrid:false},yaxis:{color:'white',showgrid:false}}, {scrollZoom: true});\n}\nbase" + index + "();\
                        \nfunction e" + index + "(){\
                        Plotly.extendTraces('" + chart_name + "'"+update_data+update_list+")}\n\
                        var t"+index+"=setInterval(e" + index + ",400);timer_list.push(t"+index+");</script>")
        self.counter += 1
        self.data.append(scalars)
        #print(self.html)
    def add_pie(self,labels,values,chart_name='defaultpie',width=600,height=600,text='this is <br>a big pie',colors=['#D62728','#FF69B4','white','#FEAF11','#A53F25'],hole=0.5):
        width = int(width / 100)
        height = int(height * 0.9)
        self.insert('\n<div class="layui-col-xs{width}"><div id="{id}" style="height:{height}px"></div></div>'.format(
            id=chart_name, width=width, height=height))
        index = str(self.counter)
        hole = str(hole)
        colors = str(colors)
        self.add("\n<script>\nvar values=[0];\
                        \nfunction get_data(){\
                        $.getJSON(web_root+'/get_data',{},function(d){values = d.values;});\
                        \n\n\treturn values;\n}\nfunction base" + index + "(){\
                        \nvar layout={title:" + chart_name + "}\
                        \ntrace = {labels:get_data()[" + index + "][0],values:get_data()[" + index + "][1],hole:"+hole+", type: 'pie',marker:{colors:" + colors + "}};\
                        \nPlotly.plot('" + chart_name + "',[trace],{\
                        annotations:[{font:{size:24,color:'white'},text:'"+text+"',x:0.5,y:0.6}]\
                        ,title:{text:'" + chart_name + "',font:{color:'white',size:20}},paper_bgcolor:'#00011A',plot_bgcolor:'#00011A',xaxis:{color:'white',showgrid:false},yaxis:{color:'white',showgrid:false}},{editable:true});\n}\nbase" + index + "();\
                        \nfunction e" + index + "(){\
                        Plotly.animate('"+chart_name+"',{layout:{title:{text:'"+chart_name+"',font:{color:'white',size:16}}},data:[{values:get_data()["+index+"][1],\
        type:'pie',marker:{colors:" + colors + "},name:'t1'}]})}\nvar t"+index+"=setInterval(e"+index+",200);timer_list.push(t"+index+");\
                        </script>")
        self.data.append([labels,values])
        self.counter += 1

    #write html(css,javascript),start train function, and render_template
    def write(self,train):
        with open(self.log,'wb') as f:
            pkl.dump(self.data,f)
        self.web.write(''.join(self.html))
        self.web.close()
        #global p
        Process(target=train).start()
        app.run(debug=True,threaded=True)

    #insert html(css,javascript code in label <body>)
    def insert(self,string):
        if self.row == 0:
            self.html = self.html[0:self.widget_counter+1]+[string]+self.html[self.widget_counter+1:]
        else:
            self.html = self.html[0:self.widget_counter+self.row] + [string] + self.html[self.widget_counter + self.row:]
        self.widget_counter += 1

    def new_row(self):
        self.html[self.widget_counter+self.row] = self.html[self.widget_counter+self.row] + '<div class="layui-row">'
        self.html = self.html[0:self.widget_counter+self.row+1]+['</div>']+self.html[self.widget_counter+self.row+1:]
        self.row += 1

    #add javascript code after label <body>
    def add(self,string):
        tail = self.html.pop()
        self.html.append(string)
        self.html.append(tail)



def f(tensor):
    fl = tensor.flatten().tolist()
    #print(fl.shape)
    return fl



def train():
    from supervise_log import log
    import math
    l = log(6)
    i = 0.05
    while(1):
        time.sleep(0.2)
        l.log_weights([10*torch.rand((200,)),10*torch.rand((200,)),10*torch.rand((200,))])
        l.log_scalar(math.sin(i))
        l.log_weight(5*torch.rand((100,)))
        l.log_scalar(math.exp(i))
        l.log_pie(labels=[1,2,3,4,5],values=[random.random(),random.random(),random.random(),random.random(),random.random()])
        #l.log_weight(5*torch.rand((100,)))
        l.log_scalars([math.sin(i),math.cos(i)])
        l.log_end()
        i = i+0.05







if __name__ == "__main__":
    f = Figure()

    f.new_row()
    f.add_weights([torch.rand((200,)),torch.rand((200,)),torch.rand((200,))],['w1','w2','w3'],'weights')
    f.add_scalar(random.random(),chart_name='Morning',fill=True)

    f.new_row()
    f.add_weight(torch.rand((100,)),'My',width=300,color='#6BDE31')
    f.add_scalar(0,'lovely',width=300,color='#85A3E4')
    f.add_pie([1,2,3,4,5],[1,3,3,2,1],'Princess',width=300,hole=0.8,text='pie chart<br>001')
    f.add_scalars([1,2],['a1','a2'],chart_name='test',width=300,fill=True,colors=['#DD1A78','#E75D2E'])
    f.write(train)
    '''
    f.add_weights([torch.rand((200,)),torch.rand((200,))],['a1','a2'])
'''


