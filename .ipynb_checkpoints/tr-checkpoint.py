import folium
import pandas as pd
import os
# Create your views here.

districts= os.path.join('E:\Final project\covid19impactmap','bd-divisions.json')
covid_data=os.path.join('E:\Final project\covid19impactmap','data.csv')
main_data=pd.read_csv(covid_data)

m=folium.Map(location=[25, 88], zoom_start=4)

m.choropleth(
    
    geo_data =districts,
    name='choropleth',
    data=main_data,
    columms=['Name','test_positivity1'],
    key_on='Name',
    fill_color='YlGn',
    legend_name='covid-19 impact'
    )


folium.LayerControl().add_to(m)

m.save('map2.html')