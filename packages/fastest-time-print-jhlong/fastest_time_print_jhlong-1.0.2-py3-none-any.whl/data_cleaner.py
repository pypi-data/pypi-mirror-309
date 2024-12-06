from sanitize_jhlong import sanitize
"""
在使用该函数时，需要安装 sanitize_jhlong 包
pip install sanitize_jhlong
这个函数可以帮助你进行清洗数据，标准化、去重排序、最后切片打印的功能
"""
def clean_and_print(file_path):
    '''
        清洗数据文件中的数据，并返回排序后最靠前的三条数据

        参数：
        file_path（str）：数据文件的路径

        返回：
        list:清洗后排序的前3条数据
        None：文件读取或处理过程中出现错误

        异常：
        - IOError：文件读取失败
        - ValueError:文件处理失败

    '''
    try:
        # 读取数据文件
        with open (file_path, 'r') as file:
            data = file.readline()

        # 数据清洗和标准化
        data_clean = data.strip().split(',')
        top_cleaned_data = sorted(set(sanitize(each_t) for each_t in data_clean))[0:3]
        return(top_cleaned_data)


    except IOError as err:
        print('文件读取错误' + str(err))
        return (None)

    except Exception as err:
        print('文件处理错误' + str(err))

__all__ = ['clean_and_print']

