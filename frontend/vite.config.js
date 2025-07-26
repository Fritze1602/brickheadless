// frontend/vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

const isDev = process.env.NODE_ENV === "development";

export default defineConfig({
    plugins: [react()],
    root: __dirname,
    base: isDev ? "http://localhost:5173/" : "/static/",
    build: {
        outDir: "../brickheadless/static",
        emptyOutDir: true,
        manifest: true,
        rollupOptions: {
            input: {
                "app.bundle.js": path.resolve(__dirname, "src/main.ts"),
            },
            output: {
                entryFileNames: "app.bundle.[hash].js",
                assetFileNames: (assetInfo) => {
                    if (assetInfo.name?.endsWith(".css")) {
                        return "styles.[hash].css";
                    }
                    return "[name].[hash].[ext]";
                },
            },
        },
    },
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "src"),
        },
    },
    server: {
        port: 5173,
        strictPort: true,
        origin: "http://localhost:5173",
    },
});
