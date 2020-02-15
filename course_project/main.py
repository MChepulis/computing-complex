
import matplotlib.pyplot as plt
from Data import Data
from DataReader import read_csv
import numpy

plot_dict_path = "plots"


def get_wnd(length, index, width):
    wnd_ind = [i for i in range(index - width, index + width + 1)]

    res_wnd = []
    for value in wnd_ind:
        if 0 <= value < length:
            res_wnd.append(value)
    return res_wnd


def med_smooth(data, smooth_coef):
    tmp_data = data.copy()
    for i in range(0, data.size):
        wnd_ind = get_wnd(data.size, i, smooth_coef)
        wnd_value = [data.amplitude[ind] for ind in wnd_ind]
        tmp_data.amplitude[i] = numpy.median(wnd_value)
    tmp_data.smooth_coef = smooth_coef
    return tmp_data


def exp_smooth(data, smooth_coef):
    tmp_data = data.copy()
    for i in range(0, data.size):
        wnd_ind = get_wnd(data.size, i, smooth_coef)
        wnd_value = [data.amplitude[ind] for ind in wnd_ind]
        tmp_data.amplitude[i] = numpy.mean(wnd_value)
    tmp_data.smooth_coef = smooth_coef
    return tmp_data


def merge_local_min(ind, count, flag):
    min_count = 250
    max_ind = []
    min_ind = []

    prev_flag = flag[0]
    prev_ind = ind[0]
    print(count)
    print(flag)
    print()
    print(ind)
    for i in range(1, len(count)):
        curr_count = count[i]
        curr_flag = flag[i]
        curr_ind = ind[i]

        if curr_count >= min_count:
            if prev_flag == curr_flag:
                prev_ind = curr_ind
                prev_flag = curr_flag
            else:
                if prev_flag:
                    max_ind.append(prev_ind)
                else:
                    min_ind.append(prev_ind)
                prev_ind = curr_ind
                prev_flag = curr_flag

    return max_ind, min_ind


def find_local_extremum(data):

    result_count = []
    result_grow_flag = []
    monotone_count = 1
    result_ind = []

    grow_flag = data.amplitude[0] <= data.amplitude[1]

    for i in range(1, data.size-1):
        prev_value = data.amplitude[i - 1]
        curr_value = data.amplitude[i]
        next_value = data.amplitude[i + 1]
        cur_time = data.time[i]

        monotone_count += 1
        if prev_value >= curr_value <= next_value or prev_value <= curr_value >= next_value:
            result_ind.append(i)
            result_count.append(monotone_count)
            result_grow_flag.append(grow_flag)
            monotone_count = 0
        grow_flag = prev_value <= curr_value <= next_value

    result_ind.append(i)
    result_count.append(monotone_count)
    result_grow_flag.append(grow_flag)
    max_ind, min_ind = merge_local_min(result_ind, result_count, result_grow_flag)
    return max_ind, min_ind


def find_global_min(data, a_ind, b_ind):
    min_ind = b_ind
    min_value = data.amplitude[b_ind]
    for i in range(a_ind, b_ind):
        cur_value = data.amplitude[i]
        if cur_value < min_value:
            min_value = cur_value
            min_ind = i
    return min_ind


def find_global_max(data, a_ind, b_ind):
    min_ind = b_ind
    min_value = data.amplitude[b_ind]
    for i in range(a_ind, b_ind):
        cur_value = data.amplitude[i]
        if cur_value > min_value:
            min_value = cur_value
            min_ind = i
    return min_ind


def get_global_min(data, min_ind, max_ind):
    if len(max_ind) == 0 or len(min_ind) == 0:
        return
    tmp_max_ind = max_ind.copy()
    tmp_min_ind = min_ind.copy()
    if tmp_max_ind[0] > tmp_min_ind[0]:
        tmp_max_ind = [0] + tmp_max_ind

    global_min_ind = []
    for i in range(0, len(min_ind)):
        a = tmp_max_ind[i]
        b = tmp_min_ind[i]
        tmp_gl_min = find_global_min(data, a, b)
        global_min_ind.append(tmp_gl_min)
    return global_min_ind


def get_global_max(data, min_ind, max_ind):
    if len(max_ind) == 0 or len(min_ind) == 0:
        return
    tmp_max_ind = max_ind.copy()
    tmp_min_ind = min_ind.copy()
    if tmp_max_ind[0] > tmp_min_ind[0]:
        tmp_max_ind = [0] + tmp_max_ind

    global_max_ind = []
    for i in range(0, len(min_ind)):
        a = tmp_max_ind[i]
        b = tmp_min_ind[i]
        tmp_gl_min = find_global_max(data, a, b)
        global_max_ind.append(tmp_gl_min)
    return global_max_ind


