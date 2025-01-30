<script>
    import { onMount } from "svelte";
    import { writable, derived } from "svelte/store";
    import Banner from "../Banner.svelte";
    import Graphic from "./Graphic.svelte";

    
    import {data, connected_modules} from "./data.js";

    import { backend_host, backend_port } from "../../config.js";
    
    // // Send a request to the backend to get the data
    // async function fetchData(endpoint, store) {
    //     try {
    //         console.log(`Fetching ${endpoint.split("fetch_")[1]} ...`);
    //         const response = await fetch(endpoint); // Send a request to the backend
    //         const data = await response.json(endpoint); // Parse response and get data as a JSON object
    //         // console.log(data);
    //         if (data.ok === true) {
    //             store.set(data.data); // Set the store with the data received
    //         } else {
    //             console.error("Error:", data.error);
    //             store.set(data.default); // Set the store with the default value
    //         }
    //     } catch (error) {
    //         console.error("Error:", error);
    //         store.set([]); // Set the store with an empty array
    //     }
    // }


    // const power_infos = writable([]);
    // const data = writable({});
    // const data_array = writable([]);

    // function updateData(power_infos) {
    //     console.log("Power_infos ",power_infos);
    //     power_infos.forEach(module => {
    //         if ($data[module.slot_id]) {
    //             $data[module.slot_id].push({date: new Date(), power_flow: module.power_flow});
    //         } else {
    //             $data[module.slot_id] = [{date: new Date(), power_flow: module.power_flow}];
    //         }
    //         });
    //     data_array.set(Object.entries($data).map(([key, value]) => ({id: key, data: value})));
    //     console.log("Data_array ",$data_array);
    // };

    // $: power_infos && data && data_array && updateData($power_infos);

    const availableModules = writable([]);
    const selectedModules = writable([]); // Liste des modules cochés
    const selectedCharacteristic = writable(""); // Caractéristique choisie
    const selectedUnit = writable(""); // Unité associée
    const yLabel = writable("Y label"); // Légende Y par défaut
    const graphTitle = writable("Titre du graphique"); // Titre du graphique

    const allCharacteristics = {
        power_flow: ["Puissance","W"],
        energy: ["Energie","J"],
        state_of_charge: ["Etat de charge","%"],
        speed: ["Vitesse","m/s"],
        current: ["Courant","A"],
        temperature: ["Température","°C"],
        cell_voltages: ["Tension des cellules","V"],
    }

    if (connected_modules) availableModules.set(connected_modules.filter((mod) => mod.characteristics.length > 0)); // Exclure les modules vides

    // Liste des caractéristiques disponibles en fonction des modules cochés
    const availableCharacteristics = derived(selectedModules, ($selectedModules) => {
        if ($selectedModules.length === 0) return [];

        const commonCharacteristics = $selectedModules
            .map((mod) => mod.characteristics.filter((c) => c !== "name" && c !== "state"))
            .reduce((a, b) => a.filter((c) => b.includes(c)));

        return commonCharacteristics;
    });

    // Met à jour l'unité lorsqu'on change la caractéristique
    selectedCharacteristic.subscribe((char) => {
        if (char && allCharacteristics[char]) {
            console.log(allCharacteristics[char]);
            yLabel.set(allCharacteristics[char][0] || "");
            selectedUnit.set(allCharacteristics[char][1] || "");
        }
    });


    // selectedModules.subscribe((modules) => {
    //     if (modules.length === 0) {
    //         selectedCharacteristic.set("");
    //     }
    // });




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
        // const interval = setInterval(() => {fetchData(`http://${backend_host}:${backend_port}/fetch_power_infos`, power_infos);},5000);

        // return () => {
        //     clearInterval(interval);
        // };
    });



    import { curveLinear, scaleLinear, scaleUtc } from "d3";

    const width = writable(0); // the outer width of the chart, in pixels (600)
    let height = 0; // the outer height of the chart, in pixels (350)
    $: height = Math.round(0.4 * $width);

    const props = writable({}); // the properties of the chart
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

        // Number of colors array elements must match number of data sets (or be superior)
        colors: [
            "#FF662E", // Orange vif
            "#E42618", // Rouge profond
            "#239E99", // Bleu-vert
            "#A04040", // Marron rougeâtre
            "#4B1338", // Bordeaux foncé
            "#656780", // Gris bleuté
            "#FFB400", // Jaune doré
            "#0A9D58", // Vert foncé
            "#0085C7", // Bleu vif
            "#C724B1", // Violet magenta
            "#795548", // Brun terreux
            "#1E1E1E", // Gris anthracite
        ], // fill color for dots && number of colors in fill array MUST match number of subsets in data ("#F50057","#42A5F5","#26A69A","#9575CD"])

        // Inner style
        horizontalGrid: true, // show horizontal grid lines
        verticalGrid: true, // show vertical grid lines
        showDots: true, // whether dots should be displayed or not
        dotsFilled: true, // whether dots should be filled or outlined
        r: 4, // (fixed) radius of dots, in pixels (5)
        strokeWidth: 3, // stroke width of line, in pixels (5)
        strokeOpacity: 0.4, // stroke opacity of line (0.8)
        tooltipBackground: "white", // background color of tooltip
        tooltipTextColor: "black", // text color of tooltip
        strokeLinecap: "round", // stroke line cap of the line
        strokeLinejoin: "round", // stroke line join of the line
    });

    function updateProps(width, graphTitle, yLabel, selectedUnit) {
        $props.width = width;
        $props.height = Math.round(0.4 * width);
        $props.xScalefactor = width / 80;
        $props.yScalefactor = Math.round(0.4 * width) / 40;
        $props.title = graphTitle;
        $props.yLabel = "↑ " + yLabel + " (" + selectedUnit + ")";
        $props.yFormat = selectedUnit;}

    $: updateProps($width, $graphTitle, $yLabel, $selectedUnit);
        

    function calculateGraphicDimensions(content_width, content_height) {
        if (content_width > 0) {
            props.width = Math.round(content_width - (15 + 10 + 10 + 15));
            props.height = Math.round(0.4 * props.width);
            props.xScalefactor = props.width / 80;
            props.yScalefactor = props.height / 40;
            width.set(props.width);
        }
    }

    $: calculateGraphicDimensions(content_width, content_height);





    
    let svgRef = null;

    function downloadSvg() {
        console.log("svgRef", svgRef);
        if (svgRef) {
            const htmlStr = svgRef.outerHTML;
            const blob = new Blob([htmlStr], { type: "image/svg+xml" });

            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.setAttribute("download", "chart.svg");
            a.setAttribute("href", url);
            a.style.display = "none";
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        }
    }

    let playing = false;
    let paused = false;
    let stopped = false;

    function togglePlayPause() {
        if (playing) {
            playing = false;
            paused = true;
        } else {
            playing = true;
            paused = false;
            stopped = false;
        }
    }

    function stopGraph() {
        playing = false;
        paused = false;
        stopped = true;
    }

    function restartGraph() {
        playing = true;
        paused = false;
        stopped = false;
    }

    function saveData() {
        console.log("Données enregistrées !");
    }
