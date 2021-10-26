# -*-coding=utf-8-*-

from utils.pubulic.DictUtil import DictUtils
from config.path_config import base_dir
from utils.compare.DrawPicture import picture
from config.path_config import picture_type,template_group_2

class GenerateCompareReport:
    def __init__(self, mapping_dict=None):
        """
        :function：定义字段和字段list之间的映射，如果没有传输mapping_dict默认传值为--
        :param mapping_dict:
        """
        self.mapping_dict = mapping_dict

    def __xchange(self, dict_param, key):
        """
        :function:取出key在一个映射关系中的子key，之后取出dict_param中的value值
        :param dict_param: 其中一个字典
        :param key: 多个字典公用的key
        :return:
        """
        if self.mapping_dict and isinstance(self.mapping_dict, dict):
            res = []
            if key in self.mapping_dict.keys():
                for i in self.mapping_dict[key]:
                    res.append(dict_param.get(i))
                try:
                    string = [str for str in res if str not in [None]][0]  # res=[None,value,None,None...] 此行主要是删除None，保留第一个value
                except IndexError:
                    string = '漏配主键:' + key
            else:
                string = dict_param[key]
        else:
            try:
                string = dict_param[key]
            except KeyError:
                string = f'未配置{key}的映射关系'
        return string

    def _generateCNHtml(self, *args, cn_map_dic=None, black_list=None, skipped_list=None):
        """
        :function: 处理字段，传入(dict1,dict2,dict3...)或者[dict1,dict2,dict3...],取第一个dict1作为预期值，也是对比的标准
        :param args: 索要对比的dict,(dict1,dict2,dict3...)或者[dict1,dict2,dict3...]
        :param cn_map_dic: 中英文字段映射dict
        :param black_list: 设置黑名单，黑名单内的公用key不再对比，skipped_list忽略的字段，不做对比操作
        :return:返回元组，供函数_generateHtml中的*args使用
        """
        tem_dict_list = []
        for i in range(len(*args)):  # 自动更具*args的长度来生成对应的空字典
            exec('dict' + str(i) + ' = ' + "{}")
            tem_dict_list.append(eval('dict' + str(i)))

        compareResult, field_cn = [], []
        fieldList, compareList, passinfo = DictUtils().multcompare(list(*args), black_list, skipped_list)

        for index, key in enumerate(fieldList):
            for iindex, _dict in enumerate(tem_dict_list):
                _dict[key] = self.__xchange(list(*args)[iindex], key)

            flag = "失败"
            if compareList[index] == "passed":
                flag = "通过"
            elif compareList[index] == "skipped":
                flag = "跳过"
            compareResult.append(flag)

        if not cn_map_dic:
            cn_map_dic = dict()

        for key in fieldList:
            temp = "未映射中文名称"
            if key in list(cn_map_dic.keys()):
                temp = cn_map_dic[key]
            field_cn.append(temp)

        pic = picture(
            wedgeLables=("passed","failed","skipped"),
            ngramPercent=(passinfo[1],passinfo[2],passinfo[3]),
            type=picture_type
        )
        pic = 'data:image/png;base64,' + pic

        return fieldList, field_cn, list(tem_dict_list[0].values()), list(tem_dict_list[1].values()), list(
        ), list(), compareResult, pic

    def _generateHtml(self, senerioName, *args
                      , message2='APPLICATION'):
        """

        :param senerioName: HTML文件的名称，和HTML中的标题
        :param args: _generateCNHtml的返回值
        :param message1: 消息列的名称，如TBS-DP-0039
        :param message2:
        :param message3:
        :param message4:
        :return: HTML文件，可浏览器打开
        """
        pic = list(*args)[-1]

        with open(template_group_2,"r",encoding="utf-8") as f:
            html = f.read()
        f.close()

        html = html % (senerioName, pic,message2)

        filedList = list(*args)[0]
        field_cn = list(*args)[1]
        compareResult = list(*args)[-2]

        for index,value in enumerate(filedList):
            flag = 'failed'
            if compareResult[index] == "通过":
                flag = 'passed'
            elif compareResult[index] == "跳过":
                flag = 'skipped'
            html += '''
            <tbody class="%s results-table-row">
                <tr>
                  <td class="col-time">%d</td>
                  <td class="col-time">%s</td>
                  <td class="col-time">%s</td>
                  <td class="col-name" style="color:orange;font-weight:bolder">%s</td>
                  <td>%s</td>
                  <td class="col-result result">%s</td>
                <tr>
                        ''' % (
                flag,index+1, filedList[index], field_cn[index], list(*args)[2][index], list(*args)[3][index],compareResult[index])

        html += '''</tbody></table></body></html> '''
        abs_path = '%s\%s.html' % (base_dir + r"\static\compare", senerioName)
        with open(abs_path, 'w', encoding="utf-8") as f:
            f.write(html)
        f.close()
        reletive_path = '%s\%s.html' % (r"\static\compare", senerioName)
        return reletive_path


