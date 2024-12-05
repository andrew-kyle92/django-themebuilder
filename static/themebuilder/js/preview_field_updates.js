document.addEventListener("DOMContentLoaded", function() {
    const iframe = document.getElementById('live-preview');
    const header_iframe = document.getElementById(`preview-header`);
    const footer_iframe = document.getElementById(`preview-footer`);
    const headerInput = document.getElementById("id_header");
    const footerInput = document.getElementById("id_footer");

    // function updateSection(section, data) {
    //     const header_iframe = document.getElementById(`preview-${section}`);
    //     iframe.contentWindow.postMessage(data, '*');
    // }
    //
    // document.getElementById('header-options').addEventListener('input', function () {
    //     const headerData = { /* collect header data */ };
    //     updateSection('header', headerData);
    // });
    //
    // document.getElementById('footer-options').addEventListener('input', function () {
    //     const footerData = { /* collect footer data */ };
    //     updateSection('footer', footerData);
    // });

    function updatePreview() {
        const themeData = {
            primary_color: document.getElementById('id_primary_color').value,
            secondary_color: document.getElementById('id_secondary_color').value,
            background_color: document.getElementById('id_background_color').value,
            text_color: document.getElementById('id_text_color').value,
            accent_color: document.getElementById('id_accent_color').value,
            font_family: document.getElementById('id_font_family').value,
            base_font_size: document.getElementById('id_base_font_size').value,
            h1: document.getElementById('id_h1_size').value,
            h2: document.getElementById('id_h2_size').value,
            h3: document.getElementById('id_h3_size').value,
            h4: document.getElementById('id_h4_size').value,
            h5: document.getElementById('id_h5_size').value,
            h6: document.getElementById('id_h6_size').value,
            container_width: document.getElementById('id_container_width').value,
            padding: document.getElementById('id_padding').value,
            margin: document.getElementById('id_margin').value,
            border_radius: document.getElementById('id_border_radius').value,
            animation_type: document.getElementById('id_animation_type').value,
            duration: document.getElementById('id_duration').value,
            delay: document.getElementById('id_delay').value,
            // Add other settings as needed
        };
        // iframe.contentWindow.postMessage(themeData, '*');
        header_iframe.contentWindow.postMessage(themeData, '*');
        footer_iframe.contentWindow.postMessage(themeData, '*');
    }

    // update after load
    updatePreview();

    document.querySelectorAll('.general-config').forEach(field => {
        field.addEventListener('input', updatePreview);
    });

    // reload the header and footer iframes input on change
    // ** Header
    headerInput.addEventListener("change", () =>{
        header_iframe.src = header_iframe.src + `&requestedHeader=${headerInput.value}`;
    });

    // ** Footer
    footerInput.addEventListener("change", () =>{
        footer_iframe.src = header_iframe.src + `&requestedFooter=${footerInput.value}`;
    });
});
