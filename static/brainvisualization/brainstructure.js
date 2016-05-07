var w = 1120,
    h = 600,
    x = d3.scale.linear().range([0, w]),
    y = d3.scale.linear().range([0, h]);

var vis = d3.select("#icicle").append("div")
    .attr("class", "chart")
    .style("width", w + "px")
    .style("height", h + "px")
    .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

var partition = d3.layout.partition()
    .value(function(d) { return d.size; });

var highlightPath = function (path_route, color) {
  var d3_path = d3.select(path_route[path_route.length - 1]);  
  d3_path.style("fill", function (data) { return color; });
}


var highlightSubtree = function (root, slice_id, highlight, offset) {
  if (root.slice_ids_enum != null) {
    var all_slices = root.slice_ids_enum;
    var slices = all_slices[slice_id];
    if (slices) {
      for (var i = 0; i < slices.length; i++) {
        var tempcolor;
        if (highlight) {
          tempcolor = "red";
        } else {
          tempcolor = "#" + root.color_hex_triplet;
        }
        highlightPath(root.path_routes[slices[i]], tempcolor);
      }
    }
  }
  var children = root.children;
  if (children != undefined && children != null) {
    for (var i = 0; i < children.length; i++) {
      highlightSubtree(children[i], slice_id, highlight, offset);
    }
  }
}

// Helper function for dealing with the weirdness of xml. Find the first
// child of elem "n" that is of type "element".
// Adapted from: http://www.w3schools.com/dom/prop_element_firstchild.asp
var get_firstchild = function (n) {
  var localfirstchild = n.firstChild;
  while (localfirstchild.nodeType != 1) {
    localfirstchild = localfirstchild.nextSibling;
  }
  return localfirstchild;
}

var xml_elem;


var mouseover = function(d, slice_id, offset) {
  d3.select("#" + slice_id).style("display", "inline");
  highlightSubtree(d, slice_id, true, offset);
  d3.select("#region-description")
    .html(d.summary);
}

var mouseout = function(d, slice_id, offset) {
  d3.select("#tooltip").classed("hidden", true);
  d3.selectAll("#" + slice_id).style("display", "none");
  highlightSubtree(d, slice_id, false, offset);
}

//Load all of the slices.
d3.json("/init/static/brainvisualization/extra/slices.json", function (filenames) {
    for (var i = 0; i < filenames.length; i++) {
      d3.xml("/init/static/brainvisualization/svgslices/" + filenames[i], "images/svg+xml", function (xml) {
        var xml_elem = get_firstchild(xml.documentElement);
        var filename = get_firstchild(xml_elem).attributes.sub_image_id.value + ".svg";
        var svgShapeURL = "url(/init/static/brainvisualization/svgslices/" + filename + ')';
        var slice_id = "p" + get_firstchild(xml_elem).attributes.id.value;
        
        var d3_slice_div = d3.select("#brain")
            .append("div")
            .attr("id", slice_id)
            .attr("class", "brain")
            .style("display", "none")
            .style("shape-outside", svgShapeURL)
            .style("background-image", svgShapeURL);
        d3_slice_div[0][0].appendChild(xml.documentElement)
            .setAttribute("class", "slice_svg");
      });
    }
});

d3.json("/init/static/brainvisualization/allencurrent.json", function(root) {
  var g = vis.selectAll("g")
      .data(partition.nodes(root))
    .enter().append("svg:g")
      .attr("transform", function(d) { return "translate(" + x(d.y) + "," + y(d.x) + ")"; })
      .on("click", click);

  var kx = w / root.dx,
      ky = h / 1;

  g.append("svg:rect")
      .attr("width", root.dy * kx)
      .attr("id", function(d) { return  d.id; })
      .attr("best_slice", function(d) { if (d.best_slice) return d.best_slice.id; })
      .attr("height", function(d) { return d.dx * ky; })
      .attr("class", function(d) { return d.children ? "parent" : "child"; })
      .style("fill", function(d) { return '#' + d.color_hex_triplet; })
      .on("mouseover", function (d) { 
          mouseover(d, d.best_slice.id, 0);
      }).on("mousemove", function(d){
        d3.select("#tooltip")
          .classed("hidden", false)
          .style("left", event.pageX + "px")
          .style("top", event.pageY + 20 + "px");
      })
      .on("mouseout", function (d) {
        mouseout(d, d.best_slice.id, 0);
      });

  g.append("svg:text")
      .attr("transform", transform)
      .attr("dy", ".35em")
      .style("opacity", function(d) { return d.dx * ky > 12 ? 1 : 0; })
      .text(function(d) { return d.name; });

  d3.select(window)
      .on("click", function() { click(root); })

  function click(d) {
    if (!d.children) return;

    kx = (d.y ? w - 40 : w) / (1 - d.y);
    ky = h / d.dx;
    x.domain([d.y, 1]).range([d.y ? 40 : 0, w]);
    y.domain([d.x, d.x + d.dx]);

    var t = g.transition()
        .duration(d3.event.altKey ? 7500 : 750)
        .attr("transform", function(d) { return "translate(" + x(d.y) + "," + y(d.x) + ")"; });

    t.select("rect")
        .attr("width", d.dy * kx)
        .attr("height", function(d) { return d.dx * ky; });

    t.select("text")
        .attr("transform", transform)
        .style("opacity", function(d) { return d.dx * ky > 12 ? 1 : 0; });

    d3.event.stopPropagation();
  }

  function transform(d) {
    return "translate(8," + d.dx * ky / 2 + ")";
  }
});
