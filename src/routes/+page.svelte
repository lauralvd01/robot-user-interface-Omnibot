<script>
    import { onMount } from "svelte";
    import Banner from "./Banner.svelte";
    import RobotInfos from "./RobotInfos.svelte";
    import Blocs from "./Blocs.svelte";
    import Omnibot from "./Omnibot.svelte";
    import PageInfo from "./PageInfo.svelte";

    import { writable } from "svelte/store";

    const connected_modules = writable([]);

    async function fetchConnectedModules() {
        try {
            console.log("Fetching connected modules ...");
            const response = await fetch("http://localhost:8001/fetch_modules");
            const data = await response.json();
            connected_modules.set(data.data);
        } catch (error) {
            console.error("Error:", error);
        }
    }

    let bannerHeight = 0;

    onMount(async () => {
        const banner = document.querySelector(".banner");
        if (banner) {
            //récupération de la taille de la bannière
            bannerHeight = banner.offsetHeight;
        }

        await fetchConnectedModules();
    });

    connected_modules.subscribe((connected_modules_value) => {
        console.log("connected_modules_value", connected_modules_value);
    });
</script>

<div class="homepage">
    <Banner class="banner" />
    <div class="body">
        <div class="content">
            <div class="top" style="margin-top: {bannerHeight}px;">
                <div class="modules">
                    <Blocs connected_modules={$connected_modules}/>
                </div>
                <div class="omnibot">
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
