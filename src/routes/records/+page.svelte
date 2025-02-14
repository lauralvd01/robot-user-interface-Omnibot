<script>
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import { curveLinear, scaleLinear, scaleUtc } from "d3";

    import Banner from "../Banner.svelte";
    import Button from "../Button.svelte";
    import Graphic from "../graphics/Graphic.svelte";

    import { fetchData, records, sendEraseRequest } from "../data_store";

    let content_width = 0;
    let bannerHeight = 0;
    onMount( () => {
        const banner = document.querySelector(".banner");
        if (banner) bannerHeight = banner.offsetHeight;

        const content = document.querySelector(".content");
        if (content) content_width = content.clientWidth;
        fetchData("records");
    })

const currentRecords = writable([])


function updateCurrentRecords(records){
    currentRecords.set(records);
    console.log(records);
}

$: records && updateCurrentRecords($records);

let record_names = []
function getRecordsNames(records){
    record_names = []
    for (let index = 0; index < records.length; index++) {
        record_names.push(records[index].date)
        
    }

}

$: records && getRecordsNames($records);

const props = writable({}); // the fixed properties of the chart (and default values from d3 package)
    props.set({
        // width: $width,
        // height: height,

        // Labels and formats
        // title: $graphTitle, // a title for the chart ('')
        xLabel: "-> temps", // a label for the x-axis
        // yLabel: "↑ " + $yLabel + "(" + $selectedUnit + ")", // a label for the y-axis
        // yFormat: $selectedUnit, // a format specifier string for the y-axis

        xType: scaleUtc, // type of x-scale
        yType: scaleLinear, // type of y-scale

        // xScalefactor: $width / 80, // x-axis number of values
        // yScalefactor: height / 40, // y-axis number of values
        curve: curveLinear, // method of interpolation between points

        // Number of colors array elements must match number of data sets (12 here)
        colors: [ 
            "#FF662E", // Bright orange
            "#E42618", // Deep red
            "#239E99", // Blue-green
            "#A04040", // Reddish brown
            "#4B1338", // Dark burgundy
            "#656780", // Bluish grey
            "#FFB400", // Golden yellow
            "#0A9D58", // Dark green
            "#0085C7", // Bright blue
            "#C724B1", // Magenta violet
            "#795548", // Earthy brown
            "#1E1E1E", // Anthracite grey
        ], // fill color for dots && number of colors in fill array MUST match number of subsets in data ("#F50057","#42A5F5","#26A69A","#9575CD"])

        // Inner style
        horizontalGrid: true, // show horizontal grid lines
        verticalGrid: true, // show vertical grid lines
        showDots: true, // whether dots should be displayed or not
        dotsFilled: true, // whether dots should be filled or outlined
        r: 3, // (fixed) radius of dots, in pixels (5)
        strokeWidth: 2.5, // stroke width of line, in pixels (5)
        strokeOpacity: 0.4, // stroke opacity of line (0.8)
        tooltipBackground: "white", // background color of tooltip
        tooltipTextColor: "black", // text color of tooltip
        strokeLinecap: "round", // stroke line cap of the line
        strokeLinejoin: "round", // stroke line join of the line
    });

    // Update width-dependant properties of the chart when the width of the window is updated, update properties modified by the user
    function updateProps(width, graphTitle, yLabel, selectedUnit) {
        $props.width = width;
        $props.height = Math.round(0.4 * width);
        $props.xScalefactor = width / 80;
        $props.yScalefactor = Math.round(0.4 * width) / 40;
        $props.title = graphTitle;
        $props.yLabel = "↑ " + yLabel + " (" + selectedUnit + ")";
        $props.yFormat = selectedUnit;}

    const width = writable(600); // the outer width of the chart, in pixels (600 by default)

    $: width.set(Math.round(content_width - (15 + 10 + 10 + 15))); // Update the width of the chart when the content width is updated, counting out margins of inner contents
    $: updateProps($width, graphTitle, yLabel, selectedUnit); // Update props when needed


    let svgRef = null; // Reference to the SVG element of the graphic, updated by Graphic component when mounted
    function downloadSvg() {
        if (svgRef) {
            const htmlStr = svgRef.outerHTML; // Get the SVG element as an HTML string
            const blob = new Blob([htmlStr], { type: "image/svg+xml" }); // Create a blob from the HTML string

            const url = URL.createObjectURL(blob); // Create a URL linked the blob
            const a = document.createElement("a"); // Create an anchor element (like a button link that can be clicked to access the URL)
            a.setAttribute("download", "chart.svg"); // Set the download attribute to the anchor element to download the file as chart.svg
            a.setAttribute("href", url); // Set the href attribute to the anchor element to link the URL
            a.style.display = "none"; // Hide the anchor element to prevent it from being displayed on the page
            document.body.appendChild(a); // Add the anchor element to the body of the page
            a.click(); // Simulate a click on the anchor element to download the file
            a.remove(); // Remove the anchor element from the body of the page
            URL.revokeObjectURL(url); // Revoke the URL to free memory
        }
    }
