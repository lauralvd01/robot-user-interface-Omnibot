<script>
	import Controller from "../Controller.svelte";

    import { backend_host, backend_port } from '../../config.js';

    function sendMoveData(moves) {
        console.log(moves);
        // Send a request to the backend to move the robot
        fetch(`http://${backend_host}:${backend_port}/post_move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(moves)
        });
    }
</script>

<h1>Plug in an XBOX controller, and play around!</h1>
<Controller move={sendMoveData}/>
<h2>Experimenting with the <a href="https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API/Using_the_Gamepad_API">GamePadApi</a> with Svelte</h2>

<style>
	
	:global(*) {
		box-sizing: border-box;
	}
	
	:global(body,html) {
		width: 100%;
		height: 100%;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	
	h1 {
		margin: 3vw;
		font-size: 3vw;
	}
	
	h2 {
		margin: 2.4vw;
		font-size: 2.4vw;
	}
	
	a {
		color: #17a1cc;
	}
	
</style>