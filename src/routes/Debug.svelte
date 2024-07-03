<script>
    import { onMount } from 'svelte';
  
    let lastCommand = '';
  
    // Function to handle key presses
    function handleKeyPress(event) {
      switch (event.key) {
        case 'z':
          lastCommand = 'Forward';
          break;
        case 's':
          lastCommand = 'Backward';
          break;
        case 'd':
          lastCommand = 'Right';
          break;
        case 'q':
          lastCommand = 'Left';
          break;
        case 'a':
          lastCommand = 'Rotate Left';
          break;
        case 'e':
          lastCommand = 'Rotate Right';
          break;
        case ' ':
          lastCommand = 'Stop';
          break;
        default:
          break;
      }
    }
  
    // Event listener for keydown event
    onMount(() => {
      window.addEventListener('keydown', handleKeyPress);
      return () => {
        window.removeEventListener('keydown', handleKeyPress);
      };
    });
  </script>
  
  <style>
    .container {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
  
    .message {
      font-size: 24px;
    }
  </style>
  
  <div class="container">
    {#if lastCommand}
      <p class="message">Last Command: {lastCommand}</p>
    {/if}
  </div>
  