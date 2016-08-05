from os.path import dirname, join

#import numpy as np
import pandas.io.sql as psql
import sqlite3 as sql
import pandas as pd
from pandas import DataFrame 
import numpy as np

from bokeh.client import push_session
from bokeh.plotting import figure,output_file,show
from bokeh.charts import Bar,Area,Line
from bokeh.models import ColumnDataSource, HoverTool, HBox, VBoxForm,CustomJS,VBox
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc,vform
#whole_data read
data_all=pd.read_table('results/newresults',sep=' \t',names=['name','company','industry','location'])
#three 
data1=data_all[data_all.location.str.contains('Beijing')==True]
data1_industry_counts=data1['industry'].value_counts()
data1_industry_counts.to_csv('here.csv')
data2=pd.read_csv('here.csv',names=['industry','numbers'])

x=data2['industry'].values
np.savetxt('here1.csv',x,fmt='%s')
#m=pd.read_csv('here1.csv')

b=np.loadtxt('here1.csv',str,delimiter='\n')
print b 


local_counts=data_all['location'].value_counts()
industry_counts=data_all['industry'].value_counts()
company_counts=data_all['company'].value_counts()

local_counts.to_csv('out3.csv',sep=',')
industry_counts.to_csv('out4.csv',sep=',')
company_counts.to_csv('out5.csv',sep=',')
industry_counts1=pd.read_csv('out4.csv',names=['industry','numbers'],sep=',')
local_counts1=pd.read_csv('out3.csv',names=['location','numbers'],sep=',')
company_counts1=pd.read_csv('out5.csv',names=['company','numbers'],sep=',')
test=industry_counts1['industry']
a=test.values
test.to_csv('outout.csv',sep=',')
test1=pd.read_csv('outout.csv')
