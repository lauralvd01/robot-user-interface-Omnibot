<script>

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
        color:white;
    }

</style>