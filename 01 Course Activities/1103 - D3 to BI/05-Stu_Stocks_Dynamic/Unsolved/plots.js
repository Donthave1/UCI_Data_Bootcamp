
/**
 * Helper function to select stock data
 * Returns an array of values
 * @param {array} rows
 * @param {integer} index
 * index 0 - Date
 * index 1 - Open
 * index 2 - High
 * index 3 - Low
 * index 4 - Volume
 */
function unpack(rows, index) {
  return rows.map(function(row) {
    return row[index];
  });
}

// Submit Button handler
function handleSubmit() {
  // @TODO: YOUR CODE HERE
  // Prevent the page from refreshing
  d3.event.preventDefault();

  // Select the input value from the form
  let stock = d3.select("#stockInput").node().value;
  console.log(stock)

  // clear the input value
  d3.select("#stockInput").node().value = ""

  // Build the plot with the new stock
  buildPlot(stock);

}

function buildPlot(stock) {
  const apiKey = "y4kEMqRt56f5-TJ-fEK9";

  const url = `https://www.quandl.com/api/v3/datasets/WIKI/${stock}.json?start_date=2016-10-01&end_date=2017-10-01&api_key=${apiKey}`;

    d3.json(url).then(function(data) {

      // Grab values from the response json object to build the plots
      let name = data.dataset.name;
      let stock = data.dataset.dataset_code;
      let startDate = data.dataset.start_dates;
      let endDate = data.dataset.end_date;
      let dates = unpack(data.dataset.data, 0);
      let closingPrices = unpack(data.dataset.data, 1);
  
      let trace = {
        type: "scatter",
        mode: "lines",
        name: name,
        x: dates,
        y: closingPrices,
        line: {
          color: "#17BECF"
        }
      };
  
      let dataArr = [trace];
  
      let layout = {
        title:`${stock} closing prices`,
        xaxis: {
          range: [startDate, endDate],
          type: "date"
        },
        yaxis: {
          autorange: true,
          type: "linear"
        }
      };
  
      Plotly.newPlot("plot", dataArr, layout)
    });
}

// Add event listener for submit button
d3.select("#submit").on("click", handleSubmit);