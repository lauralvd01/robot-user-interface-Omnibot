<script>
    import picto_intelligence from '$lib/images/picto_intelligence.svg'
    
</script>

<div class="network-category category">
    <div class="image-container">
        <img class="picto" alt="picto network" src={picto_intelligence}>
    </div>
    <ul>
        <li>Antenne 5G</li>
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

    .network-category{
        background-color:  #4B1338;
        color:white;
    }

    ul{
        font-family: 'Roboto',sans-serif;
    }

    .picto{
        height: 40px;
        width: 40px;
    }

    .image-container{
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