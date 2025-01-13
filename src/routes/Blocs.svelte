<script>
    // import { onMount } from 'svelte';
    import Storage from './module_blocs/Storage.svelte';
    import Mobility from './module_blocs/Mobility.svelte';
    import Processor from './module_blocs/Processor.svelte';
    import Network from './module_blocs/Network.svelte';
    import Production from './module_blocs/Production.svelte';
    import Sensor from './module_blocs/Sensor.svelte';

    let categories = [Storage, Mobility, Processor, Network, Production, Sensor];
</script>

<div class="blocs">
    <h1 class="titles">EQUIPEMENTS ROBOT</h1>
    <div class="scrolable">
        {#each categories as category}
            <svelte:component this={category}/>
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