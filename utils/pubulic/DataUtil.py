import random
from decimal import Decimal,ROUND_HALF_UP
from utils.pubulic import logger

logger = logger.Logger("DataUtil")


class DataUtil(object):

    def calculate_percentage(self, first_num, second_num):
        if second_num <= 0:
            return '0%'
        format = '{:.0%}'
        return format.format(first_num / second_num)


    def format_num(self, num, precision=4):
        """
        :function:float数据类型进行设置精度
        :param num:
        :param precision:
        :return:
        """
        try:
            format = "{:.%sf}" % int(precision)
            return format.format(float(num))
        except Exception as e:
            logger.error(f"Fail to format {num},error as follow {e}")
            return num

    def get_random_float(self, first_num, second_num, precision):
        try:
            num = random.uniform(float(first_num), float(second_num))
            num = self.format_num(num, precision)
            logger.debug(f"The random num is {num},and the limit is [{first_num, second_num}]")
            return num
        except Exception as e:
            logger.error(f"Fail to get the random num between {first_num} and {second_num},error as follow {e}")
            return None

    def get_random_int(self, first_num, second_num):
        try:
            num = random.randint(int(first_num), int(second_num))
            logger.debug(f"The random num is {num},and the limit is [{first_num, second_num}]")
            return num
        except Exception as e:
            logger.error(f"Fail to get the random num between {first_num} and {second_num},error as follow {e}")
            return None

    def keepAnddel(self,string,precision=2):
        """
        :function: 四舍五入
        :param string: string类型，不是float类型
        :param precision:
        :return:
        """
        if precision == 1:
            formater = '0.0'
        elif precision == 2:
            formater = '0.00'
        elif precision == 3:
            formater = '0.000'
        elif precision == 4:
            formater = '0.0000'
        elif precision == 5:
            formater = '0.00000'
        else:
            logger.error(f"Max precision is 5!")
        if isinstance(string,str):
            result = Decimal(string).quantize(Decimal(formater),rounding=ROUND_HALF_UP)
            return str(result)
        else:
            logger.error(f"Only support string type!")

    def splitInteger(self,num):
        if isinstance(num,int):
            x=random.randint(1,num-1)
            y=num-x
            return x,y
        else:
            raise NameError('The data type must be an integer!')


    def multListCombination(self,list_array):
        from itertools import product
        result_list = []
        for i in product(*list_array):
            result_list.append(i)
        return result_list

    def multListPytest(self,list_array):
        from itertools import product
        result_list = []
        ids_list = []
        for i in product(*list_array):
            result_list.append(i)
            p='Condition:'
            for j in i:
                p=p+"-"+j
            ids_list.append(p)

        logger.info(f"Prepare to execute {len(result_list)} cases in total!")
        return result_list,ids_list



    def listNoRepeat(self,list_:list):
        """
        :function:列表去重
        :param list_:
        :return:
        """
        list_ = sorted(set(list_), key=list_.index)
        return list_


if __name__ == "__main__":
    sample = DataUtil()
    print(sample.calculate_percentage(11, 100))

    print(sample.format_num(-3, 3))

    print(sample.get_random_float(-2.2322344, 5.33242432425, 5))

    print(sample.keepAnddel("3.45545556",precision=5))

    print(sample.splitInteger(7))

    x=['1','2']
    y=['A','N']

    print(sample.multListPytest([x,y]))
