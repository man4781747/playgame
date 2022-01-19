var looper
var PeopleList = [...Array(50).keys()]

// var PeopleList = ['A','B','C']


var PeopleCountList
function buildPeopleCountList(){
    PeopleCountList = []
    for (let name of PeopleList){
        PeopleCountList.push(0)
    }
}
buildPeopleCountList()

function resetCounter(){
    for (let index in PeopleCountList){
        PeopleCountList[index] = 0
    }
    Plotly.redraw('myDiv');
}

var Vue_main = new Vue({
	el: '#app',
	data: {
        PeopleList: PeopleList,
        PeopleCountList:PeopleCountList,
        loop: false,
        GetIndex: 0,
	},
  
	computed: {},
  
	methods: {
        changePeople(){
            this.GetIndex = generateRandomInt(PeopleList.length)
            PeopleCountList[this.GetIndex] += 1
            Plotly.redraw('myDiv');
        },
    },

	mounted: function(){
	},
})

var socket;

$(document).ready(function() {
  var url = 'http://34.80.222.210';
  var port = '80';
  socket = io.connect(url + ':' + port);

  socket.on('START', function(msg) {
    runLooper()
  });
  socket.on('STOP', function(msg) {
    stopLooper()
  });
  socket.on('reset', function(msg) {
    resetCounter()
  });

  return false;});


function generateRandomInt(max){
    return Math.floor(Math.random() * max);
}

function stopLooper(){
    clearInterval(looper);
}

function runLooper(){
    looper = setInterval(function(){
        Vue_main.changePeople()
    }, 10);
}

var trace1 = {
    x: PeopleList,
    y: PeopleCountList,
    name: 'SF Zoo',
    type: 'bar'
  };
var data = [trace1];
var layout = {
        barmode: 'stack',
        yaxis: {
            rangemode: 'nonnegative',
            autorange: true
        },
    };
Plotly.newPlot('myDiv', data, layout);