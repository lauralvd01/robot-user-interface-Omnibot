<script>
    import { onMount } from 'svelte';
    import Storage from './module_blocs/Storage.svelte';
    import Mobility from './module_blocs/Mobility.svelte';
    import Processor from './module_blocs/Processor.svelte';
    import Network from './module_blocs/Network.svelte';
    import Production from './module_blocs/Production.svelte';
    import Sensor from './module_blocs/Sensor.svelte';

    let categories = [Storage, Mobility, Processor, Network, Production, Sensor];
    let connected_modules = [];
    $: display_connected_modules = connected_modules;

    onMount( () => {
        // fetchConnectedModules();
        // return () => {
        //     console.log('cleanup');
        // }
    });

    async function fetchConnectedModules(){
        try{
            const response = await fetch('http://localhost:8001/fetch_modules');
            if(response.ok){
                const data = await response.json();
                connected_modules = data.data;
            } else {
                console.error('Failed to fetch connected modules :', response.statusText);
            }
        }catch (error){
            console.error('Error :',error);
        }
    }

    $: ( () => {
        display_connected_modules = connected_modules
    }) ()
</script>

<div class="blocs">
    <h1 class="titles">EQUIPEMENTS ROBOT</h1>
    <div class="scrolable">
        <div>Module test</div>
        {#each display_connected_modules as module}
            <p>{module}</p>
        {/each}
    </div>    <div class="scrolable">
        {#each categories as category}
            <svelte:component this={category} modules={{}}/>
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