<template>
    <div class="code-block">
        <div class="code-header">
            <span>Python Code</span>
            <div class="button-group">
                <div class="copy-container">
                    <button @click="copyToClipboard" class="action-button" title="Copy to clipboard">
                        <i v-if="!copied" class="bi bi-clipboard"></i>
                        <i v-else class="bi bi-clipboard-check"></i>
                    </button>
                </div>
                <button @click="downloadCode" class="action-button" title="Download as .py file">
                    <i class="bi bi-download"></i>
                </button>
            </div>
        </div>
        <pre><code v-html="highlightedCode"></code></pre>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import hljs from 'highlight.js'
import 'highlight.js/styles/vs2015.css'

const props = defineProps({
    code: {
        type: String,
        required: true
    },
    game_name: {
        type: String,
        required: true
    }
})

const copied = ref(false)

const highlightedCode = computed(() => {
    if (!props.code) return ''
    return hljs.highlight(props.code, { language: 'python' }).value
})

const copyToClipboard = async () => {
    try {
        await navigator.clipboard.writeText(props.code)
        copied.value = true
        setTimeout(() => {
            copied.value = false
        }, 3000)
    } catch (err) {
        console.error('Failed to copy text: ', err)
    }
}

const downloadCode = () => {
    const blob = new Blob([props.code], { type: 'text/plain' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = props.game_name + '_template.py'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
}
</script>

<style>
/* Override highlight.js styles for better contrast */
.hljs {
    background: #1E1E1E !important;
    color: #D4D4D4 !important;
    padding: 1em !important;
    border-radius: 0 0 8px 8px !important;
}
</style>

<style scoped>
.code-block {
    margin-top: 2rem;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    background-color: #1E1E1E;
}

.code-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    background-color: #2D2D2D;
    color: #D4D4D4;
    border-bottom: 1px solid #3D3D3D;
}

.button-group {
    display: flex;
    gap: 0.5rem;
}

.copy-container {
    position: relative;
}

.action-button {
    padding: 0.25rem 0.5rem;
    background-color: #3D3D3D;
    border: 1px solid #4D4D4D;
    border-radius: 3px;
    font-size: 0.875rem;
    cursor: pointer;
    transition: background-color 0.2s;
    color: #D4D4D4;
    display: flex;
    align-items: center;
    justify-content: center;
}

.action-button:hover {
    background-color: #4D4D4D;
}

.action-button i {
    font-size: 1rem;
}

pre {
    margin: 0;
    overflow-x: auto;
}

code {
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
    font-size: 0.875rem;
    line-height: 1.5;
}
</style>
