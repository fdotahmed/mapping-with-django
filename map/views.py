from django.shortcuts import render
import folium
import pandas as pd
import os
from urllib.request import urlopen
import json
import csv
import math
import requests
# Create your views here.



#view for every district separately
def district(request, dist_name):


    loc = 'COVID-19 IMPACT MAP'
    title_html = '''
             <h3 align="center"  style="color:red;" style="font-size:50px"><b>{}</b></h3>
             '''.format(dist_name.upper())




    file=dist_name+".json"
    districts = os.path.join('data', file)
    covid_data = os.path.join('data', 'data.csv')
    graph_data =os.path.join('data','graph.json')
    spread_data = pd.read_csv(covid_data)

    
    
    

    
    dists_name = list( spread_data['Name'])
    rate = list( spread_data['test_positivity1'])
    lat= list( spread_data['Latitude (generated)'])
    long= list ( spread_data['Longitude (generated)'])
    url="http://127.0.0.1:8000/"

    for a,b,c,d in zip(dists_name,rate,lat,long):
        if(str(a).lower() in dist_name):
            m = folium.Map(location=[c, d], tiles="cartodbpositron" , zoom_start=10)
            
            folium.Marker(location=[c, d],popup=folium.Popup(max_width=1500).add_child(folium.Vega(json.load(open(graph_data))))).add_to(m)
            

     
     
    m.choropleth(
        geo_data=districts,
        name='choropleth',
        data=spread_data,
        columns=['Name', 'test_positivity1'],
        key_on='properties.ADM2_EN',
        fill_color= 'YlGn',
        fill_opacity=1,
        line_opacity=0.2,
        legend_name='covid-19 impact map'
    )
     
    folium.LayerControl().add_to(m)
    
    m.get_root().html.add_child(folium.Element(title_html))
    m = m._repr_html_()
    context = {
        'm': m,
        
        }
    
    return render (request,'district.html',context)

