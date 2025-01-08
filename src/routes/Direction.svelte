<script>
    import { onMount } from "svelte";
    import arrow from '$lib/images/icone-fleche-droite-noir.png';

    let rotation = 0;
    let arrowElement;
    let keysPressed = {};
    let isAnyKeyPressed = false;

    //fonctions permettant de voir si une touche du clavier est pressée ou non
    function handleKeydown(event) {
        keysPressed[event.key] = true;
        updateRotation();
    }

    function handleKeyup(event) {
        keysPressed[event.key] = false;
        updateRotation();
    }

    //Fonction permettant de mettre à jour l'orientation de la flèche selon les touches pressées
    function updateRotation() {
        if (keysPressed['d'] && keysPressed['z']) {
            rotation = 315; 
        } else if (keysPressed['q'] && keysPressed['z']) {
            rotation = 225; 
        } else if (keysPressed['q'] && keysPressed['s']) {
            rotation = 135; 
        } else if (keysPressed['d'] && keysPressed['s']) {
            rotation = 45; 
        } else if (keysPressed['d']) {
            rotation = 0; 
        } else if (keysPressed['q']) {
            rotation = 180; 
        } else if (keysPressed['z']) {
            rotation = -90; 
        } else if (keysPressed['s']) {
            rotation = 90; 
        }
        if (arrowElement){
            arrowElement.style.transform = `rotate(${rotation}deg)`;
        }
       
        updateDisplay();
    }

    function updateDisplay() {
        isAnyKeyPressed = keysPressed['z'] || keysPressed['q'] || keysPressed['s'] || keysPressed['d'];
    }

    onMount(() => {
        window.addEventListener('keydown', handleKeydown);
        window.addEventListener('keyup', handleKeyup);
        return () => {
            window.removeEventListener('keydown', handleKeydown);
            window.removeEventListener('keyup', handleKeyup);
        };
    });
</script>

<div class="deplacements">
    <div class="direction">
        <h1 class="titles">DIRECTION</h1>
        <div class="center">
            {#if isAnyKeyPressed} <!--Permet de voir si une touche a été pressée-->
            <img bind:this={arrowElement} class="arrow" alt="fleche directionnelle" src={arrow} style="transform: rotate(0deg);"/> <!--Fait tourner l'image en fonction de la touche-->
            {:else}
                <div class="point"></div> <!--Affiche un point si aucune touche n'est pressée-->
        {/if}
        </div>
    </div>
    
    <div class="vitesse">
        <p>x m/s</p>   
    </div>
</div>


<style>
    .deplacements{
        display:flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .direction{
        width: 300px;
        height: 150px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .center{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 150px;
    }

    .arrow{
        height:100px;
        width: 100px;
        transition: transform 0.2s;
    }

    .titles {
        grid-column: 1 / span 3;
        font-weight: bold;
        font-size: 24px;
        color:black;
        font-family: 'Roboto', sans-serif;
    }

    .vitesse{
        border: 3px solid black; 
        padding: 5px; 
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 8px;
        max-width: 80px; 
        max-height: 20px;
        margin-left: 20px;
    }

    .vitesse p{
        margin:0;
        color:#FF662E;
        font-family: 'Roboto',sans-serif;
        font-weight: 600;
        width: 50px;
        padding:10px;
    }

    .point{
        width:20px;
        height:20px;
        background-color: black;
        border-radius: 50%;
    }

</style>