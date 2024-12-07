from setuptools import setup, find_packages

# 读取 README 文件内容
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# 读取 LICENSE 文件内容
with open('LICENSE', 'r', encoding='utf-8') as f:
    license_content = f.read()

setup(
    name="js_code",  # 包名，替换为你的项目名称
    version="1.2.4",  # 版本号，根据实际情况修改
    author="Aduh",  # 作者名
    author_email="aduh73285@gmail.com",  # 作者邮箱
    description="A simple library to run JavaScript code based on Python",  # 简短描述
    long_description=long_description,  # 从 README 文件获取的长描述
    long_description_content_type='text/markdown',  # 如果 README 是 markdown 格式
    packages=find_packages(),  # 自动查找并包含所有的包
    install_requires=[  # 依赖项，这里列出项目所需要的 Python 库
        "PyExecJS2",  # 你项目的依赖库，确保在 PyPI 上可以找到
    ],
    classifiers=[  # 分类器帮助其他用户了解你的项目类型
        "Programming Language :: Python :: 3",  # 支持 Python 3
        "License :: OSI Approved :: BSD License",  # 更新为 BSD 2-Clause License
        "Operating System :: OS Independent",  # 支持跨平台
    ],
    license=license_content,  # 在这里展示 LICENSE 文件的内容
    python_requires='>=3.6',  # 指定项目支持的最低 Python 版本
    include_package_data=True,  # 确保包括所有非 Python 文件（如配置文件、静态文件等）
    zip_safe=False,  # 允许不使用 zip 格式的包安装（如果需要的话）
)
