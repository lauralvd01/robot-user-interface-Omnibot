<script>
    import picto_energie from '$lib/images/picto_energie.svg'
    
</script>

<div class="production-category category">
    <div class="image-container">
        <img class="picto" alt="picto production d'énergie" src={picto_energie}>
    </div>
    <ul>
        <li>Chargeur USB-C</li>
        <li>Pile à hydrogène</li>
        <li>Panneau Photovoltaïque</li>
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

    .production-category{
        background-color: #A04040;
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