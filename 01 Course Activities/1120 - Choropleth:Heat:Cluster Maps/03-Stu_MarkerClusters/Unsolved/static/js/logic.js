// Creating map object
const myMap = L.map("map", {
  center: [40.7, -73.95],
  zoom: 11
});

// Adding tile layer to the map
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);

// TODO:

// Store API query variables
const baseUrl = "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?";
let date = "$where=created_date between '2016-01-10T12:00:00' and '2017-01-01T14:00:00'";
let complaint = "&complaint_type=Rodent";
let limit = "&$limit=10000";


// Assemble API query URL

let url = baseUrl + date + complaint + limit;
console.log(url);
// Grab the data with d3
d3.json(url, function(response){
  // Create a new marker cluster group
  const markers = L.markerClusterGroup();

  // Loop through data
  for(let i = 0, ii = response.length; i < ii; i++){
    // Set the data location property to a variable
    const location = response[i].location;

    // Check for location property
    if (location) {
      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([location.coordinates[1], location.coordinates[0]])
        .bindPopup(response[i].descriptor));
    }
  }

  // Add our marker cluster layer to the map
  myMap.addLayer(markers);
});