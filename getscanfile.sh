#!/bin/bash

# 定义本地下载目录
local_dir="/mnt/ssdc"

# 从SMB共享获取文件列表，排除前两行，因为它们不是文件
# 提取包括文件名、日期和时间的列
# 将日期转换为可排序的格式（YYYY-MM-DD）
# 从最新到最旧按新日期格式和时间排序
# 然后，取最新的10个文件
file_list=$(smbclient -N //192.168.1.5/USBSTORAGE -c 'cd EPSCAN; ls' | \
            awk '/blocks/ {next} NR>2 && $1 !~ /^.$/ {print $1, $3, $2}' | \
            awk '{print $2 " " $3 " " $1}' | \
            sort -k1,1Mr -k2,2r -k3,3r | head -10)

# 检查列表是否为空
if [ -z "$file_list" ]; then
  echo "没有文件可下载。"
  exit 1
fi

# 打印排序后的列表和行号
echo "可用文件："
echo "$file_list" | nl

# 提示用户输入要下载的文件编号（用空格分隔）
echo "输入要下载的文件编号（用空格分隔）："
read -a selections

# 循环每一个选中的文件编号
for selection in "${selections[@]}"; do
  # 从列表中提取相应的文件名
  file_name=$(echo "$file_list" | sed -n "${selection}p" | awk '{print $3}')
  
  # 使用smbclient下载文件
  smbclient -N //192.168.1.5/USBSTORAGE -c "cd EPSCAN; get \"$file_name\" \"$local_dir/$file_name\"" 2>/dev/null
  
  # 检查下载是否成功
  if [ $? -eq 0 ]; then
    echo "已下载：$file_name"
  else
    echo "下载失败：$file_name"
  fi
done

echo "下载完成。"
