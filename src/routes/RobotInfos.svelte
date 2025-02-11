<script>
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import Direction from "./Direction.svelte";
    import OperatingMode from "./OperatingMode.svelte";
    import Range from "./Range.svelte";
    import Controller from "./Controller.svelte";

    import { speed_data, step, d_speed } from "./data_store";
    import { sendMoveData, sendSpeedData } from "./data_store";

    let count_d_speed = { du: 0, dd: 0, dl: 0, dr: 0 };
    
    export function check_d_speed(d_speed) {
        for (const [key, value] of Object.entries(d_speed)) {
            if (value && count_d_speed[key] == 0) {
                count_d_speed[key] += 1;
                if (key === "du") {
                    $speed_data.linear_speed += 1;
                } else if (key === "dd") {
                    $speed_data.linear_speed -= 1;
                } else if (key === "dl") {
                    $speed_data.angular_speed -= 1;
                } else if (key === "dr") {
                    $speed_data.angular_speed += 1;
                }
                sendSpeedData($speed_data);
                count_d_speed[key] = 0;
                d_speed[key] = false;
            }
        }
    }

    $: d_speed && check_d_speed($d_speed);


        //Booleans representing the state of the a, z, e, q, s and d keys of the keyboard
        let isActiveKeyA = false, isActiveKeyZ = false, isActiveKeyE = false, isActiveKeyQ = false, isActiveKeyS = false, isActiveKeyD = false;

        //Handle keydown event to send move data to the backend if a, z, e, q, s or d keys are pressed. Press r to stop any movement
        function handleKeyDown(event) {
            switch (event.key.toLowerCase()) {
                case "z":
                    isActiveKeyZ = true;
                    break;

                case "a":
                    isActiveKeyA = true;
                    break;

                case "e":
                    isActiveKeyE = true;
                    break;
                
                case "q":
                    isActiveKeyQ = true;
                    break;

                case "s":
                    isActiveKeyS = true;
                    break;

                case "d":
                    isActiveKeyD = true;
                    break;
                    
                case "r":
                    isActiveKeyA = false; isActiveKeyD = false; isActiveKeyE = false; isActiveKeyQ = false; isActiveKeyS = false; isActiveKeyZ = false;
                    break;
            
                default:
                    isActiveKeyA = false; isActiveKeyD = false; isActiveKeyE = false; isActiveKeyQ = false; isActiveKeyS = false; isActiveKeyZ = false;
                    break;
            }
            if ( ["z","a","e","q","s","d","r"].includes(event.key.toLowerCase()) ) {
                sendMoveData({
                    x_linear_vel: isActiveKeyZ ? 1 : isActiveKeyS ? -1 : 0,
                    y_linear_vel: isActiveKeyQ ? 1 : isActiveKeyD ? -1 : 0,
                    angular_vel: isActiveKeyA ? 1 : isActiveKeyE ? -1 : 0,
                });
            }
        }
        // Handle keyup event to send move data to the backend if a, z, e, q, s or d keys are released
        function handleKeyUp(event) {
            switch (event.key.toLowerCase()) {
                case "z":
                    isActiveKeyZ = false;
                    break;

                case "a":
                    isActiveKeyA = false;
                    break;

                case "e":
                    isActiveKeyE = false;
                    break;

                case "q":
                    isActiveKeyQ = false;
                    break;

                case "s":
                    isActiveKeyS = false;
                    break;

                case "d":
                    isActiveKeyD = false;
                    break;

                default:
                    isActiveKeyA = false; isActiveKeyD = false; isActiveKeyE = false; isActiveKeyQ = false; isActiveKeyS = false; isActiveKeyZ = false;
                    break;
            }
            if ( ["z","a","e","q","s","d"].includes(event.key.toLowerCase()) ) {
                sendMoveData({
                    x_linear_vel: isActiveKeyZ ? 1 : isActiveKeyS ? -1 : 0,
                    y_linear_vel: isActiveKeyQ ? 1 : isActiveKeyD ? -1 : 0,
                    angular_vel: isActiveKeyA ? 1 : isActiveKeyE ? -1 : 0,
                });
            }
        }

        // Add event listeners to handle keyboard commands, remove it when the page component is destroyed
        onMount(async () => {
            window.addEventListener("keydown", handleKeyDown);
            window.addEventListener("keyup", handleKeyUp);

            return () => {
                window.removeEventListener("keydown", handleKeyDown);
                window.removeEventListener("keyup", handleKeyUp);
            };
        });

    import { is_gamepad_connected, batteries } from "./data_store";
</script>

