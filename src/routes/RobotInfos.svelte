<script>
    import Button from './Button.svelte';
    import Direction from './Direction.svelte'
    import OperatingMode from "./OperatingMode.svelte";
    import { onMount } from 'svelte';
    
    //Creation de booléens pour savoir si une touche du clavier est pressée
    let isActiveKeyA = false;
    let isActiveKeyZ = false;
    let isActiveKeyE = false;
    let isActiveKeyQ = false;
    let isActiveKeyS = false;
    let isActiveKeyD = false;
    let batteryLevel = 0;
    let robotState = {"status": "stopped", "speed": 0};
    let UpdatedBatteryLevel = batteryLevel;
    let UpdatedRobotState = robotState;
    // $: displayBatteryLevel = batteryLevel;
    // $: displayRobotState = robotState;

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

    //Fonction permettant de voir le niveau de batterie sur l'interface. NON TESTEE
    async function fetchBatteryLevel(){
        try{
            console.log('Fetching battery level ...')
            const response = await fetch('http://localhost:8001/battery');
            const data = await response.json();
            batteryLevel = Math.round(data.battery_level);
        }catch (error){
            console.error('Error:',error);
        }
    }

    async function fetchRobotState() {
        try {
            const response = await fetch('http://localhost:8001/motor_state');
            if (response.ok) {
                const data = await response.json();
                robotState = data;
            } else {
                console.error('Failed to fetch robot state:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching robot state:', error);
        }
    }
    
    onMount(async () => {
        window.addEventListener('keydown', handleKeyDown);
        window.addEventListener('keyup', handleKeyUp);
        
        //Permet d'actualiser le niveau de batterie et le statut du robot sur l'interface
        // await fetchBatteryLevel();
        // await fetchRobotState();

        // Refrexh battery level and robot status every 5 seconds
        // const interval = setInterval(() => {UpdatedBatteryLevel = batteryLevel; UpdatedRobotState = robotState}, 5000);
        
        // Refrexh battery level and robot status every 5 seconds
        // const interval1 = setInterval(fetchRobotState, 5000);
        // const interval2 = setInterval(fetchBatteryLevel, 5000);

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
            window.removeEventListener('keyup', handleKeyUp);
            // clearInterval(interval);
            // clearInterval(interval1);
            // clearInterval(interval2);
        };
    });

    console.log(robotState);
    console.log(batteryLevel);
    console.log('RobotInfos mounted');

    function increment() {
        batteryLevel += 2;
        robotState.speed += 2;
    }
    // function update() {
    //     displayBatteryLevel = batteryLevel;
    //     displayRobotState = robotState;
    // }

    let state = UpdatedRobotState.status;
    let speed = UpdatedRobotState.speed;
    let count = 0;
    $: ( () => {
        count += 1
        console.log(`Count updated ${count} times : ${batteryLevel}`);
        state = `State updated ${count} times : ${UpdatedRobotState.status}`;
        speed = `Speed updated ${count} times : ${UpdatedRobotState.speed}`;
        console.log(`Battery level updated : ${UpdatedBatteryLevel}`);
        console.log(`Robot state updated : status: ${UpdatedRobotState.status}, speed: ${UpdatedRobotState.speed}`);
    }) ()
</script>


<div class="content">
        <div class="command-row">
            <div class="command-row-element" style="width: 25%">
                <Direction/> <!--Import du composant Direction-->
            </div>

            <div class="command-row-element" style="width: 25%">
                <div class="control-container">
                    <h1 class="titles">COMMANDES</h1>
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
            </div>

            <div class="command-row-element" style="width: 30%">
                <OperatingMode/> <!--Import du composant OperatingMode-->
            </div>

            <div class="command-row-element" style="width: 20%">
                <div class="battery-lvl-container">
                    <h1 class="titles">BATTERIE</h1>
                    <div class="battery">
                        <div class="battery-bar">
                            <!--Actualisation de la barre de batterie selon le niveau de batterie restant dans l'Omnibot-->
                            <div class="battery-level" style="width: {UpdatedBatteryLevel}%"></div> 
                            <div class="battery-text">{UpdatedBatteryLevel}%</div>
                        </div>
                        <div class="battery-shape"></div>
                    </div>
                    <p>{state}</p>
                    <p>{speed}</p>
                    <Button class="primary" on:click={increment}>Incrémenter</Button>
                    <!-- <Button class="primary" on:click={update}>Actualiser</Button> -->
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
    }

    .control-container {
        width: 300px;
        height: 30%;
        background-color: #A8A8A8;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: auto auto auto;
        border-radius: 10px;
        text-align: center;
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