<script>
    import { onMount } from "svelte";
    import { writable, derived } from "svelte/store";
    import { curveLinear, scaleLinear, scaleUtc } from "d3";

    import Banner from "../Banner.svelte";
    import Graphic from "./Graphic.svelte";







    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// Definitions and actions about graphic data
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    import { connected_modules } from "../data_store"; // Import connected modules from data store to select the ones for the graphic
    import { batteries_data, power_infos } from "../data_store"; // Import data from data store. This data is updated every 1000ms

    // Data to display in the graphic, one subset per slot id
    // List updated by updateData function, starting when a characteristic is selected and then every period seconds until playing is true
    const data_array = writable([{"id": 1, "data": []}, {"id": 2, "data": []}, {"id": 3, "data": []}, {"id": 4, "data": []}, {"id": 5, "data": []}, {"id": 6, "data": []}, {"id": 7, "data": []}, {"id": 8, "data": []}, {"id": 9, "data": []}, {"id": 10, "data": []}, {"id": 11, "data": []}, {"id": 12, "data": []}]);

    const nb_data_points = writable(0); ; // Number of data points in the graphic

    let task_queue = []; // List of data fetching tasks

    let playing = false; // When true, data fetching loop is running, graphic is updating
    let paused = false; // When true, data fetching loop is paused, graphic is not updating, when playing is true again, data fetching restarts, keeping old values
    let stopped = false; // Data fetching loop is stoped, graphic is not updating, and data is cleaned before restarting
    
    // List of connected modules sorted by slot id and represented by a null if no module is connected
    // List updated by updateAvailableModules function every time connected_modules is updated (every 1000ms)
    const availableModules = writable(new Array(12).fill(null));
    // List of modules beyond available modules selected to be displayed in the graphic
    const selectedModules = writable([]);
    // List storing for each slot id (array index +1) if its module is selected or not
    const checkbox_inputs = writable(new Array(12).fill(false));

    // List of each possible characteristic for the modules, their names and units
    const allCharacteristics = {
        power_flow: ["Puissance","W"],
        energy: ["Energie","J"],
        state_of_charge: ["Etat de charge","%"],
        current: ["Courant","A"],
        temperature: ["Température","°C"],
        cell_voltages: ["Tension des cellules","V"],
    }
    // List of characteristics that are common to all selected modules.
    // List updated by updateAvailableCharacteristics function every time selected_modules is updated
    const availableCharacteristics = writable([]);
    // Common characteristic between selected modules, selected by the user to be displayed in the graphic
    const selectedCharacteristic = writable("");
    // Unit associated with the selected characteristic, can be modified by the user
    const selectedUnit = writable("");
    // Label of the Y axis, can be modified by the user
    const yLabel = writable("Y label");
    // Title of the graphic, can be modified by the user
    const graphTitle = writable("Titre du graphique");
    // Period of data fetching (in s), can be modified by the user if superior to 1s
    const period = writable(1);

    // Clean graphic data store
    function cleanData() {
        data_array.set([{"id": 1, "data": []}, {"id": 2, "data": []}, {"id": 3, "data": []}, {"id": 4, "data": []}, {"id": 5, "data": []}, {"id": 6, "data": []}, {"id": 7, "data": []}, {"id": 8, "data": []}, {"id": 9, "data": []}, {"id": 10, "data": []}, {"id": 11, "data": []}, {"id": 12, "data": []}]);
    }

    // Update data displayed in the graphic if playing is true and a characteristic is selected, then restart the function after period seconds. Break the loop if stopped is true
    function updateData() {
        const char = $selectedCharacteristic; // Get the selected characteristic
        if (stopped || !char || char === "") return; // If stopped is true or no characteristic is selected, do nothing and break the loop

        if (playing) { // Update data only if playing is true (and paused and stopped are false)
            let data_to_fetch = (char === "power_flow" || char === "energy") ? $power_infos : $batteries_data; // Select the store to get the data from, accordingly to the selected characteristic
            let selected_infos = data_to_fetch.filter((mod) => $checkbox_inputs[mod.slot_id-1]); // Get the data of the selected modules
            selected_infos.forEach(module => {
                $data_array[module.slot_id-1].data.push({date: new Date(), measured_value: module[char]}); // Add the data of the selected modules to the data array
            });
            nb_data_points.set($data_array.reduce((acc, dataset) => acc + dataset.data.length, 0)); // Update the number of data points in the graphic
        }

        if (!stopped) task_queue.push(setTimeout(() => updateData(), $period * 1000)); // If stopped is still false, restart the function after period seconds (add the task to the queue)
    }

    // Handle Play/Pause button click
    function togglePlayPause() {
        if (playing) { playing = false; paused = true; } 
        else {
            if (stopped) { restartGraph(); }
            playing = true; paused = false;
        }
    }
    // Handle Stop button click
    function stopGraph() { playing = false; paused = false; stopped = true; }

    // Handle Restart button click
    function restartGraph() { 
        playing = false; stopped = true; // Stop the data fetching loop
        task_queue.forEach(task => {
            clearTimeout(task); // Clear all the tasks in the queue to prevent them from restarting the data fetching loop            
        });
        task_queue = []; // Empty the queue
        cleanData(); // Clear data displayed in the graphic
        playing = true; paused = false; stopped = false;
        updateData(); // Allow to restart the data fetching loop
    }


    // Update available modules list when connected modules are updated
    // connected_modules is an array of 12 objects representing the connected modules
    // Each object has a slot_id (its position in the array, slot_id = index + 1) and a characteristics array (among other properties)
    // If no module is connected at a slot_id, the correseponding object (array[slot_id -1]) is has a slot of 32 and an empty characteristics array
    function updateAvailableModules(connected_modules) {
        if (connected_modules.length !== 12) return; // If connected_modules is not fully fetched from backend yet, do nothing

        let current_modules = [...$availableModules]; // Store list of modules currently displayed as available to compare with updated connected_modules
        for (let index = 0; index < 12; index++) {
            const element = current_modules[index]; // Current module displayed as available at slot id = index + 1
            if (element === null || element.module_id !== connected_modules[index].module_id ) { // If the module displayed have a module id different from the one of the module connected at this slot id we have to update
                selectedModules.set($selectedModules.filter((mod) => mod["slot_id"] !== index+1)); // Remove the former module from the selected modules list
                $checkbox_inputs[index] = false; // Uncheck the checkbox associated with the former module
                current_modules[index] = connected_modules[index]; // Update the store of the module displayed as available at this slot id
                availableModules.set(current_modules); // Update the list of available modules with the new one
            }
        }
    }

    // Update available modules list each time connected modules are updated
    $: connected_modules && updateAvailableModules($connected_modules);

    // Update checkbox inputs when selected modules are updated
    selectedModules.subscribe(value => {
        for (let index = 0; index < 12; index++) {
            const selected = value.find(module => module.slot_id === index + 1); // Check if the module at slot id = index + 1 is in the selected modules list
            $checkbox_inputs[index] = selected ? true : false; // If the module is in the selected modules list then selected is that module object and we can check the checkbox, otherwise selected is undefined and we uncheck the checkbox
        }
    })

    // Update available characteristics list when selected modules are updated
    // selectedModules is an array of objects representing the selected modules
    // Each object is a module with a slot_id and a characteristics array
    function updateAvailableCharacteristics(selectedModules) {
        if (selectedModules.length === 0) { // If no module is selected, no characteristic is available
            selectedCharacteristic.set(""); // Unselect the characteristic
            restartGraph(); // Clean data and restart the graphic
            return []
        };

        const commonCharacteristics = selectedModules
            .map((mod) => mod.characteristics.filter((c) => Object.keys(allCharacteristics).includes(c))) // Get charachteristics of each selected modules, removing characteristics that are not in allCharacteristics
            .reduce((a, b) => a.filter((c) => b.includes(c))); // Get the common characteristics between result characteristics arrays of the previous map
        availableCharacteristics.set(commonCharacteristics); // Update the list of available characteristics with the new one

        if (!commonCharacteristics.includes($selectedCharacteristic)) { // If the selected characteristic is not in the new list of available characteristics
            selectedCharacteristic.set(""); // Unselect the characteristic
            restartGraph(); // Clean data and restart the graphic
        }
    };

    // Update available characteristics list each time selected modules are updated
    $: selectedModules && updateAvailableCharacteristics($selectedModules);

    // When a characteristic is selected, update the data displayed in the graphic
    selectedCharacteristic.subscribe((char) => {
        if (char && char !== "") { // If a characteristic is selected
            const [char_name, char_unit] = allCharacteristics[char]; // Get the name and unit of the selected characteristic
            yLabel.set(char_name); // Update the Y axis label with the name of the characteristic
            selectedUnit.set(char_unit); // Update the unit of the characteristic
            graphTitle.set(`${char_name} (${char_unit}) en fonction du temps`); // Update the title of the graphic
            period.set(1); // Reset the period of data fetching to 1s
        }
        else {
            yLabel.set("Y label");
            selectedUnit.set("");
            graphTitle.set("Titre du graphique");
            period.set(1);
        }
        restartGraph(); // Stop data fetching loop, clear data and restart data fetching loop
    });
    


    import { sendGraphicData } from "../data_store";
    // Handle Enregistrer button click
    function saveData() {
        const now = new Date(); // Get the current date
        console.log(now);
        sendGraphicData({ // Send the data to the backend to save the record
            date: now,
            title: $graphTitle,
            yLabel: $yLabel,
            yUnit: $selectedUnit,
            data: $data_array,
        });
        alert("Données enregistrées !"); // Alert the user that the data is saved
    }

    // Handle Exporter button click
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






    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// Set graphic properties
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // Store banner height to adjust the top margin of the content under it
    let bannerHeight = 0;
    // Store content width to adjust the graphic dimensions
    let content_width = 0;
    onMount( () => {
        const banner = document.querySelector(".banner");
        if (banner) bannerHeight = banner.offsetHeight;

        const content = document.querySelector(".content");
        if (content) content_width = content.clientWidth;
    })


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
    $: updateProps($width, $graphTitle, $yLabel, $selectedUnit); // Update props when needed
        
 
  


    
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// Handle keyboard and gamepad commands, battery level display, as in RobotInfos.svelte
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    import Controller from "../Controller.svelte";
    import { is_gamepad_connected, batteries } from "../data_store";

    import { sendMoveData } from "../data_store";

    //Booleans representing the state of the a, z, e, q, s and d keys of the keyboard
    let isActiveKeyA = false, isActiveKeyZ = false, isActiveKeyE = false, isActiveKeyQ = false, isActiveKeyS = false, isActiveKeyD = false;

    //Handle keydown event to send move data to the backend if a, z, e, q, s or d keys are pressed
    function handleKeyDown(event) {
        switch (event.key.toLowerCase()) {
            case "z":
                isActiveKeyZ = true;
                break;

            case "a":
                isActiveKeyA = true;
                break;

            case "e":
                isActiveKeyE = true;
                break;
            
            case "q":
                isActiveKeyQ = true;
                break;

            case "s":
                isActiveKeyS = true;
                break;

            case "d":
                isActiveKeyD = true;
                break;
        
            default:
                break;
        }
        if ( ["z","a","e","q","s","d"].includes(event.key.toLowerCase()) ) {
            sendMoveData({
                x_linear_vel: isActiveKeyZ ? 1 : isActiveKeyS ? -1 : 0,
                y_linear_vel: isActiveKeyQ ? 1 : isActiveKeyD ? -1 : 0,
                angular_vel: isActiveKeyA ? 1 : isActiveKeyE ? -1 : 0,
            });
        }
    }
    // Handle keyup event to send move data to the backend if a, z, e, q, s or d keys are released
    function handleKeyUp(event) {
        switch (event.key.toLowerCase()) {
            case "z":
                isActiveKeyZ = false;
                break;

            case "a":
                isActiveKeyA = false;
                break;

            case "e":
                isActiveKeyE = false;
                break;

            case "q":
                isActiveKeyQ = false;
                break;

            case "s":
                isActiveKeyS = false;
                break;

            case "d":
                isActiveKeyD = false;
                break;

            default:
                break;
        }
        if ( ["z","a","e","q","s","d"].includes(event.key.toLowerCase()) ) {
            sendMoveData({
                x_linear_vel: isActiveKeyZ ? 1 : isActiveKeyS ? -1 : 0,
                y_linear_vel: isActiveKeyQ ? 1 : isActiveKeyD ? -1 : 0,
                angular_vel: isActiveKeyA ? 1 : isActiveKeyE ? -1 : 0,
            });
        }
    }

    // Add event listeners to handle keyboard commands, remove it when the page component is destroyed
    onMount(async () => {
        window.addEventListener("keydown", handleKeyDown);
        window.addEventListener("keyup", handleKeyUp);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
            window.removeEventListener("keyup", handleKeyUp);
        };
    });
