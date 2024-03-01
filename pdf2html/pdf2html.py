import os
import glob
import subprocess

# 指定搜索PDF文件的目录
directory = input("Enter the path of the pdf: ").rstrip("/\\")

# 使用glob模块查找目录下的所有PDF文件
pdf_files = glob.glob(os.path.join(directory, '**', '*.pdf'), recursive=True)

# 遍历找到的PDF文件，并执行Docker命令进行转换
for pdf_file in pdf_files:
    # 获取PDF文件的目录，用于-v参数
    pdf_dir = os.path.dirname(pdf_file)
    # 获取PDF文件的相对路径，以便在Docker命令中使用
    pdf_relative_path = os.path.relpath(pdf_file, pdf_dir).replace("\\", "/")  # 确保路径格式在Unix系统上有效
    # 构建Docker命令的基本部分，动态设置-v参数
    docker_command_base = f'docker run -i --rm -v "{pdf_dir}:/pdf" pdf2htmlex/pdf2htmlex:0.18.8.rc2-master-20200820-alpine-3.12.0-x86_64'
    # 构建用于转换当前PDF文件的Docker命令
    docker_command = f'{docker_command_base} "/pdf/{pdf_relative_path}"'
    # 执行Docker命令
    print(f"开始转换: {pdf_dir}\\{pdf_relative_path}")
    subprocess.run(docker_command, shell=True)
