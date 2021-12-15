import datetime
import folium
import geopandas as gpd
import geopy
import networkx as nx
import joblib

import osmnx as ox
import shapely.wkt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time

from folium.features import DivIcon
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config(
    page_title="Japan Earthquake Safe Path",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.markdown('<h1 style="margin-left:8%; color:#1a5276">Japan Earthquake Safe Path </h1>', unsafe_allow_html=True)

add_selectbox = st.sidebar.radio(
    "",
    ("About", "Find Path", "Maps", "Collaborators")
)

if add_selectbox == 'About':
    st.subheader('ABOUT THE PROJECT')

    st.markdown('<h4>The Background</h4>', unsafe_allow_html=True)
    st.markdown('Natural Disasters are problems in Japan, with risk of earthquakes, floods and tsunamis. Japan has well-developed \
        disaster response systems, but densely populated cities and narrow roads make managing the response difficult. By giving \
            individuals information about the safest ways from their homes and places of work, it will increase their awareness of \
                the surrounding area and improve their preparedness.', unsafe_allow_html=True)
    st.markdown('<h4>The Problem</h4>', unsafe_allow_html=True)
    st.markdown('Design a model collecting data about the local roads from satellite images, classify them and indicate the safest \
        route to be taken from point A to point B. Design an interactive dashboard to display the safest route in a map.', 
        unsafe_allow_html=True)
    st.markdown('By making individuals aware, it will improve their preparedness and it can be used within families to prepare disaster \
        response plans, depending on their circumstances. To be used by individuals, families and groups, and foreign residents who may \
            not understand local information. Further development will be covering more geographical areas and publicising on a local level.'
            , unsafe_allow_html=True)

elif add_selectbox == 'Find Path':
    st.subheader('Find Safest Path')

    sentence = st.text_input('Input your current location:') 

    # G_walk = ox.graph_from_place('Manhattan Island, New York City, New York, USA',
    #                          network_type='walk')

    G_walk = joblib.load('G_walk.sav')

    orig_node = ox.get_nearest_node(G_walk,
                                    (40.748441, -73.985664))

    dest_node = ox.get_nearest_node(G_walk,
                                    (40.748441, -73.4))

    route = nx.shortest_path(G_walk,
                            orig_node,
                            dest_node,
                            weight='length')

    route_map = ox.plot_route_folium(G_walk, route)

    folium_static(route_map, width=900)

elif add_selectbox == 'Maps':
    st.subheader('Maps')

    col1, col2 = st.columns(2)

    map_type = col1.selectbox(
        "",
        ("Shelters",  "Schools", "Parks")
    )

    city_type = col2.selectbox(
        "City",
        ( '横手市 (Yokote City)', '湯沢市 (Yuzawa City)', '大仙市 (Daisen City)', '仙北市 (Semboku City)',
        '北秋田市 (Kitaakita City)', '鹿角市 (Kazuno City)', '大館市 (Odate City)',  'にかほ市 (Nikaho City)',
         '由利本荘市 (Yurihonjo City)',  '潟上市 (Katagami City)', '能代市 (Noshiro City)', '男鹿市 (Oga City)', 
         '十和田市 (Towada City)', '三沢市 (Misawa City)', '青森市 (Aomori City)',  '八戸市 (Hachinohe City)',
         '弘前市 (Hirosaki City)', '五所川原市 (Goshogawara City)', 
         'つがる市 (Tsugaru City)',  '千葉市 (Chiba City)',  '松山市 (Matsuyama City)', '大洲市 (Ozu City)', '西予市 (Seiyo City)', '宇和島市 (Uwajima City)', 
          '今治市 (Imabari)', '西条市 (Saijo City)', '四国中央市 (Shikokuchuo City)', '新居浜市 (Niihama City)', 
           '小浜市 (Obama City)', '坂井市 (Sakai City)', '越前市 (Echizen City)', '鯖江市 (Sabae City)', '福井市 (Fukui City)',
            '敦賀市 (Tsuruga City)', '勝山市 (Katsuyama City)', '大野市 (Ono City)', '柳川市 (Yanagawa City)', '久留米市 (Kurume City)', 
             '筑後市 (Chikugo City)', 'みやま市 (Miyama City)', '八女市 (Yame city)', '大牟田市 (Omuta City)', '太宰府市 (Dazaifu City)', 
             '大野城市 (Onojo City)', '福岡市 (Fukuoka City)', '古賀市 (Koga City)', '飯塚市 (Iizuka City)', '嘉麻市 (Kama City)', 
             '直方市 (Nogata City)', '北九州市 (Kitakyushu City)', '福津市 (Fukutsu City)', '宗像市 (Munakata City)',
             '羽島市 (Hashima City)', '瑞穂市 (Mizuho City)', '海津市 (Kaizu City)', '岐阜市 (Gifu City)', '大垣市 (Ogaki City)', 
             '本巣市 (Motosu City)', '郡上市 (Gujo City)', '高山市 (Takayama City)', '多治見市 (Tajimi City)', '可児市 (Kani City)', 
             '各務原市 (Kakamigahara City)', '松本市 (Matsumoto)', '中津川市 (Nakatsugawa City)', '恵那市 (Ena City)', 
             '安中市 (Annaka City)', '伊勢崎市 (Isesaki City)', '渋川市 (Shibukawa)', '桐生市 (Kiryu City)', '前橋市 (Maebashi City)',
              '高崎市 (Takasaki City)', '富岡市 (Tomioka City)', '藤岡市 (Fujioka City)', 'みどり市 (Midori City)', '館林市 (Tatebayashi City)', '太田市 (Ota City)', '広島市 (Hiroshima city)', '函館市 (Hakodate City)', '札幌市 (Sapporo)', '伊達市 (Date city)', '登別市 (Noboribetsu City)', '室蘭市 (Muroran City)', '砂川市 (Sunagawa City)', '滝川市 (Takikawa City)', '三笠市 (Mikasa City)', '北広島市 (Kitahiroshima City)', '江別市 (Ebetsu City)', '岩見沢市 (Iwamizawa City)', '苫小牧市 (Tomakomai City)', '千歳市 (Chitose City)', '士別市 (Shibetsu City)'
        )
    )

    if st.button('Search'):

        if map_type == 'Shelters':
            map_data = pd.read_csv('japan_shelters.csv')
        elif map_type == 'Schools':
            map_data = pd.read_csv('japan_schools.csv')

        city = city_type.split(" ")

        details = map_data[map_data['city']==city[0]]

        coordinates = {
            '横手市 (Yokote City)': [39.3138, 140.5666],
            '湯沢市 (Yuzawa City)': [39.1644, 140.4957],
            '大仙市 (Daisen City)': [39.4533, 140.4755],
            '仙北市 (Semboku City)': [39.7001, 140.7307],
            '北秋田市 (Kitaakita City)': [39.7001, 140.7307],
            '鹿角市 (Kazuno City)': [40.2260, 140.3708],
            '大館市 (Odate City)': [40.2714, 140.5641],
            'にかほ市 (Nikaho City)': [39.2030, 139.9077],
            '由利本荘市 (Yurihonjo City)': [39.3858, 140.0489],
            '秋田市 (Akita City)': [39.7200, 140.1035],
            '潟上市 (Katagami City)': [39.8573, 140.0130],
            '能代市 (Noshiro City)': [40.2119, 140.0271],
            '男鹿市 (Oga City)': [39.8869, 139.8476], 
            '十和田市 (Towada City)': [40.6126, 141.2069], 
            '三沢市 (Misawa City)': [40.6832, 141.3690], 
            '青森市 (Aomori City)': [40.8222, 140.7474], 
            '八戸市 (Hachinohe City)': [40.5122, 141.4883],
            '弘前市 (Hirosaki City)': [40.6031, 140.4641],
            '五所川原市 (Goshogawara City)': [40.8077, 140.4461],
            'つがる市 (Tsugaru City)': [40.8082, 140.3805],
            '千葉市 (Chiba City)': [35.6074, 140.1065],
            '松山市 (Matsuyama City)': [33.8394, 132.7653],
            '大洲市 (Ozu City)': [33.5062, 132.5446],
            '西予市 (Seiyo City)': [33.3626, 132.5110],
            '宇和島市 (Uwajima City)': [33.2236, 132.5604], 
            '今治市 (Imabari)': [34.0662, 132.9978], 
            '西条市 (Saijo City)': [33.9194466, 133.1813268],
            '四国中央市 (Shikokuchuo City)': [33.980744, 133.5499338],
            '新居浜市 (Niihama City)': [33.9603497, 133.2835899],
            '小浜市 (Obama City)': [35.4938281, 135.7446614],
            '坂井市 (Sakai City)': [36.1677146, 136.2262832],
            '越前市 (Echizen City)': [35.9034571, 136.1689317],
            '鯖江市 (Sabae City)': [35.9565096, 136.1843593],
            '福井市 (Fukui City)': [36.061751, 136.2260542],
            '敦賀市 (Tsuruga City)': [35.6445135, 136.0734634],
            '勝山市 (Katsuyama City)': [36.060766, 136.5007964],
            '大野市 (Ono City)': [35.9797101, 136.4874356],
            '柳川市 (Yanagawa City)': [33.1630969, 130.4058091],
            '久留米市 (Kurume City)': [33.3196648, 130.5081592],
            '筑後市 (Chikugo City)': [33.2123783, 130.5017727],
            'みやま市 (Miyama City)': [33.1523675, 130.4746267],
            '八女市 (Yame city)': [33.2116721, 130.5579706],
            '大牟田市 (Omuta City)': [33.047013, 130.464155],
            '太宰府市 (Dazaifu City)': [33.5128647, 130.5238111],
            '大野城市 (Onojo City)': [33.547399, 130.488786],
            '福岡市 (Fukuoka City)': [33.5898988, 130.4017509],
            '古賀市 (Koga City)': [33.728578, 130.4701731],
            '飯塚市 (Iizuka City)': [33.646594, 130.6911579],
            '嘉麻市 (Kama City)': [33.5632103, 130.7118029],
            '直方市 (Nogata City)': [33.743936, 130.7297462],
            '北九州市 (Kitakyushu City)': [33.8829996, 130.8749015],
            '福津市 (Fukutsu City)': [33.7668264, 130.4913329],
            '宗像市 (Munakata City)': [33.8055642, 130.5406875],
            '羽島市 (Hashima City)': [35.3199495, 136.7034315],
            '瑞穂市 (Mizuho City)': [35.3919614, 136.6911268],
            '海津市 (Kaizu City)': [35.2205087, 136.637211],
            '岐阜市 (Gifu City)': [35.4230949, 136.7627526],
            '大垣市 (Ogaki City)': [35.3671141, 136.6179746],
            '本巣市 (Motosu City)': [35.4830261, 136.6780554],
            '郡上市 (Gujo City)': [35.748417, 136.9643095],
            '高山市 (Takayama City)': [36.1396246, 137.2510322],
            '多治見市 (Tajimi City)': [35.3357572, 137.127762],
            '可児市 (Kani City)': [35.4261093, 137.0613166],
            '各務原市 (Kakamigahara City)': [35.3995831, 136.8485648],
            '松本市 (Matsumoto)': [36.2382047, 137.9687141],
            '中津川市 (Nakatsugawa City)': [35.4876463, 137.5005402],
            '恵那市 (Ena City)': [35.4498094, 137.4128269],
            '安中市 (Annaka City)': [36.3263653, 138.8878314],
            '伊勢崎市 (Isesaki City)': [36.3111734, 139.1968083],
            '渋川市 (Shibukawa)': [36.4894606, 139.0001287],
            '桐生市 (Kiryu City)': [36.4055296, 139.3310209],
            '前橋市 (Maebashi City)': [36.3893418, 139.0632826],
            '高崎市 (Takasaki City)': [36.3220984, 139.0032758],
            '富岡市 (Tomioka City)': [33.5898988, 130.4017509],
            '藤岡市 (Fujioka City)': [36.258633, 139.0745021],
            'みどり市 (Midori City)': [36.3949015, 139.2822984],
            '館林市 (Tatebayashi City)': [36.2454338, 139.5421576],
            '太田市 (Ota City)': [36.2911561, 139.3754233],
            '広島市 (Hiroshima city)': [34.3916058, 132.4518156],
            '函館市 (Hakodate City)': [41.768793, 140.729008],
            '札幌市 (Sapporo)': [43.061936, 141.3542924],
            '伊達市 (Date city)': [42.4717601, 140.8646839],
            '登別市 (Noboribetsu City)': [42.4127547, 141.1064964],
            '室蘭市 (Muroran City)': [42.3152461, 140.9740731],
            '砂川市 (Sunagawa City)': [43.494928, 141.9034816],
            '滝川市 (Takikawa City)': [43.5577956, 141.9103697],
            '三笠市 (Mikasa City)': [43.2457557, 141.8746092],
            '北広島市 (Kitahiroshima City)': [42.9853877, 141.5629536],
            '江別市 (Ebetsu City)': [43.1037358, 141.535894],
            '岩見沢市 (Iwamizawa City)': [43.1959915, 141.7761132],
            '苫小牧市 (Tomakomai City)': [42.6340602, 141.6055453],
            '千歳市 (Chitose City)': [42.8209335, 141.6509612],
            '士別市 (Shibetsu City)': [44.1785114, 142.4001645]


            # '旭川市': ['43.770625', '142.3649743'],
            # '深川市': ['43.7234297', '142.0540685'],
            # '夕張市': ['43.0563455', '141.9739081'],
            # '富良野市': ['43.3419744', '142.383188'],
            # '北見市': ['43.8029391', '143.8946351'],
            # '釧路市': ['42.9849503', '144.3820491'],
            # '根室市': ['43.3301154', '145.5829068'],
            # '神栖市': ['35.8898999', '140.6645754'],
            # '鹿嶋市': ['35.9661164', '140.6450292'],
            # 'ひたちなか市': ['36.3961235', '140.5353397'],
            # '日立市': ['36.5991225', '140.6504604'],
            # '牛久市': ['35.9794247', '140.1494034'],
            # 'つくば市': ['36.0833877', '140.0765098'],
            # '土浦市': ['36.0786297', '140.2045934'],
            # '香取市': ['35.8978273', '140.4992787'],
            # '龍ケ崎市': ['35.9113158', '140.181878'],
            # '水戸市': ['36.3657792', '140.4713933'],
            # '笠間市': ['36.3452244', '140.3042261'],
            # '石岡市': ['36.1905988', '140.2874309'],
            # '高萩市': ['36.7193917', '140.716351'],
            # '常陸大宮市': ['36.5429197', '140.4116172'],
            # '古河市': ['36.178025', '139.7553638'],
            # '筑西市': ['36.3051944', '139.9790903'],
            # '鹿児島市': ['31.5841689', '130.543387'],
            # '垂水市': ['31.4926939', '130.7012264'],
            # '高知市': ['33.5680384', '133.5394221'],
            # '熊本市': ['32.7833323', '130.7333361'],
            # '合志市': ['32.8859288', '130.7899793'],
            # '宇城市': ['32.647181', '130.6839693'],
            # '八代市': ['32.5081425', '130.6020211'],
            # '宇土市': ['32.6879177', '130.6598222'],
            # '阿蘇市': ['32.9524903', '131.1214674'],
            # '京都市': ['35.021041', '135.7556075'],
            # '熊野市': ['33.8885409', '136.100411'],
            # '名張市': ['34.6279243', '136.1086582'],
            # '伊賀市': ['34.7497761', '136.1423355'],
            # '津市': ['34.7341973', '136.5153283'],
            # '鈴鹿市': ['34.8817102', '136.5836516'],
            # '松阪市': ['34.5868422', '136.5412491'],
            # '伊勢市': ['34.4996115', '136.7271774'],
            # '志摩市': ['34.3411841', '136.8196451'],
            # '鳥羽市': ['34.4714464', '136.8293576'],
            # '宮崎市': ['31.9076334', '131.4204022'],
            # '飯田市': ['35.5147101', '137.8219519'],
            # '安曇野市': ['36.3044083', '137.9054972'],
            # '長野市': ['36.6485851', '138.1947664'],
            # '大町市': ['36.5029093', '137.8508885'],
            # '千曲市': ['36.5336984', '138.120123'],
            # '上田市': ['36.4021192', '138.2490506'],
            # '茅野市': ['35.98562', '138.157854'],
            # '塩尻市': ['36.124957', '137.952801'],
            # '伊那市': ['35.830452', '137.954916'],
            # '中野市': ['36.7599193', '138.3534521'],
            # '東御市': ['36.3594225', '138.3305353'],
            # '須坂市': ['36.6510923', '138.3071289'],
            # '佐久市': ['36.2488014', '138.4767695'],
            # '対馬市': ['34.2053717', '129.2946547'],
            # '佐世保市': ['33.1799965', '129.7152872'],
            # '平戸市': ['33.3680705', '129.5539153'],
            # '長崎市': ['32.7501611', '129.8781002'],
            # '諫早市': ['32.843426', '130.0530537'],
            # '雲仙市': ['32.83515', '130.18772'],
            # '南島原市': ['32.6597338', '130.2976992'],
            # '奈良市': ['34.6845445', '135.8048359'],
            # '十日町市': ['37.1276085', '138.755504'],
            # '柏崎市': ['37.3719095', '138.5591406'],
            # '長岡市': ['37.446996', '138.8512199'],
            # '新潟市': ['37.9160769', '139.0365006'],
            # '燕市': ['37.6730751', '138.8825389'],
            # '三条市': ['37.6361174', '138.9613971'],
            # '阿賀野市': ['37.8343618', '139.2258539'],
            # '五泉市': ['37.7444474', '139.1826005'],
            # '新発田市': ['37.9478881', '139.3271831'],
            # '見附市': ['37.53145', '138.9126572'],
            # '魚沼市': ['37.2303274', '138.9611531'],
            # '南魚沼市': ['37.0655723', '138.8760989'],
            # '胎内市': ['38.0596893', '139.4102658'],
            # '上越市': ['37.1478816', '138.2359501'],
            # '佐渡市': ['38.0182578', '138.3683995'],
            # '糸魚川市': ['37.0390341', '137.8627939'],
            # '佐伯市': ['32.9601732', '131.8996704'],
            # '臼杵市': ['33.1261032', '131.8048454'],
            # '豊後大野市': ['32.9775643', '131.5841178'],
            # '別府市': ['33.2845752', '131.4913063'],
            # '由布市': ['33.1800993', '131.4269323'],
            # '大分市': ['33.2393864', '131.6096524'],
            # '豊後高田市': ['33.5562136', '131.4469025'],
            # '宇佐市': ['33.532005', '131.3496745'],
            # '竹田市': ['32.9736821', '131.3979534'],
            # '中津市': ['33.5982794', '131.1883225'],
            # '日田市': ['33.3211655', '130.9411316'],
            # '岡山市': ['34.6553944', '133.9194595'],
            # '沖縄市': ['26.3343738', '127.8056597'],
            # '那覇市': ['26.2122345', '127.6791452'],
            # 'うるま市': ['26.384705', '127.851324'],
            # '浦添市': ['26.249754', '127.716591'],
            # '糸満市': ['26.106017', '127.686066'],
            # '南城市': ['26.1625434', '127.771152'],
            # '名護市': ['26.5914524', '127.9773062'],
            # '宜野湾市': ['26.2815839', '127.7785754'],
            # '豊見城市': ['26.1772381', '127.6863791'],
            # '貝塚市': ['34.432856', '135.360043'],
            # '泉南市': ['34.3657277', '135.2739742'],
            # '箕面市': ['34.862898', '135.475719'],
            # '東大阪市': ['34.678147', '135.597728'],
            # '枚方市': ['34.818215', '135.659225'],
            # '四條畷市': ['34.730447', '135.674005'],
            # '高槻市': ['34.8812905', '135.6012398'],
            # '茨木市': ['34.834009', '135.5539509'],
            # '吹田市': ['34.764884', '135.51735'],
            # '大阪市': ['34.6937569', '135.5014539'],
            # '寝屋川市': ['34.76751', '135.633907'],
            # '豊中市': ['34.7862025', '135.4737093'],
            # '大東市': ['34.710679', '135.635478'],
            # '八尾市': ['34.626275', '135.605845'],
            # '和泉市': ['34.487280150000004', '135.4242118943296'],
            # '河内長野市': ['34.4575979', '135.5643131'],
            # '堺市': ['34.529124', '135.50156'],
            # '泉大津市': ['34.506612', '135.408793'],
            # '松原市': ['45.1335025', '124.8165152'],
            # '高石市': ['34.532059', '135.424388'],
            # '佐賀市': ['33.2639134', '130.3008378'],
            # '神埼市': ['33.3107434', '130.3730748'],
            # '小城市': ['33.2738076', '130.2171043'],
            # '唐津市': ['33.4503405', '129.9679345'],
            # '多久市': ['33.2885725', '130.1100243'],
            # '伊万里市': ['33.2644557', '129.8808439'],
            # '武雄市': ['33.1935518', '130.0194484'],
            # '静岡市': ['34.979149', '138.38299'],
            # '栃木市': ['36.3818177', '139.733591'],
            # '小山市': ['36.3147373', '139.800148'],
            # '徳島市': ['34.0698307', '134.5550353'],
            # '日野市': ['35.6610715', '139.4147051'],
            # '八王子市': ['35.660175', '139.283071'],
            # '青梅市': ['35.803601', '139.238128'],
            # 'あきる野市': ['35.731042', '139.217028'],
            # '東京都': ['35.6828387', '139.7594549'],
            # '町田市': ['35.564193', '139.442839'],
            # '国立市': ['35.681991', '139.43624'],
            # '昭島市': ['35.70248', '139.350065'],
            # '立川市': ['35.724463', '139.404766'],
            # '東大和市': ['35.740869', '139.428831'],
            # '東村山市': ['35.768929', '139.484539'],
            # '羽村市': ['35.764833', '139.307862'],
            # '多摩市': ['35.637188', '139.443503'],
            # '武蔵村山市': ['35.756509', '139.385637'],
            # '渋谷区': ['35.6645956', '139.6987107'],
            # '武蔵野市': ['35.712898', '139.563534'],
            # '小金井市': ['35.7041083', '139.5106759'],
            # '府中市': ['34.5683141', '133.2366327'],
            # '北区': ['35.755838', '139.736687'],
            # '世田谷区': ['35.646096', '139.65627'],
            # '品川区': ['35.599252', '139.73891'],
            # '大田区': ['35.561206', '139.715843'],
            # '江東区': ['35.649154', '139.81279'],
            # '新宿区': ['35.6937632', '139.7036319'],
            # '稲城市': ['35.638229', '139.507776'],
            # '練馬区': ['35.74836', '139.638735'],
            # '港区': ['35.6432274', '139.7400553'],
            # '江戸川区': ['35.678278', '139.871091'],
            # '千代田区': ['35.6938097', '139.7532163'],
            # '文京区': ['35.71881', '139.744732'],
            # '豊島区': ['35.736156', '139.714222'],
            # '小平市': ['35.72522', '139.476606'],
            # '葛飾区': ['35.751733', '139.863816'],
            # '墨田区': ['35.700429', '139.805017'],
            # '足立区': ['35.783703', '139.795319'],
            # '荒川区': ['35.737529', '139.78131'],
            # '杉並区': ['35.6994929', '139.6362876'],
            # '中央区': ['35.666255', '139.775565'],
            # '台東区': ['35.71745', '139.790859'],
            # '横浜市': ['35.444991', '139.636768'],
            # '三鷹市': ['35.685227', '139.572916'],
            # '中野区': ['35.718123', '139.664468'],
            # '米子市': ['35.4276408', '133.331459'],
            # '境港市': ['34.979149', '138.38299'],
            # '倉吉市': ['35.430166', '133.825525'],
            # '鳥取市': ['35.4943948', '134.2219282'],
            # '富山市': ['36.6957569', '137.2136215'],
            # '和歌山市': ['34.234617', '135.1782181'],
            # '山口市': ['34.1781317', '131.4737077'],
            # '山梨市': ['35.6928452', '138.6871263']
        }

        m = folium.Map(location=coordinates[city_type], zoom_start=10)
        for index, row in details.iterrows():
            if row['geometry'].startswith("POINT"):
                geometry = shapely.wkt.loads(row['geometry'])
            else:
                p = shapely.wkt.loads(row['geometry'])
                geometry = p.centroid

            folium.Marker(
                [geometry.y, geometry.x], popup=row['display_name'],
            ).add_to(m)

        
        
        # london_location = [35.183334,136.899994]

        # m = folium.Map(location=london_location, zoom_start=15)
        folium_static(m, width=900)

elif add_selectbox == 'Collaborators':
    st.subheader('Collaborators')

    st.markdown('<a href="https://omdena.com/omdena-chapter-page-japan/">Omdena Japan Chapter</a>', unsafe_allow_html=True)

    st.markdown('Project Manager: Galina Naydenova', unsafe_allow_html=True)
