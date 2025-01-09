<script>
    import picto_stockage from '$lib/images/picto_stockage_energie.svg'
    
</script>

<div class="storage-category category">
    <div class="image-container">
        <img class="picto" alt="picto stockage d'énergie" src={picto_stockage}>
    </div>
    <ul>
        <li>Batterie</li>
        <li>Supercondensateur</li>
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

    .storage-category{
        background-color: #E42618;
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