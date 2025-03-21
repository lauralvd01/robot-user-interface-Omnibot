<script>
  import {
    line,
    curveLinear,
    Delaunay,
    range,
    scaleLinear,
    scaleUtc,
  } from "d3";

  export let data;
  export let props;

  console.log("Graphic data", data);
  let first_not_empty = data.findIndex((dataset) => dataset.data.length > 0);
  console.log("First not empty dataset", first_not_empty);

  if (!data || data.length === 0 || first_not_empty === -1) {
    console.error("No data provided");
    console.log(data.reduce((acc, dataset) => acc + dataset.data.length, 0))
    data = [{"id": 1, "data": [{"title_X": new Date(), "title_Y": 0}]}];
    first_not_empty = 0;
  }

  const marginTop = props.marginTop || 40; // the top margin, in pixels (40)
  const marginRight = props.marginRight || 5; // the right margin, in pixels (0)
  const marginBottom = props.marginBottom || 35; // the bottom margin, in pixels (30)
  const marginLeft = props.marginLeft || 35; // the left margin, in pixels (50)
  const width = props.width || 550; // the outer width of the chart, in pixels
  const height = props.height || Math.round(0.4*width); // the outer height of the chart, in pixels
  const title = props.title || "Graphic title"; // a title for the chart
  const xLabel = props.xLabel || "->"; // a label for the x-axis
  const yLabel = props.yLabel || "↑"; // a label for the y-axis
  const xFormat = props.xFormat || ""; // a format specifier string for the x-axis
  const yFormat = props.yFormat || ""; // a format specifier string for the y-axis
  const xType = props.xType || scaleUtc; // type of x-scale
  const yType = props.yType || scaleLinear; // type of y-scale
  const horizontalGrid = props.horizontalGrid || true; // show horizontal grid lines
  const verticalGrid = props.verticalGrid || true; // show vertical grid lines
  const colors = props.colors || ["#F50057", "#42A5F5", "#26A69A", "#9575CD"]; // fill color for dots && number of colors in fill array MUST match number of subsets in data
  const showDots = props.showDots || true; // whether dots should be displayed
  const dotsFilled = props.dotsFilled || true; // whether dots should be filled or outlined
  const r = props.r || 5; // (fixed) radius of dots, in pixels
  const strokeWidth = props.strokeWidth || 5; // stroke width of line, in pixels
  const strokeOpacity = props.strokeOpacity || 0.8; // stroke opacity of line
  const tooltipBackground = props.tooltipBackground || "white"; // background color of tooltip
  const tooltipTextColor = props.tooltipTextColor || "black"; // text color of tooltip
  const strokeLinecap = props.strokeLinecap || "round"; // stroke line cap of the line
  const strokeLinejoin = props.strokeLinejoin || "round"; // stroke line join of the line
  const xScalefactor = props.xScalefactor || width / 80; //x-axis number of values
  const yScalefactor = props.yScalefactor || height / 40; //y-axis number of values
  const curve = props.curve || curveLinear; // method of interpolation between points
  const xRange = props.xRange || [marginLeft, width - marginRight]; // [left, right]
  const yRange = props.yRange || [height - marginBottom, marginTop]; // [bottom, top]
  // xRange = [ left, right ] x_positions of the x axis ( in pixels inside the (0 0 width height) viewbox)
  // yRange = [ bottom, top ] y_positions of the y axis ( in pixels inside the (0 0 width height) viewbox)

  let x,y,dotInfo,lines,xVals = [],yVals = [],points = [],subsets = [],colorVals = [];


  // One dataset = "title_X,title_Y\nvalue_X_1,value_Y_1\nvalue_X_2,value_Y_2\n..."
  // Converted datasets array = [ { id: 1, data: [ { title_X: value_X_1, title_Y: value_Y_1 }, ... ] }, ... ]
    x = Object.keys(data[first_not_empty].data[0])[0]; // title_X
    y = Object.keys(data[first_not_empty].data[0])[1]; // title_Y
    data.forEach((subset, i) => {
      // subset = { id: 1, data: [ { title_X: value_X_1, title_Y: value_Y_1 }, ... ] }
      // i = subset index in data array
      subset.data.forEach((coordinate) => {
        // coordinate = { title_X: value_X_n, title_Y: value_Y_n }
        // coordinate[x] = coordinate[title_X] = value_X_n
        xVals.push(new Date(coordinate[x])); // xVals = [ value_X_1, value_X_2, ... ] all X_values for all subsets, for all datasets        ## Assuming x values are dates
        yVals.push(coordinate[y]); // yVals = [ value_Y_1, value_Y_2, ... ] all Y_values for all subsets, for all datasets
        // Associate each point of the dataset with the dataset color : color of subset data[index] = colors[index]
        colorVals.push(i); // colorVals = [ 0, 0, ... ], lenght = lenght(subset.data), then [ 1, 1, ... ], then [ 2, 2, ... ] for each dataset
        // Create a point with associated color for each coordinate of the subset, for all datasets
        points.push({
          x: new Date(coordinate[x]), // Assuming x values are dates
          y: coordinate[y],
          color: i,
        });
      });
      subsets.push(subset.id); // subsets = [ 1, 2, ... ] all subset ids
    });

  const date = points[0].x;
  const year = date.getFullYear();
  let month = date.getMonth() + 1;
  if (month < 10) month = "0" + month;
  const day = date.getDate();
  const hour = date.getHours();

  const I = range(xVals.length); // list of integers betwwen 0 (included) and xVals.length (excluded)
  const gaps = (d, i) => !isNaN(xVals[i]) && !isNaN(yVals[i]); // check if xVals[i] and yVals[i] data are correct numbers 
  const cleanData = points.map(gaps); // cleanData = [ true, true, ... ] if xVals[i] and yVals[i] are correct numbers, false otherwise


  // Create functions to scale x and y values to the chart width and height
  const Xmin = Math.min(...xVals);
  const Xmax = Math.max(...xVals);
  const xDomain = [Xmin, Xmax]; 
  const Ymin = Math.min(...yVals);
  const Ymax = Math.max(...yVals);
  const yDomain = [Ymin, Ymax];
  // xRange = [ left, right ] x_positions of the x axis ( in pixels inside the (0 0 width height) viewbox)
  // yRange = [ bottom, top ] y_positions of the y axis ( in pixels inside the (0 0 width height) viewbox)
  const xScale = xType(xDomain, xRange); // xScale(x_value) = x_position in the svg, xScale.invert(x_position) = x_value
  const yScale = yType(yDomain, yRange); // yScale(y_value) = y_position in the svg, yScale.invert(y_position) = y_value
  
  // Assuming yType is scaleLinear, get a visual y scale that extends the domain so that it starts and ends on rounds values
  const niceY = scaleLinear()
    .domain(yDomain)
    .nice();
  
  // Get the list of ticks (values for the legend) for the x and y axis
  const xTicks = xScale.ticks(xScalefactor); // Scalefactor = number of ticks wished (may differ as ticks are restricted to rounded-values)
  const xTicksFormatted = xTicks.map((el) => el.getMinutes() + "min" + el.getSeconds() + "s");
  const yTicks = niceY.ticks(yScalefactor); // Scalefactor = number of ticks wished (may differ as ticks are restricted to rounded-values)

  // Create a function that takes an array of indexes as an input to draw a curve line between points designed by these indexes
  // I is the array of the xVals, yVals and colorVals indexes. One element i for I array designates a point in the chart : xVals[i], yVals[i], colorVals[i]
  const chartLine = line()
    .defined((i) => cleanData[i]) // draw the line if xVals[i] and yVals[i] are correct numbers
    .curve(curve) // curve type
    .x((i) => xScale(xVals[i])) // x pixel position of the point indexed by i
    .y((i) => yScale(yVals[i])); // y pixel position of the point indexed by i

  // Every time there is a change, draw the lines
  $: {
    lines = [];
    colors.forEach((color, j) => { // for each color in colors, indexed by j (colors[j] = color of the dataset j --> for a point in the dataset j, colorVals[i] = j)
      const filteredI = I.filter((el, i) => colorVals[i] === j); // get the indexes i of the points xVals[i], yVals[i], colorVals[i] that have the right color (colorVals[i] === j)
      lines.push(chartLine(filteredI)); // draw the line between the points indexed by filteredI
    });
  }

  // Get the list of points pixel positions and color
  const pointsScaled = points.map((el) => [
    xScale(el.x),
    yScale(el.y),
    el.color,
  ]);

  // Create a Delaunay grid and a Voronoi grid from the points
  // Given a set of points (here positionned on the svg by pixels x and y), the Voronoi diagram partitions the plane 
  // into cells. These cells represent the region of the plane that is closest to the corresponding point.
  // This will allow to detect the closest point to the mouse cursor and display a tooltip
  const delaunayGrid = Delaunay.from(pointsScaled);
  const voronoiGrid = delaunayGrid.voronoi([0, 0, width, height]); // [Xmin, Ymin, Xmax, Ymax]

  export let svgRef;
