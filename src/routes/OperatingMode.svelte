<div class="operating-mode">
    <h1 class="titles">MODE DE FONCTIONNEMENT</h1>
    <!--Creation d'un menu déroulant-->
    <select>
        <option value="option2" selected>Tri-roues</option> <!--Option sélectionnée de base-->
        <option value="option3">Pas de roues</option>
        <option value="option4">Roue normales</option>
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