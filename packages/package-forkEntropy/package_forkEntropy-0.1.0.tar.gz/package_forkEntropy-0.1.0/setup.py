from distutils.core import setup
from setuptools import find_packages

with open("ReadMe.md", "r", encoding="utf-8") as f:
  long_description = f.read()

setup(
    name='package_forkEntropy',  # 包名
    version='0.1.0',  # 版本号
    author='XiangChenWu',  # 作者
    author_email='ixc@smail.nju.edu.cn',  # 作者邮箱
    description='The implementation and test for the measurement method fork entropy.',  # 简要描述
    long_description=long_description,  # 详细描述
    long_description_content_type='text/markdown',
    url='https://github.com/WuXiangChen/ForkEntropy_ESE',  # 项目网址
    packages=find_packages(),  # 自动查找包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 许可证
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Python版本要求
    install_requires=[
        'numpy',
        'pandas',
        'json'
    ],
    platforms=["all"]
)
