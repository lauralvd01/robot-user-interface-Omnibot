<script >
    import logo_omnibot from '../lib/images/logo_omnibot.svg'
    import Button from "./Button.svelte";
    import logo_mines from '../lib/images/logo_mines.svg'
    import { goto } from '$app/navigation'

</script>

<header>
    <div class="banner">
        <a  href="/">
            <img class="logo" alt="Logo omnibot" src={logo_omnibot}/>
        </a>
        <!--Creation d'une barre de navigation-->
        <nav class="buttons-container">
            <Button class="default" on:click={() => goto('/modules_page')}>MODULES</Button>
            <Button class="default" on:click={() => goto('/graphics')}>GRAPHICS</Button>
            <Button class="default" on:click={() => goto('/graphics')}>RECORDS</Button>
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
    z-index: 999; 
}

header {
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


</style>


