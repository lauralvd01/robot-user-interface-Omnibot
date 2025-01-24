<script>
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import Banner from "../Banner.svelte";
    import Graphic from "./Graphic.svelte";
    // import data from "./data.js";

    import { backend_host, backend_port } from "../../config.js";

    const power_infos = writable([]);
    const data = writable({});
    const data_array = writable([]);

    function updateData(power_infos) {
        power_infos.forEach(module => {
            if ($data[module.slot_id]) {
                $data[module.slot_id].push({date: new Date(), power_flow: module.power_flow});
            } else {
                $data[module.slot_id] = [{date: new Date(), power_flow: module.power_flow}];
            }
            });
        data_array.set(Object.entries($data).map(([key, value]) => ({id: key, data: value})));
        console.log("Data_array ",$data_array);
    };
//         [
//   {
//     id: 'Northeast',
//     data: northeast
//   },
//   {
//     id: 'Midwest',
//     data: midwest
//   },
//   {
//     id: 'South',
//     data: south
//   },
//   {
//     id: 'West',
//     data: west
//   }
// ]
    // }

    $: power_infos && data && data_array && updateData($power_infos);

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

        // Fetch power_infos data
        // fetchData(`http://${backend_host}:${backend_port}/fetch_power_infos`, power_infos);
        const interval = setInterval(() => {fetchData(`http://${backend_host}:${backend_port}/fetch_power_infos`, power_infos);},5000);

        return () => {
            clearInterval(interval);
        };
    });
</script>

<div class="homepage">
    <Banner />
    <div class="body" style="margin-top: {bannerHeight}px;">
        <div class="content">
            {#if $data_array.length === 0}
                <p>Loading...</p>
            {:else}
                {#key $data_array}  
                    <Graphic data={$data_array} width={1000} height={500}/> 
                {/key}
            {/if}
        </div>
    </div>
</div>

<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .homepage {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .body {
        margin: 20px;
        display: flex;
        width: 100%;
        height: 100%;
        flex-direction: column;
        align-items: center;
    }

    .content {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        overflow: auto;
        height: 100%;
        width: 80%;
    }

    </style>
