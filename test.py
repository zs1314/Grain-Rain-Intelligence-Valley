# from zhipuai import ZhipuAI
#
# client = ZhipuAI(api_key="9ee745c98d90ac30bd8d386cc9a7dcbe.0HBoOevy5NB2jqog")  # 填写您自己的APIKey
# while True:
#     prompt = input("user:")
#     response = client.chat.completions.create(
#         model="glm-4",  # 填写需要调用的模型名称
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#     )
#     answer = response.choices[0].message.content
#     print("ZhipuAI:", answer)


#
# import streamlit as st
# from zhipuai import ZhipuAI
#
# # 初始化ZhipuAI客户端
# client = ZhipuAI(api_key="9ee745c98d90ac30bd8d386cc9a7dcbe.0HBoOevy5NB2jqog")  # 使用您自己的API密钥填充
#
# def get_wheat_info(query):
#     """使用ZhipuAI的API获取小麦病害相关信息"""
#     response = client.chat.completions.create(
#         model="glm-4",  # 指定需要调用的模型
#         messages=[
#             {"role": "user", "content": query}
#         ],
#     )
#     if response.choices:
#         return response.choices[0].message.content
#     else:
#         return "未能获取有效的响应，请重试。"
#
# # 设置Streamlit应用的标题
# st.title('小麦病害信息抽取应用')
#
# # 创建一个文本输入框，用户可以输入查询关于小麦的问题
# user_input = st.text_input("输入您关心的小麦病害", "锈病")
#
# # 当用户点击按钮时进行处理
# if st.button('获取病害信息'):
#     with st.spinner('正在从ZhipuAI模型获取信息...'):
#         result = get_wheat_info(user_input)
#         if result:
#             st.success("成功获取信息！")
#             st.write(result)  # 直接显示文本结果
#         else:
#             st.error("无法获取信息，请检查输入和API设置。")


import streamlit as st
from zhipuai import ZhipuAI
import matplotlib.pyplot as plt
import networkx as nx
def chat():
    # 初始化ZhipuAI客户端
    client = ZhipuAI(api_key="9ee745c98d90ac30bd8d386cc9a7dcbe.0HBoOevy5NB2jqog")  # 使用您自己的API密钥填充

    def construct_prompt(disease_name):
        """根据病害名称构建详细的Prompt"""
        return (f"请根据小麦病害 '{disease_name}' 返回以下格式化信息："
                "\n1. 高发地区：[地区列表]"
                "\n2. 典型症状和特征：[描述性文本]"
                "\n3. 推荐的防治措施：[步骤列表]")

    def get_wheat_info(prompt):
        """使用ZhipuAI的API获取小麦病害相关信息"""
        response = client.chat.completions.create(
            model="glm-4",  # 指定需要调用的模型
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        if response.choices:
            return response.choices[0].message.content
        else:
            return "未能获取有效的响应，请重试。"

    # 设置Streamlit应用的标题
    st.title('小麦病害信息抽取应用')

    # 创建文本输入框
    user_input = st.text_input("输入您关心的小麦病害", "锈病")
    # 处理用户点击事件
    if st.button('获取病害信息'):
        with st.spinner('正在从ZhipuAI模型获取信息...'):
            detailed_prompt = construct_prompt(user_input)
            result = get_wheat_info(detailed_prompt)
            if result:
                st.success("成功获取信息！")
                st.write(result)  # 直接显示文本结果
            else:
                st.error("无法获取信息，请检查输入和API设置。")

    # 另一个输入框处理小麦品种的关系图
    wheat_variety = st.text_input("输入您感兴趣的小麦品种", "品种A")
    if st.button('显示小麦品种关系图'):
        with st.spinner('正在从ZhipuAI模型获取关系图信息...'):
            relation_prompt = f"请返回与小麦品种 '{wheat_variety}' 相关的品种关系图信息，地区关系图"
            edge_list = get_wheat_info(relation_prompt)
            # st.write(edge_list)
            if edge_list:
                st.write(edge_list)
            else:
                st.error("无法获取关系图，请检查输入和API设置。")

