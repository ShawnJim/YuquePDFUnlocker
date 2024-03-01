# PDF导出被语雀加密|限制的知识库

## 背景

逛论坛时碰到合适的资料, 碰到在维护在语雀中的资料时突然想备份到本地, 但是有些语雀库是加密或者不可导出的, 于是就有了此项目.

## 快速运行

```shell
git clone https://github.com/ShawnJim/YuquePDFUnlocker.git && cd YuquePDFUnlocker
python .\spider-virtual-optimize.py
# 输入参数
# "Enter the browser path: " -> 浏览器程序路径
# "Enter the driver path: " -> 浏览器驱动路径
# "Enter the URL: " -> 爬取的语雀地址
# "Enter the password: " -> 语雀文档加密的密码
# "Enter the save path: " -> 文档保存的目录
```
## 实现思路

基于selenium 自动化操作浏览器, 通过CDP(Chrome DevTools Protocol) 协议转储文档页面为pdf.

## 环境

- python-3.11
- pywinauto~=0.6.8
- PyAutoGUI~=0.9.54
- pyperclip~=1.8.2
- selenium~=4.18.1
- [google for testing](https://googlechromelabs.github.io/chrome-for-testing/)

## 最后

本项目仅供学习交流使用，不得用于任何商业用途

有任何疑问请在 Issues 中讨论沟通