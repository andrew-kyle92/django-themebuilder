import {EditorView, basicSetup} from "codemirror"
import {javascript} from "@codemirror/lang-javascript"
import {css} from "codemirror/"

let editor = new EditorView({
    "extensions": [basicSetup, javascript()],
    parent: document.body,
})