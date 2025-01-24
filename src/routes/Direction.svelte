<script>
    import arrow from "$lib/images/icone-fleche-droite-noir.png";
    import turn from "$lib/images/chargement-de-la-fleche-noire.png";

    export let moving = { x_linear_vel: 0, y_linear_vel: 0, angular_vel: 0 };
</script>

<div class="deplacements">
    <h1 class="titles">DIRECTION</h1>
    <div class="center">
        {#if moving.x_linear_vel !== 0 || moving.y_linear_vel !== 0 || moving.angular_vel !== 0}
            {#if moving.angular_vel === 0}
                <img
                    class="arrow"
                    alt="fleche directionnelle"
                    src={arrow}
                    style:transform={`scale(${Math.min(Math.sqrt((moving.x_linear_vel)**2+(moving.y_linear_vel)**2),1)}) rotate(${moving.x_linear_vel >= 0 ? (-Math.atan(moving.y_linear_vel / moving.x_linear_vel) * 180) / Math.PI : 180 - (Math.atan(moving.y_linear_vel / moving.x_linear_vel) * 180) / Math.PI}deg)`}
                />
            {:else}
                <img
                    class="arrow"
                    alt="fleche demi-tour"
                    src={turn}
                    style:transform={`scale(${Math.min(Math.abs(moving.angular_vel),1)}) rotateZ(90deg) ${moving.angular_vel > 0 ? "rotateX(180deg)" : ""}`}
                />
            {/if}
        {/if}
    </div>
</div>

<style>
    .deplacements {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
        height: 100%;
    }

    .titles {
        font-weight: bold;
        font-size: 24px;
        color: black;
        font-family: "Roboto", sans-serif;
        height: 20%;
    }

    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 90%;
        height: 80%;
    }

    .arrow {
        height: 30%;
        width: 30%;
        transition: transform 0.1s;
    }
</style>
