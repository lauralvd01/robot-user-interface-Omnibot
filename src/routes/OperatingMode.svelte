<script>
    import { wheels_count } from "./store";

    const possible_options = ["Pas de roues", "Une roue ?", "Roue normales", "Tri-roues"];
    let actual_options = [];

    function updateOptions(wheels_count) {
        actual_options = [];
        actual_options.push(possible_options[wheels_count]);
    }

    $: updateOptions($wheels_count);
</script>

<div class="operating-mode">
    <h1 class="titles">MODE DE FONCTIONNEMENT</h1>
    <!--Creation d'un menu déroulant-->
    <select>
        {#each actual_options as mode_option, index}
            <option value={index}>{mode_option}</option>
        {/each}
    </select>
</div>

<style>
    .titles {
        grid-column: 1 / span 3;
        font-weight: bold;
        font-size: 24px;
        color:black;
        font-family: 'Roboto', sans-serif;
    }
    .operating-mode{
        margin:15px;
    }

    select {
        background-color: #FF662E;
        color: black;
        font-size: 16px;
        border: 1px solid black;
        border-radius: 15px;
        padding: 8px 12px;
        width: 200px;
    }
</style>