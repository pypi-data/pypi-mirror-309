from sanitize_jhlong import sanitize
'''
在使用该函数时，需要安装 sanitize_jhlong 包
这个函数可以帮助你进行清洗数据，标准化、去重排序、最后切片打印的功能
'''
def fastest_time_print(data_file):
    '''
        data_file为你需要处理的数据的文件名称
    '''
    try:
        with open (data_file) as f:
            data = f.readline()
        data_clean = data.strip().split(',')
        good_data = sorted(set(sanitize(each_t) for each_t in data_clean))[0:3]
        return(good_data)      
    except IOError as err:
        print('find file error' + str(err))
        return (None)

