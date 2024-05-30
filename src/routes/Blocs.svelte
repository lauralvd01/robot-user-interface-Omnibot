<script>
    import picto_intelligence from '$lib/images/picto_intelligence.svg'
    import picto_energie from '$lib/images/picto_energie.svg'
    import picto_mobilite from '$lib/images/picto_mobilite.svg'
    import picto_stockage from '$lib/images/picto_stockage_energie.svg'
    import picto_capteur from '$lib/images/picto_capteur.svg'

    let defaultInfo = "Cliquez sur un bloc afin d'avoir les informations liées à celui-ci";

    function handleClick(text) {
        const infoComponent = document.querySelector('info');
        if (infoComponent) {
            infoComponent.updateInfo(text);
        }
    }
</script>
<div class="blocs">
    <h1 class="titles">EQUIPEMENTS ROBOT</h1>
    <div class="intelligence-category category">
        <div class="image-container">
            <img class="picto-intelligence picto" alt="picto intelligence" src={picto_intelligence}>
        </div>
        <ul>
            <li>Unité centrale</li>
            <li>5G</li>
        </ul>
    </div>
    <div class="production-category category">
        <div class="image-container">
            <img class="picto-energie picto" alt="picto production d'énergie" src={picto_energie}>
        </div>
        <ul>
            <li>Pile à hydrogène</li>
            <li>Panneau solaire</li>
            <li>Chargeur usb-c</li>
        </ul>
    </div>
    <div class="storage-category category">
        <div class="image-container">
            <img class="picto-stockage picto" alt="picto stockage d'énergie" src={picto_stockage}>
        </div>
        <ul>
            <li>Batterie</li>
            <li>Supercondensateur</li>
        </ul>
    </div>
    <div class="shift-category category">
        <div class="image-container">
            <img class="picto-deplacement picto" alt="picto déplacement" src={picto_mobilite}>
        </div>
        <ul>
            <li>Roue omnidirectionnelle 1</li>
        </ul>
    </div>
</div>

<style>
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

    .storage-category .production-category .intelligence-category .shift-category{
        display: grid; 
    }

    .storage-category{
        background-color: #ffa682;
    }

    .production-category{
        background-color: #828fff;
    }

    .intelligence-category{
        background-color: #656780; 
    }

    .shift-category{      
        background-color: #99d478;
    }

    .blocs h2 {
        font-size: 18px;
        color: black;
        font-family: 'Roboto', sans-serif;
    }
    ul{
        font-family: 'Roboto',sans-serif;
    }

    .picto{
        height: 60px;
        width: 60px;
    }

    .image-container{
        display: inline-block;
        background-color: white; 
        border-radius: 30px;
        margin:5px; 
        padding: 0px;
       
    }

    ul li::before {
            content: '•';
            color: black;
            display: inline-block; 
            width: 1em;
            margin-left: -1em;
        }
</style>