<script>
    import { onMount } from "svelte";
    import { writable, derived } from "svelte/store";
    import Banner from "../Banner.svelte";
    import Graphic from "./Graphic.svelte";

    
    const data = writable({1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []});
    const data_array = writable([]);
    const checkbox_inputs = writable(new Array(12).fill(false));

    
    let playing = false;
    let paused = false;
    let stopped = false;

    import { connected_modules } from "../data_store";

    const availableModules = writable(new Array(12).fill(null)); // Liste des modules connectés
    const selectedModules = writable([]); // Liste des modules cochés
    const selectedCharacteristic = writable(""); // Caractéristique choisie
    const selectedUnit = writable(""); // Unité associée
    const yLabel = writable("Y label"); // Légende Y par défaut
    const graphTitle = writable("Titre du graphique"); // Titre du graphique
    const period = writable(1000); // Période de rafraîchissement des données

    const allCharacteristics = {
        power_flow: ["Puissance","W"],
        energy: ["Energie","J"],
        state_of_charge: ["Etat de charge","%"],
        speed: ["Vitesse","m/s"],
        current: ["Courant","A"],
        temperature: ["Température","°C"],
        cell_voltages: ["Tension des cellules","V"],
    }

    function updateAvailableModules(connected_modules) {
        if (connected_modules.length !== 12) return;
        let current_modules = [...$availableModules];
        for (let index = 0; index < 12; index++) {
            const element = current_modules[index];
            if (element !== connected_modules[index] ) {
                current_modules[index] = connected_modules[index];
                availableModules.set(current_modules);
                if (connected_modules[index].characteristics.length === 0) {
                    selectedModules.set($selectedModules.filter((mod) => mod["slot_id"] !== index+1));
                    $checkbox_inputs[index] = false;
                }
            }
        }
    }

    $: connected_modules && updateAvailableModules($connected_modules);

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
            yLabel.set(allCharacteristics[char][0]);
            selectedUnit.set(allCharacteristics[char][1]);
            graphTitle.set(`${allCharacteristics[char][0]} (${allCharacteristics[char][1]}) en fonction du temps`);
            period.set(1000);
            playing = true;
        }
        else {
            yLabel.set("Y label");
            selectedUnit.set("");
            graphTitle.set("Titre du graphique");
            period.set(1000);
            if (data) restartGraph();
        }
    });


    availableCharacteristics.subscribe((value) => {
        if (!value.includes($selectedCharacteristic)) {
            selectedCharacteristic.set("");
            if (data) restartGraph();
        }
    });


    selectedModules.subscribe(value => {
        for (let index = 0; index < 12; index++) {
            const selected = value.find(module => module.slot_id === index + 1);
            $checkbox_inputs[index] = selected ? true : false;
        }
    })


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



    import { curveLinear, scaleLinear, scaleUtc } from "d3";

    const props = writable({}); // the properties of the chart (and default values)
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


    const width = writable(0); // the outer width of the chart, in pixels (600 by default)

    $: width.set(Math.round(content_width - (15 + 10 + 10 + 15)));
    $: updateProps($width, $graphTitle, $yLabel, $selectedUnit);
        



    import { power_infos } from "../data_store";


    function updateData(power_infos) {
        if (!playing) return;

        let selected_infos = power_infos.filter((mod) => $checkbox_inputs[mod.slot_id-1]);
        selected_infos.forEach(module => {
            $data[module.slot_id].push({date: new Date(), power_flow: module.power_flow});
        });
        data_array.set(Object.entries($data).map(([key, value]) => ({id: key, data: value})));
    };

    $: power_infos && data && data_array && updateData($power_infos);



    

    function togglePlayPause() {
        if (playing) {
            playing = false;
            paused = true;
        } else {
            if (stopped) {
                restartGraph();
            }
            else {
                playing = true;
                paused = false;
                stopped = false;
            }
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
        data.set({1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []});
        updateData($power_infos);
    }

    import { graphic_saved_data } from "../data_store";
    function saveData() {
        const now = new Date();
        console.log(now);
        $graphic_saved_data[now] = $data_array;
        alert("Données enregistrées !");
    }

    let svgRef = null;

    function downloadSvg() {
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





    import Controller from "../Controller.svelte";
    import { is_gamepad_connected, batteries } from "../data_store";

    import { sendMoveData } from "../data_store";

    //Creation de booléens pour savoir si une touche du clavier est pressée
    let isActiveKeyA = false, isActiveKeyZ = false, isActiveKeyE = false, isActiveKeyQ = false, isActiveKeyS = false, isActiveKeyD = false;

    //Fonctions permettant de savoir si la touche est pressée ou non
    function handleKeyDown(event) {
        if (event.key.toLowerCase() === "z") {
            isActiveKeyZ = true;
        }
        if (event.key.toLowerCase() === "a") {
            isActiveKeyA = true;
        }
        if (event.key.toLowerCase() === "e") {
            isActiveKeyE = true;
        }
        if (event.key.toLowerCase() === "s") {
            isActiveKeyS = true;
        }
        if (event.key.toLowerCase() === "q") {
            isActiveKeyQ = true;
        }
        if (event.key.toLowerCase() === "d") {
            isActiveKeyD = true;
        }
        if (
            isActiveKeyZ ||
            isActiveKeyS ||
            isActiveKeyQ ||
            isActiveKeyD ||
            isActiveKeyA ||
            isActiveKeyE
        ) {
            sendMoveData({
                x_linear_vel: isActiveKeyZ ? 1 : isActiveKeyS ? -1 : 0,
                y_linear_vel: isActiveKeyQ ? 1 : isActiveKeyD ? -1 : 0,
                angular_vel: isActiveKeyA ? 1 : isActiveKeyE ? -1 : 0,
            });
        }
    }

    function handleKeyUp(event) {
        if (event.key.toLowerCase() === "z") {
            isActiveKeyZ = false;
        }
        if (event.key.toLowerCase() === "a") {
            isActiveKeyA = false;
        }
        if (event.key.toLowerCase() === "e") {
            isActiveKeyE = false;
        }
        if (event.key.toLowerCase() === "q") {
            isActiveKeyQ = false;
        }
        if (event.key.toLowerCase() === "s") {
            isActiveKeyS = false;
        }
        if (event.key.toLowerCase() === "d") {
            isActiveKeyD = false;
        }
        if (
            !(
                isActiveKeyZ ||
                isActiveKeyS ||
                isActiveKeyQ ||
                isActiveKeyD ||
                isActiveKeyA ||
                isActiveKeyE
            )
        ) {
            sendMoveData({
                x_linear_vel: isActiveKeyZ ? 1 : isActiveKeyS ? -1 : 0,
                y_linear_vel: isActiveKeyQ ? 1 : isActiveKeyD ? -1 : 0,
                angular_vel: isActiveKeyA ? 1 : isActiveKeyE ? -1 : 0,
            });
        }
    }

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
                    <label for="period">Période (en ms) :</label>
                    <input type="rnumber" min=50 bind:value={$period} />
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
                {#if $props.width !== 0 && $selectedCharacteristic !== "" && $data_array.length > 0}
                    {#key $data_array}
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
