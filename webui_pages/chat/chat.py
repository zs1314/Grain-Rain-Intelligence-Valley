import streamlit as st
from zhipuai import ZhipuAI
import networkx as nx
import matplotlib.pyplot as plt

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
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content if response.choices else "未能获取有效的响应，请重试。"

    def create_relation_graph(edge_list):
        """根据返回的边列表创建关系图"""
        G = nx.parse_edgelist(edge_list, nodetype=str)
        plt.figure(figsize=(8, 8))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_color='k', linewidths=2, font_size=12)
        return plt

    st.title('小麦信息咨询')

    with st.form("query_form"):
        user_input = st.text_input("输入您关心的小麦病害", "锈病")
        submit_button = st.form_submit_button("获取病害信息")
        clear_button = st.form_submit_button("清空结果")

    if submit_button:
        with st.spinner('正在获取病害信息...'):
            detailed_prompt = construct_prompt(user_input)
            result = get_wheat_info(detailed_prompt)
            if result:
                st.success("成功获取信息！")
                st.write(result)
            else:
                st.error("无法获取信息，请检查输入和API设置。")

    if clear_button:
        st.empty()



    with st.form("query1_form"):
        wheat_variety = st.text_input("输入您感兴趣的小麦品种", "冬小麦")
        submit1_button = st.form_submit_button("显示小麦品种关系图")
        clear1_button = st.form_submit_button("清空结果")

    if submit1_button:
        with st.spinner('正在获取关系图信息...'):
            relation_prompt = f"请返回与小麦品种 '{wheat_variety}' 相关的品种关系图信息"
            edge_list = get_wheat_info(relation_prompt)
            if edge_list:
                st.success("成功获取信息！")
                st.write(edge_list)
            else:
                st.error("无法获取关系图，请检查输入和API设置。")

    if clear1_button:
        st.empty()


    with st.form("query2_form"):
        user_input = st.text_input("输入您关心的小麦生长阶段", "开花和生殖阶段（Heading）")
        submit2_button = st.form_submit_button("获取小麦生长阶段信息")
        clear2_button = st.form_submit_button("清空结果")

    if submit2_button:
        with st.spinner('正在获取信息...'):
            detailed_prompt = f"请返回与小麦生长阶段： '{user_input}' 相关的一切信息。包括该生长阶段的特征、注意事项、农民该做什么等等。注意：要有组织、有条理的写清楚，而且不能只涵盖我说的几点"
            result = get_wheat_info(detailed_prompt)
            if result:
                st.success("成功获取信息！")
                st.write(result)
            else:
                st.error("无法获取信息，请检查输入和API设置。")

    if clear2_button:
        st.empty()

if __name__ == "__main__":
    chat()

