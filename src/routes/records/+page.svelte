<script>
    import { onMount } from "svelte";
    import { writable } from "svelte/store";

    import Banner from "../Banner.svelte";
    import Button from "../Button.svelte";
    import Graphic from "../graphics/Graphic.svelte";

    import { fetchData, records } from "../data_store";

    let bannerHeight = 0;
    onMount( () => {
        const banner = document.querySelector(".banner");
        if (banner) bannerHeight = banner.offsetHeight;
        fetchData("records");
    })

const currentRecords = writable([])

function updateCurrentRecords(records){
    currentRecords.set(records);
    console.log(records);
}

$: records && updateCurrentRecords($records);
</script>

<div class="homepage">
    <Banner />
    <div class="body" style="margin-top: {bannerHeight}px;">
        <div class="sidebar">
                <Button class="primary" on:click={() => fetchData("records")}>Actualiser</Button>
                <h2>Données enregistrées</h2>
        </div>
    </div>
</div>

<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .homepage {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .body {
        margin: 2%;
        display: flex;
        width: 96%;
        height: 100%;
        font-family: "Roboto", sans-serif;
    }

    .sidebar {
        width: 30%;
        padding: 20px;
        background-color: #ffd7c9;
        border-radius: 10px;
        margin-right: 2%;
    }

    .sidebar h2 {
        margin-bottom: 20px;
        font-weight: bold;
    }

    .select-group, .input-group {
        width: 100%;
        margin-bottom: 15px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .select-group label, .input-group label {
        font-weight: bold;
        margin-bottom: 5px;
    }

    select, input {
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    .module-entry {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #fff;
        padding: 8px;
        margin-bottom: 5px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }

    .module-entry .slot-id {
        font-weight: bold;
        color: #ff662e;
    }

    .module-entry .module-name {
        flex-grow: 1;
        margin-left: 10px;
    }

    .content {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        overflow: auto;
        height: 100%;
        width: 60%;
    }

    .toolbar {
        display: flex;
        flex-direction: column;
        gap: 1%;
        margin-top: 2%;
    }

    .toolbar-row {
        display: flex;
        justify-content: center;
        gap: 2%;
    }

    .tool-btn {
        display: flex;
        align-items: center;
        background-color: #ff662e;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 15px;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.2s ease-in-out;
        min-width: 120px;
    }

    .tool-btn:hover {
        background-color: #e65528;
    }

    .tool-btn:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }

    .icon {
        font-size: 1.2em;
        margin-right: 8px;
    }

    .command-row {
        margin-top: 2%;
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

    .control-container {
        width: 100%;
        padding: 2%;
        background-color: #a8a8a8;
        border-radius: 5%;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .keyboard {
        width: 95%;
        height: 95%;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: auto auto auto;
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