from tkinter import font
from tracemalloc import start
import mysql.connector
from mysql.connector import Error
import dash as Dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from datetime import date
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc 
import plotly.io as pio
import numpy as np



# Connect to the database
try:
    connection = mysql.connector.connect(host='db-weight-estimation.cc02jmpcbera.us-east-1.rds.amazonaws.com',
                                         database='weight_estimation',
                                         user='admin',
                                         password='weight-estimation-master-password')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)



db_cursor = connection.cursor()
db_cursor.execute('SELECT * FROM weight')# query database
table_rows = db_cursor.fetchall()

app = Dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG]) 

################################################################################################
#Import Current Data into a Dataframe 



df = pd.DataFrame(table_rows)
df[1] = pd.to_datetime(df[1])
df[0] = df[0].astype(int)
df[2] = df[2].astype(float)
df[3] = df[3].astype(int)
df[4]= df[4].astype(int)


print(df)


################################################################################################
# Create intial Figures 



################################################################################################
# App Layout 

app.layout = html.Div([

                    # This is the header
                    html.H1("Kentland Farm Cattle Weights", style = {'text-align': 'center'}),
                    html.Br(),

                    # Bootstrap row that contains date picker as well as title names for card kpi display
                    dbc.Row(dbc.Col(html.Div(id ='output-container', style={'fontSize':24}), width =4), ),
                    dbc.Row(
                        [dbc.Col(dcc.DatePickerRange(
                            id='start_date',
                            min_date_allowed=df[1].iat[0],
                            max_date_allowed=df[1].iat[len(df)-1],
                            initial_visible_month=date(2022, 4, 19),
                            start_date= date(2022,4,19),
                            end_date=date(2022, 4, 19), 
                            style={'color':'#1a1a1a','background_color': '#1a1a1a','text-align':'center'}
                        ), 
                        
                        
                        width = 2),# These are the title names for the cards and the kpi value
                        dbc.Col([html.Div("Number of Cows",style ={'fontSize':36,'text-align':'center', 'backgroundColor': '#1a1a1a'}),
                        (html.H3(id='number_of_cows',style ={'fontSize':40,'text-align':'center','backgroundColor': '#1a1a1a'}))]), 
                        dbc.Col([html.Div("Average Cow Weight (kg)",style ={'fontSize':36,'text-align':'center','backgroundColor': '#1a1a1a'}),
                        html.H3(id='average_weight',style ={'fontSize':40,'text-align':'center','backgroundColor': '#1a1a1a'})]), 
                        dbc.Col([html.Div("Number of Sessions",style ={'fontSize':36,'text-align':'center','backgroundColor': '#1a1a1a'}),
                        html.H3(id='number_of_sessions',style ={'fontSize':40,'text-align':'center','backgroundColor': '#1a1a1a'}),
                        ])]

                        ),
                    

                    html.Div(id='output-container-date-picker-range'),


                    

                    html.Br(),
                    html.Br(),
            #dsiplay for all the charts
                    dbc.Row([
                            dbc.Col(dcc.Graph(id = 'pie_chart', figure= {}),width={'size':2,'offset':.5}),
                            dbc.Col(dcc.Graph(id = 'weight_hist', figure ={}),width ={'size':5,'offset':1}),
                            dbc.Col(dcc.Graph(id = 'table_data',figure = {}),width = 4)])


                                ])

################################################################################################
# Call Backs

@app.callback(
    [Output(component_id='output-container',component_property='children'), #This is to print a statemtent about the current selected dates in the date picker
     Output(component_id = 'weight_hist', component_property='figure'), # Histogram output
     Output(component_id = 'pie_chart', component_property='figure'), # Pie Chart
     Output(component_id = 'table_data', component_property='figure'), # Table Print
     Output(component_id = 'number_of_cows', component_property='children'),# Card for number of cows
     Output(component_id = 'average_weight', component_property='children'), # 
     Output(component_id = 'number_of_sessions', component_property='children')
    ],


    [Input(component_id = "start_date", component_property='start_date'), # input for date Picker
     Input(component_id = "start_date", component_property='end_date')] # input for date Picker

    )

def update_graph(start_date, end_date): 

   
    container= 'The Selected Date Ranges are: {} through {}'.format(start_date, end_date) # Text to display date picker choices
    
    dff = df.copy() 
    dff =  df[(df[1] >= start_date) & (df[1] <= end_date)]# filter dates

    print(dff)
    number_of_cows = len(dff.index) # card disply value
    dff[2] = dff[2].fillna(0)

    


    avg_weight = round(dff[2].mean())# Card displayvalue

    
    dff[3].replace(to_replace=[0, 1], value=['Jersey','Holstein'], inplace=True)

    percent_holstein =df[df[3]=='Holstein'].count()/number_of_cows

    session_groupby = dff.groupby([1]).count().reset_index()
    sessions = len(session_groupby.index) 

    weight_dist = df[2]

    pie_groupby = dff.groupby(3).count().reset_index()
    print(pie_groupby)
    # Hist Figure
    hist = px.histogram(

        data_frame= dff,
        x = 2, 
        nbins=13, 
        labels = dict(x = "Cow Weights (kg)", count = 'Weigh Range Frequency'), 
        template='plotly_dark' , 
        color_discrete_sequence= ['red'],
        title="Weight Ditribution", 

    

    )
    hist.update_xaxes(title_text='Cow Weight (kg)')
    hist.update_yaxes(title_text='Weight Frequency')
    hist.update_layout(
    margin=dict(l=50, r=50, t=50, b=50),
)


# Pie Figure
    pie_chart = px.pie(

        data_frame=pie_groupby, 
        names = 3,
        values = 0,
        hole=.4, 
        width  = 300, 
        height = 300,
        template='plotly_dark', 
        color=3, 
        color_discrete_map={'jersey':'orange','holstein':'yellow'}, 
        title="Breed Distribution"




    )       

    pie_chart.update_layout(
    margin=dict(l=50, r=50, t=50, b=50),
)
# Table figure

    table_data = go.Figure(data=[go.Table(
        header=dict(values=['Cow Id', 'Weight', 'Date','Breed'],
                    fill_color='black',
                    line_color='orange',
                    align='right'),
        cells=dict(values=[dff[0], dff[2], dff[1] ,dff[3]],
                   fill_color='black',
                   line_color = 'orange',
                   align='left'), )
    ])

    table_data.update_layout(autosize=True, template = 'plotly_dark')

    table_data.update_layout(
    margin=dict(l=40, r=20, t=20, b=20),
)




    return container, hist, pie_chart, table_data, number_of_cows, avg_weight, sessions

app.run_server(debug = True) # This statement runs the app











    













