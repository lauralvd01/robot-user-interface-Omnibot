<script>
    import { onMount } from 'svelte';
    import Banner from './Banner.svelte'
    import RobotInfos from "./RobotInfos.svelte";
    import Blocs from "./Blocs.svelte";
    import Omnibot from './Omnibot.svelte';
    import PageInfo from './PageInfo.svelte';

    let bannerHeight = 0;

    onMount(() => {
        const banner = document.querySelector('.banner');
        if (banner) {
            bannerHeight = banner.offsetHeight;
        }
    });
</script>

<div class="homepage">
    <Banner/>
    <div class="top" style="margin-top: {bannerHeight}px;">
        <div class="infos">
            <Blocs/>   
        </div>
        <Omnibot/>
        <PageInfo/>
    </div>
    <div class = "bottom">
        <RobotInfos/>
    </div>
</div>

<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
    }
    .homepage {
        height: 100vh;
        display: flex;
        flex-direction: column;
        margin: 10px 30px;
    }

    .top {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        flex-grow: 1;
    }

</style>
