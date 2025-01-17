import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

// See https://vite.dev/config/server-options.html for more options
export default defineConfig({
	plugins: [sveltekit()],
	server: { 				// Options for npm run dev
		port: 5173,				// default = 5173
		strictPort: true,		// true = fail if port is already in use, false = run server on next available port
		host: 'localhost',		// default = 'localhost'
	},
	preview: { 				// Options for npm run preview (after npm run build)
		port: 4173,				// default = 4173
		strictPort: true,		// true = fail if port is already in use, false = run server on next available port
	}
});
