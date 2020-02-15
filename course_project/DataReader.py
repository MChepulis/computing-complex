import csv

from Data import Data


def read_csv(filename, t1=-1, t2=-1, read_all=False):
    fd = open(filename)
    reader = csv.reader(fd)
    result_time = []
    result_data = []
    # если не передано время, то считываем весь файл
    if t1 <= -1 and t2 <= -1:
        read_all = True

    first_flag = True
    for line in reader:
        cur_time = float(line[0])
        cur_data = float(line[1])

        if read_all:
            result_time.append(cur_time)
            result_data.append(cur_data)
            if first_flag:
                t1 = cur_time
                first_flag = False
        elif t1 <= cur_time <= t2:
            result_time.append(cur_time)
            result_data.append(cur_data)
    if read_all:
        t2 = cur_time
    result = Data(result_time, result_data, t1, t2, filename, len(result_time))
    return result