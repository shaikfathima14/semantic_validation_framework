/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#5B8DEF",
        secondary: "#A8D8FF",
        background: "#EEF7FF",
        pastel: "#C9B6FF",
        success: "#9EE6B8",
        warning: "#FFD6A5",
        danger: "#FFB7C5",
      },

      fontFamily: {
        heading: ["Poppins", "sans-serif"],
        body: ["Inter", "sans-serif"],
      },

      borderRadius: {
        xl: "20px",
        "2xl": "28px",
      },

      boxShadow: {
        soft: "0 10px 30px rgba(91,141,239,0.12)",
      },
    },
  },
  plugins: [],
}