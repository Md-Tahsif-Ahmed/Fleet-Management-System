$(document).ready(function(){
    /****************************
    **  Cart
    *****************************/
    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(document.getElementById("myChart"), {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Blue", "Yellow" ],
            datasets: [{
                 label: '',
                data: [ 0, 60, 10, 30, 0, 100],
                backgroundColor: [
                    '#fff',
                    '#437CBF',
                    '#6DC496',
                    '#D36060',
                ],
                borderWidth: 0,
            }]
        },
        options: {
            barRoundness: 8,
            legend: {
                display: true,
                labels: {
                    fontColor: 'rgb(255, 99, 132)'
                }
            },
            scales: {
                yAxes: [{
                    stacked: true,
                    zeroLineWidth:0,
                    ticks: {
                        beginAtZero:true,

                    },
                    gridLines: {

                        drawBorder: false
                    },
                }],
                xAxes: [{
                    barPercentage: 0.4,
                    stacked: true,
                    // display: false,
                    zeroLineWidth:0,
                    gridLines: {
                        display: false,
                        //  showBorder:false
                        drawBorder: false
                    },
                }]
            },

        }
    });

    /****************************
    **  Cart 2
    *****************************/
    var ctx2 = document.getElementById("myChart2").getContext('2d');
    var myChart2 = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Blue", "Yellow" ],
            datasets: [{
                 label: '',
                data: [ 0, 60, 0, 0, 0, 100],
                backgroundColor: [
                    '#fff',
                    '#437CBF',
                    '#6DC496',
                    '#D36060',
                ],
                borderWidth: 0,
            }]
        },
        options: {
            barRoundness: 8,
            legend: {
                display: true,
                labels: {
                    fontColor: 'rgb(255, 99, 132)'
                }
            },
            scales: {
                yAxes: [{
                    stacked: true,
                    zeroLineWidth:0,
                    ticks: {
                        beginAtZero:true,
                    },
                    gridLines: {
                        drawBorder: false
                    },
                }],
                xAxes: [{
                    barPercentage: 0.4,
                    stacked: true,
                    zeroLineWidth:0,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                }]
            },
        }
    });

    /****************************
    **  Cart 3
    *****************************/
    var ctx3 = document.getElementById("myChart3").getContext('2d');
    var myChart3 = new Chart(ctx3, {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Blue", "Yellow" ],
            datasets: [{
                 label: '',
                data: [ 0, 60, 0, 0, 0, 100],
                backgroundColor: [
                    '#fff',
                    '#437CBF',
                    '#6DC496',
                    '#D36060',
                ],
                borderWidth: 0,
            }]
        },
        options: {
            barRoundness: 8,
            legend: {
                display: true,
                labels: {
                    fontColor: 'rgb(255, 99, 132)'
                }
            },
            scales: {
                yAxes: [{
                    stacked: true,
                    zeroLineWidth:0,
                    ticks: {
                        beginAtZero:true,
                    },
                    gridLines: {

                        drawBorder: false
                    },
                }],
                xAxes: [{
                    barPercentage: 0.4,
                    stacked: true,
                    zeroLineWidth:0,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                }]
            },
        }
    });



    /****************************
    **  Cart 5
    *****************************/
     new Chart( document.getElementById("myChart5"), {
        type: 'doughnut',
        data: {
            labels: ["Germany", "Canada" ],
            datasets: [{
                label: '',
                data: [ 46, 54],
                backgroundColor: [
                    '#437CBF',
                    '#3D8E36',
                ],
                borderWidth: 0,
            }]
        },
        options: {
            barRoundness: 4,
            cutoutPercentage: 80,
            legend: {
                display: false,
            },
            scaleShowLabels : false,
            omitXLabels: true,
            scales: {
                yAxes: [{
                    stacked: false,
                    display: false,
                    zeroLineWidth:0,
                    ticks: {
                        beginAtZero:false,

                    },
                    gridLines: {
                        drawBorder: false,
                        display: false,
                    },
                }],
                xAxes: [{
                    barPercentage: 0.4,
                    stacked: false,
                     display: false,
                    zeroLineWidth:0,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                }]
            },
        }
    });

    /****************************
    **  Cart 6
    *****************************/
     new Chart( document.getElementById("myChart6"), {
        type: 'doughnut',
        data: {
            labels: ["Germany", "Canada" ],
            datasets: [{
                label: '',
                data: [ 86, 54],
                backgroundColor: [
                    '#437CBF',
                    '#C86464',
                ],
                borderWidth: 0,
            }]
        },
        options: {
            barRoundness: 4,
            cutoutPercentage: 80,
            legend: {
                display: false,
            },
            scaleShowLabels : false,
            omitXLabels: true,
            scales: {
                yAxes: [{
                    stacked: false,
                    display: false,
                    zeroLineWidth:0,
                    ticks: {
                        beginAtZero:false,

                    },
                    gridLines: {
                        drawBorder: false,
                        display: false,
                    },
                }],
                xAxes: [{
                    barPercentage: 0.4,
                    stacked: false,
                     display: false,
                    zeroLineWidth:0,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                }]
            },
        }
    });

    /****************************
    **  Cart 7
    *****************************/
     new Chart( document.getElementById("myChart7"), {
        type: 'doughnut',
        data: {
            labels: ["Germany", "Canada" ],
            datasets: [{
                label: '',
                data: [ 86, 54],
                backgroundColor: [
                    '#C86464',
                    '#6DC496',
                ],
                borderWidth: 0,
            }]
        },
        options: {
            barRoundness: 4,
            cutoutPercentage: 80,
            legend: {
                display: false,
            },
            scaleShowLabels : false,
            omitXLabels: true,
            scales: {
                yAxes: [{
                    stacked: false,
                    display: false,
                    zeroLineWidth:0,
                    ticks: {
                        beginAtZero:false,

                    },
                    gridLines: {
                        drawBorder: false,
                        display: false,
                    },
                }],
                xAxes: [{
                    barPercentage: 0.4,
                    stacked: false,
                     display: false,
                    zeroLineWidth:0,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                }]
            },
        }
    });
    /****************************
    **  myChart8
    *****************************/
    var myChart8 = new Chart(document.getElementById("myChart8"), {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Blue", "Yellow" ],
            datasets: [{
                 label: '',
                data: [ 0, 60, 0, 0, 0, 100],
                backgroundColor: [

                    '#fff',
                    '#437CBF',
                    '#6DC496',
                    '#D36060',
                ],
                borderWidth: 0,
            }]
        },
        options: {
            barRoundness: 8,
            legend: {
                display: true,
                labels: {
                    fontColor: 'rgb(255, 99, 132)'
                }
            },
            scales: {
                yAxes: [{
                    stacked: true,
                    zeroLineWidth:0,
                    ticks: {
                        beginAtZero:true,

                    },
                    gridLines: {

                        drawBorder: false
                    },
                }],
                xAxes: [{
                    barPercentage: 0.4,
                    stacked: true,
                    zeroLineWidth:0,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                }]
            },
        }
    });


    /****************************
    **  myChart9
    *****************************/
    var myChart9 = new Chart(document.getElementById("myChart9"), {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Blue", "Yellow" ],
            datasets: [{
                 label: '',
                data: [ 0, 90, 0, 40, 0, 100],
                backgroundColor: [

                    '#fff',
                    '#437CBF',
                    '#6DC496',
                    '#D36060',
                ],
                borderWidth: 0,
            }]
        },
        options: {
            barRoundness: 8,
            legend: {
                display: true,
                labels: {
                    fontColor: 'rgb(255, 99, 132)'
                }
            },
            scales: {
                yAxes: [{
                    stacked: true,
                    zeroLineWidth:0,
                    ticks: {
                        beginAtZero:true,

                    },
                    gridLines: {

                        drawBorder: false
                    },
                }],
                xAxes: [{
                    barPercentage: 0.4,
                    stacked: true,
                    zeroLineWidth:0,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                }]
            },
        }
    });

    /****************************
    **  myChart10
    *****************************/
    var myChart10 = new Chart(document.getElementById("myChart10"), {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Blue", "Yellow" ],
            datasets: [{
                 label: '',
                data: [ 0, 60, 0, 0, 0, 100],
                backgroundColor: [

                    '#fff',
                    '#437CBF',
                    '#6DC496',
                    '#D36060',
                ],
                borderWidth: 0,
            }]
        },
        options: {
            barRoundness: 8,
            legend: {
                display: true,
                labels: {
                    fontColor: 'rgb(255, 99, 132)'
                }
            },
            scales: {
                yAxes: [{
                    stacked: true,
                    zeroLineWidth:0,
                    ticks: {
                        beginAtZero:true,

                    },
                    gridLines: {

                        drawBorder: false
                    },
                }],
                xAxes: [{
                    barPercentage: 0.4,
                    stacked: true,
                    zeroLineWidth:0,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                }]
            },
        }
    });


});
