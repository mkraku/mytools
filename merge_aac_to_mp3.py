import os
import subprocess
from pathlib import Path

def get_aac_files(directory='.'):
    """
    获取指定目录下的所有aac文件。
    :param directory: 要搜索的目录，默认为当前目录
    :return: 包含aac文件路径的列表
    """
    aac_files = list(Path(directory).glob('*.aac'))
    return sorted(aac_files)  # 按文件名排序

def concatenate_files(file_list, output_file):
    """
    创建一个文本文件，包含要合并的文件列表，这是ffmpeg需要的格式。
    :param file_list: 文件路径列表
    :param output_file: 输出文件路径
    """
    with open('file_list.txt', 'w', encoding='utf-8') as f:
        for file_path in file_list:
            f.write(f"file '{file_path}'\n")
    
    # 使用ffmpeg合并文件
    command = [
        'ffmpeg',
        '-f', 'concat',  # 使用concat demuxer
        '-safe', '0',    # 允许不安全的文件路径
        '-i', 'file_list.txt',  # 输入文件列表
        '-c', 'copy',    # 不重新编码，直接复制流
        '-y',            # 如果输出文件已存在，则覆盖
        output_file
    ]
    subprocess.run(command)

def convert_to_mp3(input_file, output_file):
    """
    将输入文件转换为mp3格式。
    :param input_file: 输入文件路径
    :param output_file: 输出文件路径
    """
    command = [
        'ffmpeg',
        '-i', input_file,      # 输入文件
        '-b:a', '192k',        # 音频比特率，可根据需要调整
        '-y',                  # 如果输出文件已存在，则覆盖
        output_file
    ]
    subprocess.run(command)

def main():
    # 获取所有aac文件
    aac_files = get_aac_files()
    if not aac_files:
        print("没有找到任何aac文件。")
        return
    
    # 合并aac文件到一个临时文件
    temp_merged_file = 'merged.aac'
    concatenate_files(aac_files, temp_merged_file)
    
    # 将合并后的aac文件转换为mp3
    final_mp3_file = 'all_combined.mp3'
    convert_to_mp3(temp_merged_file, final_mp3_file)
    
    print(f"所有aac文件已经合并并转换为 {final_mp3_file}")

if __name__ == '__main__':
    main()