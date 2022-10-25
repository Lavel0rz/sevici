import streamlit as st
import pandas as pd



st.set_page_config(page_title="SeviciMap", page_icon="bike", layout='wide', initial_sidebar_state='auto')
st.sidebar.title('Sevici Visualization app')
st.sidebar.image(r"sevici.jpeg", use_column_width=True)
option = st.sidebar.selectbox('Menu', ['Home','Datos','Visualizacion','Filtrado'])
df = pd.read_csv('sevicidist.csv').drop('Unnamed: 0',axis = 1)
df.rename(columns={"LON": "lon", "LAT": "lat",'CAPACITY':'capacity','Distrito':'distrito'}, inplace=True)
df['capacity']= df['capacity'].astype(int)
df['distrito']= df['distrito'].astype(int)


uploaded_file = st.sidebar.file_uploader("Carga tus propios datos", type=['csv'])
if uploaded_file != None:
    df = pd.read_csv(uploaded_file)
if option == 'Home':
    st.title('Bienvenidos a Sevici Visualization app')
    st.subheader('Obtencion de datos')
    st.markdown('Los datos vendrán extraidos a traves de la API de [OpenStreetMap](https://www.openstreetmap.org/): OverPass')
    st.markdown('Utilizaremos la libreria request utilizando como url la api de Overpass: "https://lz4.overpass-api.de/api/interpreter"')
    st.markdown('La query que utilizaremos sera la siguiente :')
    st.code(""" overpass_query = '''
[out:json];node[amenity=bicycle_rental]
(37.3582,-7,37.4428,-5.8599);out;'''
""")
    st.markdown('Para investigar un poco mas sobre como construir queries para la api Overpass consultar este [enlace](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_API_by_Example)')
    st.markdown('Los datos que nos interasan seran: Longitud, Latitud, Capacidad y el Nombre de la Calle para que podamos construir un dataframe tal que:')
    st.dataframe(df.head())
    st.markdown('Nuestra aplicacion contendra 3 pestañas principales ')
    st.markdown('''<ul>
<li>Datos →→ Dataframe y KPI numero total bicis</li>
<li>Visualizacion  →→ Mapa que contiene todos los puntos Sevici utilizando latitud y longitud</li>
<li>Filtrado →→ Mapa con opciones de filtrado para filtrar por calle, distrito, capacidad</li>
</ul>''',unsafe_allow_html=True)

    st.markdown('Para ello nos apoyaremos en la documentacion de [streamlit](https://docs.streamlit.io/library/api-reference)')
elif option == 'Datos':
    st.metric('Numero total de bicis Sevici en Sevilla', df.capacity.sum(), delta=20, delta_color="normal")
    st.dataframe(df)
    st.balloons()
    st.subheader("Capacidad por distrito")
    chart_data = df[['distrito', 'capacity']].groupby(['distrito']).sum(['capacity']).sort_values(
        by=['distrito'])
    st.bar_chart(chart_data)
elif option == 'Visualizacion':

    st.map(df[['lon', 'lat']],use_container_width=True)
    st.balloons()

elif option == 'Filtrado':
    menu = st.sidebar.radio(
        "Seleccione una opción de filtro",
        ('Calle', 'Capacidad & Distrito'))
    if menu =='Capacidad & Distrito':
        capacidades = st.sidebar.radio('Capacidades',('<20','>=20'))
        distritos = st.sidebar.radio('Distritos',list(df.distrito.unique()))
        if capacidades == '<20':
            df = df[(df['capacity'] < 20) & (df['distrito'] == distritos)]
            st.map(df[['lon', 'lat']], use_container_width=False)
            st.dataframe(df)
        else:
            df = df[(df['capacity'] >= 20) & (df['distrito'] == distritos)]
            st.map(df[['lon', 'lat']], use_container_width=False)
            st.dataframe(df)




    if menu == 'Calle':
        calles = list(df['CALLE'].unique())
        calle = st.sidebar.selectbox('Calles',options = calles)
        df = df[df['CALLE'] == calle]
        st.dataframe(df)
        st.map(df[['lon', 'lat']],use_container_width=False)
