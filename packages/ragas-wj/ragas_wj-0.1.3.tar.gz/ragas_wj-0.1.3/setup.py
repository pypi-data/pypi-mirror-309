from setuptools import setup, find_packages

setup(
    name="ragas_wj",  # 包名，pip install 时用的名字
    version="0.1.3",  # 版本号
    author="wangjie",
    author_email="wj15733866022@163.com",
    description="ragas for my project",
    # long_description=open("README.md").read(),  # 从 README 文件中加载长描述
    # long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/my_package",  # 项目主页链接
    packages=find_packages(),  # 自动发现所有子包
    classifiers=[  # 分类标签
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  # Python 版本要求
    install_requires=[  # 可选：依赖项
            "appdirs==1.4.4",
            "pysbd==0.3.4",
            "langchain-openai==0.2.8",
            "loguru==0.7.2",
            "datasets==2.12.0",
            "openpyxl==3.1.5",
            "langchain-community==0.3.7",
            "nltk==3.9.1",
        ],
)