</script>

<div class="chart-container">
  <!-- Title -->
  <h2>{title}</h2>

  <!-- Y label -->
  <label for="yLabel" style:margin-left=10px style:align-self=start>{yLabel}</label>

  <div style:position=relative style:margin-top=10px>
    <!-- Graph background : a box of pixels going from x=0, y=0 (top left) to x=width, y=height (bottom right) -->
    <svg
      {width}
      {height}
      viewBox="0 0 {width} {height}"
      cursor="crosshair"
      on:mouseout={() => (dotInfo = null)}
      on:blur={() => (dotInfo = null)}
      role="img"
      xmlns="http://www.w3.org/2000/svg"
      bind:this={svgRef}
    >

    <text class="hidden-title" x={marginLeft + 5} y={16} font-size="14px" color="black" font-family="Roboto">{title}</text>
    <text class="hidden-title" x={marginLeft + 5} y={marginTop + 12} font-size="12px" color="black" font-family="Roboto">{yLabel}</text>
    <text class="hidden-title" x={width - marginRight} y={height} font-size="12px" color="black" font-family="Roboto" text-anchor="end">{xLabel} ({year}/{month}/{day} . {hour}h)</text>

      <!-- Dots (if enabled) -->
      {#if showDots && !dotInfo}
        {#each I as i}
          <g class="dot" pointer-events="none">
            <circle
              cx={xScale(xVals[i])}
              cy={yScale(yVals[i])}
              {r}
              stroke={colors[colorVals[i]]}
              fill={dotsFilled ? colors[colorVals[i]] : "none"}
            />
          </g>
        {/each}
      {/if}

      <!-- Chart lines -->
      {#each lines as subsetLine, i}
        <g class="chartlines" pointer-events="none">
          {#if dotInfo}
            <path
              class="line"
              fill="none"
              stroke-opacity={points[dotInfo[1]].color === i ? "1" : "0.1"}
              stroke={colors[i]}
              d={subsetLine}
              stroke-width={strokeWidth}
              stroke-linecap={strokeLinecap}
              stroke-linejoin={strokeLinejoin}
            />
            <circle
              cx={xScale(points[dotInfo[1]].x)}
              cy={yScale(points[dotInfo[1]].y)}
              {r}
              stroke={colors[points[dotInfo[1]].color]}
              fill={dotsFilled}
            />
          {:else}
            <path
              class="line"
              fill="none"
              stroke={colors[i]}
              d={subsetLine}
              stroke-opacity={strokeOpacity}
              stroke-width={strokeWidth}
              stroke-linecap={strokeLinecap}
              stroke-linejoin={strokeLinejoin}
            />
          {/if}
        </g>
      {/each}

      <!-- Y-axis and horizontal grid lines -->
      <g
        class="y-axis"
        transform="translate({marginLeft}, 0)"
        pointer-events="none"
      >
        <path
          class="domain"
          stroke="black"
          d="M0, 0 V{height - marginBottom + 16}"
        />
        {#each yTicks as tick, i}
          <g class="tick" transform="translate(0, {yScale(tick)})">
            <line class="tick-start" stroke="black" x1={-8}/>
            {#if horizontalGrid}
              <line class="tick-grid" stroke=black stroke-opacity={tick === 0 ? "0.6" : "0.2"} x2={width - marginRight}/>
            {/if}
            <text font-size="11px" x="-{marginLeft}" y="5">{tick + yFormat}</text>
          </g>
        {/each}
      </g>

      <!-- X-axis and vertical grid lines -->
      <g
        class="x-axis"
        transform="translate(0,{height - marginBottom + 5})"
        pointer-events="none"
      >
        <path
          class="domain"
          stroke="black"
          d="M{marginLeft},0.5 H{width - marginRight + 8}"
        />
        {#each xTicks as tick, i}
          <g class="tick" transform="translate({xScale(tick)}, 0)">
            <line class="tick-start" stroke="black" y2="8" />
            {#if verticalGrid}
              <line class="tick-grid" stroke=black stroke-opacity="0.2" y2={- (height - marginBottom)} />
            {/if}
            <text font-size="8px" x={-marginLeft / 4} y="18">{xTicksFormatted[i] + xFormat}</text>
          </g>
        {/each}
      </g>

      <!-- Voronoi grid for mouse events -->
      {#each pointsScaled as point, i}
        <path
          stroke="none"
          fill-opacity="0"
          class="voronoi-cell"
          d={voronoiGrid.renderCell(i)}
          on:mouseover={(e) => (dotInfo = [point, i, e])}
          on:focus={(e) => (dotInfo = [point, i, e])}
          role="button"
          tabindex="0"
        ></path>
      {/each}

    </svg>

    <!-- Tooltip -->
    {#if dotInfo}
      <div
        class="tooltip"
        style:left="{Math.max(50-marginLeft,xScale(points[dotInfo[1]].x)-100)}px"
        style:top="{yScale(points[dotInfo[1]].y)-40}px" 
        style:background-color={tooltipBackground}
        style:color={tooltipTextColor}
      >
        <strong>
          {subsets ? subsets[points[dotInfo[1]].color] : ""}:
        </strong>
        {points[dotInfo[1]].x.getSeconds()}s; {points[dotInfo[1]].y.toFixed(2)}{yFormat}
      </div>
    {/if}
  </div>

  <!-- X label -->
  <label for="xLabel" style:align-self=end>{xLabel} ({year}/{month}/{day} . {hour}h)</label>
</div>

<style>
  .chart-container {
    justify-content: center;
    align-items: center;
    text-align: center;
    display:flex;
    flex-direction: column;
    margin:15px;
    margin-top: 0;
  }

  .chart-container h2 {
    margin-bottom: 10px;
    font-weight: bold;
  }

  svg {
    margin-left: 10px;
    margin-right: 10px;
  }
  
  .hidden-title {
    display: none;
  }

  path {
    fill: "green";
  }

  .y-axis {
    font-size: "10px";
    font-family: "Roboto", sans-serif;
    text-anchor: "start";
  }

  .x-axis {
    font-size: "10px";
    font-family: "Roboto", sans-serif;
    text-anchor: "end";
  }

  .tick {
    opacity: "1";
  }

  .tick-start {
    stroke: "black";
    stroke-opacity: "1";
  }
  
  .tick-grid {
    stroke: black;
    stroke-opacity: "0.2";
  }
  .tick text {
    fill: "black";
    text-anchor: "start";
  }

  .tooltip {
    position: absolute;
    pointer-events: none;
    border-radius: 5px;
    padding: 5px;
    box-shadow:
      rgba(0, 0, 0, 0.4) 0px 2px 4px,
      rgba(0, 0, 0, 0.3) 0px 7px 13px -3px,
      rgba(0, 0, 0, 0.2) 0px -3px 0px inset;
  }

  .tooltip strong {
    color: #ff662e;
  }
</style>
