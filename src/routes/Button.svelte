<script>
    export let type = 'default';

    let buttonProps = {
        class:[$$restProps.class]
    }

</script>
<button on:click
        on:mouseover
        on:mouseenter
        on:mouseleave
        {...buttonProps}>
    <slot/>
</button>

<style>
    button {
        border: none;
        padding: 0.2rem 1.7rem;
        background-color: rgba(0,0,0,0);
        font-size: 15px;
        border-radius: 8px;
        transition: all 250ms;
        transform-origin: center;
    }

    button:hover {
        cursor: pointer;
        transform: scale(0.975);
    }

    .default {
        background-color: rgba(0,0,0,0);
    }
    .default:hover{
        color:white;
    }

    .primary{
        border:solid 2px black;
        border-radius: 12px;
        background-color: #ff3700;
        font-family: "Roboto";
        font-weight: 500;
        color:white;
    }

    .primary:hover{
        background-color: #FF662E;
        color:black;
    }

</style>