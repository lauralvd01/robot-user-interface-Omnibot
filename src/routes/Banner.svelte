<script >
    import logo_omnibot from '$lib/images/logo_omnibot.svg'
    import Button from "./Button.svelte";
    import logo_mines from '$lib/images/logo_mines.svg'
    export let bannerHeight;
</script>

<header>
    <div class="banner">
        <img class="logo" alt="Logo omnibot" src={logo_omnibot}/>
        <nav class="buttons-container">
            <Button class="default">PANNEAU DE CONTROLE</Button>
            <Button class="default">MANUEL D'UTILISATION</Button>
            <Button class="default">LE PROJET</Button>
        </nav>
        <img class="logo" alt="logo mines" src={logo_mines}>
    </div>
</header>

<style>

.banner {
    position: fixed; 
    top: 0; 
    left:0;
    width: 100%;
    display: flex;
    height: 80px;
    justify-content: space-between;
    align-items: center;
    background-color: #FF662E;
    padding: 0 45px;
    box-sizing: border-box;
    z-index: 999; /* Assurez-vous que la banner est au-dessus de tout */
}

.banner-content {
    width: 100%;
    max-width: 1200px; 
    margin: 0 auto; 
}


body, header {
    margin: 0;
}

.logo {
    height: 60px;
    margin: 0;
}

.buttons-container {
    display: flex;
    align-items: center;
}

.button {
    color: black;
    margin: 0 10px;
}

</style>


