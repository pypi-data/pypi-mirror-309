from setuptools import setup, find_packages

setup(
    name="mtclabpy",
    version="0.6.3",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'biopython',
        'requests'
    ],
    package_data={
        'mtclabpy': ['*/*.py'],
    },
    include_package_data=True,
    author="Menglei Xia",
    author_email="xiamenglei321@163.com",
    description="A comprehensive tool for molecular and enzyme calculations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
