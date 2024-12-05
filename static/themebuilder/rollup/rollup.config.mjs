import {nodeResolve} from '@rollup/plugin-node-resolve'
import del from "rollup-plugin-delete"
export default {
    input: './src/js/editor.js',
    output: {
        file: '../js/editor.bundle.js',
        format: 'iife',
        name: 'editor',
    },
    plugins: [
        nodeResolve(),
        del({
            targets: ["../js/editor.bundle.js"],
            hook: "buildStart",
            force: true,
        })
    ],
    watch: true,
}