def draw_data(data, dataset=[], legends=None, markers=None, add_title="", add_filename=""):

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(data.time, data.amplitude, label="data")
    for i in range(0, len(dataset)):
        curr_data = dataset[i]
        if legends is not None:
            legend = legends[i]
        else:
            legend = None
        if markers is not None:
            marker = markers[i]
        else:
            marker = None
        if marker is not None:
            linestyle = ""
        else:
            linestyle = None


        ax.plot(curr_data.time, curr_data.amplitude, label=legend, marker=marker, linestyle=linestyle)
    ax.set_xlabel("time")
    ax.set_ylabel("amplitude")
    ax.set_title("%s time=[%.3f, %.3f]\n%s" % (data.filename, data.t1, data.t2, add_title))
    fig.legend()
    plt.grid(ax)
    fig.show()
    fig.savefig("%s\\%s time=[%.3f, %.3f]%s.png" % (plot_dict_path, data.filename, data.t1, data.t2, add_filename), dpi=300, format='png', bbox_inches='tight')
    plt.close(fig)


def draw_sections(data, global_min_ind):
    max_amp = max(data.amplitude)
    min_amp = min(data.amplitude)

    lines_x = []
    lines_y = []
    for ind in global_min_ind:
        x = [data.time[ind], data.time[ind]]
        y = [min_amp, max_amp]
        lines_x.append(x)
        lines_y.append(y)

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(data.time, data.amplitude, label="data")
    length = len(lines_x)
    if length > 0:
        ax.plot(lines_x[0], lines_y[0], label="sections", linestyle="--", color="red")
    for i in range(1, length):
        ax.plot(lines_x[i], lines_y[i], linestyle="--", color="red")
    ax.set_xlabel("time")
    ax.set_ylabel("amplitude")
    ax.set_title("%s time=[%.3f, %.3f]\n%s" % (data.filename, data.t1, data.t2, "sections"))
    fig.legend()
    plt.grid(ax)
    fig.show()
    fig.savefig("%s\\%s time=[%.3f, %.3f]%s.png" % (plot_dict_path, data.filename, data.t1, data.t2, "sections"),
                dpi=300, format='png', bbox_inches='tight')
    plt.close(fig)


def draw_saw(data, global_min_ind):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    a = global_min_ind[0]
    for i in range(1, len(global_min_ind)):
        b = global_min_ind[i]
        x = data.time[a:b]
        y = data.amplitude[a:b]
        ax.plot(x, y)
        a = b
    ax.set_xlabel("time")
    ax.set_ylabel("amplitude")
    ax.set_title("%s time=[%.3f, %.3f]\n%s" % (data.filename, data.t1, data.t2, "saw"))
    plt.grid(ax)
    fig.show()
    fig.savefig("%s\\%s time=[%.3f, %.3f]%s.png" % (plot_dict_path, data.filename, data.t1, data.t2, "saw"),
                dpi=300, format='png', bbox_inches='tight')
    plt.close(fig)


def main():
    filename = "SXR 50 mkm.csv"
    #filename = "SXR 27 мкм.csv"
    #filename = "SXR 80 mkm.csv"
    t1 = 0.1927
    t2 = 0.242
    smooth_coef = 250
    data = read_csv(filename, t1, t2)
    print("size = %i" % data.size)
    print("file = \"%s\"" % filename)
    print("smooth coeff = %i" % smooth_coef)

    smooth_data = exp_smooth(data, smooth_coef)
    res_data = data.copy()
    res_data.amplitude = [data.amplitude[ind] - smooth_data.amplitude[ind] for ind in range(0, data.size)]

    draw_data(data, add_title="all data", add_filename="all data")
    draw_data(smooth_data, add_title="smooth_data(exp)", add_filename="smooth_data(exp)")
    draw_data(res_data, add_title="residual_data", add_filename="residual_data")
    draw_data(data, [smooth_data], legends=["smooth"], add_title="data and exp_smooth(%i)" % smooth_coef, add_filename="data and smooth(%i)" % smooth_coef)

    max_ind, min_ind = find_local_extremum(smooth_data)

    max_t = [smooth_data.time[ind]for ind in max_ind]
    max_a = [smooth_data.amplitude[ind]for ind in max_ind]
    min_t = [smooth_data.time[ind]for ind in min_ind]
    min_a = [smooth_data.amplitude[ind]for ind in min_ind]
    minimum = Data(min_t, min_a)
    maximum = Data(max_t, max_a)
    draw_data(data, [smooth_data, minimum, maximum], legends=["smooth", "min", "max"], markers=[None, "o", "o"], add_title="extremum\nsmooth coeff = %i" % smooth_coef, add_filename="extremum(%i)" % smooth_coef)

    global_min_ind = get_global_min(data, min_ind, max_ind)

    if global_min_ind is not None:
        min_t = [data.time[ind]for ind in global_min_ind]
        min_a = [data.amplitude[ind]for ind in global_min_ind]
        glob_minimum = Data(min_t, min_a)
        draw_data(data, [smooth_data, glob_minimum], legends=["smooth", "min"], markers=[None, "o"], add_title="minimum in section", add_filename="minimum in section")
        draw_sections(data, global_min_ind)
        draw_saw(data, global_min_ind)
    else:
        print("Can`t find minimums")



if __name__ == "__main__":
    main()
