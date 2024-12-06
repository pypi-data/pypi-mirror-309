from setuptools import setup, find_packages

setup(
    name="mtclabpy",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        # 你的依赖项会在这里列出
    ],
    author="Menglei Xia",  # 请填写作者名
    author_email="xiamenglei321@163.com",  # 请填写作者邮箱
    description="A comprehensive tool for molecular and enzyme calculations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",  # 项目的GitHub或其他代码仓库URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
