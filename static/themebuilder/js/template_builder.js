// ***** Imports *****
import { getCookie } from "./main";
import { Element, Template } from "./templateClasses";

// ***** Getting the csrf cookie *****
const csrftoken = getCookie("csrftoken");

// ***** Fetch Calls *****
const get_element = async (el) => {
    let url = "/get-element/?" + new URLSearchParams({"element": el});
    return await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        }
    }).then(async (response) => {
        return response.json()
    });
}

// ***** Global variables *****
let templateConfigs = {};

// ***** Script Functions *****
let templateConfig = {};

function renderElement(element, parentId) {
    const parentElement = parentId
        ? document.getElementById(parentId)
        : document.getElementById("template-root");
    const newDiv = document.createElement("div");
    newDiv.id = element.id;
    newDiv.innerHTML = `
        <div>${element.type}</div>
        <button onclick="editContent('${element.id}')">Edit Content</button>
        <button onclick="editOptions('${element.id}')">Element Options</button>
        <button onclick="addElement('new-type', '${element.id}')">Add Child Element</button>
    `;
    parentElement.appendChild(newDiv);
}

function addElement(type, parentId = null) {
    const elementId = generateUniqueId();
    const newElement = {
        id: elementId,
        type: type,
        content: "",
        options: {},
        children: [],
    };

    if (parentId) {
        templateConfig[parentId].children.push(elementId);
    } else {
        templateConfig[elementId] = newElement;
    }

    renderElement(newElement, parentId);
}

function updateElementContent(elementId, content) {
    templateConfig[elementId].content = content;
}

function updateElementOptions(elementId, options) {
    templateConfig[elementId].options = options;
}

function generateUniqueId() {
    return "id-" + Math.random().toString(36).substr(2, 9);
}

// ***** Main Logic *****
window.addEventListener("load", () => {
    // get element
    let elements = document.getElementsByClassName("element-span");
    for (let i = 0; i < elements.length; i++) {
        elements[i].addEventListener("click", async () => {
            let elementText = elements[i].innerText;
            let res = await get_element(elementText);

            if (!res.errors) {
                let elementsDiv = document.getElementById("elementsDiv");
                let widgetTemplate = document.getElementById("elementDivTemplate");
                let elementWidget = widgetTemplate.firstElementChild.cloneNode(true);
                elementWidget.querySelector(".widget-header").innerText = elementText;
                elementsDiv.appendChild(elementWidget);
            }
        });
    }
});
