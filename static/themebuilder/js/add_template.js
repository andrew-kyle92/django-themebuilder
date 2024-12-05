// add_template.js
// Description: logic for inline-uploading a new template file for the Header and Footer models.

// ***** Getting the csrf token for the fetch calls *****
function getCookie(name) {
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
const csrftoken = getCookie("csrftoken");

// ***** Fetch Methods *****
const saveTemplate = async (form) => {
    let formData = new FormData(form);
    return await fetch(form.action, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: formData,
    }).then(async (response) => {
        return response.json()
    });
}

window.addEventListener("load", () => {
    const addTemplateBtns = document.getElementsByClassName("addTemplate");
    if (addTemplateBtns) {
        // finding both add buttons, changing the text of the label on click
        for (let i = 0; i < addTemplateBtns.length; i++) {
            let templateBtn = addTemplateBtns[i];
            templateBtn.addEventListener("click", () => {
                let templateType = templateBtn.dataset.templateType;
                let templateTypeText = document.getElementById("templateTypeText");
                templateTypeText.innerText = templateType;
                // adding the template type to the form's hiddenfield
                let templateTypeInput = document.getElementById("id_template_type");
                templateTypeInput.value = templateType;
            });
        }

        // saving the template on submit
        const saveTemplateBtn = document.getElementById("saveTemplate");
        const form = document.getElementById("templateForm");
        form.addEventListener("submit", async (e) =>{
            // disable default
            e.preventDefault()

            let form = e.target
            let templateType = document.getElementById("id_template_type").value;
            let res = await saveTemplate(form);
            if (!res.errors) {
                let templateInput = document.getElementById(`id_${templateType}`);
                // remove current option
                while(templateInput.childElementCount > 0) {
                    templateInput.removeChild(templateInput.firstElementChild);
                }
                // adding the new options
                let newChoices = res.choices;
                for (let i = 0; i < newChoices.length; i++) {
                    let option = document.createElement("option");
                    option.value = newChoices[i][0];
                    option.innerText = newChoices[i][1];
                    templateInput.appendChild(option);
                }
                // clearing the form
                form.reset();
                // closing the form
                document.getElementById("templateUploadModal").querySelector(".btn-close").click();
            }
        });

        // hiding/un-hiding path input
        const customPathCheckbox = document.getElementById("id_custom_path");

        customPathCheckbox.addEventListener("change", () => {
            const uploadPathDiv = document.getElementById("uploadPathDiv");
            uploadPathDiv.hidden = !customPathCheckbox.checked;
        });
    }
});
