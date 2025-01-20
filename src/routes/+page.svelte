<script>
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import Banner from "./Banner.svelte";
    import RobotInfos from "./RobotInfos.svelte";
    import Blocs from "./Blocs.svelte";
    import Omnibot from "./Omnibot.svelte";
    import PageInfo from "./PageInfo.svelte";
    import Button from "./Button.svelte";

    import { backend_host, backend_port } from "../config.js";

    const connected_modules = writable([]);
    const batteries_data = writable([]);
    const settings = writable(1);
    const simulating = writable(true);

    // Send a request to the backend to get the data
    async function fetchData(endpoint, store) {
        try {
            console.log(`Fetching ${endpoint.split("fetch_")[1]} ...`);
            const response = await fetch(endpoint); // Send a request to the backend
            const data = await response.json(endpoint); // Parse response and get data as a JSON object
            console.log(data);
            if (data.ok === true) {
                store.set(data.data); // Set the store with the data received
            } else {
                console.error("Error:", data.error);
                store.set(data.default); // Set the store with the default value
            }
        } catch (error) {
            console.error("Error:", error);
            store.set([]); // Set the store with an empty array
        }
    }

    function simulateRobot() {
        fetchData(`http://${backend_host}:${backend_port}/fetch_simulating`, simulating);
    }

    let bannerHeight = 0;

    // Function that runs when the component is mounted
    onMount(async () => {
        // Get banner height to adjust the top margin of the content under it
        const banner = document.querySelector(".banner");
        if (banner) {
            bannerHeight = banner.offsetHeight;
        }

        // Fetch connected modules every second
        // fetchData(`http://${backend_host}:${backend_port}/fetch_connected_modules`, connected_modules);
        const interval = setInterval(() => fetchData(`http://${backend_host}:${backend_port}/fetch_connected_modules`, connected_modules), 1000);

        // Fetch batteries data every second
        // fetchData(`http://${backend_host}:${backend_port}/fetch_batteries`, batteries_data);
        const interval2 = setInterval(() => fetchData(`http://${backend_host}:${backend_port}/fetch_batteries`, batteries_data), 1000);

        // Temporary
        const interval3 = setInterval(() => fetchData(`http://${backend_host}:${backend_port}/fetch_settings`, settings), 5000);

        return () => {
            clearInterval(interval);
            clearInterval(interval2);
            clearInterval(interval3);
        };
    });
</script>

<div class="homepage">
    <Banner />
    <div class="body">
        <div class="content">
            <div class="top" style="margin-top: {bannerHeight}px;">
                <div class="modules">
                    <Blocs connected_modules={$connected_modules}/>
                </div>
                <div class="omnibot">
                    <Button class="primary-inverse" on:click={simulateRobot}>{ $simulating ? "Se connecter au robot" : "Simuler le robot" }</Button>
                    <Omnibot connected_modules={$connected_modules}/>
                </div>
                <div class="infos">
                    <PageInfo />
                </div>
            </div>
        </div>
        <div class="bottom">
            <RobotInfos batteries_data={$batteries_data}/>
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
