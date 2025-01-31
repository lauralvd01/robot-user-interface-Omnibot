<script>
    import { onMount } from "svelte";
    import { writable } from "svelte/store";
    import Banner from "../Banner.svelte";

    let bannerHeight = 0;
    onMount( () => {
        const banner = document.querySelector(".banner");
        if (banner) bannerHeight = banner.offsetHeight;
    })
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
        /* margin: 0px 5px 0px 5px; */
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
        /* margin: 0px 20px 0px 20px;
        padding: 0; */
        margin: 20px;
        display: flex;
        width: 100%;
        height: 100%;
        /* flex-direction: column;
        align-items: center; */
    }

    .content {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        overflow: auto;
        height: 100%;
        /* width: 70%; */
        width: 60%;
    }

    </style>