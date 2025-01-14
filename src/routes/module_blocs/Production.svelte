<script>
    import picto_energie from "$lib/images/picto_energie.svg";

    export let modules;
</script>

<div class="production-category category">
    <div class="image-container">
        <img
            class="picto"
            alt="picto production d'énergie"
            src={picto_energie}
        />
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

    .production-category {
        background-color: #a04040;
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
