import os
import sys
from streamlit_option_menu import option_menu
import streamlit as st

# from webui_pages.dialogue.dialogue import dialogue_page, chat_box
# from webui_pages.knowledge_base.knowledge_base import knowledge_base_page
# from webui_pages.introduce.introduce import introduce
from webui_pages.detection.detection import detection
from webui_pages.segment.segment import segment
from webui_pages.tianqi.tianqi import tianqi
from webui_pages.chat.chat import chat
from webui_pages.grow_stage.grow_stage import grow_stage
if __name__ == "__main__":

    st.set_page_config(
        "禾霖智谷",
        os.path.join("img", "小麦.png"),
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://zsspce.top',
            'Report a bug': "https://zsspce.top",
            'About': f"""欢迎使用WheatExpert-小麦多信息测控系统_1！"""
        }
    )

    pages = {
        "小麦头检测及计数": {
            "icon": "chat",
            "func": detection,
        },
        "小麦病害实例分割": {
            "icon": "gear",
            "func": segment,
        },
        "小麦生长智能识别": {
            "icon": "list-task",
            "func": grow_stage,
        },
        "智能天气预警":{
            "icon":"cloud-upload",
            "func":tianqi
        },
        "小麦咨询": {
            "icon": "house",
            "func": chat
        }
    }

    with st.sidebar:

        options = list(pages)
        icons = [x["icon"] for x in pages.values()]

        default_index = 0
        selected_page = option_menu(
            "",
            options=options,
            icons=icons,
            # menu_icon="chat-quote",
            default_index=default_index,
            styles={
                "container": {"padding": "0!important", "background-color": "#f5f5f5"},
                "icon": {"color": "orange", "font-size": "20px"},
                "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "green"},
            }
        )

    if selected_page in pages:
        pages[selected_page]["func"]()
