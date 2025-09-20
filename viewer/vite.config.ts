import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  // Ensure assets resolve correctly on GitHub Pages project site
  // e.g., https://soheibthriber.github.io/langchain/
  base: '/langchain/',
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://127.0.0.1:8000'
    }
  }
})