let currentGraph = [];
let graphTitle = "";
let yLabel = "";
let selectedUnit = "";



</script>

<div class="homepage">
    <Banner />
    <div class="body" style="margin-top: {bannerHeight}px;">
        <div class="sidebar">
                <div class="refresh">
                    <Button class="primary" on:click={() => fetchData("records")}>Actualiser</Button>
                </div>
                
                <h2>Données enregistrées</h2>
                {#each $currentRecords as record, index}
                    <Button class="default" on:click={() => {currentGraph = record.data; graphTitle = record.title; yLabel = record.yLabel; selectedUnit = record.yUnit;}}>{record.title}</Button>
                {/each}

                <div class='delete'>
                    <Button class = "primary" on:click={() => sendEraseRequest(record_names)}>Supprimer les enregistrements</Button>
                </div>
        </div>
        <div class = "content">
                <div style:width=100%>
                    {#key $props && currentGraph}
                        {#if $props.width !== 0 && currentGraph.length > 0}
                            <Graphic props={$props} bind:svgRef={svgRef} data={currentGraph}/>
                        {/if}
                    {/key}
                </div>
        </div>
    </div>
</div>

<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    .refresh, .delete{
        margin-top: 5%;
        margin-bottom: 5%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .homepage {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .body {
        margin: 2%;
        display: flex;
        width: 96%;
        height: 100%;
        font-family: "Roboto", sans-serif;
    }

    .sidebar {
        width: 30%;
        padding: 20px;
        background-color: #ffd7c9;
        border-radius: 10px;
        margin-right: 2%;
    }

    .sidebar h2 {
        margin-bottom: 20px;
        font-weight: bold;
    }

    .select-group, .input-group {
        width: 100%;
        margin-bottom: 15px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .select-group label, .input-group label {
        font-weight: bold;
        margin-bottom: 5px;
    }

    select, input {
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    .module-entry {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #fff;
        padding: 8px;
        margin-bottom: 5px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }

    .module-entry .slot-id {
        font-weight: bold;
        color: #ff662e;
    }

    .module-entry .module-name {
        flex-grow: 1;
        margin-left: 10px;
    }

    .content {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        overflow: auto;
        height: 100%;
        width: 60%;
    }

    .toolbar {
        display: flex;
        flex-direction: column;
        gap: 1%;
        margin-top: 2%;
    }

    .toolbar-row {
        display: flex;
        justify-content: center;
        gap: 2%;
    }

    .tool-btn {
        display: flex;
        align-items: center;
        background-color: #ff662e;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 15px;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.2s ease-in-out;
        min-width: 120px;
    }

    .tool-btn:hover {
        background-color: #e65528;
    }

    .tool-btn:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }

    .icon {
        font-size: 1.2em;
        margin-right: 8px;
    }

    .command-row {
        margin-top: 2%;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        flex-grow: 1;
        overflow: hidden;
    }

    .command-row-element {
        flex-shrink: 0;
        overflow-y: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .control-container {
        width: 100%;
        padding: 2%;
        background-color: #a8a8a8;
        border-radius: 5%;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .keyboard {
        width: 95%;
        height: 95%;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: auto auto auto;
    }

    .pad_controller {
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        display: var(--displayGamepad);
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .titles {
        font-weight: bold;
        font-size: 24px;
        color: black;
        font-family: "Roboto", sans-serif;
    }

    span {
        color: black;
    }

    .key {
        background-color: #ff662e;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 6px;
        border-radius: 6px;
        white-space: pre-line;
        height: auto;
        line-height: 1;
        font-family: "Roboto", sans-serif;
    }

    .key .first-line {
        font-weight: bold;
        font-size: 24px;
    }

    .key .second-line {
        font-size: 16px;
    }

    /*Permet de changer le style lorsque qu'une touche du clavier est pressée */
    .key.active {
        background-color: #239e99;
        color: white;
    }

    .battery-lvl-container {
        display: flex;
        flex-direction: column;
    }

    .battery {
        position: relative;
        display: flex;
        align-items: center;
    }

    .battery-bar {
        position: relative;
        width: 135px;
        height: 50px;
        background-color: #494949;
        border: black solid 3px;
        border-radius: 10px;
        overflow: hidden;
    }

    .battery-level {
        height: 100%;
        background-color: #ff662e;
        width: 0;
        transition: width 0.5s;
    }

    .battery-text {
        position: absolute;
        top: 50%;
        left: 20px;
        transform: translateY(-50%);
        font-family: "Roboto", sans-serif;
        color: white;
        font-weight: bold;
        padding-bottom: 3px;
        display: flex;
        justify-content: left;
    }

    .battery-shape {
        width: 10px;
        height: 30px;
        background-color: black;
        border-radius: 4px;
        margin-left: 3px;
    }
</style>