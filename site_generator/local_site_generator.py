import os

root_dir = input("指定你的HTML文件所在的根目录: ")

def generate_links(directory, prefix="", indent=0):
    links = []
    # 遍历目录下的所有文件和子目录
    items = sorted(os.listdir(directory), key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    for item in items:
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            # 对于子目录，生成一个可点击的目录名以展开或折叠
            unique_id_path = path.replace('\\', '_').replace('/', '_')
            unique_id = f"folder_{unique_id_path}"
            links.append(f'{prefix}<li class="folder-item"><span onclick="toggleVisibility(\'{unique_id}\')" class="folder-name">{item}/<span class="toggle">[+]</span></span></li>')
            links.append(f'{prefix}<ul id="{unique_id}" class="nested" style="display:none;">')
            links += generate_links(path, prefix + "  ", indent+1)
            links.append(f'{prefix}</ul>')
        elif item.endswith('.html'):
            # 对于HTML文件，生成链接
            relative_path = os.path.relpath(path, start=root_dir).replace("\\", "/")
            link = f'<li><a href="{relative_path}" target="contentFrame">{item}</a></li>'
            links.append(f'{prefix}{link}')
    return links

html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的网站导航</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            height: 100%;
            font-family: Arial, sans-serif;
        }}
        #sidebar {{
            width: 300px;
            background: #343a40;
            color: #fff;
            float: left;
            height: 100%;
            overflow-y: auto;
            position: fixed;
            padding: 10px;
        }}
        #content {{
            margin-left: 300px;
            height: 100%;
            overflow: hidden;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
            overflow: auto;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
            font-size: 12px;
        }}
        ul .folder-item > .folder-name {{
            cursor: pointer;
            display: block;
            padding: 5px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }}
        ul .folder-item > .folder-name:hover {{
            background-color: #495057;
        }}
        ul .nested {{
            margin-left: 20px;
        }}
        ul .nested li {{
            margin-top: 5px;
        }}
        .toggle {{
            margin-left: 5px;
            font-size: smaller;
            color: #bbb;
        }}
        a {{
            color: #ffc107;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
    <script>
        function toggleVisibility(id) {{
            var element = document.getElementById(id);
            var toggle = element.previousElementSibling.querySelector('.toggle');
            if (element.style.display === "none") {{
                element.style.display = "block";
                toggle.innerHTML = '[-]';
            }} else {{
                element.style.display = "none";
                toggle.innerHTML = '[+]';
            }}
        }}
    </script>
</head>
<body>
    <div id="sidebar">
        <h1>网站导航</h1>
        <ul>
            {links}
        </ul>
    </div>
    <div id="content">
        <iframe name="contentFrame"></iframe>
    </div>
</body>
</html>
"""

# 生成导航页的HTML内容
links_html = '\n'.join(generate_links(root_dir))
navigation_page = html_template.format(links=links_html)

# 保存导航页到根目录
with open(os.path.join(root_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(navigation_page)

print('导航页已生成。')
