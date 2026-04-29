(() => {
    const root = document.documentElement;
    const toggle = document.querySelector("[data-theme-toggle]");

    const setTheme = (theme) => {
        root.dataset.theme = theme;
        localStorage.setItem("theme", theme);
        const isDark = theme === "dark";
        const label = isDark ? "Escuro" : "Claro";
        const icon = isDark ? "🌙" : "☀️";
        if (toggle) {
            toggle.setAttribute("aria-pressed", String(isDark));
            toggle.querySelector(".theme-toggle__icon").textContent = icon;
            toggle.querySelector(".theme-toggle__label").textContent = label;
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
