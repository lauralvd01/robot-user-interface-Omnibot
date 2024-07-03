<script>
    import Direction from './Direction.svelte'
    import OperatingMode from "./OperatingMode.svelte";
    import { onMount } from 'svelte';
      
    let isActiveKeyA = false;
    let isActiveKeyZ = false;
    let isActiveKeyE = false;
    let isActiveKeyQ = false;
    let isActiveKeyS = false;
    let isActiveKeyD = false;
    let batteryLevel = 0;

    onMount(() => {
        window.addEventListener('keydown', handleKeyDown);
        window.addEventListener('keyup', handleKeyUp);
        
        fetchBatteryLevel();

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
            window.removeEventListener('keyup', handleKeyUp);
        };
    });

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
       
    }


    async function fetchBatteryLevel(){
        try{
            const response = await fetch('http://localhost:8000/battery');
            const data = await response.json();
            if(response.ok){
                batteryLevel = data.battery_level;
            } else {
                console.error('Error:',data.error);
            }
        }catch (error){
            console.error('Error:',error);
        }
    }
</script>


<div class="robot_infos">
    <Direction/>
    <div class="control-container">
        <h1 class="titles">COMMANDES</h1>
        <div class="key {isActiveKeyA ? 'active' : ''}">
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
    <OperatingMode/>
    <div class="battery-lvl-container">
        <h1 class="titles">BATTERIE</h1>
        <div class="battery">
            <div class="battery-bar">
                <div class="battery-level" style="width: {batteryLevel}%"></div> 
                <div class="battery-text">{batteryLevel}%</div>
            </div>
            <div class="battery-shape"></div>
        </div>
    </div>
</div>

<style>
    .robot_infos{
        display: flex;
    }

    .control-container {
        width: 300px;
        height: 215px;
        background-color: #A8A8A8;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: auto auto auto;
        border-radius: 10px;
        text-align: center;
        margin:15px 15px 15px 15px;
    }

    .titles {
        grid-column: 1 / span 3;
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
        padding-bottom: 5px;
        font-family: 'Roboto', sans-serif;
    }

    .key .first-line{
        font-weight: bold;
        font-size: 24px;
    }

    .key .second-line{
        font-size: 16px;

    }

    .key.active {
        background-color: #239E99;
        color: white;
    }

    .battery-lvl-container{
        display:flex;
        flex-direction: column;
        margin:15px;
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
        background-color: #040B8C;
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