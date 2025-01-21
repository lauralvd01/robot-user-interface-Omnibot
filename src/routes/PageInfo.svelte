<script>
    import { writable } from 'svelte/store'; // Importer la fonction writable
    import { selectedTriangle, triangleData, triangleImages, triangleTitle } from './store'; // Importer le store

    let currentContent = "Cliquez sur un bloc afin d'avoir les informations lié a celui-ci";
    let currentImage = null;
    let currentTitle = null;

    // Déclaration réactive pour mettre à jour le contenu lorsque selectedTriangle change
    $: {
        const id = $selectedTriangle.id;
        currentContent = id !== null ? $triangleData[id] : "Cliquer sur un bloc pour avoir les informations liées à celui-ci";
        currentImage = id !=  null ? $triangleImages[id] : null;
        currentTitle = id != null ? $triangleTitle[id] : " ";
        };
    
    


    export let batteries_data;

    const batteries = writable({});

    function updateBatteryLevel(batteries_data) {
        $batteries = {};
        if (batteries_data.length > 0) {
            for (const battery_data of batteries_data) {
                $batteries[battery_data.slot_id] = {
                    name: battery_data.name.toUpperCase(),
                    state_of_charge: Math.round(
                        battery_data.state_of_charge * 100,
                    ),
                };
            }
            $batteries = $batteries;
        }
    }

    $: batteries_data && updateBatteryLevel(batteries_data);
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
        <p>{currentContent}</p>

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

    p {
        font-family: 'Roboto', sans-serif;
        font-size: 16px;
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
