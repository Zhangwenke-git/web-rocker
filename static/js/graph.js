$(document).ready(function(){

$.ajax({
    type: "GET",
    dataType: "json",
    url: "/api/analytics/current_day_graph_ajax/",
    contentType: 'application/json',
    success: function (res) {
        if (res.success){
            Highcharts.chart('chart1', {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },
                title: {
                    text: res.result.title
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                            style: {
                                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                            }
                        }
                    }
                },
                series: [{
                    name: 'Brands',
                    colorByPoint: true,
                    data:res.result.series
                }]
            });
        }else{
            var error = '错误码：'+res.code+'，'+'原因：'+res.message;

            swal({
                text:error,
                type:'error'
            });
        }

    },
    error: function (jqXHR,textStatus,errorThrown) {
        var error = '错误码：'+textStatus+'，'+'原因：'+errorThrown;
        swal({
            text:error,
            type:'error'
        });
    }
});

$.ajax({
    type: "GET",
    dataType: "json",
    url: "/api/analytics/current_month_graph_ajax/",
    contentType: 'application/json',
    success: function (res) {
        if (res.success){
            Highcharts.chart('chart2', {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },
                title: {
                    text: res.result.title
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                            style: {
                                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                            }
                        }
                    }
                },
                series: [{
                    name: 'Brands',
                    colorByPoint: true,
                    data:res.result.series
                }]
            });
        }else{
            var error = '错误码：'+res.code+'，'+'原因：'+res.message;

            swal({
                text:error,
                type:'error'
            });
        }

    },
    error: function (jqXHR,textStatus,errorThrown) {
        var error = '错误码：'+textStatus+'，'+'原因：'+errorThrown;
        swal({
            text:error,
            type:'error'
        });
    }
});


$.ajax({
    type: "GET",
    dataType: "json",
    url: "/api/analytics/project_graph_ajax/",
    contentType: 'application/json',
    success: function (res) {
        if (res.success){
            var chart = Highcharts.chart('container1', {
                    title: {
                            text: res.result.title
                    },
                    subtitle: {
                            text: res.result.subtitle
                    },
                    yAxis: {
                            title: {
                                    text: res.result.yAxis
                            }
                    },
                    legend: {
                            layout: 'vertical',
                            align: 'right',
                            verticalAlign: 'middle'
                    },
                    xAxis: {
                        categories:res.result.xAxis
                    },
                    plotOptions: {
                        line: {
                            dataLabels: {
                                // 开启数据标签
                                enabled: true
                            },
                            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
                            enableMouseTracking: false
                        }
                    },

                    series: res.result.series,
                    responsive: {
                            rules: [{
                                    condition: {
                                            maxWidth: 500
                                    },
                                    chartOptions: {
                                            legend: {
                                                    layout: 'horizontal',
                                                    align: 'center',
                                                    verticalAlign: 'bottom'
                                            }
                                    }
                            }]
                    }
            });





        }else{
            var error = '错误码：'+res.code+'，'+'原因：'+res.message;

            swal({
                text:error,
                type:'error'
            });
        }

    },
    error: function (jqXHR,textStatus,errorThrown) {
        var error = '错误码：'+textStatus+'，'+'原因：'+errorThrown;
        swal({
            text:error,
            type:'error'
        });
    }
});

$.ajax({
    type: "GET",
    dataType: "json",
    url: "/api/analytics/through_graph_ajax/",
    contentType: 'application/json',
    success: function (res) {
        if (res.success){
            var chart = Highcharts.chart('container2',{
            chart: {
                type: 'column'
            },
            title: {
                text: res.result.title
            },
            subtitle: {
                text: res.result.subtitle
            },
            xAxis: {
                categories: res.result.xAxis,
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: '执行量 (条)'
                }
            },
            tooltip: {
                // head + 每个 point + footer 拼接成完整的 table
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} 条</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    borderWidth: 0
                }
            },
            series: res.result.series
        });

        }else{
            var error = '错误码：'+res.code+'，'+'原因：'+res.message;

            swal({
                text:error,
                type:'error'
            });
        }

    },
    error: function (jqXHR,textStatus,errorThrown) {
        var error = '错误码：'+textStatus+'，'+'原因：'+errorThrown;
        swal({
            text:error,
            type:'error'
        });
    }
});

