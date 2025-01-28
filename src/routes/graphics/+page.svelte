<script>
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import Banner from "../Banner.svelte";
    import Graphic from "./Graphic.svelte";

    import { backend_host, backend_port } from "../../config.js";

    const power_infos = writable([]);
    const data = writable({});
    const data_array = writable([]);

    function updateData(power_infos) {
        power_infos.forEach(module => {
            if ($data[module.slot_id]) {
                $data[module.slot_id].push({date: new Date(), power_flow: module.power_flow});
            } else {
                $data[module.slot_id] = [{date: new Date(), power_flow: module.power_flow}];
            }
            });
        data_array.set(Object.entries($data).map(([key, value]) => ({id: key, data: value})));
        console.log("Data_array ",$data_array);
    };

    $: power_infos && data && data_array && updateData($power_infos);

    // Send a request to the backend to get the data
    async function fetchData(endpoint, store) {
        try {
            console.log(`Fetching ${endpoint.split("fetch_")[1]} ...`);
            const response = await fetch(endpoint); // Send a request to the backend
            const data = await response.json(endpoint); // Parse response and get data as a JSON object
            // console.log(data);
            if (data.ok === true) {
                store.set(data.data); // Set the store with the data received
            } else {
                console.error("Error:", data.error);
                store.set(data.default); // Set the store with the default value
            }
        } catch (error) {
            console.error("Error:", error);
            store.set([]); // Set the store with an empty array
        }
    }

    let bannerHeight = 0;
    let content_width = 0;
    let content_height = 0;

    // Function that runs when the component is mounted
    onMount(async () => {
        // Get banner height to adjust the top margin of the content under it
        const banner = document.querySelector(".banner");
        if (banner) {
            bannerHeight = banner.offsetHeight;
        }

        const content = document.querySelector(".content");
        if (content) {
            content_width = content.offsetWidth;
            content_height = content.offsetHeight;
        }

        // Fetch power_infos data
        // fetchData(`http://${backend_host}:${backend_port}/fetch_power_infos`, power_infos);
        const interval = setInterval(() => {fetchData(`http://${backend_host}:${backend_port}/fetch_power_infos`, power_infos);},5000);

        return () => {
            clearInterval(interval);
        };
    });


    import { curveLinear, scaleLinear, scaleUtc } from 'd3';

    // Global style
    // let marginTop = 15; // the top margin, in pixels (40)
    // let marginRight = 15; // the right margin, in pixels (0)
    // let marginBottom = 15; // the bottom margin, in pixels (30)
    // let marginLeft = 15; // the left margin, in pixels (50)

    const width = writable(0); // the outer width of the chart, in pixels (600)
    let height = 0; // the outer height of the chart, in pixels (350)

    let inset = 0; // inset the default range (padding) (0)
    let insetTop = inset; // inset from top
    let insetRight = inset; // inset from right
    let insetBottom = inset; // inset from bottom
    let insetLeft = inset; // inset from left

    // Labels and formats
    let title = 'Power flow (Watts flowing in (+) or (out) of a component) over time'; // a title for the chart ('')
    let xLabel = '-> time'; // a label for the y-axis ('')
    let yLabel = '↑ Power flow (Watts)'; // a label for the y-axis
    let xFormat = ''; // a format specifier string for the y-axis
    let yFormat = 'W'; // a format specifier string for the y-axis

    let xType = scaleUtc; // type of x-scale
    let yType = scaleLinear; // type of y-scale

    let xScalefactor = $width / 80; //x-axis number of values
    let yScalefactor = height / 40; //y-axis number of values
    let curve = curveLinear; // method of interpolation between points

    // Number of colors array elements must match number of data sets
    let colors = ["#e42618","#239e99","#a04040","#4B1338", "#4b1338", "#656780"]; // fill color for dots && number of colors in fill array MUST match number of subsets in data ("#F50057","#42A5F5","#26A69A","#9575CD"])

    // Inner style
    let horizontalGrid = true; // show horizontal grid lines
    let verticalGrid = true; // show vertical grid lines
    let showDots = true; // whether dots should be displayed
    let dotsFilled = true; // whether dots should be filled or outlined
    let r = 4; // (fixed) radius of dots, in pixels (5)
    let strokeWidth = 3; // stroke width of line, in pixels (5)
    let strokeOpacity = 0.4; // stroke opacity of line (0.8)
    let tooltipBackground = 'white'; // background color of tooltip
    let tooltipTextColor = 'black'; // text color of tooltip

    let strokeLinecap = 'round'; // stroke line cap of the line
    let strokeLinejoin = 'round'; // stroke line join of the line
    
    let props = {
        // marginTop,
        // marginRight,
        // marginBottom,
        marginLeft: 35,
        width: {$width},
        height,
        inset,
        insetTop,
        insetRight,
        insetBottom,
        insetLeft,
        title,
        xLabel,
        yLabel,
        xFormat,
        yFormat,
        xType,
        yType,
        xScalefactor,
        yScalefactor,
        curve,
        colors,
        horizontalGrid,
        verticalGrid,
        showDots,
        dotsFilled,
        r,
        strokeWidth,
        strokeOpacity,
        tooltipBackground,
        tooltipTextColor,
        strokeLinecap,
        strokeLinejoin
    };

    
    function calculateGraphicDimensions(content_width, content_height) {
        if (content_width > 0) {
            props.width = Math.round(content_width - (15+10+10+15));
            props.height = Math.round(0.4*props.width);
            props.xScalefactor = props.width / 80;
            props.yScalefactor = props.height / 40;
            width.set(props.width);
        }
    }

    $: calculateGraphicDimensions(content_width, content_height);
</script>

<div class="homepage">
    <Banner />
    <div class="body" style="margin-top: {bannerHeight}px;">
        <div class="sidebar">
            <h2>Caractéristique</h2>
            <h2>Modules</h2>
        </div>




        <div class="content" bind:clientWidth={content_width} bind:clientHeight={content_height}>
            {#key $width}
                {#if $data_array.length === 0}
                    <p>Loading...</p>
                {:else}
                    {#key $data_array}  
                        <Graphic data={$data_array} props={props}/> 
                    {/key}
                {/if}
            {/key}
        </div>
    </div>
</div>

<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .homepage {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .body {
        margin:2%;
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

   .content {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        overflow: auto;
        height: 100%;
        width: 60%;
    }
    </style>
