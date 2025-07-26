// tailwind.config.js (im Projekt-Root, NICHT in /frontend)
export default {
    content: [
        "./frontend/src/**/*.{js,jsx,ts,tsx}", // React-Komponenten
        "./templates/**/*.html",               // Django Templates
        "./**/*.html",                         // Optional: alle HTML-Dateien
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    DEFAULT: "#1e40af",
                    light: "#60a5fa",
                    dark: "#1e3a8a",
                },
            },
        },
    },
    plugins: [],
};
