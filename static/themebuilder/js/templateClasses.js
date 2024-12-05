// ********** templateClasses holds all the logic for all classes used within template_builder.js **********
export class Element {
    constructor(id, type, parent=null) {
        this.id = id || Element.generateUniqueId();
        this.type = type;
        this.content = "";
        this.options = {};
        this.children = [];
        this.parent = parent;   // Reference to parent element
    }

    static generateUniqueId() {
        return "id-" + Math.random().toString(36).substring(2, 9);
    }

    addChild(type) {
        const child = new Element(null, type, this.id);
        this.children.push(child);
        return child;
    }

    updateContent(newContent) {
        this.content = newContent;
    }

    updateOptions(newOptions) {
        this.options = newOptions;
    }
}

export class Template {
    constructor() {
        this.elements = {}; // Store all elements by their ID
    }

    addElement(type, parentId=null) {
        const newElement = new Element(null, type, parentId);
        this.elements[newElement.id] = newElement;

        if (parentId) {
            this.elements[parentId].children.push(newElement.id);
        }

        return newElement;
    }

    getElementById(id) {
       return this.elements[id];
    }

    updateElementContent(id, content) {
        const element = this.getElementById(id);
        if (element) {
            element.updateContent(content);
        }
    }

    updateElementOptions(id, options) {
        const element = this.getElementById(id);
        if (element) {
            element.updateOptions(options);
        }
    }
}