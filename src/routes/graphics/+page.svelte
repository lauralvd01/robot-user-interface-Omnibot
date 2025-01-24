<script>
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import Banner from "../Banner.svelte";

    import { backend_host, backend_port } from "../../config.js";

    const modules = writable([]);

    // Send a request to the backend to get the data
    async function fetchData(endpoint, store) {
        try {
            console.log(`Fetching ${endpoint.split("fetch_")[1]} ...`);
            const response = await fetch(endpoint); // Send a request to the backend
            const data = await response.json(endpoint); // Parse response and get data as a JSON object
            // console.log(data);
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

    let bannerHeight = 0;

    // Function that runs when the component is mounted
    onMount(async () => {
        // Get banner height to adjust the top margin of the content under it
        const banner = document.querySelector(".banner");
        if (banner) {
            bannerHeight = banner.offsetHeight;
        }

        // Fetch existant modules
        fetchData(`http://${backend_host}:${backend_port}/fetch_modules`, modules);
    });
</script>

<div class="homepage">
    <Banner />
    <div class="body" style="margin-top: {bannerHeight}px;">
        <div class="content">
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

    </style>
