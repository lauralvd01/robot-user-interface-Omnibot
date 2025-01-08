<script>
    import Button from "./Button.svelte";
    import { selectedTriangle, triangleData, triangleImages, triangleTitle } from './store'; // Importer le store
    import { get } from 'svelte/store';

    let currentContent = "Cliquez sur un bloc afin d'avoir les informations lié a celui-ci";
    let currentImage = null;
    let currentTitle = null;

    // Déclaration réactive pour mettre à jour le contenu lorsque selectedTriangle change
    $: {
        const id = $selectedTriangle.id;
        currentContent = id !== null ? $triangleData[id] : "Cliquer sur un bloc pour avoir les informations liées à celui-ci";
        currentImage = id !=  null ? $triangleImages[id] : null;
        currentTitle = id != null ? $triangleTitle[id] : " ";
        };
    
</script>

<div class="info-bloc">
    <div class="info-container">
        <h1>{currentTitle}</h1>
        {#if currentImage}
            <img src={currentImage} alt="Triangle" class="triangle-image"/>
        {/if}
        <p>{currentContent}</p>

        <div class="button-container">
            <Button class="primary">Plus d'informations</Button> <!-- Insertion d'un bouton du style "primary" -->
        </div> 
    </div> 
</div>

<style>
    .info-container {
        display: flex;
        align-items: center;
        background-color: #FF662E;
        flex-direction: column;
        justify-content: center;
        border-radius: 15px;
        padding: 10px;
        margin: 10px; 
        width: 90%; 
        max-width: 95%;
        box-sizing: border-box;
        min-height: 90%;
        position: relative;
        overflow: auto;
    }

    .button-container { 
        align-self: flex-start;
        margin-top: auto;
        margin-left:20px;
    }

    p {
        font-family: 'Roboto', sans-serif;
        font-size: 16px;
    }

    h1 {
        font-family: 'Roboto', sans-serif;
        font-size: 24px;
    }

    .triangle-image {
        max-width: 100px; /* Limiter la taille de l'image */
        max-height: 100px; 
        height: auto;
        margin-top: 10px;
    }
</style>
