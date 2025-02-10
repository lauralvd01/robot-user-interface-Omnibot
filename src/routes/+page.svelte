<script>
    import { onMount } from "svelte";
    import Banner from "./Banner.svelte";
    import RobotInfos from "./RobotInfos.svelte";
    import Blocs from "./Blocs.svelte";
    import Omnibot from "./Omnibot.svelte";
    import PageInfo from "./PageInfo.svelte";
    import Button from "./Button.svelte";

    import { connected_modules, fetchData } from "./data_store";
    import { simulating } from "./data_store";

    // Store banner height to adjust the top margin of the content under it
    let bannerHeight = 0;

    // Function that runs when the component is mounted
    onMount(async () => {
        const banner = document.querySelector(".banner");
        if (banner) bannerHeight = banner.offsetHeight;

        // Start fetching data from backend every second (Start automatically when simulating is initialized to true)
        // fetchData("current_data");
    });

    // let interval;
    // $: {if ($simulating) {
    //     interval = setInterval(() => fetchData("settings"), 5000); // Change the simulated response settings every 5 seconds
    //     }
    //     else if (interval) {
    //         clearInterval(interval);
    //     }
    // }
</script>

<div class="homepage">
    <Banner />
    <div class="body">
        <div class="content">
            <div class="top" style="margin-top: {bannerHeight}px;">
                <div class="modules">
                    <Blocs/>
                </div>
                <div class="omnibot">
                    <Button class="primary-inverse" on:click={() => fetchData("simulating")}>{ $simulating ? "Se connecter au robot" : "Simuler le robot" }</Button>
                    <Omnibot />
                </div>
                <div class="infos">
                    <PageInfo />
                </div>
            </div>
        </div>
        <div class="bottom">
            <RobotInfos />
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
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
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
