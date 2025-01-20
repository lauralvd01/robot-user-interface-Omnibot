<script>
    import Controller from "../Controller.svelte";
    import Range from "../Range.svelte";

    import { backend_host, backend_port } from "../../config.js";

    function sendMoveData(moves) {
        console.log(moves);
        // Send a request to the backend to move the robot
        fetch(`http://${backend_host}:${backend_port}/post_move`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(moves),
        });
    }

    let linear_speed = 1;
    let angular_speed = 2;

    function sendSpeedData() {
        console.log(linear_speed, angular_speed);
        // Send a request to the backend to move the robot
        fetch(`http://${backend_host}:${backend_port}/set_speed`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                linear_speed: linear_speed,
                angular_speed: angular_speed,
            }),
        });
    }

</script>

<div>
    <div>
        <Controller move={sendMoveData} />
    </div>
</div>
    <!-- <div>
        <label for="linear-range">Linear speed</label>
        <Range
            on:change={(e) => {
                linear_speed = e.detail.value;
                sendSpeedData();
            }}
            min={0}
            max={25}
            initialValue={1}
            bind:value={linear_speed}
            id="speed-slider"
        />
        
    <h3>
        Linear speed: {linear_speed}
    </h3>
        <label for="angular-range">Angular speed</label>
        <Range on:change={(e) => {angular_speed = e.detail.value; sendSpeedData();}}
            min={0}
            max={25}
            initialValue={2}
            bind:value={angular_speed}
            id="angular-slider"
        />
    <h3>
        Angular speed: {angular_speed}
    </h3>
    </div> -->
    
    <style>

        h3 {
            text-align: center;
        }
        
        label {
            margin: 8px;
            font-size: 16px;
            font-weight: 600;
        }

    :global(*) {
        box-sizing: border-box;
    }

    :global(body, html) {
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    </style>