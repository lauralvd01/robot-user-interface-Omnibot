<script>
    import picto_sensor from "$lib/images/picto_capteur.svg";

    export let modules;
</script>

<div class="sensor-category category">
    <div class="image-container">
        <img class="picto" alt="picto sensor d'énergie" src={picto_sensor} />
    </div>
    <ul>
        {#each Object.entries(modules) as [name, count]}
            <li>{name} x{count}</li>
        {/each}
    </ul>
</div>

<style>
    .category {
        display: flex;
        align-items: center;
        border-radius: 15px;
        padding: 0 10px;
        margin-bottom: 10px;
        width: 100%;
        box-sizing: border-box;
    }

    .sensor-category {
        background-color: #239e99;
        color: white;
    }

    ul {
        font-family: "Roboto", sans-serif;
    }

    .picto{
        height: 80%;
        width: 80%;
        position: relative;
    }

    .image-container{
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: white;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        margin: 5px;
    }


    ul li::before {
        color: white;
        display: inline-block;
        width: 1em;
        margin-left: -1em;
    }
</style>
