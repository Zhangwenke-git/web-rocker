from utils.pubulic.logger import Logger

logger = Logger("Assertion")


class Assertion(object):
    def _assertList(self, alist):
        flag = True
        if isinstance(alist, list):
            if len(alist) != 0:
                for item_index, item_value in enumerate(alist):
                    if item_value == "失败":
                        flag = False
                        logger.debug(f"Fail to get expected result in position {item_index + 1}")
                        break
        return flag

    def _assertBoolList(self, slist):
        re_flag = True
        if isinstance(slist, list):
            if len(slist) != 0:
                for item_index, item_value in enumerate(slist):
                    if not item_value:
                        re_flag = False
                        logger.debug(f"Fail to get expected result in position {item_index + 1}")
                        break
            else:
                logger.error(f'There is no data in {slist}!')
                re_flag = False
        return re_flag


    def _aseertPFS(self,slist):
        re_flag = True
        if isinstance(slist, list):
            if len(slist) != 0:
                for item_index, item_value in enumerate(slist):
                    if item_value=="failed":
                        re_flag = "failed"
                        logger.debug(f"Fail to get expected result in position {item_index + 1}")
                        break
                    if item_value=="skipped":
                        re_flag = "skipped"
                        logger.debug(f"Skip to get expected result in position {item_index + 1}")
                        break
                    else:
                        re_flag = "passed"

            else:
                logger.error(f'There is no data in {slist}!')
                re_flag = False
        return re_flag


if __name__ == "__main__":
    test_list = [True,False,True]
    #test_list = []
    sample = Assertion()
    print(sample._assertBoolList(test_list))
