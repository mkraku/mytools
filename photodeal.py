import os
from PIL import Image, ImageEnhance, ImageFilter

def enhance_document(image_path, output_path):
    # 打开图片
    with Image.open(image_path) as img:
        # 转换为RGB模式（如果不是的话）
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # 增加曝光（亮度）
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.5)  # 值大于1增加亮度，可以根据需要调整

        # 增加对比度
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)  # 可以调整这个值

        # 保存结果
        img.save(output_path)

def process_folder(input_folder, output_folder):
    # 创建输出文件夹(如果不存在)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"enhanced_{filename}")
            try:
                enhance_document(input_path, output_path)
                print(f"处理完成: {filename}")
            except Exception as e:
                print(f"处理 {filename} 时出错: {str(e)}")

# 设置输入和输出文件夹
input_folder = '.'  # 当前文件夹
output_folder = './output'

# 处理文件夹
process_folder(input_folder, output_folder)

print("所有图片处理完成!")