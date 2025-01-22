<script>
    import { writable } from "svelte/store"; // Importer la fonction writable
    import {
        selectedTriangle,
        triangleData,
        triangleImages,
        triangleTitle,
    } from "./store"; // Importer le store
    import { onMount } from "svelte";

    let currentContent =
        "Cliquez sur un bloc afin d'avoir les informations lié a celui-ci";
    let currentImage = null;
    let currentTitle = null;

    // Déclaration réactive pour mettre à jour le contenu lorsque selectedTriangle change
    $: {
        const id = $selectedTriangle.id;
        if (id !== null) {
            const module = $triangleData[id]; // module = {slot_id, module_id, functionality, characteristics[]}
            if (module === "Aucun module connecté") {
                currentContent = module;
            }
            else {
                currentContent = {...module, characteristics: {"slot_id": module.slot_id}};
                if (module.characteristics) {
                    (module.characteristics).forEach(characteristic => {
                        currentContent.characteristics[characteristic] = null;
                        if (characteristic === "name") {
                            currentContent.characteristics[characteristic] = module.name;
                        }
                    });
                }
            }
            currentImage = $triangleImages[id];
            currentTitle = $triangleTitle[id];
        } else if (id === 32) {
            currentContent = "";
            currentImage = null;
            currentTitle = "Emplacement vide";
        } else {
            currentContent =
                "Cliquez sur un bloc afin d'avoir les informations lié a celui-ci";
            currentImage = null;
            currentTitle = "Aucun bloc sélectionné";
        }
    }

    export let batteries_data;

    const batteries = writable({});

    const BatteryState = [
        "BatteryState_OK",
        "BatteryState_Overcurrent",
        "BatteryState_Overtemperature",
        "BatteryState_Overvoltage",
        "BatteryState_Undertemperature",
        "BatteryState_Undervoltage"
    ];

    function updateBatteryData(batteries_data) {
        $batteries = {};
        if (batteries_data.length > 0) {
            for (const battery_data of batteries_data) {
                $batteries[battery_data.slot_id] = {
                    name: battery_data.name.toUpperCase(),
                    state: BatteryState[battery_data.state],
                    state_of_charge: Math.round(
                        battery_data.state_of_charge * 100,
                    ),
                    current: Math.round(battery_data.current * 100),
                    temperature: Math.round(battery_data.temperature * 100),
                    cell_voltages: battery_data.cell_voltages,
                    power_flow: $batteries[battery_data.slot_id] ? $batteries[battery_data.slot_id].power_flow : 0,
                    energy: $batteries[battery_data.slot_id] ? $batteries[battery_data.slot_id].energy : 0,
                };
            }
        }
    }

    $: batteries_data && updateBatteryData(batteries_data);

    import { backend_host, backend_port } from "../config.js";

    export let fetchData;
    const power_infos = writable([]);

    function fetch_power_infos() {
        fetchData(
            `http://${backend_host}:${backend_port}/fetch_power_infos`,
            power_infos,
        );
    }

    onMount(() => {
        const interval = setInterval(fetch_power_infos, 500);
        return () => clearInterval(interval);
    });

    function updateCurrentContent(power_infos, batteries) {
        if (currentContent.slot_id !== undefined) {
            const power_info = power_infos.find(
                (power_info) => power_info.slot_id === currentContent.slot_id,
            );
            if (power_info !== undefined) {
                currentContent.characteristics.power_flow = (power_info.power_flow).toFixed(2);
                currentContent.characteristics.energy = (power_info.energy).toFixed(2);

                if (currentContent.slot_id in batteries) {
                    batteries[currentContent.slot_id].power_flow = (power_info.power_flow).toFixed(2);
                    batteries[currentContent.slot_id].energy = (power_info.energy).toFixed(2);
                    for(const key in batteries[currentContent.slot_id]){
                        currentContent.characteristics[key] = batteries[currentContent.slot_id][key];
                    }
                }
            }
        }
    }

    $: power_infos && batteries && updateCurrentContent($power_infos, $batteries);
</script>

<div class="info-bloc">
    <div class="info-container">
        <div class="title-container">
            {#if currentImage}
                <div class="image-container">
                    <img
                        src={currentImage}
                        alt="Triangle"
                        class="triangle-image"
                    />
                </div>
            {/if}
            <h1>{currentTitle}</h1>
        </div>
        <div class="content-container">
            {#if currentImage}
                <!-- <p>Slot id : {currentContent.slot_id}</p> -->
                <p>Fonction : {currentContent.functionality}</p>
                <p>Caractéristiques :</p>
                {#if Object.entries(currentContent.characteristics).length > 0}
                    <ul>
                        {#each Object.entries(currentContent.characteristics) as [characteristic, value]}
                            <li>{characteristic} : {(value || value === 0) ? value : "?"}</li>
                        {/each}
                    </ul>
                {:else}
                    <p>Aucune</p>
                {/if}
            {:else}
                <p>{currentContent}</p>
            {/if}
        </div>

        <!-- <div class="button-container">
            <Button class="primary">Plus d'informations</Button>
        </div>  -->
    </div>
</div>

<style>
    .info-container {
        display: flex;
        align-items: center;
        background-color: #ff662e;
        flex-direction: column;
        justify-content: center;
        border-radius: 15px;
        padding: 10px;
        margin: 10px;
        width: 90%;
        max-width: 95%;
        box-sizing: border-box;
        min-height: 90%;
        position: relative;
        overflow: auto;
    }

    .title-container {
        display: inline-flex;
        justify-content: space-between;
        width: 90%;
        height: 20%;
    }

    .image-container {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: white;
        border-radius: 50%;
        width: 50px;
        height: 50px;
    }

    .content-container {
        display: flex;
        align-items: start;
        flex-direction: column;
        justify-content: start;
        width: 90%;
        height: 80%;
        position: relative;
        overflow: hidden;
    }

    p {
        font-family: "Roboto", sans-serif;
        font-size: 16px;
        margin: 0;
    }

    ul {
        list-style-type: circle;
        margin: 0;
    }

    li {
        font-family: "Roboto", sans-serif;
        font-size: 14px;
    }

    h1 {
        font-family: "Roboto", sans-serif;
        font-size: 24px;
    }

    .triangle-image {
        width: 80%;
        height: 80%;
        position: relative;
    }
</style>
