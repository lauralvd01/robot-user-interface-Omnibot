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

  const marginTop = props.marginTop || 40; // the top margin, in pixels (40)
  const marginRight = props.marginRight || 0; // the right margin, in pixels (0)
  const marginBottom = props.marginBottom || 30; // the bottom margin, in pixels (30)
  const marginLeft = props.marginLeft || 50; // the left margin, in pixels (50)
  const inset = props.inset || 0; // inset the default range, in pixels
  const width = props.width || 600; // the outer width of the chart, in pixels
  const height = props.height || 350; // the outer height of the chart, in pixels
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
  const insetTop = props.insetTop || inset; // inset from top
  const insetRight = props.insetRight || inset; // inset from right
  const insetBottom = props.insetBottom || inset; // inset from bottom
  const insetLeft = props.insetLeft || inset; // inset from left
  const xRange = props.xRange || [marginLeft + insetLeft,width - marginRight - insetRight]; // [left, right]
  const yRange = props.yRange || [height - marginBottom - insetBottom,marginTop + insetTop]; // [bottom, top]

  let x,y,dotInfo,lines,xVals = [],yVals = [],points = [],subsets = [],colorVals = [];

  // For a single set of data
  if (!("data" in data[0])) {
    x = Object.keys(data[0])[0];
    y = Object.keys(data[0])[1];
    xVals = data.map((el) => el[x]);
    yVals = data.map((el) => el[y]);
    colorVals = data.map((el) => 0);
    points = data.map((el) => ({
      x: el[x],
      y: el[y],
      color: 0,
    }));
  }
  // For data with subsets (NOTE: expects 'id' and 'data' keys)
  else {
    x = Object.keys(data[0]?.data[0])[0];
    y = Object.keys(data[0]?.data[0])[1];
    data.forEach((subset, i) => {
      subset.data.forEach((coordinate) => {
        xVals.push(coordinate[x]);
        yVals.push(coordinate[y]);
        colorVals.push(i);
        points.push({
          x: coordinate[x],
          y: coordinate[y],
          color: i,
        });
      });
      subsets.push(subset.id);
    });
  }

  const I = range(xVals.length);
  const gaps = (d, i) => !isNaN(xVals[i]) && !isNaN(yVals[i]);
  const cleanData = points.map(gaps);

  const xDomain = [xVals[0], xVals[xVals.length - 1]];
  const yDomain = [0, Math.max(...yVals)];
  const xScale = xType(xDomain, xRange);
  const yScale = yType(yDomain, yRange);
  const niceY = scaleLinear()
    .domain([0, Math.max(...yVals)])
    .nice();

  const chartLine = line()
    .defined((i) => cleanData[i])
    .curve(curve)
    .x((i) => xScale(xVals[i]))
    .y((i) => yScale(yVals[i]));

  $: {
    lines = [];
    colors.forEach((color, j) => {
      const filteredI = I.filter((el, i) => colorVals[i] === j);
      lines.push(chartLine(filteredI));
    });
  }

  const pointsScaled = points.map((el) => [
    xScale(el.x),
    yScale(el.y),
    el.color,
  ]);
  const delaunayGrid = Delaunay.from(pointsScaled);
  const voronoiGrid = delaunayGrid.voronoi([0, 0, width, height]);

  const xTicks = xScale.ticks(xScalefactor);
  const xTicksFormatted = xTicks.map((el) => el.getMinutes() + "min" + el.getSeconds() + "s");
  const yTicks = niceY.ticks(yScalefactor);
</script>

<div class="chart-container">
  <!-- Title -->
  <h2>{title}</h2>

  <!-- Y label -->
  <label for="yLabel" style:margin-left=10px style:align-self=start>{yLabel}</label>

  <div style:position=relative>
    <!-- Graph background -->
    <svg
      {width}
      {height}
      viewBox="0 0 {width} {height}"
      cursor="crosshair"
      on:mouseout={() => (dotInfo = null)}
      on:blur={() => (dotInfo = null)}
      role="img"
    >
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
          d="M{insetLeft}, {marginTop} V{height - marginBottom + 6}"
        />
        {#each yTicks as tick, i}
          <g class="tick" transform="translate(0, {yScale(tick)})">
            <line class="tick-start" x1={insetLeft - 6} x2={insetLeft} />
            {#if horizontalGrid}
              <line
                class="tick-grid"
                x1={insetLeft}
                x2={width - marginLeft - marginRight}
              />
            {/if}
            <text x="-{marginLeft}" y="5">{tick + yFormat}</text>
          </g>
        {/each}
      </g>
      <!-- X-axis and vertical grid lines -->
      <g
        class="x-axis"
        transform="translate(0,{height - marginBottom - insetBottom})"
        pointer-events="none"
      >
        <path
          class="domain"
          stroke="black"
          d="M{marginLeft},0.5 H{width - marginRight}"
        />
        {#each xTicks as tick, i}
          <g class="tick" transform="translate({xScale(tick)}, 0)">
            <line class="tick-start" stroke="black" y2="6" />
            {#if verticalGrid}
              <line class="tick-grid" y2={-height + 70} />
            {/if}
            <text font-size="8px" x={-marginLeft / 4} y="20"
              >{xTicksFormatted[i] + xFormat}</text
            >
          </g>
        {/each}
      </g>

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
        style:left="{Math.max(100-marginLeft,xScale(points[dotInfo[1]].x)-100)}px"
        style:top="{yScale(points[dotInfo[1]].y)-40}px" 
        style:background-color={tooltipBackground}
        style:color={tooltipTextColor}
      >
        {subsets ? subsets[points[dotInfo[1]].color] : ""}:
        {points[dotInfo[1]].x.getSeconds()}s; {points[dotInfo[1]].y.toFixed(2)}{yFormat}
      </div>
    {/if}
  </div>

  <!-- X label -->
  <label for="xLabel" style:align-self=end>{xLabel} ({points[0].x.getFullYear()}/{points[0].x.getMonth()+1}/{points[0].x.getDate()} {points[0].x.getHours()}h)</label>
</div>

<style>
  .chart-container {
    justify-content: center;
    align-items: center;
    text-align: center;
    display:flex;
    flex-direction: column;
    margin:15px
  }

  .chart-container h2 {
    margin-bottom: 10px;
    font-weight: bold;
  }

  .y-axis {
    font-size: 10px;
    font-family: "Roboto", sans-serif;
    text-anchor: start;
  }

  svg {
    margin-left: 10px;
    margin-right: 10px;
  }
  
  path {
    fill: "green";
  }

  .x-axis {
    font-size: 10px;
    font-family: "Roboto", sans-serif;
    text-anchor: end;
  }

  .tick {
    opacity: 1;
  }
  .tick-start {
    stroke: black;
    stroke-opacity: 1;
  }
  .tick-grid {
    stroke: black;
    stroke-opacity: 0.2;
    font-size: 11px;
    color: black;
  }
  .tick text {
    fill: black;
    text-anchor: start;
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
    max-width: 100px;
  }
</style>
