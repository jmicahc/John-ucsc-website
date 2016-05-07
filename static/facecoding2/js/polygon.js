var rect_width = 5,
    rect_height = 5;

var polys = {
    "left-eye": [],
    "right-eye": [],
    "lip-top": [],
    "lip-bottom": [],
    "left-eye-brow": [],
    "right-eye-brow": []
};

var current_poly = null;


var xScale = d3.scale.linear()
		.domain([0,1000])
		.range([0,1000]);

var	yScale = d3.scale.linear()
		.domain([0,1000])
		.range([0,1000]);


var zoom = d3.behavior.zoom()
  .x(xScale)
  .y(yScale)
  .scaleExtent([1,10])
  .on("zoom", zoomed);


var svg = d3.select("body")
    .append("svg")
    .attr("width", "100%")
    .attr("height", "80%")
    .call(zoom)
    .on("mousedown", function() { processClick(); });


var buttons = d3.select("body").append("div")
    .attr("style", "width:400px;height:20%;")
    .attr("id", "hello");

buttons.append('input')
    .attr("type", "button")
    .attr("data-inline", "true")
    .attr("value", "Undo")
    .html("undo")
    .on("click", function() { 
       d3.select("#label-" + current_poly + "-" + polys[current_poly].length)
         .remove();
       d3.select("#rect-" + current_poly + "-" + polys[current_poly].length)
         .remove();
       polys[current_poly].pop();
       d3.select('#polygon-' + current_poly)
         .attr("points", function() { return polys[current_poly].map(function(d) { return [d.x, d.y].join(","); }).join(" ");});
    });
buttons.append('input')
    .attr("type", "button")
    .attr("value", "finish")
    .attr("data-inline", "true")
    .html("undo")
    .on("click", function() { 
        finishPoly(current_poly);
    });
buttons.append('input')
    .attr("type", "button")
    .attr("value", "submit")
    .attr("data-inline", "true")
    .html("undo")
    .on("click", function() { 
        savepolys(polys);
    });


var container = svg.append("g");

function zoomed() {
    container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
}


container.append("image")
   .attr("xlink:href",'../static/facecoding2/images/img1.png')
   .attr("x", "0")
   .attr("y", "0")
   .attr("height", "100%")
   .attr("width", "80%");

var savepolys = function() {
    var data = JSON.stringify(polys);
    $.ajax({
      type: 'POST',
      url: "../facecoding2/savedata",
      contentType: "application/json; charset=utf-8",
      data: data,
      dataType: 'json',
      success: function(data) {
            console.log('success');
            console.log(data);
            }
    })
}

var dragVertex = d3.behavior.drag()
    .on("dragstart", function(d) {console.log("drag starting!"); console.log(d); })
    .on("drag", function(d) {      var rect = d3.select(this);
      rect.attr("x", xScale.invert(event.pageX - (rect_width / 2)))
          .attr("y", yScale.invert(event.pageY - (rect_width / 2)));
      
      var label = d3.select("#" + rect.attr("textid"))
          .attr("x", xScale.invert(event.pageX - (rect_width / 2)))
          .attr("y", yScale.invert(event.pageY - (rect_width / 2)));
     
      var vertex_index = +rect.attr("vertex-index");
      var poly = container.select("#polygon-" + rect.attr("class"));
      poly.attr("points", function (d) {
        console.log(event.pageX);
        d[vertex_index] = {x: xScale.invert(event.pageX), y: yScale.invert(event.pageY)};
        return d.map(function(d) { return [d.x, d.y].join(","); }).join(" ");
      });
    })
    .on("dragend", function(){ console.log("drag ended"); });

var processClick = function () {
  /*
  Select between 2 actions: (1) add vertex to polygon, or
                            (2) start new polygon.
  
   If current current_polygon is null:
       create new polygon (addPolygon).
   Else:
       add vertex to polygon.
  */
  var mouse = {x: d3.event.pageX, y: d3.event.pageY};

  if (current_poly == null) {
    getLabel( mouse );
  }
  else {
    addPoint( mouse, current_poly );
  }
}
var finishPoly = function(name) { 
    d3.select('#polygon-' + name)
      .attr('fill', 'black')
      .attr('stroke', 'white')
    current_poly = null; 
    d3.event.stoppropagation();
}


var getLabel = function( point ) {
  //Create a pop-up window with polygon selector.
  console.log('getting label');
  $('#myPopupDialog').popup("open", {x: point.x, y: point.y, transition: "fade"})
  .on('popupafterclose', function(event, ui) {
      console.log(event);
      var name = $('#region').val();
      addPolygon( name, point);
      event.stopPropagatfion();
  });
}

var addPoint = function( point, name ) {
     container.select("#polygon-" + name)
        .attr("points",function(d) {
          console.log('adding point');
          d.push({x: xScale.invert(point.x), y: yScale.invert(point.y)});
          return d.map(function(d) { return [d.x, d.y].join(","); }).join(" ");
        });

    var vertex_box = container.append('g');
    var text = vertex_box.append('text')
        .attr("id","label-" + name + "-" + polys[name].length)
        .attr("fill", "white")
        .attr("class", name)
        .text(polys[name].length)
        .attr("x", xScale.invert(point.x - (rect_width / 2)) )
        .attr("y", yScale.invert(point.y - (rect_height / 2)) );

    vertex_box.append('rect')
        .attr("class", name)
        .attr("id", "rect-" + name + "-" + polys[name].length)
        .attr("textid", "label-" + name + "-" + polys[name].length)
        .attr("label", 10)
        .attr("x", xScale.invert(point.x - (rect_width / 2)) )
        .attr("y", yScale.invert(point.y - (rect_height / 2)) )
        .attr("width", rect_width)
        .attr("height", rect_height)
        .attr("vertex-index", polys[name].length - 1)
        .attr("style","fill:red;stroke:black;stroke-width:1")
        .on("mousedown", function() { d3.event.stopPropagation(); })
        .on("dblclick", function() { 
          finishPoly(name);
        })
        .call(dragVertex);
};


var addPolygon = function( name, point ) {
  console.log('adding polygon');
  current_poly = name;

  if (d3.select('#polygon-' + name)[0][0] == null) {
    container.append("polygon")
      .attr("class", name)
      .attr("id", 'polygon-' + name)
      .attr("stroke", "green")
      .attr("fill", "red")
      .attr("stroke-width", 2)
      .attr("fill-opacity", .3)
      .data([polys[name]]).enter();
  } else {
    d3.select('#polygon-' + name)
      .attr('fill', 'red')
      .attr('stroke', 'green');
  }
}
