<script>
    import picto_intelligence from '$lib/images/picto_intelligence.svg'
    import picto_energie from '$lib/images/picto_energie.svg'
    import picto_mobilite from '$lib/images/picto_mobilite.svg'
    import picto_stockage from '$lib/images/picto_stockage_energie.svg'
    import picto_capteur from '$lib/images/picto_capteur.svg'

</script>

<div class="blocs">
    <h1 class="titles">EQUIPEMENTS ROBOT</h1>
    <div class="scrolable">
        <div class="intelligence-category category">
            <div class="image-container">
                <img class="picto" alt="picto intelligence" src={picto_intelligence}>
            </div>
            <ul>
                <li>Unité centrale</li>
                <li>5G</li>
            </ul>
        </div>
        <div class="production-category category">
            <div class="image-container">
                <img class="picto" alt="picto production d'énergie" src={picto_energie}>
            </div>
            <ul>
                <li>Pile à hydrogène</li>
                <li>Panneau solaire</li>
            
            </ul>
        </div>
        <div class="storage-category category">
            <div class="image-container">
                <img class="picto" alt="picto stockage d'énergie" src={picto_stockage}>
            </div>
            <ul>
                <li>Batterie</li>
                <li>Supercondensateur</li>
            </ul>
        </div>
        <div class="shift-category category">
            <div class="image-container">
                <img class="picto" alt="picto déplacement" src={picto_mobilite}>
            </div>
            <ul>
                <li>Roue omnidirectionnelle 1</li>
            </ul>
        </div>
        <div class="sensor-category category">
            <div class="image-container">
                <img class="picto" alt="picto capteur" src={picto_capteur}>
            </div>
            <ul>
                <li>Camera</li>
            </ul>
        </div>
    </div>   
</div>

<style>
    .scrolable{
        width: 350px; 
        height: 250px; 
        overflow-y: auto; 
        padding: 10px; 
        margin: auto;
        background-color: #f9f9f9; 
    }

    .titles {
        grid-column: 1 / span 3;
        font-weight: bold;
        font-size: 24px;
        color:black;
        font-family: 'Roboto', sans-serif;
    }

    .category {
    display: flex;
    align-items: center;
    border-radius: 15px;
    padding-right: 10px;
    margin-bottom: 10px; 
    width: 100%; 
    box-sizing: border-box;
    }

    .storage-category .production-category .intelligence-category .shift-category .sensor-category{
        display: grid; 
    }

    .storage-category{
        background-color: #E42618;
        color:white;
    }

    .production-category{
        background-color: #A04040;
        color:white;
    }

    .intelligence-category{
        background-color:  #4B1338;
        color:white;
    }

    .shift-category{      
        background-color: #656780;
        color:white;
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
        margin:5px; 
        padding: 3px;
       
    }

    ul li::before {
            color: white;
            display: inline-block; 
            width: 1em;
            margin-left: -1em;
        }
</style>