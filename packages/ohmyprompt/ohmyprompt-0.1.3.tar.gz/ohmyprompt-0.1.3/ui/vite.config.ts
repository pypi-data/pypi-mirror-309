import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "../src/ohmyprompt/web/static/dist",
    // emptyOutDir: true,
    // sourcemap: true,
    rollupOptions: {
      output: {
        entryFileNames: "assets/index.js",
        assetFileNames: 'assets/[name].[ext]',
        manualChunks: () => 'index',
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