<svelte:window
    on:gamepadconnected={(e) => {
        is_gamepad_connected.set(true);
    }}
    on:gamepaddisconnected={(e) => {
        is_gamepad_connected.set(false);
    }}
/>

<div class="content">
    <div class="command-row">
        <div class="command-row-element" style="width: 20%">
            <Direction />
        </div>

        <div class="command-row-element" style="width: 25%">
            <div class="control-container">
                <p class="titles">COMMANDES</p>
                {#if !$is_gamepad_connected}
                    <div class="keyboard">
                        <div class="key {isActiveKeyA ? 'active' : ''}">
                            <!--vérification de si la touche est pressée -->
                            <span class="first-line">A</span><br />
                            <span class="second-line">Rotation G</span>
                        </div>
                        <div class="key {isActiveKeyZ ? 'active' : ''}">
                            <span class="first-line">Z</span><br />
                            <span class="second-line">Avancer</span>
                        </div>
                        <div class="key {isActiveKeyE ? 'active' : ''}">
                            <span class="first-line">E</span><br />
                            <span class="second-line">Rotation D</span>
                        </div>
                        <div class="key {isActiveKeyQ ? 'active' : ''}">
                            <span class="first-line">Q</span><br />
                            <span class="second-line">Gauche</span>
                        </div>
                        <div class="key {isActiveKeyS ? 'active' : ''}">
                            <span class="first-line">S</span><br />
                            <span class="second-line">Reculer</span>
                        </div>
                        <div class="key {isActiveKeyD ? 'active' : ''}">
                            <span class="first-line">D</span><br />
                            <span class="second-line">Droite</span>
                        </div>
                    </div>
                {/if}
                <div
                    class="pad_controller"
                    style="--displayGamepad:{$is_gamepad_connected ? 'flex' : 'none'};"
                >
                    <Controller />
                </div>
            </div>
        </div>

        <div class="command-row-element" style="width: 30%">
            <!--Import du composant OperatingMode-->
            <OperatingMode />
            <div style="width: 60%; margin: 10px 0px;">
                <label for="linear-range" class="speed-label">Linear speed : {($speed_data.linear_speed*step).toFixed(1)}</label>
                <Range
                    on:change={(e) => { $speed_data.linear_speed = e.detail.value; sendSpeedData($speed_data); }}
                    min={0} max={5} {step}
                    bind:value={$speed_data.linear_speed}
                    id="speed-slider"
                />
                <label for="angular-range" class="speed-label">Angular speed : {($speed_data.angular_speed*step).toFixed(1)}</label>
                <Range
                    on:change={(e) => { $speed_data.angular_speed = e.detail.value; sendSpeedData($speed_data); }}
                    min={0} max={5} {step}
                    bind:value={$speed_data.angular_speed}
                    id="angular-slider"
                />
            </div>
        </div>

        <div class="command-row-element" style="width: 25%">
            <div class="battery-lvl-container">
                {#each Object.entries($batteries) as [battery_slot, battery]}
                    <h1 class="titles">{battery["name"]}</h1>
                    <div class="battery">
                        <div class="battery-bar">
                            <!--Actualisation de la barre de batterie selon le niveau de batterie restant dans l'Omnibot-->
                            <div
                                class="battery-level"
                                style="width: {battery['state_of_charge']}%"
                            ></div>
                            <div class="battery-text">
                                {battery["state_of_charge"]}%
                            </div>
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
        color: #ff662e;
        font-family: "Roboto", sans-serif;
        font-weight: 600;
    }

    .control-container {
        width: 100%;
        height: 90%;
        background-color: #a8a8a8;
        border-radius: 5%;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .keyboard {
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
        color: black;
        font-family: "Roboto", sans-serif;
    }

    span {
        color: black;
    }

    .key {
        background-color: #ff662e;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 6px;
        border-radius: 6px;
        white-space: pre-line;
        height: auto;
        line-height: 1;
        font-family: "Roboto", sans-serif;
    }

    .key .first-line {
        font-weight: bold;
        font-size: 24px;
    }

    .key .second-line {
        font-size: 16px;
    }

    /*Permet de changer le style lorsque qu'une touche du clavier est pressée */
    .key.active {
        background-color: #239e99;
        color: white;
    }

    .battery-lvl-container {
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
        border: black solid 3px;
        border-radius: 10px;
        overflow: hidden;
    }

    .battery-level {
        height: 100%;
        background-color: #ff662e;
        width: 0;
        transition: width 0.5s;
    }

    .battery-text {
        position: absolute;
        top: 50%;
        left: 20px;
        transform: translateY(-50%);
        font-family: "Roboto", sans-serif;
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
