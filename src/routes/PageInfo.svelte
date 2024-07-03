<script>
    import Button from "./Button.svelte";
    import {selectedTriangle } from './store';
    import {writable} from 'svelte/store';
    import {onMount} from "svelte";

    const content = {
        1: {
            title: "Moteur",
            text: "bloc moteur",

        },
        2: {
            title: "jetson",
            text: "voici le bloc de la jetson nano"
        }
    };

    let currentContent = { title: "", text: "", image: "" };

$: selectedTriangle.subscribe(value => {
  if (value !== null && content[value]) {
    currentContent = content[value];
  } else {
    currentContent = { title: "", text: "", image: "" };
  }
});
</script>

<div class = "info-bloc">
    <div class="info-container">
        {#if currentContent.text}
            <h1>{currentContent.title}</h1>
            <p>{currentContent.text}</p>
        {:else}
            <p>Cliquez sur un bloc afin d'avoir les informations lié a celui-ci</p>
    {/if}
        <div class="button-container">
            <Button class="primary">Plus d'informations</Button>
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