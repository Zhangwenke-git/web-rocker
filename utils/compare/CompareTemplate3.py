from src.Utils.Public.DictUtil import DictUtils
from config.path_config import attachment_html
from src.Utils.Compare.CN_fields_map import projectFieldMapDict
from src.Utils.Compare.MappingConfig import mapping_dict

class GenerateCompareReport:
    def __init__(self, mapping_dict=None):
        """
        :function：定义字段和字段list之间的映射，如果没有传输mapping_dict默认传值为--
        :param mapping_dict:
        """
        self.mapping_dict = mapping_dict

    def __xchange(self, dict_param, key):
        """
        :function:取出key在一个映射关系中的key_copy，之后取出dict_param中的value值
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
                    if string == "":
                        string = "--"
                except IndexError:
                    string = '漏配主键'
            else:
                string = dict_param[key]
        else:
            try:
                string = dict_param[key]
            except KeyError:
                string = f'未配置{key}的映射关系'
        return string

    def _generateCNHtml(self, *args, cn_map_dic=None, black_list=None):
        """
        :function: 处理字段，传入(dict1,dict2,dict3...)或者[dict1,dict2,dict3...],取第一个dict1作为预期值，也是对比的标准
        :param args: 索要对比的dict,(dict1,dict2,dict3...)或者[dict1,dict2,dict3...]
        :param cn_map_dic: 中英文字段映射dict
        :param black_list: 设置黑名单，黑名单内的公用key不再对比
        :return:返回元组，供函数_generateHtml中的*args使用
        """
        Dict_list = []
        for i in range(len(*args)):  # 自动更具*args的长度来生成对应的空字典
            exec('Dict' + str(i) + ' = ' + "{}")
            Dict_list.append(eval('Dict' + str(i)))

        compareResult, field_cn = [], []
        fieldList, compareList,passinfo = DictUtils().multcompare(list(*args),black_list)

        for index, key in enumerate(fieldList):
            for iindex, Dict in enumerate(Dict_list):
                Dict[key] = self.__xchange(list(*args)[iindex], key)

            flag = "失败"
            if compareList[index]:
                flag = "通过"
            compareResult.append(flag)

        if not cn_map_dic:
            cn_map_dic = dict()
        for key in fieldList:
            temp = "未映射中文名称"
            if key in list(cn_map_dic.keys()):
                temp = cn_map_dic[key]
            field_cn.append(temp)

        return fieldList, field_cn, list(Dict_list[0].values()), list(Dict_list[1].values()), list(
            Dict_list[2].values()), list(), compareResult,passinfo

    def _generateHtml(self, senerioName, *args,url='未配置',
                      message2='TBS-DP-0039', message3='ODM-DP-0039'):
        """

        :param senerioName: HTML文件的名称，和HTML中的标题
        :param args: _generateCNHtml的返回值
        :param message1: 消息列的名称，如TBS-DP-0039
        :param message2:
        :param message3:
        :param message4:
        :return: HTML文件，可浏览器打开
        """
        passinfo = list(*args)[-1]
        html = '''
        <!DOCTYPE html>
            <html>
              <head>
                <meta charset="utf-8"/>
                <title>中国外汇交易中心</title>

                <link href="../tools/bootstrap-3.3.7-dist/css/bootstrap.min.css" rel="stylesheet">


                <style>body {
                font-family: Helvetica, Arial, sans-serif;
                font-size: 12px;
                /* do not increase min-width as some may use split screens */
                min-width: 800px;
                color: #999;
            }

            h1 {
                font-size: 24px;
                color: black;
            }

            h2 {
                font-size: 16px;
                color: black;
            }

            p {
                color: black;
            }

            a {
                color: #999;
            }

            table {
                border-collapse: collapse;
            }

            /******************************
             * SUMMARY INFORMATION
             ******************************/

            #environment td {
                padding: 5px;
                border: 1px solid #E6E6E6;
            }

            #environment tr:nth-child(odd) {
                background-color: #f6f6f6;
            }

            /******************************
             * TEST RESULT COLORS
             ******************************/
            span.passed, .passed .col-result {

                color: green;
                border-radius: 12px;
                padding: 3px 14px;
                cursor: pointer;
                border: 1px solid green;

            }
            span.skipped, span.xfailed, span.rerun, .skipped .col-result, .xfailed .col-result, .rerun .col-result {
                color: orange;
                border-radius: 12px;
                padding: 3px 14px;
                cursor: pointer;
                border: 1px solid orange;
            }
            span.error, span.failed, span.xpassed, .error .col-result, .failed .col-result, .xpassed .col-result  {
                color: red;
                border-radius: 12px;
                padding: 3px 14px;
                cursor: pointer;
                border: 1px solid red;
            }


            /******************************
             * RESULTS TABLE
             *
             * 1. Table Layout
             * 2. Extra
             * 3. Sorting items
             *
             ******************************/

            /*------------------
             * 1. Table Layout
             *------------------*/

            #results-table {
                border: 1px solid #e6e6e6;
                color: #999;
                font-size: 12px;
                width: 100%%ds
            }

            #results-table th, #results-table td {
                padding: 5px;
                border: 1px solid #E6E6E6;
                text-align: left
            }
            #results-table th {
                font-weight: bold
            }

            /*------------------
             * 2. Extra
             *------------------*/

            .log:only-child {
                height: inherit
            }
            .log {
                background-color: #e6e6e6;
                border: 1px solid #e6e6e6;
                color: black;
                display: block;
                font-family: "Courier New", Courier, monospace;
                height: 230px;
                overflow-y: scroll;
                padding: 5px;
                white-space: pre-wrap
            }
            div.image {
                border: 1px solid #e6e6e6;
                float: right;
                height: 240px;
                margin-left: 5px;
                overflow: hidden;
                width: 320px
            }
            div.image img {
                width: 320px
            }
            .collapsed {
                display: none;
            }
            .expander::after {
                content: " (show)";
                color: #BBB;
                font-style: italic;
                cursor: pointer;
            }
            .collapser::after {
                content: " (hide)";
                color: #BBB;
                font-style: italic;
                cursor: pointer;
            }

            /*------------------
             * 3. Sorting items
             *------------------*/
            .sortable {
                cursor: pointer;
            }

            .sort-icon {
                font-size: 0px;
                float: left;
                margin-right: 5px;
                margin-top: 5px;
                /*triangle*/
                width: 0;
                height: 0;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
            }

            .inactive .sort-icon {
                /*finish triangle*/
                border-top: 8px solid #E6E6E6;
            }

            .asc.active .sort-icon {
                /*finish triangle*/
                border-bottom: 8px solid #999;
            }

            .desc.active .sort-icon {
                /*finish triangle*/
                border-top: 8px solid #999;
            }
            </style></head>
              <body onLoad="init()">
                <script>/* This Source Code Form is subject to the terms of the Mozilla General
             * License, v. 2.0. If a copy of the MPL was not distributed with this file,
             * You can obtain one at http://mozilla.org/MPL/2.0/. */


            function toArray(iter) {
                if (iter === null) {
                    return null;
                }
                return Array.prototype.slice.call(iter);
            }

            function find(selector, elem) {
                if (!elem) {
                    elem = document;
                }
                return elem.querySelector(selector);
            }

            function find_all(selector, elem) {
                if (!elem) {
                    elem = document;
                }
                return toArray(elem.querySelectorAll(selector));
            }

            function sort_column(elem) {
                toggle_sort_states(elem);
                var colIndex = toArray(elem.parentNode.childNodes).indexOf(elem);
                var key;
                if (elem.classList.contains('numeric')) {
                    key = key_num;
                } else if (elem.classList.contains('result')) {
                    key = key_result;
                } else {
                    key = key_alpha;
                }
                sort_table(elem, key(colIndex));
            }

            function show_all_extras() {
                find_all('.col-result').forEach(show_extras);
            }

            function hide_all_extras() {
                find_all('.col-result').forEach(hide_extras);
            }

            function show_extras(colresult_elem) {
                var extras = colresult_elem.parentNode.nextElementSibling;
                var expandcollapse = colresult_elem.firstElementChild;
                extras.classList.remove("collapsed");
                expandcollapse.classList.remove("expander");
                expandcollapse.classList.add("collapser");
            }

            function hide_extras(colresult_elem) {
                var extras = colresult_elem.parentNode.nextElementSibling;
                var expandcollapse = colresult_elem.firstElementChild;
                extras.classList.add("collapsed");
                expandcollapse.classList.remove("collapser");
                expandcollapse.classList.add("expander");
            }

            function show_filters() {
                var filter_items = document.getElementsByClassName('filter');
                for (var i = 0; i < filter_items.length; i++)
                    filter_items[i].hidden = false;
            }

            function add_collapse() {
                // Add links for show/hide all
                var resulttable = find('table#results-table');
                var showhideall = document.createElement("p");
                showhideall.innerHTML = '<a href="javascript:show_all_extras()">unfold</a> / ' +
                                        '<a href="javascript:hide_all_extras()">collapse</a>';
                resulttable.parentElement.insertBefore(showhideall, resulttable);

                // Add show/hide link to each result
                find_all('.col-result').forEach(function(elem) {
                    var collapsed = get_query_parameter('collapsed') || 'Passed';
                    var extras = elem.parentNode.nextElementSibling;
                    var expandcollapse = document.createElement("span");
                    if (collapsed.includes(elem.innerHTML)) {
                        extras.classList.add("collapsed");
                        expandcollapse.classList.add("expander");
                    } else {
                        expandcollapse.classList.add("collapser");
                    }
                    elem.appendChild(expandcollapse);

                    elem.addEventListener("click", function(event) {
                        if (event.currentTarget.parentNode.nextElementSibling.classList.contains("collapsed")) {
                            show_extras(event.currentTarget);
                        } else {
                            hide_extras(event.currentTarget);
                        }
                    });
                })
            }

            function get_query_parameter(name) {
                var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
                return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
            }

            function init () {
                reset_sort_headers();

                add_collapse();

                show_filters();

                sort_column(find('.initial-sort'));

                find_all('.sortable').forEach(function(elem) {
                    elem.addEventListener("click",
                                          function(event) {
                                              sort_column(elem);
                                          }, false)
                });

            };

            function sort_table(clicked, key_func) {
                var rows = find_all('.results-table-row');
                var reversed = !clicked.classList.contains('asc');
                var sorted_rows = sort(rows, key_func, reversed);
                /* Whole table is removed here because browsers acts much slower
                 * when appending existing elements.
                 */
                var thead = document.getElementById("results-table-head");
                document.getElementById('results-table').remove();
                var parent = document.createElement("table");
                parent.id = "results-table";
                parent.appendChild(thead);
                sorted_rows.forEach(function(elem) {
                    parent.appendChild(elem);
                });
                document.getElementsByTagName("BODY")[0].appendChild(parent);
            }

            function sort(items, key_func, reversed) {
                var sort_array = items.map(function(item, i) {
                    return [key_func(item), i];
                });

                sort_array.sort(function(a, b) {
                    var key_a = a[0];
                    var key_b = b[0];

                    if (key_a == key_b) return 0;

                    if (reversed) {
                        return (key_a < key_b ? 1 : -1);
                    } else {
                        return (key_a > key_b ? 1 : -1);
                    }
                });

                return sort_array.map(function(item) {
                    var index = item[1];
                    return items[index];
                });
            }

            function key_alpha(col_index) {
                return function(elem) {
                    return elem.childNodes[1].childNodes[col_index].firstChild.data.toLowerCase();
                };
            }

            function key_num(col_index) {
                return function(elem) {
                    return parseFloat(elem.childNodes[1].childNodes[col_index].firstChild.data);
                };
            }

            function key_result(col_index) {
                return function(elem) {
                    var strings = ['Error', 'Failed', 'Rerun', 'XFailed', 'XPassed',
                                   'Skipped', 'Passed'];
                    return strings.indexOf(elem.childNodes[1].childNodes[col_index].firstChild.data);
                };
            }

            function reset_sort_headers() {
                find_all('.sort-icon').forEach(function(elem) {
                    elem.parentNode.removeChild(elem);
                });
                find_all('.sortable').forEach(function(elem) {
                    var icon = document.createElement("div");
                    icon.className = "sort-icon";
                    icon.textContent = "vvv";
                    elem.insertBefore(icon, elem.firstChild);
                    elem.classList.remove("desc", "active");
                    elem.classList.add("asc", "inactive");
                });
            }

            function toggle_sort_states(elem) {
                //if active, toggle between asc and desc
                if (elem.classList.contains('active')) {
                    elem.classList.toggle('asc');
                    elem.classList.toggle('desc');
                }

                //if inactive, reset all other functions and add ascending active
                if (elem.classList.contains('inactive')) {
                    reset_sort_headers();
                    elem.classList.remove('inactive');
                    elem.classList.add('active');
                }
            }

            function is_all_rows_hidden(value) {
              return value.hidden == false;
            }

            function filter_table(elem) {
                var outcome_att = "data-test-result";
                var outcome = elem.getAttribute(outcome_att);
                class_outcome = outcome + " results-table-row";
                var outcome_rows = document.getElementsByClassName(class_outcome);

                for(var i = 0; i < outcome_rows.length; i++){
                    outcome_rows[i].hidden = !elem.checked;
                }

                var rows = find_all('.results-table-row').filter(is_all_rows_hidden);
                var all_rows_hidden = rows.length == 0 ? true : false;
                var not_found_message = document.getElementById("not-found-message");
                not_found_message.hidden = !all_rows_hidden;
            }
            </script>

                <h1>%s</h1>

                <h2>Environment</h2>
                <table id="environment">

                  <tr>
                    <td>所属部门</td>
                    <td>新本币测试部</td>
                  </tr>

                  <tr>
                    <td>项目名称</td>
                    <td>新本币项目</td>
                  </tr>

                  <tr>
                    <td>服务器地址</td>
                    <td>58.246.35.21</td>
                  </tr>
                  <tr>
                    <td>接口地址</td>
                    <td><a href="%s" target="_blank">%s</a></td>
                  </tr>
                </table>


                <h2 class="filter" hidden="true">Filter</h2>
                <input checked="true" class="filter" data-test-result="passed" hidden="true" name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/><span class="passed">通过</span>
                <input checked="true" class="filter" data-test-result="failed" hidden="true" name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/><span class="failed">失败</span> 
                
                <h2>Result</h2>
                <h3>
                    <b><span style="color: orange">%s </span> fields in totle,failed<span style="color: red"> %s</span>, pass rate: </b>
                    <span style="width:auto;display:inline;color:green">%s</span>
                </h3>
                <table id="results-table" class="table table-striped">
                  <thead id="results-table-head">
                    <tr style='background-color :Teal'>
                      <th class="sortable time initial-sort" col="time">字段英文名称</th>
                      <th class="sortable time" col="time">字段中文名称</th>

                      <th>预期结果</th>
                      <th>%s</th>
                      <th>%s</th>
                      <th class="sortable time" col="time">对比结果</th>

                    <tr hidden="true" id="not-found-message">
                      <th colspan="8">No results found. Try to check the filters</th></tr></thead>


               ''' % (senerioName, url,url,passinfo[0],passinfo[1],passinfo[2],message2, message3)
        filedList = list(*args)[0]
        field_cn = list(*args)[1]
        compareResult = list(*args)[-2]

        for i in range(len(filedList)):
            color = 'MediumVioletRed'
            flag = 'failed'
            if compareResult[i] == "通过":
                flag = 'passed'
                color = 'SeaGreen'
            html += '''
                        <tbody class="%s results-table-row">
            <tr>
              <td class="col-time">%s</td>
              <td class="col-time">%s</td>
              <td class="col-name" style="color:orange; font-weight:bolder">%s</td>
              <td class="col-name">%s</td>
              <td>%s</td>
              <td class="col-time" style='background-color: %s'>%s</td>
            <tr>
                        ''' % (
                flag, filedList[i], field_cn[i], list(*args)[2][i], list(*args)[3][i], list(*args)[4][i],
                color,
                compareResult[i])

        html += '''
                    </tbody></table></body></html>
                '''

        with open('%s/%s.html' % (attachment_html, senerioName), 'w', encoding="utf-8") as f:
            f.write(html)
        f.close()
        return html


if __name__ == "__main__":
    dict1 = {'clntQtCd': '', 'stlmntSpdNm': '2', 'cntngncyIndctr': None, 'flxblNetPrc': None, 'trdAcntCnShrtNm': '中信证券', 'qtTp': '5', 'netPrc': 1050000, 'instnCd': '100035', 'nmnlVol': 100000000, 'ordrTpIndctr': '1', 'trdrCd': '6274', 'dir': 'B', 'traTlCd': '180210', 'bndsNm': '18国开10', 'userRefInfo': {'key': '1', 'vl': '2'}, 'prdctCd': 'CBT', 'stlmntDt': '2020/07/20', 'clrngMthd': '2', 'isrCd': '100034', 'qtSrc': '0', 'trdngAcntCd': '100035', 'srNoId': 338, 'trdAcntSrNo': 2839, 'dlrSqncNoId': 2955, 'instnSrno': 576, 'ordrCd': '200717050100000006', 'flxblSpd': '', 'dtCnfrm': '2020-07-17', 'alctnIndctr': '0', 'yldToMrty': '3.3294', 'exrcsYld': '', 'bondTpNm': '政策性金融债', 'ttm': '7.97Y', 'flxblExrcsYld': '', 'flxblYldToMrty': '', 'acrdIntrst': '3.36667', 'prmrktBondF': '0'}

    dict2 = {'institutionEnglishFullName': '', 'institutionEnglishShortName': '', 'traderCode': '', 'tradingAccountCode': '100035', 'tradeAccountCfetsCode': '', 'tradeAccountChineseFullName': '中信证券股份有限公司', 'tradeAccountChineseShortName': '', 'tradeAccountEnglishFullName': '', 'tradeAccountEnglishShortName': '', 'direction': 'B', 'netPrice': '105.0000', 'yieldToMaturity': '3.3294', 'exerciseYield': '', 'flexibleSpread': '', 'flexibleNetPrice': '', 'flexibleYieldToMaturity': '', 'flexibleExerciseYield': '', 'nominalVolume': '100000000', 'settlementSpeedName': '2', 'clearingMethod': '2', 'settlementMethodName': '1', 'settlementDate': '2020-07-20 00:00:00.000', 'accruedInterest': '3.36667', 'allPrice': '108.3667', 'totalAccruedInterest': '3366666.67', 'dealtCurrency': '', 'amount': '105000000.00', 'settlementCurrency': '', 'settlementAmount': '108366666.67', 'orderCode': '200717050100000006', 'dateConfirmed': '', 'businessDate': '2020-07-17 00:00:00.000', 'businessTime': '2020-07-17 14:15:07.426', 'orderTypeName': '限价订单', 'productCode': 'CBT', 'orderStatus': '0', 'splitIndicator': '1', 'bondCode': '180210', 'bondsName': '18国开10', 'bondCurrency': '', 'exchangeRate': '', 'termToMaturityYearly': '', 'orderValidTimeType': '0', 'tradingModeCode': '', 'tradingMethodCode': '', 'quoteMode': '', 'quoteType': '5', 'marketScope': '1', 'channelType': '4', 'channel': '', 'institutionCode': '100035', 'cfetsInstitutionCode': '', 'institutionChineseFullName': '中信证券股份有限公司', 'institutionChineseShortName': ''}

    dict3 = {'ordrCd': '200717050100000006', 'dtCnfrm': '2020-07-17 00:00:00', 'prdctCd': 'CBT', 'trdngMdCd': 'ODM', 'trdngMthdCd': 'Matching', 'qtTp': '5', 'ordrSt': '0', 'srNoId': '229763', 'traTlCd': '180210', 'bndsNm': '18国开10', 'bondCcy': 'CNY', 'instnCd': '100035', 'cfetsInstnCd': '101010111000000205011', 'instnCnShrtNm': '中信证券', 'trdrCd': '6274', 'trdngAcntCd': '100035', 'trdAcntCfetsCd': '101010111000000205011', 'trdAcntCnShrtNm': '中信证券', 'dir': 'B', 'netPrc': '105.0', 'yldToMrty': '3.329370234', 'exrcsYld': '', 'flxblSpd': '', 'flxblNetPrc': '', 'flxblYldToMrty': '', 'flxblExrcsYld': '', 'nmnlVol': '100000000.0', 'stlmntSpdNm': '2', 'clrngMthd': '2', 'stlmntMthdNm': '1', 'stlmntDt': '2020-07-20 00:00:00', 'acrdIntrst': '3.3666666667', 'allPrc': '108.3666666667', 'totlAcrdIntrst': '3366666.66666667', 'amnt': '105000000.0', 'stlmntCcy': '', 'stlmntAmnt': '108366666.666667', 'mktScp': '1', 'chnlTp': '4', 'chnl': '', 'ttmYrly': '7.97Y', 'qtSrc': '0', 'ocoOrdrCd': '', 'ifdoneOrdrCd': '', 'bondTpId': '100003', 'bondTpNm': '政策性金融债', 'trdrNm': '高远', 'rmngTotlAmnt': '100000000.0', 'dlAmnt': '', 'ttm': '7.97Y', 'oprtnTp': 'N', 'isrCd': '100034', 'prmrktBondF': '0', 'alctnIndctr': '0'}

    sample = GenerateCompareReport(mapping_dict)

    dict_tuple = (dict1, dict2, dict3)

    field_result = sample._generateCNHtml(dict_tuple, cn_map_dic=projectFieldMapDict, black_list=None)

    html = sample._generateHtml("3条信息对比", field_result)
