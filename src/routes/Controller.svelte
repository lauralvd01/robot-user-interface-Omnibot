
<script>
    import { sendMoveData as move} from "./data_store";	
	import { d_speed } from "./data_store"; // = {"du": false, "dd": false, "dl": false, "dr": false};

	let poll;
	
	$: stickl = () => {
		let x = axisMap.lx * 25;
		let y = axisMap.ly * 25;
		let rx = axisMap.lx * 10;
		let ry = axisMap.ly * 10;
		let z = 1 - buttonMap.lstick * 0.05;
        if (x > 25 || y > 25 || x < -25 || y < -25) {
            move({
                x_linear_vel: Math.round(y/25),
                y_linear_vel: Math.round(x/25),
                angular_vel: 0
            });
        };
		return `translateX(${x}%) translateY(${y}%) rotateY(${rx}deg) rotateX(${ry}deg) scale(${z})`; 
	}
	
	$: stickr = () => {
		let x = axisMap.rx * 25;
		let y = axisMap.ry * 25;
		let rx = axisMap.rx * 10;
		let ry = axisMap.ry * 10;
		let z = 1 - buttonMap.rstick * 0.05;
        if (rx > 10 || ry > 10 || rx < -10 || ry < -10 ) {
            move({
                x_linear_vel: 0,
                y_linear_vel: 0,
                angular_vel: Math.round(x)/10
            });
        };
		return `translateX(${x}%) translateY(${y}%) rotateY(${rx}deg) rotateX(${ry}deg) scale(${z})`;
	}
	
	$: trigger = (side) => {
		let s = buttonMap[side];
		let sx = ( side === 'rt' ) ? -s : s;
		return `
			transform: scaleX(${sx}) scaleY(${s}) rotate(-69deg);
			opacity: ${0.3 + s};
		`;
	}

	let buttonMap = {
		a: 0,
		b: 0,
		x: 0,
		y: 0,
		lb: 0,
		rb: 0,
		lt: 0,
		rt: 0,
		map: 0,
		menu: 0,
		lstick: 0,
		rstick: 0,
		du: 0,
		dd: 0,
		dl: 0,
		dr: 0,
		xbox: 0
	};
	
	let axisMap = {
		lx: 0,
		ly: 0,
		rx: 0,
		rx: 0
	};

	const plugIn = () => {
        // console.log("Gamepad connected");
		startController();
	}
	
	const unPlug = () => {
        // console.log("Gamepad disconnected");
		cancelAnimationFrame(poll);
	}

	const startController = () => {
		
		const gamepads = navigator.getGamepads();
		if (!gamepads) { return; }
		const defined_gamepads = gamepads.reduce((acc, pad) => {
			if (pad) { acc.push(pad); }
			return acc;
		}, []);
		if (!defined_gamepads.length) { return; }
		const pad = defined_gamepads[0];
		const buttons = ["a","b","x","y","lb","rb","lt","rt","map","menu","lstick","rstick","du","dd","dl","dr","xbox"];
		const axes = ["lx","ly","rx","ry"];
		
		pad.buttons.forEach((button,i) => {
			buttonMap[buttons[i]] = ( button.pressed ) ? button.value : 0;
            if (button.pressed && button.value > 0.01) {
                console.log(buttons[i], button.value);
				if (buttons[i] === "du") {
					$d_speed["du"] = true;
				} else if (buttons[i] === "dd") {
					$d_speed["dd"] = true;
				} else if (buttons[i] === "dl") {
					$d_speed["dl"] = true;
				} else if (buttons[i] === "dr") {
					$d_speed["dr"] = true;
				}
            }
		});
		
		pad.axes.forEach((axis,i) => {
			axisMap[axes[i]] = ( axis > 0.01 || axis < -0.01 ) ? parseFloat(axis.toFixed(3)) : 0;
		});
		
		poll = requestAnimationFrame(startController);
		
	}

</script>

<svelte:window 
  on:gamepadconnected={plugIn}
  on:gamepaddisconnected={unPlug}
/>

