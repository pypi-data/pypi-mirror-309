from setuptools import setup

# 读取 README.md 和 CHANGELOG.md 文件的内容
with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

# 如果存在 CHANGELOG.md 文件，合并到 long_description 中
try:
    with open("CHANGELOG.md", encoding="utf-8") as changelog_file:
        changelog = changelog_file.read()
except FileNotFoundError:
    changelog = ""

# 合并 README 和 CHANGELOG
long_description = readme + "\n\n" + changelog

setup(
    name='fastest_time_print_jhlong',
    version='1.0.2',  # 修改版本号
    description='这个函数可以帮助你进行清洗数据，标准化、去重排序、最后切片打印的功能',
    long_description=long_description,  # 合并后的长描述
    long_description_content_type="text/markdown",  # 指定描述文件的格式
    py_modules=['data_cleaner'],  # 修改为更清晰的模块名称
    author='jhlong',
    author_email='jhlong2024@163.com',
)
