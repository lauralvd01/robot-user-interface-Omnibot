<script>
    import { onMount } from "svelte";
    import { writable } from "svelte/store";

    const connected_modules = writable([])

    async function fetchConnectedModules() {
        try {
            console.log("Fetching connected modules ...");
            const response = await fetch("http://localhost:8001/fetch_modules");
            const data = await response.json();
            connected_modules.set(data.data);
        } catch (error) {
            console.error("Error:", error);
        }
    }

    let modules_by_categories = {"Stockage d'énergie": {}, "Mobilité": {}, "Processeur": {}, "Réseau": {}, "Production d'énergie": {}, "Capteur": {}}
    connected_modules.subscribe((connected_modules_value) => {
        // Group modules by functionality
        let modules_group_by_categories = Object.groupBy(connected_modules_value, ({funcionality}) => funcionality);

        Object.entries(modules_group_by_categories).forEach(element => {
            let [functionality, modules] = element;
            // For each functionality, count and store occurences of each module name : { name_module1: count_module1, name_module2: count_module2, ... }
            modules_by_categories[functionality] = modules.map(({name}) => name).reduce(((acc, val) => { acc[val] = ( acc[val] || 0) + 1; return acc}), {});
        });
    })

    onMount(async () => {
        await fetchConnectedModules();
    });

    import Storage from "../module_blocs/Storage.svelte";
    import Mobility from "../module_blocs/Mobility.svelte";
    import Processor from "../module_blocs/Processor.svelte";
    import Network from "../module_blocs/Network.svelte";
    import Production from "../module_blocs/Production.svelte";
    import Sensor from "../module_blocs/Sensor.svelte";
</script>

<div class="blocs">
    <h1 class="titles">EQUIPEMENTS ROBOT</h1>
    <div class="scrolable">
        <div>Module test</div>
        {#each Object.entries(modules_by_categories) as [funcionality, modules]}
            {#if funcionality == "Stockage d'énergie"}
                <Storage modules={modules}/>
            {/if}
            {#if funcionality == "Mobilité"}
                <Mobility modules={modules}/>
            {/if}
            {#if funcionality == "Processeur"}
                <Processor modules={modules}/>
            {/if}
            {#if funcionality == "Réseau"}
                <Network modules={modules}/>
            {/if}
            {#if funcionality == "Production d'énergie"}
                <Production modules={modules}/>
            {/if}
            {#if funcionality == "Capteur"}
                <Sensor modules={modules}/>
            {/if}
        {/each}
    </div>
</div>

<style>
    .scrolable {
        width: 95%;
        height: 95%;
        overflow-y: auto;
        padding: 5px;
        margin: auto;
    }

    .titles {
        grid-column: 1 / span 3;
        font-weight: bold;
        width: 100%;
        font-size: 24px;
        color: black;
        font-family: "Roboto", sans-serif;
    }
</style>
