<script>
    import { onMount } from 'svelte';
    import Banner from './Banner.svelte'
    import RobotInfos from "./RobotInfos.svelte";
    import Blocs from "./Blocs.svelte";
    import Omnibot from './Omnibot.svelte';
    import PageInfo from './PageInfo.svelte';
    //import Debug from './Debug.svelte';

    let bannerHeight = 0;

    onMount(() => {
        const banner = document.querySelector('.banner');
        if (banner) {
            bannerHeight = banner.offsetHeight;
        }
    });
</script>

<div class="homepage">
    <Banner class="banner"/>
    <div class="content">
        <div class="top" style="margin-top: {bannerHeight}px;">
            <div class="infos">
                <Blocs/>   
            </div>
            <Omnibot/>
            <PageInfo/>
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

    html, body {
        margin: 0px 20px 0px 20px;
        padding: 0;
        width: 100%;
        height: 100%;
    }

    .homepage {
        display: flex;
        flex-direction: column;
        height: 100vh;
        overflow: hidden;
    }

    .banner {
        flex-shrink: 0;
    }

    .content {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        overflow: hidden;
    }

    .top {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        flex-grow: 1;
        overflow: hidden;
    }

    .infos {
        flex-shrink: 0;
        overflow-y: auto;
    }

    .bottom {
        flex-shrink: 0;
        overflow-y: auto;
    }
</style>