import numpy as np
import pandas as pd
import requests
import streamlit as st
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


from datetime import datetime
import os

from typing import List, Dict
import altair as alt
from datetime import datetime, timedelta

def tianqi():
    # 天气查询模块
    st.header('智能天气查询')

    def get_location_id(city_name, heweather_api_key):
        base_url = 'https://geoapi.qweather.com/v2/city/lookup?'

        params = {
            'location': city_name,
            'key': heweather_api_key,
        }

        response = requests.get(base_url, params=params)
        location_data = response.json()

        if location_data["code"] == "200":
            return location_data['location'][0]['id']
        else:
            return None

    # 用户输入城市名称
    city_name = st.text_input('输入城市名称:')
    if city_name:
        # 和风天气 API 密钥，请替换成你自己的密钥
        heweather_api_key = '6e9ddf7704cb48608ad25b81f006cf8f'

        # 获取 Location_ID
        city_id = get_location_id(city_name, heweather_api_key)
        if city_id:
            with st.spinner('正在查询天气信息...'):
                base_url = 'https://devapi.qweather.com/v7/weather/now?'
                params = {'location': city_id, 'key': heweather_api_key}

                # 发送 API 请求
                response = requests.get(base_url, params=params)
                weather_data = response.json()
                print(weather_data)
            # 显示天气信息
            if weather_data["code"] == "200":
                now_weather = weather_data['now']
                temperature = float(now_weather['temp'])
                feels_like = float(now_weather['feelsLike'])
                humidity = int(now_weather['humidity'])
                wind_direction = now_weather['windDir']
                wind_speed = float(now_weather['windSpeed'])

                # 显示当前天气信息
                st.subheader('当前天气信息')
                st.write(f'**温度:** {temperature}°C')
                st.write(f'**体感温度:** {feels_like}°C')
                st.write(f'**湿度:** {humidity}%')
                st.write(f'**风向:** {wind_direction}')
                st.write(f'**风速:** {wind_speed} m/s')

                # 创建交互式饼图，显示温度和湿度占比
                fig_pie = go.Figure()
                fig_pie.add_trace(go.Pie(labels=['温度', '湿度'], values=[temperature, humidity], hole=0.4))
                fig_pie.update_layout(title='温度和湿度占比', template='seaborn')
                st.plotly_chart(fig_pie, use_container_width=True)

                # 创建交互式雷达图，显示各项天气指标
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(r=[temperature, humidity, wind_speed],
                                                    theta=['温度', '湿度', '风速'],
                                                    fill='toself',
                                                    marker=dict(color='rgba(255, 102, 102, 0.5)'),
                                                    line=dict(color='rgba(255, 102, 102, 1)'),
                                                    name='实时指标'))
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 40])))
                st.plotly_chart(fig_radar, use_container_width=True)

                # 绘制温度和体感温度曲线图
                fig_temperature = go.Figure()
                fig_temperature.add_trace(
                    go.Scatter(x=[0, 1], y=[temperature, feels_like], mode='lines', name='Temperature'))
                fig_temperature.update_layout(title='温度和体感温度变化', xaxis_title='', yaxis_title='°C',
                                              template='seaborn')
                st.plotly_chart(fig_temperature, use_container_width=True)

                # 绘制湿度仪表盘
                fig_humidity = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=humidity,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "湿度 (%)"},
                    gauge={'axis': {'range': [0, 100]},
                           'bar': {'color': "lightblue"},
                           'steps': [
                               {'range': [0, 50], 'color': "lightgreen"},
                               {'range': [50, 80], 'color': "yellow"},
                               {'range': [80, 100], 'color': "red"}],
                           'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 90}}))
                fig_humidity.update_layout(template='seaborn')
                st.plotly_chart(fig_humidity, use_container_width=True)

                # 绘制风向和风速极坐标图
                fig_wind = px.scatter_polar(theta=[wind_direction], r=[wind_speed], labels={'theta': '', 'r': 'm/s'},
                                            title='实时风向和风速',
                                            template='seaborn')
                st.plotly_chart(fig_wind, use_container_width=True)

                # 添加提示信息
                st.subheader('农业建议')
                st.warning('请根据气象信息前往智能决策模块询问！')
                if temperature > 25:
                    st.warning('当前温度较高，注意防暑降温，确保植物有足够的水分。')
                elif temperature < 10:
                    st.warning('当前温度较低，需注意保暖，冷冻对植物有害。')

                if humidity > 80:
                    st.warning('当前湿度较高，需防范霉菌和病害的发生。')

                if wind_speed > 5:
                    st.warning('当前风速较大，需注意风害，为植物提供支撑。')

                # 添加一些炫酷效果
                st.success('天气信息查询完成！')
                st.balloons()

            else:
                st.error('无法获取实时气候信息，请检查城市名称或稍后再试。')