$.ajax({
  type: 'GET',
  dataType: 'json',
  url: '/api/analytics/case_info_graph_ajax/',
  contentType: 'application/json',
  success: function (res) {
    if (res.success) {
      var chart = Highcharts.chart('container3', {
        chart: {
          type: 'bar'
        },
        title: {
          text: res.result.xAxis.title
        },
        subtitle: {
          text: res.result.xAxis.subtitle
        },
        xAxis: {
          categories: res.result.xAxis,
          title: {
            text: null
          }
        },
        yAxis: {
          min: 0,
          title: {
            text: '总量 (条)',
            align: 'high'
          },
          labels: {
            overflow: 'justify'
          }
        },
        tooltip: {
          valueSuffix: ' 条'
        },
        plotOptions: {
          bar: {
            dataLabels: {
              enabled: true,
              allowOverlap: true // 允许数据标签重叠
            }
          }
        },
        legend: {
          layout: 'vertical',
          align: 'right',
          verticalAlign: 'top',
          x: -40,
          y: 100,
          floating: true,
          borderWidth: 1,
          backgroundColor:
            (Highcharts.theme && Highcharts.theme.legendBackgroundColor) ||
            '#FFFFFF',
          shadow: true
        },
        series: res.result.series
      });
    } else {
      var error = '错误码：' + res.code + '，' + '原因：' + res.message;

      swal({
        text: error,
        type: 'error'
      });
    }
  },
  error: function (jqXHR, textStatus, errorThrown) {
    var error = '错误码：' + textStatus + '，' + '原因：' + errorThrown;
    swal({
      text: error,
      type: 'error'
    });
  }
});


