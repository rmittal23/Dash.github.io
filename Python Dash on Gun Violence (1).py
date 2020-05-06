
# coding: utf-8

# In[1]:


import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sorted_months_weekdays import *
from sort_dataframeby_monthorweek import *


# In[2]:


df_mass = pd.read_csv(r'https://raw.githubusercontent.com/rmittal23/Data/master/mass%20shooing.csv')
df_mass['Incident Date'] = pd.to_datetime(df_mass['Incident Date'])
external_stylesheets = ['https://rmittal23.github.io/dash.github.io/learn.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# In[3]:


df_2019 = df_mass[df_mass['Year']==2019]
df19=df_2019.groupby('Month')[['Killed']].sum().reset_index()

# 2019 Dataframe sorted by month involving killed people
df19=Sort_Dataframeby_MonthandNumeric_cols(df = df19, monthcolumn='Month',numericcolumn='Killed')

df191=df_2019.groupby('Month')[['Injured']].sum().reset_index()

# 2019 Dataframe sorted by month involving injured people
df191=Sort_Dataframeby_MonthandNumeric_cols(df = df191, monthcolumn='Month',numericcolumn='Injured')

df_2020 = df_mass[df_mass['Year']==2020]
df20=df_2020.groupby('Month')[['Killed']].sum().reset_index()

# 2020 Dataframe sorted by month involving killed people
df20=Sort_Dataframeby_MonthandNumeric_cols(df = df20, monthcolumn='Month',numericcolumn='Killed')

df201=df_2020.groupby('Month')[['Injured']].sum().reset_index()

# 2020 Dataframe sorted by month involving injured people
df201=Sort_Dataframeby_MonthandNumeric_cols(df = df201, monthcolumn='Month',numericcolumn='Injured')


# In[4]:


import folium
map_usa = folium.Map(location=[37.0902, -95.7129],zoom_start=4)
for lat, lng, city, state, killed, injured, month in zip(df_2019['Latitude'], df_2019['Longitude'], df_2019['City Or County'],df_2019['State'], df_2019['Killed'], df_2019['Injured'], df_2019['Month']):
    label = 'City: {}, State:{}, Killed: {}, Injured: {}, Month:{}'.format(city,state,killed,injured, month)
    folium.CircleMarker(
        [lat, lng],
        radius=injured,
        popup=label,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.1,
        parse_html=False).add_to(map_usa)


# In[5]:


app.layout = html.Div(children=[html.H1(children='Python Dash',style={'textAlign':'center'}),
                                html.H1(children='Gun Violence cases in USA',style={'textAlign':'center'}),
                                dash_table.DataTable(columns=[{'name':i,'id':i} for i in df_mass.columns], data=df_mass.head().to_dict('records'),),
                               dcc.Graph(figure={'data':[
                                   {'x':df191.Month,'y':df191.Injured, 'type':'bar','name':'Injured'},
                                   {'x':df19.Month,'y':df19.Killed, 'type':'bar','name':'Killed'},],
                                                'layout': {'title': '2019 Violence'}}),
                               dcc.Graph(figure={'data':[
                                   {'x':df201.Month,'y':df201.Injured, 'type':'bar','name':'Injured'},
                                   {'x':df20.Month,'y':df20.Killed, 'type':'bar','name':'Killed'},],
                                                'layout': {'title': '2020 Violence'}}),
                               html.Div([html.H3(children='2019 Gun Violence',style={'textAlign':'center'}),html.Iframe(srcDoc=open('t.html','r').read(),width='100%',height='600')]),
                               html.Div([html.H3(children='2020 Gun Violence',style={'textAlign':'center'}), html.Iframe(srcDoc=open('t2.html','r').read(),width='100%',height='600')])])
                               
                                 


# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=False)

