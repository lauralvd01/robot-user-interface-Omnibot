<script>
    import Storage from './module_blocs/Storage.svelte';
    import Mobility from './module_blocs/Mobility.svelte';
    import Processor from './module_blocs/Processor.svelte';
    import Network from './module_blocs/Network.svelte';
    import Production from './module_blocs/Production.svelte';
    import Sensor from './module_blocs/Sensor.svelte';

    import { writable } from 'svelte/store';
    import { wheels_count } from './store';

    // Get connected_modules from data store
    import { connected_modules } from './data_store';

    // Create a store to store modules grouped by categories
    const modules_by_categories = writable({"Stockage d'energie": {}, "Mobilite": {}, "Processeur": {}, "Reseau": {}, "Production d'energie": {}, "Capteur": {}});

    // Group modules by categories and set modules_by_categories accordingly
    function group_connected_modules_by_categories(connected_modules) {
        $modules_by_categories = {"Stockage d'energie": {}, "Mobilite": {}, "Processeur": {}, "Reseau": {}, "Production d'energie": {}, "Capteur": {}};

        // Group modules by functionality
        let modules_group_by_categories = Object.groupBy(connected_modules, ({functionality}) => functionality);
        
        Object.entries(modules_group_by_categories).forEach(element => {
            let [functionality, modules] = element;
            // For each functionality, count and store occurences of each module name : { name_module1: count_module1, name_module2: count_module2, ... }
            $modules_by_categories[functionality] = modules.map(({name}) => name).reduce(((acc, val) => { acc[val] = ( acc[val] || 0) + 1; return acc}), {});
            if (functionality == "Mobilite") {
                wheels_count.set($modules_by_categories[functionality]["Roue Omnidirectionnelle"] || 0);
            }
        });
    }

    // Wait for connected_modules to be fetched from parent component and then run group_connected_modules_by_categories
    $: connected_modules && group_connected_modules_by_categories($connected_modules);
</script>

<div class="blocs">
    <h1 class="titles">EQUIPEMENTS ROBOT</h1>
    <div class="scrolable">
        {#each Object.entries($modules_by_categories) as [functionality, modules] (functionality)}
            {#if Object.entries(modules).length > 0}
                {#if functionality == "Stockage d'energie"}
                    <Storage modules={modules}/>
                {:else if functionality == "Mobilite"}
                    <Mobility modules={modules}/>
                {:else if functionality == "Processeur"}
                    <Processor modules={modules}/>
                {:else if functionality == "Reseau"}
                    <Network modules={modules}/>
                {:else if functionality == "Production d'energie"}
                    <Production modules={modules}/>
                {:else if functionality == "Capteur"}
                    <Sensor modules={modules}/>
                {/if}
            {/if}
        {/each}
    </div>   
</div>

<style>
    .scrolable{
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
        color:black;
        font-family: 'Roboto', sans-serif;
    }
</style>