<script>
    import { writable } from 'svelte/store'; // Importer la fonction writable
    import { selectedTriangle, triangleData, triangleImages, triangleTitle } from './store'; // Importer le store

    let currentContent = "Cliquez sur un bloc afin d'avoir les informations lié a celui-ci";
    let currentImage = null;
    let currentTitle = null;

    // Déclaration réactive pour mettre à jour le contenu lorsque selectedTriangle change
    $: {
        const id = $selectedTriangle.id;
        if (id !== null) {
            const module = $triangleData[id]
            currentContent = module;
            // console.log(module);
            // `Module id : ${module.module_id}, Fonction : ${module.functionality !== null ? module.functionality : "Aucune"}, Caractéristiques : ${module.characteristics.length > 0 ? module.characteristics.join(", ") : "Aucune"}`;
            currentImage = $triangleImages[id];
            currentTitle = $triangleTitle[id];
        }
        else {
            currentContent = "Cliquez sur un bloc afin d'avoir les informations lié a celui-ci";
            currentImage = null;
            currentTitle = "Aucun bloc sélectionné";
        }
        };
    
    
    export let batteries_data;

    const batteries = writable({});

    function updateBatteryData(batteries_data) {
        $batteries = {};
        if (batteries_data.length > 0) {
            for (const battery_data of batteries_data) {
                $batteries[battery_data.slot_id] = {
                    name: battery_data.name.toUpperCase(),
                    state: battery_data.state,
                    state_of_charge: Math.round(
                        battery_data.state_of_charge * 100,
                    ),
                    current: Math.round(
                        battery_data.current * 100,
                    ),
                    temperature: Math.round(
                        battery_data.temperature * 100,
                    ),
                    cell_voltages: battery_data.cell_voltages,
                    power_flow: 0,
                    energy: 0
                };
            }
        }
    }

    $: batteries_data && updateBatteryData(batteries_data);
</script>

<div class="info-bloc">
    <div class="info-container">
        <div class="title-container">
            {#if currentImage}
                <div class="image-container">
                    <img src={currentImage} alt="Triangle" class="triangle-image"/>
                </div>
            {/if}
            <h1>{currentTitle}</h1>
        </div>
        <div class="content-container">
        {#if currentImage}
            <p>Fonction : {currentContent.functionality}</p>
            <p>Caractéristiques : </p>
            {#if currentContent.characteristics.length > 0}
                {#if currentTitle === "Batterie"}
                    <ul>
                        {#each currentContent.characteristics as characteristic}
                            <li>{characteristic} : {$batteries[1][characteristic]}</li>
                        {/each}
                    </ul>
                {:else}
                    <ul>
                        {#each currentContent.characteristics as characteristic}
                            <li>{characteristic} : </li>
                        {/each}
                    </ul>
                {/if}
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
        background-color: #FF662E;
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
        font-family: 'Roboto', sans-serif;
        font-size: 16px;
        margin: 0;
    }

    ul {
        list-style-type: circle;
        margin: 0;
    }

    li {
        font-family: 'Roboto', sans-serif;
        font-size: 14px;
    }

    h1 {
        font-family: 'Roboto', sans-serif;
        font-size: 24px;
    }

    .triangle-image {
        width: 80%;
        height: 80%;
        position: relative;
    }
</style>
