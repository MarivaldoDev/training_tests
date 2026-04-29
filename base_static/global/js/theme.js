(() => {
    const root = document.documentElement;
    const toggle = document.querySelector("[data-theme-toggle]");

    const setTheme = (theme) => {
        root.dataset.theme = theme;
        localStorage.setItem("theme", theme);
        const isDark = theme === "dark";
        if (toggle) {
            toggle.setAttribute("aria-pressed", String(isDark));
            toggle.querySelector(".theme-toggle__icon").textContent = isDark ? "🌙" : "☀️";
            toggle.querySelector(".theme-toggle__label").textContent = isDark ? "Escuro" : "Claro";
        }
    };

    if (toggle) {
        toggle.addEventListener("click", () => {
            const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
            setTheme(nextTheme);
        });
    }

    const storedTheme = localStorage.getItem("theme");
    const initialTheme = storedTheme || root.dataset.theme || "light";
    setTheme(initialTheme);
})();
