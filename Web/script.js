$(document).ready(function() {


  $.get("d1.json", function(highlightedPath) {
    $.get("d.json", function(data) {
      drawNetwork(data, highlightedPath);
    });
  });
});


function drawNetwork(data, highlightedPath) {


  const width = 800;
  const height = 600;
  const arrowSize = 5;

  const maxLinkValue = d3.max(Object.values(data).flatMap(targets => Object.values(targets)));
  const linkWidthScale = d3.scaleLinear()
    .domain([1, maxLinkValue])
    .range([1, ]);

  const colorScale = d3.scaleLinear()
    .domain([1, maxLinkValue])
    .range(["#ff0000", "#0000ff"]);

  const svg = d3.select("#network-container")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .style("background-color", "#f2f2f2");

  const arrowhead = svg.append("defs").append("marker")
    .attr("id", "arrow")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 19)
    .attr("refY", 0)
    .attr("markerWidth", arrowSize)
    .attr("markerHeight", arrowSize)
    .attr("orient", "auto");

  arrowhead.append("path")
    .attr("class", "arrowhead")
    .attr("d", "M0,-5L10,0L0,5");

    const links = [];
    const nodes = {};
    
    for (const [source, targets] of Object.entries(data)) {
      for (const [target, value] of Object.entries(targets)) {
        links.push({ source, target, value });
      }
    }
    
    links.forEach(link => {
      link.source = nodes[link.source] || (nodes[link.source] = { id: link.source });
      link.target = nodes[link.target] || (nodes[link.target] = { id: link.target });
      link.highlighted = isLinkHighlighted(link);

    });
    
    function isLinkHighlighted(link) {
      for (const pathLink of highlightedPath) {
        if (link.source.id === pathLink["Source"] && link.target.id === pathLink["Destination"]) {
          return true;
        }
      }
      return false;
    }
    
    Object.values(nodes).forEach(node => {
      node.highlighted = isLinkHighlighted2(node);
    });
    
    function isLinkHighlighted2(node) {
      for (const pathLink of highlightedPath) {


        if (node.id === pathLink["Source"] || node.id === pathLink["Destination"]) {
          console.log("true");
          return true;
        }
      }
      return false;
    }
  const simulation = d3.forceSimulation(Object.values(nodes))
    .force("link", d3.forceLink(links).id(d => d.id))
    .force("charge", d3.forceManyBody().strength(-200))
    .force("center", d3.forceCenter(width / 2, height / 2));

  const linkGroups = svg.append("g")
    .attr("class", "links")
    .selectAll("g")
    .data(links)
    .enter()
    .append("g");

  const linkLines = linkGroups.append("line")
    .style("stroke", d => (d.highlighted ? "green" : colorScale(d.value)))
    .style("stroke-width", 2)
    .attr("marker-end", "url(#arrow)");

  linkGroups.append("circle")
    .attr("r", 5)
    .style("fill", "white")
    .style("stroke", "black")
    .style("stroke-width", 1);

  linkGroups.append("text")
    .text(d => d.value)
    .attr("dy", 2)
    .attr("text-anchor", "middle")
    .style("font-size", 10)
    .style("fill", "#555");

  const node = svg.append("g")
    .attr("class", "nodes")
    .selectAll("g")
    .data(Object.values(nodes))
    .enter()
    .append("g")
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended));

  node.append("circle")
    .attr("r", 10)
    .attr("r", d => (d.highlighted ? 14 : 10))

    .style("fill", d => (d.highlighted ? "green" : "#8f8b8b"))

  node.append("text")
    .text(d => d.id)
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "middle")
    .style("font-size", "12px")
    .style("fill", "#fff");

  simulation.on("tick", ticked);
  console.log(d)

  function ticked() {
    
    linkLines
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    linkGroups.selectAll("circle")
      .attr("cx", d => d.source.x + 0.41 * (d.target.x - d.source.x))
      .attr("cy", d => d.source.y + 0.41 * (d.target.y - d.source.y));

    linkGroups.selectAll("text")
      .attr("x", d => d.source.x + 0.4 * (d.target.x - d.source.x))
      .attr("y", d => d.source.y + 0.4 * (d.target.y - d.source.y))
      .text(d => d.value);

    node.attr("transform", d => `translate(${d.x},${d.y})`);
  }

  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }

  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }
}