<section class="controller">
	<div class="pad"></div>
	<div class="well left">
		<div class="stick" class:click={buttonMap.lstick} style="transform: {stickl()};"></div>
	</div>
	<div class="well right">
		<div class="stick" class:click={buttonMap.rstick} style="transform: {stickr()};"></div>
	</div>
	<button class="button a" class:on={buttonMap.a}></button>
	<button class="button b" class:on={buttonMap.b}></button>
	<button class="button x" class:on={buttonMap.x}></button>
	<button class="button y" class:on={buttonMap.y}></button>
	<button class="button map" class:on={buttonMap.map}></button>
	<button class="button menu" class:on={buttonMap.menu}></button>
	<button class="button xbox" class:on={buttonMap.xbox}></button>
	<button class="dpad du" class:on={buttonMap.du}></button>
	<button class="dpad dr" class:on={buttonMap.dr}></button>
	<button class="dpad dd" class:on={buttonMap.dd}></button>
	<button class="dpad dl" class:on={buttonMap.dl}></button>
	<button class="bumper left" class:on={buttonMap.lb}></button>
	<button class="bumper right" class:on={buttonMap.rb}></button>
	<button class="trigger left" style="{trigger('lt')}"></button>
	<button class="trigger right" style="{trigger('rt')}"></button>
</section>

