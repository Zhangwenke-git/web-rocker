# _*_ coding=utf-8 _*_

import re


class StringUtil(object):

    @staticmethod
    def left(source, length):
        return StringUtil.sub_string(source, 0, length)

    @staticmethod
    def right(source, length):
        return StringUtil.sub_string(source, length, len(source))

    @staticmethod
    def sub_string(source, start_index, end_index):
        if not source or len(source) == 0:
            return ''
        return source[start_index:end_index]

    @staticmethod
    def remove_spechart(string):
        """remove the leading unicode designator from a string"""
        result = ''
        if string.startswith("u'"):
            result = string.replace("u'", "'", 1)
        elif string.startswith('u"'):
            result = string.replace('u"', '"', 1)
        return result

    def correctJson(self, string: str) -> object:
        string_json = eval(string, type('js', (dict,), dict(__getitem__=lambda string, n: n))())
        return string_json

    def dealJson(self, string: str):
        """
        :function：将一级且key没有双信号的字符串转换为字典
        :param string: '{name:"Zhangwenke",age:12}'
        :return:
        """
        return re.sub(r'(?<={|,)(\w+?)(?=:)', r'"\1"', string)


    def translatePic(self,pic_path):
        """
        :function:将图片转换为二进制格式，并可以在HTML中展示
        :param pic_path: 图片路径
        :return:
        """
        import base64
        f=open(pic_path,'rb')
        pic_f = base64.b64encode(f.read())
        f.close()
        return pic_f

if __name__ == "__main__":
    sample = StringUtil()
    s = '{srvcId:4091001,sndrCmpntId:"101891",sndrSubId:"czb23",tgtCmpntId:"111",tgtSubId:"11",msgSrcEnd:0,msgSndngTm:"ss",msgUuid:"acd1b10b-f670-116a-b5e5-7218a54bbf60",dplcF:12,sesnId:"4a6ac94181b8f714b4a904f370ea7cdd4f7971dec2f92e0ef8c49e271b24a77a",tpcNm:"ee",tstMdF:22,lang:"yy",erCd:"55",erMsg:"rg",},ordrData,{,clntQtCd:"",stlmntSpdNm:"2",instnCd:"101891",trdAcntCnShrtNm:"\346\265\231\345\225\206\351\223\266\350\241\214",prdctCd:"CBT",qtTp:"5",netPrc:1280000,nmnlVol:110000000,ordrTpIndctr:"1",trdAcntSrNo:1375,srNoId:328,trdrCd:"czb23",dir:"B",traTlCd:"170011",bndsNm:"17\351\231\204\346\201\257\345\233\275\345\200\27211",dlrSqncNoId:249,stlmntDt:"2020/07/14",trdngAcntCd:"101891",userRefInfo,{,key:"1",vl:"2",},clrngMthd:"2",instnSrno:55,ordrCd:"",flxblSpd:"",dtCnfrm:"2020-07-13",isrCd:"",qtSrc:"0",alctnIndctr:"0",},cbtOrdrData,{,acrdIntrst:"0.58761",bondTpNm:"\345\233\275\345\200\272",exrcsYld:"",flxblExrcsYld:"",flxblYldToMrty:"",yldToMrty:"2.9694",prmrktBondF:"0",ttm:"46.86Y"}'

    #print(sample.remove_spechart("\u2344"))
    #print(sample.dealJson(s))
    #print(sample.correctJson(s))

    collapse = sample.translatePic("collapse.png")
    expand = sample.translatePic("expand.png")

    print(collapse)
    print(expand)

    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAGUExURSZ0pv///xB+eSAAAAARSURBVAjXY2DABuR/gBA2AAAzpwIvNQARCgAAAABJRU5ErkJggg=="
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAGUExURSZ0pv///xB+eSAAAAAWSURBVAjXY2CAAcYGBJL/AULIIjAAAJJrBjcL30J5AAAAAElFTkSuQmCC"
