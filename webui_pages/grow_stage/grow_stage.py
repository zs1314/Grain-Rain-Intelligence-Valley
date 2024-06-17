import PIL
import streamlit as st
from PIL import Image
import torch
from torchvision import models, transforms
from .fasternet import fasternet_s  # 确保这是正确的导入方式
def grow_stage():
    # 初始化模型
    model = fasternet_s(num_classes=7)
    model_path = r'E:\image_classify_templete\weights\best_model.pth'  # 修改为您的权重文件的路径
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # 类别编号到类别名称的映射
    class_names = ['冠根', '早期营养生长阶段', '中期营养生长阶段', '晚期营养生长阶段', '开花和生殖阶段', '花期', '成熟阶段']

    # 图像的预处理函数
    def preprocess_image(image):
        # 如果图像有Alpha通道，转换为RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        return transform(image)

    # Streamlit页面布局
    # st.title('图像分类应用')
    # st.write("请选择一张图片进行分类。")

    # 使用列布局
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file = st.file_uploader("选择小麦/麦田图片", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            default_image = PIL.Image.open(uploaded_file)
            st.image(default_image, caption='上传的图片', use_column_width=True)

    with col2:
        if uploaded_file is not None and st.button('识别'):
            with st.spinner('正在识别中...'):
                try:
                    # 图像预处理
                    preprocessed_image = preprocess_image(default_image)
                    preprocessed_image = torch.unsqueeze(preprocessed_image, dim=0)
                    # 预测
                    with torch.no_grad():
                        prediction = model(preprocessed_image)
                    predicted_class = prediction.argmax().item()
                    st.success(f'您的麦田属于： {class_names[predicted_class]}')
                except Exception as e:
                    st.error(f"发生错误: {e}")

    # 在侧边栏添加标题
    st.sidebar.title('小麦生长阶段详细信息')

    # 在侧边栏逐个添加各个生长阶段的详细信息
    st.sidebar.write("""
    #### 第一阶段：冠根（Crown Root）
    - 通常指的是植物根部的生长初期。
    
    #### 第二阶段：早期营养生长阶段（Tillering）
    - 在这个阶段，植物开始生长新的茎杆。
    
    #### 第三阶段：中期营养生长阶段
    - 这个阶段，植物继续发展，但还未进入生殖生长阶段。
    
    #### 第四阶段：晚期营养生长阶段（Booting）
    - 在这个阶段，植物为开花做准备。
    
    #### 第五阶段：开花和生殖阶段（Heading）
    - 植物开始开花和形成种子。
    
    #### 第六阶段：花期（Anthesis）
    - 这是植物开花的阶段。
    
    #### 第七阶段：成熟阶段（Milking）
    - 在这个阶段，植物的种子开始成熟，准备收获。
    """)

    # 添加额外的信息或说明
    st.sidebar.info('此信息帮助理解小麦从种子到成熟的各个生长阶段。')
