// ***** Getting the csrf token for the fetch calls *****
export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.addEventListener("load", () => {
    // Tabs portion of the page
    var tabHeaders = document.getElementsByClassName("tab-header");
    if (tabHeaders.length > 0) {
        for (let i = 0; i < tabHeaders.length; i++) {
            tabHeaders[i].addEventListener("click", () => {
                let tab = document.getElementById(tabHeaders[i].dataset.tabId);
                let tabContentDiv = document.getElementById("tabs-content");
                let currentTabContent = tabContentDiv.querySelector(".show-tab");
                let currentTabLink = document.getElementById("tab-links").querySelector(".active");
                if (!tab.classList.contains("show-tab")) {
                    // hide current tab content
                    currentTabContent.classList.remove("show-tab");
                    // remove active class from tab link
                    currentTabLink.classList.remove("active");

                    // reveal tab content
                    tab.classList.add("show-tab");
                    // add active class to tab link
                    tabHeaders[i].classList.add("active");
                }
            });
        }
    }

    // bootstrap version input
    var bootstrapVersionInput = document.getElementById("id_bootstrap_version");
    if (bootstrapVersionInput) {
        let bootstrapCheckbox = document.getElementById("id_use_bootstrap");
        bootstrapCheckbox.addEventListener("change", () => {
           if (!bootstrapCheckbox.checked) {
               bootstrapVersionInput.setAttribute("readonly", "true");
               bootstrapVersionInput.classList.add("read-only");
           }
           else {
               bootstrapVersionInput.setAttribute("readonly", "false");
               bootstrapVersionInput.classList.remove("read-only");
           }
        });
    }
});