<script>
    import Direction from './Direction.svelte'
    import OperatingMode from "./OperatingMode.svelte";
    import Range from "./Range.svelte";
    import Controller from "./Controller.svelte";
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';

    import { backend_host, backend_port } from '../config.js';

    const step = 0.1;
    const speed_data = writable({linear_speed: 1/step, angular_speed: 2/step});
    
    // Send a request to the backend to change robot speed settigs
    function sendSpeedData() {
        fetch(`http://${backend_host}:${backend_port}/set_speed`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                linear_speed: Math.round($speed_data.linear_speed*step*10)/10,
                angular_speed: Math.round($speed_data.angular_speed*step*10)/10,
            }),
        });
    }
    
    // Send a request to the backend to move the robot
    function sendMoveData(moves) {
        fetch(`http://${backend_host}:${backend_port}/post_move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(moves)
        });
    }
    
    //Creation de booléens pour savoir si une touche du clavier est pressée
    let isActiveKeyA = false;
    let isActiveKeyZ = false;
    let isActiveKeyE = false;
    let isActiveKeyQ = false;
    let isActiveKeyS = false;
    let isActiveKeyD = false;

    //Fonctions permettant de savoir si la touche est pressée ou non
    function handleKeyDown(event) {
        if (event.key.toLowerCase() === 'z') {
            isActiveKeyZ = true;
        }
        if (event.key.toLowerCase() === 'a'){
            isActiveKeyA = true;         
        }
        if (event.key.toLowerCase() === 'e'){
            isActiveKeyE = true;
        }
        if (event.key.toLowerCase() === 's'){
            isActiveKeyS = true;
        }
        if (event.key.toLowerCase() === 'q'){
            isActiveKeyQ = true;
        }
        if (event.key.toLowerCase() === 'd'){
            isActiveKeyD = true;
        }
        if (isActiveKeyZ || isActiveKeyS || isActiveKeyQ || isActiveKeyD || isActiveKeyA || isActiveKeyE) {
            sendMoveData({
                x_linear_vel: isActiveKeyZ ? 1 : isActiveKeyS ? -1 : 0,
                y_linear_vel: isActiveKeyQ ? 1 : isActiveKeyD ? -1 : 0,
                angular_vel: isActiveKeyA ? 1 : isActiveKeyE ? -1 : 0,
            });
        }
    }

    function handleKeyUp(event) {
        if (event.key.toLowerCase() === 'z') {
            isActiveKeyZ = false;   
        }
        if (event.key.toLowerCase() === 'a') {
            isActiveKeyA = false;
        }
        if (event.key.toLowerCase() === 'e') {
            isActiveKeyE = false;
        }
        if (event.key.toLowerCase() === 'q') {
            isActiveKeyQ = false;
        }
        if (event.key.toLowerCase() === 's') {
            isActiveKeyS = false;
        }
        if (event.key.toLowerCase() === 'd') {
            isActiveKeyD = false;
        }
        if ( !(isActiveKeyZ || isActiveKeyS || isActiveKeyQ || isActiveKeyD || isActiveKeyA || isActiveKeyE) ) {
            sendMoveData({
                x_linear_vel: isActiveKeyZ ? 1 : isActiveKeyS ? -1 : 0,
                y_linear_vel: isActiveKeyQ ? 1 : isActiveKeyD ? -1 : 0,
                angular_vel: isActiveKeyA ? 1 : isActiveKeyE ? -1 : 0,
            });
        }
    }
    
    onMount(async () => {
        window.addEventListener('keydown', handleKeyDown);
        window.addEventListener('keyup', handleKeyUp);

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
            window.removeEventListener('keyup', handleKeyUp);
        };
    });


    export let batteries_data;

    const batteries = writable({});

    function updateBatteryLevel(batteries_data) {
        $batteries = {};
        if (batteries_data.length > 0) { 
            for (const battery_data of batteries_data) {
                $batteries[battery_data.slot_id] = {
                    name: battery_data.name.toUpperCase(),
                    state_of_charge: Math.round(battery_data.state_of_charge*100)
                };
            };
            $batteries = $batteries;
        }
    }

    $: batteries_data && updateBatteryLevel(batteries_data);

    
    const is_gamepad_connected = writable(false);
    $: is_gamepad_connected && console.log("Gamepad connected ?", $is_gamepad_connected);
</script>

<svelte:window 
  on:gamepadconnected={e => {is_gamepad_connected.set(true)}}
  on:gamepaddisconnected={e => {is_gamepad_connected.set(false);}}
/>

<div class="content">
        <div class="command-row">
            <div class="command-row-element" style="width: 25%">
                <Direction/> <!--Import du composant Direction-->
            </div>

            <div class="command-row-element" style="width: 25%">
                <div class="control-container">
                    <p class="titles">COMMANDES</p>
                    {#if (!$is_gamepad_connected)}
                        <div class="keyborad">
                        <div class="key {isActiveKeyA ? 'active' : ''}"> <!--vérification de si la touche est pressée -->
                            <span class="first-line">A</span><br/>
                            <span class="second-line">Rotation G</span>
                        </div>
                        <div class="key {isActiveKeyZ ? 'active' : ''}">
                            <span class="first-line">Z</span><br/>
                            <span class="second-line">Avancer</span>
                        </div>
                        <div class="key {isActiveKeyE ? 'active' : ''}">
                            <span class="first-line">E</span><br/>
                            <span class="second-line">Rotation D</span>
                        </div>
                        <div class="key {isActiveKeyQ ? 'active' : ''}">
                            <span class="first-line">Q</span><br/>
                            <span class="second-line">Gauche</span>
                        </div>
                        <div class="key {isActiveKeyS ? 'active' : ''}">
                            <span class="first-line">S</span><br/>
                            <span class="second-line">Reculer</span>
                        </div>
                        <div class="key {isActiveKeyD ? 'active' : ''}">
                            <span class="first-line">D</span><br/>
                            <span class="second-line">Droite</span>
                        </div>
                        </div>
                    {/if}
                    <div class="pad_controller" style='--displayGamepad:{$is_gamepad_connected ? "flex" : "none"};'>
                        <Controller move={sendMoveData}/>
                    </div>
                </div>
            </div>

            <div class="command-row-element" style="width: 30%">
                <OperatingMode/> <!--Import du composant OperatingMode-->
                <div style="width: 60%; margin: 10px 0px;">
                    <label for="linear-range" class="speed-label">Linear speed</label>
                    <Range on:change={(e) => {$speed_data.linear_speed = e.detail.value; sendSpeedData();}} 
                        min={0} max={5} step={step} bind:value={$speed_data.linear_speed} id="speed-slider"/>
                    <label for="angular-range" class="speed-label">Angular speed</label>
                    <Range on:change={(e) => {$speed_data.angular_speed = e.detail.value; sendSpeedData();}} 
                        min={0} max={5} step={step} bind:value={$speed_data.angular_speed} id="angular-slider"/>
                </div>
            </div>

            <div class="command-row-element" style="width: 20%">
                <div class="battery-lvl-container">
                    {#each Object.entries($batteries) as [battery_slot, battery]}
                        <h1 class="titles">{battery["name"]}</h1>
                        <div class="battery">
                            <div class="battery-bar">
                                <!--Actualisation de la barre de batterie selon le niveau de batterie restant dans l'Omnibot-->
                                <div class="battery-level" style="width: {battery["state_of_charge"]}%"></div> 
                                <div class="battery-text">{battery["state_of_charge"]}%</div>
                            </div>
                            <div class="battery-shape"></div>
                        </div>
                    {/each}
                </div>
            </div>
        </div>
</div>

<style>
    .content {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        overflow: hidden;
        width: 100%;
    }

    .command-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        flex-grow: 1;
        overflow: hidden;
    }

    .command-row-element {
        flex-shrink: 0;
        overflow-y: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .speed-label {
        color:#FF662E;
        font-family: 'Roboto',sans-serif;
        font-weight: 600;
    }

    .control-container {
        width: 100%;
        height: 90%;
        background-color: #A8A8A8;
        border-radius: 5%;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .keyborad {
        width: 90%;
        height: 90%;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: auto auto auto;
        margin-bottom: 5%;
    }

    .pad_controller {
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        display: var(--displayGamepad);
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .titles {
        font-weight: bold;
        font-size: 24px;
        color:black;
        font-family: 'Roboto',sans-serif;
    }

    span{
        color:black;
    }

    .key {
        background-color: #FF662E;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin:6px;
        border-radius: 6px;
        white-space: pre-line;
        height: auto;
        line-height: 1;
        font-family: 'Roboto', sans-serif;
    }

    .key .first-line{
        font-weight: bold;
        font-size: 24px;
    }

    .key .second-line{
        font-size: 16px;
    }

    /*Permet de changer le style lorsque qu'une touche du clavier est pressée */
    .key.active {
        background-color: #239E99;
        color: white;
    }

    .battery-lvl-container{
        display: flex;
        flex-direction: column;
    }

    .battery {
        position: relative;
        display: flex;
        align-items: center;
    }

    .battery-bar {
        position: relative;
        width: 135px;
        height: 50px;
        background-color: #494949;
        border:black solid 3px;
        border-radius: 10px;
        overflow: hidden;
    }

    .battery-level {
        height: 100%;
        background-color: #FF662E;
        width: 0;
        transition: width 0.5s;
    }

    .battery-text {
        position: absolute;
        top: 50%;
        left: 20px; 
        transform: translateY(-50%); 
        font-family: 'Roboto', sans-serif;
        color: white;
        font-weight: bold;
        padding-bottom: 3px;
        display: flex;
        justify-content: left;
    }

    .battery-shape {
        width: 10px;
        height: 30px;
        background-color: black;
        border-radius: 4px;
        margin-left: 3px;
    }
</style>