<style>
	
	.controller {
		position: relative;
		width: 90%;
		margin-bottom: 5%;
	}
	
	.controller > * {
		position: absolute;
		display: block;
		appearance: none;
		border: none;
		padding: 0;
		z-index: 1;
	}
	
	.controller > *:not(.pad):not(.stick):not(.well) {
		animation: flash 4s ease 1 2s;
	}

	.pad {
		background-image: url("https://s3-us-west-2.amazonaws.com/s.cdpn.io/13471/xbox-controller.jpg");
		background-size: contain;
		background-repeat: no-repeat;
		background-position: center;
		position: relative;
		width: 100%;
		padding-top: 56.2416%;
		border-radius: 5%;
	}
	
	.well {
		background: #16bef2;
		background-image: linear-gradient(25deg, #44494a, #555658 40%, #555658 60%, #44494a);
		left: 26.5%;
		top: 14.6%;
		width: 10.6%;
    padding-top: 10.2%;
		border-radius: 100%;
		box-shadow: inset 0.05vw -0.05vw 0.1vw 0.05vw rgba(0,0,0,0.3),  inset -0.05vw 0.05vw 0.05vw 0.05vw rgba(255,255,255,0.3);
	}
	
	.well.right {
		left: auto;
		right: 35.1%;
		top: 33.1%;
	}
	
	.well::before {
		content: "";
		position: absolute;
		left: 7%;
		top: 8%;
		width: 86%;
		height: 84%;
		border-radius: 100%;
		background-color: #16bef2;
		box-shadow: inset -0.05vw 0.1vw 0.2vw 0.2vw #444547, inset 0vw -0.1vw 0.1vw 0.1vw #18607c, inset 0 0 0 0.2vw #444547, inset 0 0 0.2vw 0.5vw #18607c, inset 0 0 2vw 1vw #18607c;
		z-index: 0;
	}
	
	.stick {
		position: absolute;
		left: 11%;
		top: 2%;
		background: url("https://s3-us-west-2.amazonaws.com/s.cdpn.io/13471/xbox-controller.jpg");
		width: 78%;
    padding-top: 78%;
    background-position: 30.1% 18.5%;
		background-size: 1300%;
		border-radius: 100%;
		box-shadow: inset 0.5vw -0.5vw 1vw 0.1vw rgba(0,0,0,0.3), -0.5vw 1vw 1vw rgba(0,0,0,0.5), -1.2vw 2vw 2vw rgba(0,0,0,0.6);
		transition: none;
		z-index: 3;
	}
	
	.stick:after {
		content: "";
		position: absolute;
		left: 0;
		top: 0;
		width: 100%;
		height: 100%;
		background: #aaa;
		border-radius: 100%;
		mix-blend-mode: overlay;
		box-shadow: inset 0 0 1vw 1vw rgba(255,255,255,0), inset 0 0 0.3vw 0.5vw rgba(97,229,255,0.5), 0 0 0.6vw .4vw rgba(94,224,248,1), 0 0 1.2vw .4vw rgba(94,224,248,0.8);
		transition: all 0.1s ease;
		opacity: 0;
	}
	
	.button.on,
	.dpad.on,
	.bumper.on,
	.stick.click:after {
		opacity: 1;
	}
	
	.button {
		width: 4.7%;
		padding-top: 4.7%;
		border-radius: 100%;
		right: 29.3%;
		top: 28%;
		background: #5cff00;
		box-shadow: 0.1vw 0.2vw 0.4vw 0.3vw #5cff00, 0.1vw 0.3vw 2vw 0.5vw #5cff00;
		mix-blend-mode: overlay;
		transition: all 0.25s ease;
		z-index: 2;
		opacity: 0;
	}
	
	.button.b {
		right: 24.4%;
		top: 21%;
		background: #ff0033;
		box-shadow: 0vw 0vw 0.4vw 0.3vw #ff0033, 0.1vw 0.3vw 2vw 0.5vw #ff0033;
	}
	
	.button.x {
		right: 34.1%;
		top: 20%;
		background: #00ebff;
		box-shadow: 0.1vw 0.2vw 0.4vw 0.3vw #00ebff, 0.1vw 0.3vw 2vw 0.5vw #00ebff;
	}
	
	.button.y {
		right: 29.3%;
		top: 12%;
		background: #ffd600;
		box-shadow: 0vw 0.1vw 0.4vw 0.3vw #ffd600, 0.1vw 0.3vw 2vw 0.5vw #ffd600;
	}
	
	.button.map,
	.button.menu {
		left: 43.4%;
		top: 21.4%;
		width: 2.9%;
		padding-top: 2.8%;
		background: white;
		box-shadow: inset 0 0 0.5vw 0.2vw #5ee0f8, 0 0.1vw 0.3vw 0.4vw #5ee0f8, 0 0.1vw 1.5vw 0.7vw #5ee0f8, 0 0.1vw 0.2vw 0.1vw #5ee0f8;
	}
	
	.button.menu {
		left: 53.8%;
	}
	
	.button.xbox {
		left: 47.6%;
		top: 7.7%;
		width: 4.8%;
		padding-top: 4.4%;
		background: #5cff00;
		mix-blend-mode: screen;
		box-shadow: inset 0 0 0.1vw 0.1vw white, 0 0.1vw 0.2vw 0.2vw white, 0 0.1vw 0.5vw 0.1vw white, 0 0.1vw 2vw 0.5vw rgba(92,255,0,0.7);
		transition-duration: 0.5s;
	}
	
	.dpad {
		width: 3.5%;
		padding-top: 4.8%;
		border-radius: 20%;
		left: 38.8%;
		top: 34.8%;
		background: linear-gradient(0deg, transparent, #4ed5e0, #33f0ff);
		box-shadow: 0 -1.4vw 1.7vw 0.2vw #4ed5e0, 0 -2vw 1.4vw 0.2vw rgba(255,255,255,1);
		mix-blend-mode: overlay;
		transition: all 0.2s ease;
		opacity: 0;
	}
	
	.dpad.dr {
		left: 42%;
		top: 40%;
		transform: rotate(90deg);
	}
	
	.dpad.dd {
		top: 46%;
		transform: rotate(180deg);
	}
	
	.dpad.dl {
		left: 35.6%;
		top: 40%;
		transform: rotate(270deg);
	}
	
	.bumper {
		left: 25.5%;
		top: 3.6%;
		width: 13%;
		padding-top: 4%;
		transform: rotate(-20deg);
		border-radius: 100%;
		background: #7edbff;
		box-shadow: -0vw -0vw 2vw 1vw #7edbff;
		mix-blend-mode: darken;
		transition: all 0.2s ease;
		opacity: 0;
	}
	
	.bumper:after {
		content: "";
		left: 20%;
		top: 10%;
		width: 60%;
		height: 40%;
		border-radius: 100%;
		background: cyan;
		mix-blend-mode: screen;
		box-shadow: -0vw -0vw 1vw 0.5vw cyan;
		z-index: 2;
	}
	
	.bumper.right {
		left: auto;
		right: 25.4%;
		transform: scaleX(-1) rotate(-22deg);
	}
	
	.trigger {
		left: 15.1%;
		top: 24%;
		width: 10%;
		padding-top: 6px;
		transform: scaleX(1) scaleY(1) rotate(-69deg); /*nice*/
		border-radius: 2vw;
		background: #7edbff;
		box-shadow: -0vw -1vw 4vw 4vw #7edbff;
		mix-blend-mode: darken;
		transition: all 0.2s ease;
		opacity: 0;
	}
	
	.trigger.right {
		left: auto;
		right: 15.1%;
		transform: scaleX(-1) scaleY(1) rotate(-69deg); /*nice*/
	}
	
	@keyframes flash {
		0% { opacity: 0; }
		25% { opacity: 1; }
	}
	
</style>