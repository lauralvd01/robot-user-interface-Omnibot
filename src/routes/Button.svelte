<script>
    //Creation de la classe contenant les boutons, donne les propriétés
    let buttonProps = {
        class:[$$restProps.class]
        
    }
</script>

<!--Applications des propriétes de "buttonProps à l'élément button"-->
<button on:click
        on:mouseover
        on:mouseenter
        on:mouseleave
        on:focus
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
        font-family: "Roboto";
        font-weight: bold;
        margin: 1px 2px 1px 2px;
    }
    .default:hover{
        color:white;
    }

    .primary{
        border:solid 2px white;
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

    .primary-inverse{
        border:solid 2px #ff3700;
        border-radius: 12px;
        font-family: "Roboto";
        font-weight: 500;
        background-color: white;
        color:#ff3700;
    }

    .primary-inverse:hover{
        border:solid 2px black;
        border-radius: 12px;
        font-family: "Roboto";
        font-weight: 500;
        background-color: #ff3700;
        color:white;
    }

</style>