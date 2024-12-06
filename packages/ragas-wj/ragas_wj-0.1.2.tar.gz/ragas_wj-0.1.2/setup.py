from setuptools import setup, find_packages

setup(
    name="ragas_wj",  # 包名，pip install 时用的名字
    version="0.1.2",  # 版本号
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
)