if __name__ == "__main__":
    dict1 = {'calc_agnt': '交易双方', 'clrng_mthd': '双边自行清算', 'prc': '32.8718', 'vol': '120', 'prd': '6Y',
             'mrty_dt': '2026/09/18', 'vl_dt': '2020/09/18', 'frst_prd_efctv_dt': '2020/09/18', 'intrst_adj': '实际天数',
             'pymnt_dt_adj': '经调整的下一营业日', 'sprds': '0.00', 'fltng_leg_pymnt_prd': '季',
             'fltng_leg_frst_rglr_pymnt_dt': '2020/12/18', 'fltng_leg_rst_frqncy': '季',
             'fltng_leg_frst_dtrmn_dt': '2020/09/18', 'fltng_leg_intrst_mthd': '单利', 'fltng_leg_intrst_bss': '实际/360',
             'fxng_leg_pymnt_prd': '季', 'fxng_leg_frst_rglr_pymnt_dt': '2020/12/18', 'fxng_leg_intrst_bss': '实际/365',
             'ref_intrst_rate_nm': 'Shibor_3M', 'splmntry_term': '—', '_ngtt_qt_src_errmsg': '对话', '_qt_dir': '支付固定利率',
             'rivalTrdActCnShrtNm': '农业银行', 'selfTrdActCnShrtNm': '中信证券', 'tra_tl_cd': 'Shibor3M_6Y', 'clrngSt': '无',
             'cpTrdrNm': '杨穆彬', 'exrcsCd': '—', 'realTmUndtkF': '否'}

    dict2 = {'qt_cd': '200917060201000005', 'selfInstant': '中信证券', 'selfTrdActCnShrtNm': '中信证券', 'selfTrdr': '张惠梓',
             'dir': '支付固定利率', 'rivalInstant': '农业银行', 'rivalTrdActCnShrtNm': '农业银行', 'rivalTrdr': '杨穆彬', 'qt_st': '成交',
             'tra_tl_cd': 'Shibor3M_6Y', 'ref_intrst_rate_nm': 'Shibor_3M', 'fixIntrstRate': '32.8718', 'vol': '120',
             'prd': '6Y', 'vl_dt': '2020-09-18', 'mrty_dt': '2026-09-18', 'frst_prd_efctv_dt': '2020-09-18',
             'intrst_adj': '实际天数', 'pymnt_dt_adj': '经调整的下一营业日', 'clrng_mthd': '双边自行清算', 'calc_agn': '交易双方',
             'sprds': '0.00', 'fltng_leg_rst_frqncy': '季', 'fltng_leg_pymnt_prd': '季',
             'fltng_leg_frst_dtrmn_dt': '2020-09-18', 'fltng_leg_intrst_mthd': '单利', 'fltng_leg_intrst_bss': '实际/360',
             'fltng_leg_frst_rglr_pymnt_dt': '2020-12-18', 'fxng_leg_pymnt_prd': '季', 'fxng_leg_intrst_bss': '实际/365',
             'splmntry_term': ''}
    # from data.字段映射.CN_ENmapping import ndm_irs_en_cn_mapping
    # from src.Utils.Compare.MappingConfig import mapping_dict
    # sample = GenerateCompareReport(mapping_dict)

    sample = GenerateCompareReport(None)
    dict_tuple = [dict1, dict2]
    field_result = sample._generateCNHtml(dict_tuple, black_list=None,skipped_list=["fltng_leg_frst_dtrmn_dt","mrty_dt"])
    #field_result = sample._generateCNHtml(dict_tuple, cn_map_dic=None, black_list=None, skipped_list=None)
    html = sample._generateHtml("2条信息对比", field_result)