</script>














<div class="homepage">
    <Banner />
    <div class="body" style="margin-top: {bannerHeight}px;">
        <div class="sidebar">
                <h2>Caractéristique</h2>
                <div class="select-group">
                    <label for="variable">Variable :</label>
                    <select bind:value={$selectedCharacteristic}>
                        <option value="" disabled>Choisir une caractéristique</option>
                        {#each $availableCharacteristics as char}
                            <option value={char}>{char}</option>
                        {/each}
                    </select>
                </div>
            
                <div class="input-group">
                    <label for="unit">Unité :</label>
                    <input type="text" bind:value={$selectedUnit} />
                </div>
            
                <div class="input-group">
                    <label for="yLabel">Légende Y :</label>
                    <input type="text" bind:value={$yLabel} />
                </div>
            
                <div class="input-group">
                    <label for="title">Titre du graphique :</label>
                    <input type="text" bind:value={$graphTitle} />
                </div>
            
                <h2>Modules</h2>
                {#each $availableModules as module, index}
                    <div class="module-entry">
                        <span class="slot-id">Slot {index + 1}</span>
                        <span class="module-name">{module.name}</span>
                        <input 
                            type="checkbox" 
                            bind:group={$selectedModules} 
                            value={module} 
                        />
                    </div>
                {/each}      
        </div>


        <div
            class="content"
            bind:clientWidth={content_width}
            bind:clientHeight={content_height}
        >
            {#key $props}
                {#if $props.width !== 0 && $selectedCharacteristic !== ""}
                    <Graphic props={$props} bind:svgRef={svgRef} data={data}/>

                    <!-- Barre d'outils -->
                    <div class="toolbar">
                        <div class="toolbar-row">
                            <button class="tool-btn" on:click={togglePlayPause}>
                                <span class="icon">{playing ? "⏸️" : "▶️"}</span
                                >
                                <span class="label"
                                    >{playing ? "Pause" : "Start"}</span
                                >
                            </button>

                            <button
                                class="tool-btn"
                                on:click={stopGraph}
                                disabled={!playing && !paused}
                            >
                                <span class="icon">⏹️</span>
                                <span class="label">Stop</span>
                            </button>

                            <button class="tool-btn" on:click={restartGraph}>
                                <span class="icon">🔄</span>
                                <span class="label">Restart</span>
                            </button>

                            <button
                                class="tool-btn"
                                on:click={saveData}
                                disabled={!paused && !stopped}
                            >
                                <span class="icon">💾</span>
                                <span class="label">Enregistrer</span>
                            </button>

                            <button
                                class="tool-btn"
                                on:click={downloadSvg}
                                disabled={!paused && !stopped}
                            >
                                <span class="icon">📤</span>
                                <span class="label">Exporter</span>
                            </button>
                        </div>
                    </div>
                {:else}
                    <p>Choisir un ou plusieurs modules ainsi que la caractéristique commune à afficher</p>
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
</style>
