import requests
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

import settings


def tianqi():
    # 天气查询模块
    st.header('智能天气查询')

    def get_location_id(city_name, heweather_api_key):
        base_url = 'https://geoapi.qweather.com/v2/city/lookup?'
        params = {
            'location': city_name,
            'key': heweather_api_key,
        }

        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        location_data = response.json()

        if location_data.get("code") == "200" and location_data.get('location'):
            return location_data['location'][0]['id']
        return None

    city_name = st.text_input('输入城市名称:')
    if not city_name:
        return

    if not settings.QWEATHER_API_KEY:
        st.error('未检测到 QWEATHER_API_KEY，请先配置环境变量后再使用天气查询。')
        return

    try:
        city_id = get_location_id(city_name, settings.QWEATHER_API_KEY)
    except requests.RequestException as exc:
        st.error(f'天气位置查询失败：{exc}')
        return

    if not city_id:
        st.error('无法解析该城市，请确认城市名称后重试。')
        return

    with st.spinner('正在查询天气信息...'):
        base_url = 'https://devapi.qweather.com/v7/weather/now?'
        params = {'location': city_id, 'key': settings.QWEATHER_API_KEY}
        try:
            response = requests.get(base_url, params=params, timeout=15)
            response.raise_for_status()
        except requests.RequestException as exc:
            st.error(f'实时天气查询失败：{exc}')
            return

        weather_data = response.json()

    if weather_data.get("code") != "200":
        st.error('无法获取实时气候信息，请检查城市名称或稍后再试。')
        return

    now_weather = weather_data['now']
    temperature = float(now_weather['temp'])
    feels_like = float(now_weather['feelsLike'])
    humidity = int(now_weather['humidity'])
    wind_direction = now_weather['windDir']
    wind_speed = float(now_weather['windSpeed'])

    st.subheader('当前天气信息')
    st.write(f'**温度:** {temperature}°C')
    st.write(f'**体感温度:** {feels_like}°C')
    st.write(f'**湿度:** {humidity}%')
    st.write(f'**风向:** {wind_direction}')
    st.write(f'**风速:** {wind_speed} m/s')

    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(labels=['温度', '湿度'], values=[temperature, humidity], hole=0.4))
    fig_pie.update_layout(title='温度和湿度占比', template='seaborn')
    st.plotly_chart(fig_pie, use_container_width=True)

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=[temperature, humidity, wind_speed],
                                        theta=['温度', '湿度', '风速'],
                                        fill='toself',
                                        marker=dict(color='rgba(255, 102, 102, 0.5)'),
                                        line=dict(color='rgba(255, 102, 102, 1)'),
                                        name='实时指标'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 40])))
    st.plotly_chart(fig_radar, use_container_width=True)

    fig_temperature = go.Figure()
    fig_temperature.add_trace(go.Scatter(x=[0, 1], y=[temperature, feels_like], mode='lines', name='Temperature'))
    fig_temperature.update_layout(title='温度和体感温度变化', xaxis_title='', yaxis_title='°C', template='seaborn')
    st.plotly_chart(fig_temperature, use_container_width=True)

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

    fig_wind = px.scatter_polar(theta=[wind_direction], r=[wind_speed], labels={'theta': '', 'r': 'm/s'},
                                title='实时风向和风速',
                                template='seaborn')
    st.plotly_chart(fig_wind, use_container_width=True)

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

    st.success('天气信息查询完成！')
    st.balloons()
