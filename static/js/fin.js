$(function(){
    $.ajax({
        url:"/fin/chart_data",
        type:"get",
        data:{},
        dataType:"json",
        success:function(data){
                shapeChartData = {
                labels: data.intdate,
                datasets: [{
                    label: '코로나 확진자',
                    data: data.dailydecide,
                    backgroundColor: [
                        'skyblue'
                    ],
                    borderColor: [
                        'skyblue'
                    ],
                    borderWidth: 4
                }]
            }
            barChart();

        },
        error:function(){
            alert("실패");
        }
    
});//function

//차트 그리기
function barChart() {

    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'bar',
    data: shapeChartData,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}//createChart 
function lineChart() {

    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'bar',
    data: shapeChartData,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}//createChart


$("#fstock1btn").click(function(){
    alert('성공')
    var code = $("#fstock1").val()
    alert(code)
    $.ajax({
        url:"/fin/code_data",
        type:"GET",
        data:{'code':code},
        dataType:"json",
        success:function(data){
            shapeChartData = {
                labels: data.codedate,
                datasets: [{
                    label: '주식데이터',
                    data: data.codeclose,
                    backgroundColor: [
                        'skyblue'
                    ],
                    borderColor: [
                        'skyblue'
                    ],
                    borderWidth: 4
                }]
            }
            lineChart();
        },error:function(){
            alert("실패");
        }
    })
})
})