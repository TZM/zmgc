console.log($("#connect").outerWidth());
var feature;

var width = 277,
    height = 215,
		centered;

var lat = 0.0, lon = 0.0;

var projection = d3.geo.azimuthal()
    .scale(95)
    .origin([lat,lon])
    .mode("orthographic")
    .translate([160, 100]);

var circle = d3.geo.greatCircle()
    .origin(projection.origin());

// TODO fix d3.geo.azimuthal to be consistent with scale
var scale = {
  orthographic: 95,
  stereographic: 95,
  gnomonic: 95,
  equidistant: 95 / Math.PI * 2,
  equalarea: 95 / Math.SQRT2
};

var path = d3.geo.path()
    .projection(projection);

var svg = d3.select("#viz").append("svg:svg")
    .attr("width", width)
    .attr("height", height)
    .on("mousedown", mousedown);


svg.append("rect")
    .attr("fill", "none")
    .attr("width", width)
    .attr("height", height)
		.on("mouseover", function() {
		    $('#howto').text("Testing123");
				console.log("IN");
		  })
		.on("mouseout", 	function() {
			    $('#howto').text("");
					console.log("Out");
			  })
		.attr("pointer-events", "all");

d3.json("/ui/data/world-countries.json", function(collection) {
  feature = svg.selectAll("path")
      .data(collection.features)
      .enter().append("svg:path")
			.on("mouseover", function(d) { d3.select(this).style("fill",
			"#6C0"); })
			.on("mouseout", function(d) { d3.select(this).style("fill",
			"#000000"); })
			.on("click", click)
      .attr("d", clip);

  feature.append("svg:title")
      .text(function(d) { return d.properties.name; });
			
	// startAnimation();
	// d3.select('#animate').on('click', function () {
	//     if (done) startAnimation(); else stopAnimation();
	// });
});

d3.select(window)
    .on("mousemove", mousemove)
    .on("mouseup", mouseup);

d3.select("select").on("change", function() {
  projection.mode(this.value).scale(scale[this.value]);
  refresh(750);
});

function startAnimation() {
  done = false;
  d3.timer(function() {
    var origin = projection.origin();
    o1 = [origin[0] + .18, origin[1] + .06];
    projection.origin(o1);
    circle.origin(o1);
    refresh();
    return done;
  });
}

var m0,
    o0;

function mousedown() {
  m0 = [d3.event.pageX, d3.event.pageY];
  o0 = projection.origin();
  d3.event.preventDefault();
}

function mousemove() {
  if (m0) {
    var m1 = [d3.event.pageX, d3.event.pageY],
        o1 = [o0[0] + (m0[0] - m1[0]) / 8, o0[1] + (m1[1] - m0[1]) / 8];
    projection.origin(o1);
    circle.origin(o1);
    refresh();
  }
}

function click(d) {
  var x = 10,
      y = 10;
  // If the click was on the centered state or the background, re-center.
  // Otherwise, center the clicked-on state.
  //if (!d || centered === d) {
  //  centered = null;
  //} else {
  //  var centroid = path.centroid(d);
  //  x = width / 2 - centroid[0];
  //  y = height / 2 - centroid[1];
  //  centered = d;
	//	console.log(centroid);
  //}

  // Transition to the new transform.
  svg.transition()
      .attr("transform", "translate(" + x + "," + y + ")");
}


function mouseup() {
  if (m0) {
    mousemove();
    m0 = null;
  }
}
function refresh(duration) {
  (duration ? feature.transition().duration(duration) : feature).attr("d", clip);
}

function clip(d) {
  return path(circle.clip(d));
}