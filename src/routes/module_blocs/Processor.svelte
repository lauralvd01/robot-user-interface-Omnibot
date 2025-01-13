<script>
    import picto_intelligence from "$lib/images/picto_intelligence.svg";

    export let modules;
</script>

<div class="procesor-category category">
    <div class="image-container">
        <img class="picto" alt="picto procesor" src={picto_intelligence} />
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

    .procesor-category {
        background-color: #4b1338;
        color: white;
    }

    ul {
        font-family: "Roboto", sans-serif;
    }

    .picto {
        height: 40px;
        width: 40px;
    }

    .image-container {
        display: inline-block;
        background-color: white;
        border-radius: 50%;
        margin: 5px;
        padding: 3px;
    }

    ul li::before {
        color: white;
        display: inline-block;
        width: 1em;
        margin-left: -1em;
    }
</style>