</script>












<svelte:window
    on:gamepadconnected={(e) => {
        is_gamepad_connected.set(true);
    }}
    on:gamepaddisconnected={(e) => {
        is_gamepad_connected.set(false);
    }}
/>


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
                            {#if allCharacteristics[char]}
                                <option value={char}>{allCharacteristics[char][0]}</option>
                            {/if}
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

                <div class="input-group">
                    <label for="period">Période (en s) :</label>
                    <input type="number" min=1 bind:value={$period} />
                </div>
            
                <h2 style:margin-top=5px>Modules</h2>
                {#key $availableModules}
                {#each $availableModules as module, index}
                    {#if module !== null && module.characteristics.length > 0}
                        <div class="module-entry">
                            <span class="slot-id">Slot {index + 1}</span>
                            <span class="module-name">{module.name}</span>
                            <input 
                                type="checkbox" 
                                bind:group={$selectedModules}
                                bind:checked={$checkbox_inputs[index]}
                                value={{"slot_id": index+1, ...module}} 
                            />
                        </div>
                    {/if}
                {/each}
                {/key}
        </div>


        <div
            class="content"
            bind:clientWidth={content_width}
        >
            <div style:width=100%>
            {#key $props}
                {#if $props.width !== 0 && $selectedCharacteristic !== "" && $data_array && $nb_data_points > 0}
                    {#key $nb_data_points}
                        <Graphic props={$props} bind:svgRef={svgRef} data={$data_array}/>
                    {/key}

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
            


            <div class="command-row" style:width=100%>
                <div class="command-row-element" style:width=50%>
                    <div class="control-container">
                        <p class="titles">COMMANDES</p>
                        {#if !$is_gamepad_connected}
                            <div class="keyboard">
                                <div class="key {isActiveKeyA ? 'active' : ''}">
                                    <!--vérification de si la touche est pressée -->
                                    <span class="first-line">A</span><br />
                                    <span class="second-line">Rotation G</span>
                                </div>
                                <div class="key {isActiveKeyZ ? 'active' : ''}">
                                    <span class="first-line">Z</span><br />
                                    <span class="second-line">Avancer</span>
                                </div>
                                <div class="key {isActiveKeyE ? 'active' : ''}">
                                    <span class="first-line">E</span><br />
                                    <span class="second-line">Rotation D</span>
                                </div>
                                <div class="key {isActiveKeyQ ? 'active' : ''}">
                                    <span class="first-line">Q</span><br />
                                    <span class="second-line">Gauche</span>
                                </div>
                                <div class="key {isActiveKeyS ? 'active' : ''}">
                                    <span class="first-line">S</span><br />
                                    <span class="second-line">Reculer</span>
                                </div>
                                <div class="key {isActiveKeyD ? 'active' : ''}">
                                    <span class="first-line">D</span><br />
                                    <span class="second-line">Droite</span>
                                </div>
                            </div>
                        {/if}
                        <div
                            class="pad_controller"
                            style="--displayGamepad:{$is_gamepad_connected ? 'flex' : 'none'};"
                        >
                            <Controller />
                        </div>
                    </div>
                </div>
                
                <div class="command-row-element" style:width=50%>
                    <div class="battery-lvl-container">
                        {#each Object.entries($batteries) as [battery_slot, battery]}
                            <h1 class="titles">{battery["name"]}</h1>
                            <div class="battery">
                                <div class="battery-bar">
                                    <!--Actualisation de la barre de batterie selon le niveau de batterie restant dans l'Omnibot-->
                                    <div
                                        class="battery-level"
                                        style="width: {battery['state_of_charge']}%"
                                    ></div>
                                    <div class="battery-text">
                                        {battery["state_of_charge"]}%
                                    </div>
                                </div>
                                <div class="battery-shape"></div>
                            </div>
                        {/each}
                    </div>
                </div>
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
