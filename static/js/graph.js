$(document).ready(function(){

$.ajax({
    type: "GET",
    dataType: "json",
    url: "/api/analytics/project_graph_ajax/",
    contentType: 'application/json',
    success: function (res) {
        if (res.success){
            var chart = Highcharts.chart('chart1', {
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
    url: "/api/analytics/through_graph_ajax/",
    contentType: 'application/json',
    success: function (res) {
        if (res.success){
            Highcharts.chart('container1', {
                chart: {
                    type: 'cylinder',
                    options3d: {
                        enabled: true,
                        alpha: 15,
                        beta: 15,
                        depth: 50,
                        viewDistance: 25
                    }
                },
                title: {
                    text: res.result.title
                },
                plotOptions: {
                    series: {
                        depth: 25,
                        colorByPoint: true
                    }
                },
                xAxis: {
                        categories:res.result.xAxis
                    },
                series: [{
                    data: res.result.series,
                    name: 'Cylinders',
                    showInLegend: false
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
    url: "/api/analytics/case_info_graph_ajax/",
    contentType: 'application/json',
    success: function (res) {
        if (res.success){
            var chart = Highcharts.chart('container2', {
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
                backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
                shadow: true
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

})



