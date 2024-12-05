import { EditorView, keymap } from "@codemirror/view";
import { defaultKeymap } from "@codemirror/commands";
import { html } from "@codemirror";

document.addEventListener("DOMContentLoaded", function () {
    const textareas = document.querySelectorAll("textarea.codemirror");
    textareas.forEach(textarea => {
        let mode = textarea.dataset.dataMode;
        CodeMirror.fromTextArea(textarea, {
            doc: "",
            tabSize: 4,
            mode: mode,
            readonly: false,
        });
    });
});
