<script>
    import Button from "./Button.svelte";
    import { selectedTriangle, triangleData } from './store'; // Importer le store

    let currentContent = "Cliquez sur un bloc afin d'avoir les informations lié a celui-ci";

    // Déclaration réactive pour mettre à jour le contenu lorsque selectedTriangle change
    $: {
        const id = $selectedTriangle.id;
        currentContent = id !== null ? $triangleData[id] : "Cliquez sur un bloc afin d'avoir les informations lié a celui-ci";
    
        };
    
</script>

<div class="info-bloc">
    <div class="info-container">
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
        width: 100%; 
        box-sizing: border-box;
        min-height: 350px;
        max-height: 400px;
        position: relative; 
        min-width: 450px;
    }

    .button-container { 
        align-self: flex-end;
        margin-top: auto;
        margin-right:20px;
    }

    p {
        font-family: 'Roboto', sans-serif;
        font-size: 16px;
        

    }
</style>