#primary view for the whole map of the country
def index(request):

    #using get request to fetch data
    result= requests.get('https://public.tableau.com/vizql/w/COVIDtestpositivityratedistrictmonth_travelers_nontravelers3_16275499908960/v/Dashboard/vudcsv/sessions/8F80B2F077394AA7946CDF4FB923ADFE-0:0/views/503254654352274410_1599158888822703424?summary=true')
    url_content = result.content
    csv_file = open('file.csv', 'wb')

    csv_file.write(url_content)
    csv_file.close()

    #importing the values in pandas
    districts = os.path.join('data', 'bd-districts.json')
    covid_data = os.path.join('data', 'data.csv')
    spread_data = pd.read_csv(covid_data)

    m = folium.Map(location=[23.75, 90.5], tiles="cartodbpositron" , zoom_start=7.8)

    #importing the values in lists
    dist_name = list( spread_data['Name'])
    rate = list( spread_data['test_positivity1'])
    lat= list( spread_data['Latitude (generated)'])
    long= list ( spread_data['Longitude (generated)'])
    url="http://127.0.0.1:8000/"



    #main choropleth map and its value distribution
    m.choropleth(
        geo_data=districts,
        name='choropleth',
        data=spread_data,
        columns=['Name', 'test_positivity1'],
        key_on='properties.ADM2_EN',
        fill_color='OrRd',
        fill_opacity=1,
        line_opacity=0.2,
        legend_name='covid-19 impact map'
    )
      
    
    #folium markers 
    for a,b,c,d in zip(dist_name,rate,lat,long):
        link=url+str(a).lower()
        if(0<b<7):
            folium.Marker(location=[c,d],popup="<b>DISTRICT Name: </b><a href="+link+" target= '_blank'>"+a+"</a>""<br><b>Infection rate : "+str(b)+"</b>"+"%",icon=folium.Icon(color="lightblue")).add_to(m)
        if(7<b<11):
            folium.Marker(location=[c,d],popup="<b>District Name: </b><a href="+link+" target= '_blank'>"+a+"</a>""<br><b>Infection rate : "+str(b)+"</b>"+"%",icon=folium.Icon(color="green")).add_to(m)
        if(11<b<15):
            folium.Marker(location=[c,d],popup="<b>District Name: </b><a href="+link+" target= '_blank'>"+a+"</a>""<br><b>Infection rate : "+str(b)+"</b>"+"%",icon=folium.Icon(color="lightblue")).add_to(m)
        if(15<b<28):
            
            folium.Marker(location=[c,d],popup="<b>District Name: </b><a href="+link+" target= '_blank'>"+a+"</a>""<br><b>Infection rate : "+str(b)+"</b>"+"%",icon=folium.Icon(color="red",icon="ambulance",prefix='fa')).add_to(m)

    # algorithm for risky districts with folium circles
    for a,b,c,d in zip(dist_name,rate,lat,long):
       
        if(15<b):
            min=34343434
            neighbor="new"
            
            for x,y,z,w in zip(dist_name,rate,lat,long):
                if(c==z and d==w):
                    pass
           
                if(c>z and d<w):
                    if(math.sqrt( ( (c-z)**2)+((d-w)**2))<min):
                        min=math.sqrt( ( (c-z)**2)+((d-w)**2))
                        neighbor= x
            
            for a1,b1,c1,d1 in zip(dist_name,rate,lat,long):
                if(a1 in neighbor):
                    if(b1<15):
                        folium.CircleMarker(location=(c1,d1),popup='High Risk of Infection',radius=45, fill_color='red').add_to(m)


            min=34343434
            neighbor="new"
            
            for x,y,z,w in zip(dist_name,rate,lat,long):
                if(c==z and d==w):
                    pass
           
                if(c<z and d>w):
                    if(math.sqrt( ( (c-z)**2)+((d-w)**2))<min):
                        min=math.sqrt( ( (c-z)**2)+((d-w)**2))
                        neighbor= x
            
            for a1,b1,c1,d1 in zip(dist_name,rate,lat,long):
                if(a1 in neighbor):
                    if(b1<15):
                        folium.CircleMarker(location=(c1,d1),popup='High Risk of Infection',radius=45, fill_color='red').add_to(m)


            min=34343434
            neighbor="new"
            
            for x,y,z,w in zip(dist_name,rate,lat,long):
                if(c==z and d==w):
                    pass
           
                if(c<z and d<w):
                    if(math.sqrt( ( (c-z)**2)+((d-w)**2))<min):
                        min=math.sqrt( ( (c-z)**2)+((d-w)**2))
                        neighbor= x
            
            for a1,b1,c1,d1 in zip(dist_name,rate,lat,long):
                if(a1 in neighbor):
                    if(b1<15):

                        folium.CircleMarker(location=(c1,d1),popup='High Risk of Infection',radius=45, fill_color='red').add_to(m)
                         

            min=34343434
            neighbor="new"
            
            for x,y,z,w in zip(dist_name,rate,lat,long):
                if(c==z and d==w):
                    pass
           
                if(c>z and d>w):
                    if(math.sqrt( ( (c-z)**2)+((d-w)**2))<min):
                        min=math.sqrt( ( (c-z)**2)+((d-w)**2))
                        neighbor= x
            
            for a1,b1,c1,d1 in zip(dist_name,rate,lat,long):
                if(a1 in neighbor):
                    if(b1<15):

                        folium.CircleMarker(location=(c1,d1),popup='High Risk of Infection',radius=45, fill_color='red').add_to(m)


       

 

           
    

    #folium.GeoJson(districts,name='bangladesh').add_to(m)
    folium.LayerControl().add_to(m)

    loc = 'COVID-19 IMPACT MAP'
    title_html = '''
             <h3 align="center"  style="color:red;" style="font-size:30px"><b>{}</b></h3>
             '''.format(loc)



    m.get_root().html.add_child(folium.Element(title_html))
    
    m = m._repr_html_()
    context = {
        'm': m,
        
        }
    
    return render (request,'index.html',context)




