Plotly.d3.csv("./dates.csv", function(err, rows){

  function unpack(rows, key) {
  return rows.map(function(row) { return row[key]; });
}


var trace1 = {
  type: "scatter",
  mode: "lines",
  name: 'Disease Posts Per Day',
  x: unpack(rows, 'Date'),
  y: unpack(rows, '0'),
  line: {color: '#17BECF'}
}

var data = [trace1];

var layout = {
  title: 'Disease Posts Per Day',
};

Plotly.newPlot('myDiv', data, layout);
})


