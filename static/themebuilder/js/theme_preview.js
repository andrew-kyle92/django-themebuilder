window.addEventListener("message", function(event) {
    const themeData = event.data;
    document.documentElement.style.setProperty('--primary-color', themeData.primary_color || '');
    document.documentElement.style.setProperty('--secondary-color', themeData.secondary_color || '');
    document.documentElement.style.setProperty('--background-color', themeData.background_color || '');
    document.documentElement.style.setProperty('--text-color', themeData.text_color || '');
    document.documentElement.style.setProperty('--accent-color', themeData.accent_color || '');
    document.documentElement.style.setProperty('--font-family', themeData.font_family || '');
    document.documentElement.style.setProperty('--base-font-size', themeData.base_font_size || '');
    document.documentElement.style.setProperty('--h1-font-size', themeData.h1 || '');
    document.documentElement.style.setProperty('--h2-font-size', themeData.h2 || '');
    document.documentElement.style.setProperty('--h3-font-size', themeData.h3 || '');
    document.documentElement.style.setProperty('--h4-font-size', themeData.h4 || '');
    document.documentElement.style.setProperty('--h5-font-size', themeData.h5 || '');
    document.documentElement.style.setProperty('--h6-font-size', themeData.h6 || '');
    document.documentElement.style.setProperty('--container-width', themeData.container_width || '');
    document.documentElement.style.setProperty('--padding', themeData.padding || '');
    document.documentElement.style.setProperty('--margin', themeData.margin || '');
    document.documentElement.style.setProperty('--border-radius', themeData.border_radius || '');
    document.documentElement.style.setProperty('--animation-type', themeData.animation_type || '');
    document.documentElement.style.setProperty('--animation-duration', themeData.duration || '');
    document.documentElement.style.setProperty('--animation-delay', themeData.delay || '');
    // Update other properties as needed
});