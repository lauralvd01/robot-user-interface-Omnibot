<script>
    import { onMount } from 'svelte';
    import Banner from './Banner.svelte';
    import RobotInfos from "./RobotInfos.svelte";
    import Blocs from "./Blocs.svelte";
    import Omnibot from './Omnibot.svelte';
    import PageInfo from './PageInfo.svelte';

    let bannerHeight = 0;

    //onMount est utilisée pour exécuter du code une fois que le composant est créé sur la page
    onMount(() => {
        const banner = document.querySelector('.banner');
        if (banner) {
            //récupération de la taille de la bannière
            bannerHeight = banner.offsetHeight;
        }
    });
</script>

<div class="homepage">
    <Banner class="banner"/>
    <div class="body">
        <div class="content">
            <div class="top" style="margin-top: {bannerHeight}px;">
                <div class="modules">
                    <Blocs/>   
                </div>
                <div class="omnibot">
                    <Omnibot/>
                </div>
                <div class="infos">
                    <PageInfo/>
                </div>
            </div>
        </div>
        <div class="bottom">
                <RobotInfos/>
        </div>
    </div>
</div>

<style>
    * {
        margin: 0px 5px 0px 5px;
        padding: 0;
        box-sizing: border-box;
    }

    
    .homepage {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .body {
        margin: 0px 20px 0px 20px;
        padding: 0;
        width: 100%;
        height: 100%;
    }

    .content {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        overflow: auto;
        height: 80%;
    }

    .top {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        flex-grow: 1;
        overflow: hidden;
        height: fit-content;
    }

    .modules {
        width: 33%;
        flex-shrink: 0;
        overflow-y: auto;
    }

    .omnibot {
        width: 33%;
        flex-shrink: 0;
    }

    .infos {
        width: 33%;
        flex-shrink: 0;
        overflow-y: auto;
    }

    .bottom {
        flex-shrink: 0;
        overflow-y: hidden;
        width: 100%;
        margin-top: 2%;
        margin-bottom: 1%;
    }
</style>
