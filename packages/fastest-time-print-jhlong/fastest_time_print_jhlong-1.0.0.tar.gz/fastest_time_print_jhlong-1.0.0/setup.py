from setuptools import setup

setup(
    name='fastest_time_print_jhlong',
    version='1.0.0',
    description='这个函数可以帮助你进行清洗数据，标准化、去重排序、最后切片打印的功能',
    long_description=open("README.md", encoding="utf-8").read(), # 从 README.md 文件读取长描述
    long_description_content_type="text/markdown",  # 指定描述文件的格式
    py_modules=['fastest_time_print'],
    author='jhlong',
    author_email='jhlong2024@163.com',
)

