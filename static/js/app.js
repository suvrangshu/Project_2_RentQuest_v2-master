function buildMetadata(sample) {

 //Define the element to select
	var cell = d3.select("#sample-metadata");
	let url = `/metadata/${sample}`;
//Clearing the html under the cell.
	cell.html('');

//Iterate the Json and post the value	
d3.json(url).then((item) => {
     Object.entries(item).forEach(([key, value]) => {
       cell.append('text').html(`${key}: ${value}<br>`);
	   
     });
	 
});
	

	
}

function buildRegiondata(sample) {

 //Define the element to select
	var cell = d3.select("#sample-metadata");
	let url = `/regiondata/${sample}`;
//Clearing the html under the cell.
	cell.html('');

//Iterate the Json and post the value	
d3.json(url).then((item) => {
     Object.entries(item).forEach(([key, value]) => {
       cell.append('text').html(`${key}: ${value}<br>`);
	   
     });
	 
});
		
}




function buildCharts() {

		//Pie Chart
		console.log("Iam inside")
        var url = `/regioncount`;
		//console.log(url);
        d3.json(url).then(function(data){
	var layout = {
				title: "'Bar' Chart",
				};
		console.log("I am function")
		var d = [{labels:data["labels"],values:data["values"],type: "pie"}]
		console.log(d)
		Plotly.newPlot("pie", d, layout);
        });

		//Bubble Chart
		
		url = `/cityavgprice`;
		d3.json(url).then(function(data){
	//		var trace1 = {x:data["labels"],y:data["values"],  mode: 'markers', text:data["labels"],hoverinfo:"text",marker: { color: data["labels"],size: data["values"]} }
		//	var layout = {
			//	title: 'Marker Size',
				//};
			var trace1 = {x:data["labels"],y:data["values"], type:"bar"}
			
			//var data = [trace1];
			var layout = {
				title: "'Bar' Chart"
			};
            Plotly.newPlot("bubble", [trace1],layout);//
			
        });














		}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");
	selector.html('');
  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
	
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
	});
	selector1 = d3.select("#selRegion");
	selector1.html('');
  // Use the list of sample names to populate the select options
  d3.json("/region").then((sampleRegion) => {
	console.log(sampleRegion)
    sampleRegion.forEach((sample) => {
      selector1
        .append("option")
        .text(sample)
        .property("value", sample);
		
    });
	const firstRegion = sampleRegion[0];
  });
    // Use the first sample from the list to build the initial plots
    
	
	
	
	
    buildCharts();
    //buildMetadata(firstSample);
  
}

function optionChanged(newSample) {
	debugger;
	console.log(newSample);
  buildMetadata(newSample);
}

function optionRegionChanged(newSample) {
	
	//buildCharts();
  // Fetch new data each time a new sample is selected
  //buildCharts(newSample);
  buildRegiondata(newSample);
}



// Initialize the dashboard
init();