$.ajax({
  type: 'GET',
  dataType: 'json',
  url: '/api/analytics/case_info_graph_ajax/',
  contentType: 'application/json',
  success: function (res) {
    if (res.success) {
      Highcharts.chart('container4', {
        chart: {
            type: 'packedbubble',
            height: '100%'
        },
        title: {
            text: '2014 年世界各地碳排放量'
        },
        tooltip: {
            useHTML: true,
            pointFormat: '<b>{point.name}:</b> {point.y}m CO<sub>2</sub>'
        },
        plotOptions: {
            packedbubble: {
                minSize: '30%',
                maxSize: '120%',
                zMin: 0,
                zMax: 1000,
                layoutAlgorithm: {
                    gravitationalConstant: 0.05,
                    splitSeries: true,
                    seriesInteraction: false,
                    dragBetweenSeries: true,
                    parentNodeLimit: true
                },
                dataLabels: {
                    enabled: true,
                    format: '{point.name}',
                    filter: {
                        property: 'y',
                        operator: '>',
                        value: 250
                    },
                    style: {
                        color: 'black',
                        textOutline: 'none',
                        fontWeight: 'normal'
                    }
                }
            }
        },
        series: [{
            name: '欧洲',
            data: [{
                name: 'Germany',
                value: 767.1
            }, {
                name: 'Croatia',
                value: 20.7
            },
            {
                name: "Belgium",
                value: 97.2
            },
            {
                name: "Czech Republic",
                value: 111.7
            },
            {
                name: "Netherlands",
                value: 158.1
            },
            {
                name: "Spain",
                value: 241.6
            },
            {
                name: "Ukraine",
                value: 249.1
            },
            {
                name: "Poland",
                value: 298.1
            },
            {
                name: "France",
                value: 323.7
            },
            {
                name: "Romania",
                value: 78.3
            },
            {
                name: "United Kingdom",
                value: 415.4
            }, {
                name: "Turkey",
                value: 353.2
            }, {
                name: "Italy",
                value: 337.6
            },
            {
                name: "Greece",
                value: 71.1
            },
            {
                name: "Austria",
                value: 69.8
            },
            {
                name: "Belarus",
                value: 67.7
            },
            {
                name: "Serbia",
                value: 59.3
            },
            {
                name: "Finland",
                value: 54.8
            },
            {
                name: "Bulgaria",
                value: 51.2
            },
            {
                name: "Portugal",
                value: 48.3
            },
            {
                name: "Norway",
                value: 44.4
            },
            {
                name: "Sweden",
                value: 44.3
            },
            {
                name: "Hungary",
                value: 43.7
            },
            {
                name: "Switzerland",
                value: 40.2
            },
            {
                name: "Denmark",
                value: 40
            },
            {
                name: "Slovakia",
                value: 34.7
            },
            {
                name: "Ireland",
                value: 34.6
            },
            {
                name: "Croatia",
                value: 20.7
            },
            {
                name: "Estonia",
                value: 19.4
            },
            {
                name: "Slovenia",
                value: 16.7
            },
            {
                name: "Lithuania",
                value: 12.3
            },
            {
                name: "Luxembourg",
                value: 10.4
            },
            {
                name: "Macedonia",
                value: 9.5
            },
            {
                name: "Moldova",
                value: 7.8
            },
            {
                name: "Latvia",
                value: 7.5
            },
            {
                name: "Cyprus",
                value: 7.2
            }]
        }, {
            name: '非洲',
            data: [{
                name: "Senegal",
                value: 8.2
            },
            {
                name: "Cameroon",
                value: 9.2
            },
            {
                name: "Zimbabwe",
                value: 13.1
            },
            {
                name: "Ghana",
                value: 14.1
            },
            {
                name: "Kenya",
                value: 14.1
            },
            {
                name: "Sudan",
                value: 17.3
            },
            {
                name: "Tunisia",
                value: 24.3
            },
            {
                name: "Angola",
                value: 25
            },
            {
                name: "Libya",
                value: 50.6
            },
            {
                name: "Ivory Coast",
                value: 7.3
            },
            {
                name: "Morocco",
                value: 60.7
            },
            {
                name: "Ethiopia",
                value: 8.9
            },
            {
                name: "United Republic of Tanzania",
                value: 9.1
            },
            {
                name: "Nigeria",
                value: 93.9
            },
            {
                name: "South Africa",
                value: 392.7
            }, {
                name: "Egypt",
                value: 225.1
            }, {
                name: "Algeria",
                value: 141.5
            }]
        }, {
            name: '大洋洲',
            data: [{
                name: "Australia",
                value: 409.4
            },
            {
                name: "New Zealand",
                value: 34.1
            },
            {
                name: "Papua New Guinea",
                value: 7.1
            }]
        }, {
            name: '北美洲',
            data: [{
                name: "Costa Rica",
                value: 7.6
            },
            {
                name: "Honduras",
                value: 8.4
            },
            {
                name: "Jamaica",
                value: 8.3
            },
            {
                name: "Panama",
                value: 10.2
            },
            {
                name: "Guatemala",
                value: 12
            },
            {
                name: "Dominican Republic",
                value: 23.4
            },
            {
                name: "Cuba",
                value: 30.2
            },
            {
                name: "USA",
                value: 5334.5
            }, {
                name: "Canada",
                value: 566
            }, {
                name: "Mexico",
                value: 456.3
            }]
        }, {
            name: '南美洲',
            data: [{
                name: "El Salvador",
                value: 7.2
            },
            {
                name: "Uruguay",
                value: 8.1
            },
            {
                name: "Bolivia",
                value: 17.8
            },
            {
                name: "Trinidad and Tobago",
                value: 34
            },
            {
                name: "Ecuador",
                value: 43
            },
            {
                name: "Chile",
                value: 78.6
            },
            {
                name: "Peru",
                value: 52
            },
            {
                name: "Colombia",
                value: 74.1
            },
            {
                name: "Brazil",
                value: 501.1
            }, {
                name: "Argentina",
                value: 199
            },
            {
                name: "Venezuela",
                value: 195.2
            }]
        }, {
            name: '亚洲',
            data: [{
                name: "Nepal",
                value: 6.5
            },
            {
                name: "Georgia",
                value: 6.5
            },
            {
                name: "Brunei Darussalam",
                value: 7.4
            },
            {
                name: "Kyrgyzstan",
                value: 7.4
            },
            {
                name: "Afghanistan",
                value: 7.9
            },
            {
                name: "Myanmar",
                value: 9.1
            },
            {
                name: "Mongolia",
                value: 14.7
            },
            {
                name: "Sri Lanka",
                value: 16.6
            },
            {
                name: "Bahrain",
                value: 20.5
            },
            {
                name: "Yemen",
                value: 22.6
            },
            {
                name: "Jordan",
                value: 22.3
            },
            {
                name: "Lebanon",
                value: 21.1
            },
            {
                name: "Azerbaijan",
                value: 31.7
            },
            {
                name: "Singapore",
                value: 47.8
            },
            {
                name: "Hong Kong",
                value: 49.9
            },
            {
                name: "Syria",
                value: 52.7
            },
            {
                name: "DPR Korea",
                value: 59.9
            },
            {
                name: "Israel",
                value: 64.8
            },
            {
                name: "Turkmenistan",
                value: 70.6
            },
            {
                name: "Oman",
                value: 74.3
            },
            {
                name: "Qatar",
                value: 88.8
            },
            {
                name: "Philippines",
                value: 96.9
            },
            {
                name: "Kuwait",
                value: 98.6
            },
            {
                name: "Uzbekistan",
                value: 122.6
            },
            {
                name: "Iraq",
                value: 139.9
            },
            {
                name: "Pakistan",
                value: 158.1
            },
            {
                name: "Vietnam",
                value: 190.2
            },
            {
                name: "United Arab Emirates",
                value: 201.1
            },
            {
                name: "Malaysia",
                value: 227.5
            },
            {
                name: "Kazakhstan",
                value: 236.2
            },
            {
                name: "Thailand",
                value: 272
            },

            {
                name: "Indonesia",
                value: 453
            },
            {
                name: "Saudi Arabia",
                value: 494.8
            },
            {
                name: "Japan",
                value: 1278.9
            },
            {
                name: "China",
                value: 10540.8
            },
            {
                name: "India",
                value: 2341.9
            },
            {
                name: "Russia",
                value: 1766.4
            },
            {
                name: "Iran",
                value: 618.2
            },
            {
                name: "Korea",
                value: 610.1
            }]
        }]
    });




    } else {
      var error = '错误码：' + res.code + '，' + '原因：' + res.message;

      swal({
        text: error,
        type: 'error'
      });
    }
  },
  error: function (jqXHR, textStatus, errorThrown) {
    var error = '错误码：' + textStatus + '，' + '原因：' + errorThrown;
    swal({
      text: error,
      type: 'error'
    });
  }
});


})



