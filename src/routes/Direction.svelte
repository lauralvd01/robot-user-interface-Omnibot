<script>
    import arrow from '$lib/images/icone-fleche-droite-noir.png'
</script>

<div class="deplacements">
    <div class="direction">
        <h1 class="titles">DIRECTION</h1>
        <img class="arrow" alt="fleche directionnelle" src={arrow}/>
    </div>
    <div class="vitesse">
        <p>x m/s</p>
    </div>
</div>


<style>
    .deplacements{
        display:flex;
        flex-direction: column;
        align-items: left;
    }

    .direction{
        width: 300px;
        height: 150px;
        display: flex;
        flex-direction: column;
        margin: 5px 15px;
        align-items: left;
    }
    .arrow{
        height:100px;
        width: 100px;
    }
    .titles {
        grid-column: 1 / span 3;
        font-weight: bold;
        font-size: 24px;
        color:black;
        font-family: 'Roboto', sans-serif;
    }

    .vitesse{
        border: 3px solid #A1CEE1; 
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
        color:black;
        font-family: 'Roboto',sans-serif;

    }
    


</style>