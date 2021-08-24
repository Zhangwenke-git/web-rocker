import time
from datetime import datetime, date


class Constant(object):


    Empty_str = ''
    Space_str = ' '

    Separator_pipe = "||"
    Separator_one = "#"

    Separator_two = "=>"
    Separator_substitution = "%s"

    persistent_time = 30
    interval = 0.5


    """
        Thu Apr  7 10:05:21 2016
    """
    time1 = time.asctime(time.localtime(time.time()))

    """
        2016-03-20 11:45:39
    """
    time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    """
        2018-08-14 22:24:23.022380
    """
    time3 = datetime.now()

    """
        21_12_03
    """
    time4 = time.strftime('%H_%M_%S')


    """
        20101203222423002
    """
    time5 = time.strftime("%Y%m%d%H%M%S", time.localtime())


    """
        2019-12-02
    """
    current_date = date.today()


    """
        2020/03/20
    """
    time6 = time.strftime("%Y/%m/%d", time.localtime())

    """
        2020/3/20
    """
    time7 = time.strftime("%Y/%m/%d", time.localtime())

    """
        20101203
    """
    time8 = time.strftime("%Y%m%d", time.localtime())


    """
        202011141337
    """
    time9 = time.strftime("%Y%m%d%H%M", time.localtime())

    success_flag = '通过'
    fail_flag = '失败'

if __name__ == "__main__":
    print(Constant.time9)