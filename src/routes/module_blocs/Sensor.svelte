<script>
    import picto_sensor from '$lib/images/picto_capteur.svg'
    
</script>

<div class="sensor-category category">
    <div class="image-container">
        <img class="picto" alt="picto sensor d'énergie" src={picto_sensor}>
    </div>
    <ul>
        <li>GPS</li>
        <li>Camera</li>
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

    .sensor-category{
        background-color: #239E99;
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