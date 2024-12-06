import Web_Component from '../../core/Web_Component.mjs'
import CSS__Forms     from '../../css/CSS__Forms.mjs'
import CSS__Buttons   from '../../css/CSS__Buttons.mjs'
import API__Invoke    from '../../data/API__Invoke.mjs'
import Div            from '../../core/Div.mjs'
import Button         from '../../core/Button.mjs'
import Raw_Html       from '../../core/Raw_Html.mjs'
import Textarea       from '../../core/Textarea.mjs'

export default class WebC__User_Files__Markdown__Editor extends Web_Component {
    load_attributes() {
        new CSS__Forms  (this).apply_framework()
        new CSS__Buttons(this).apply_framework()
        this.api_invoke = new API__Invoke()
        this.file_id    = this.getAttribute('file_id')
        this.edit_mode  = false
    }

    async connectedCallback() {
        super.connectedCallback()
        await this.build()
    }

    async build() {
        await this.load_file_data()
        this.render()
    }

    async load_file_data() {
        try {
            const response = await this.api_invoke.invoke_api( `/api/user-data/files/file-contents?file_id=${this.file_id}`)

            const base64Content = response.data.file_bytes__base64                                                      // Properly decode base64 content with UTF-8 support (this is needed to support emojis)
            const binaryContent = atob(base64Content)
            const bytes = Uint8Array.from(binaryContent, char => char.charCodeAt(0))
            this.markdown_content = new TextDecoder('utf-8').decode(bytes)

        } catch (error) {
            console.error('Error loading file:', error)
            this.show_error(error.message)
        }
    }

    async save_content() {
        try {
            const editor = this.query_selector('.markdown-editor')
            const content = editor.value


            const encoder = new TextEncoder()                                                                           // Convert string to UTF-8 bytes, then to base64 (this is needed to support emojis)
            const utf8Bytes = encoder.encode(content)
            const base64Content = btoa(Array.from(utf8Bytes).map(byte => String.fromCharCode(byte)).join(''))
            await this.api_invoke.invoke_api('/api/user-data/files/update-file',  'PUT',  { file_id : this.file_id,  file_bytes__base64: base64Content })
            this.markdown_content = content
            this.edit_mode = false
            this.render()
            this.raise_refresh_event()
        } catch (error) {
            console.error('Error saving file:', error)
            this.show_error(error.message)
        }
    }

    raise_refresh_event() {
        const event = new CustomEvent('files-refresh', {
            bubbles : true,
            composed: true
        })
        this.dispatchEvent(event)
    }

    show_error(message) {
        const error_div = this.query_selector('.error-message')
        if (error_div) {
            error_div.textContent = message
            //setTimeout(() => { error_div.textContent = '' }, 3000)
        }
    }

    toggle_edit_mode() {
        this.edit_mode = !this.edit_mode
        this.render()
    }

    render_preview() {
        const preview = new Raw_Html({
            class: 'markdown-preview',
            value: marked.marked(this.markdown_content || '')
        })
        return preview
    }

    render_editor() {
        const editor = new Textarea({
            class      : 'markdown-editor',
            value      : this.markdown_content,
            attributes : {
                spellcheck: false,
                'data-gramm': false
            }
        })
        return editor
    }

    render_toolbar() {
        const toolbar = new Div({ class: 'editor-toolbar' })

        if (this.edit_mode) {
            const save_btn   = new Button({ class: 'btn btn-success save-btn'    , value: 'Save Changes' })
            const cancel_btn = new Button({ class: 'btn btn-secondary cancel-btn', value: 'Cancel'       })
            const spacer     = new Div   ({ class: 'toolbar-spacer'                                      })
            toolbar.add_elements(save_btn, spacer, cancel_btn)
        } else {
            const edit_btn   = new Button({class: 'btn btn-primary edit-btn'     , value: 'Edit Markdown'})
            toolbar.add_element(edit_btn)
        }

        return toolbar
    }

    render() {
        const container = new Div({ class: 'markdown-container' })
        const toolbar = this.render_toolbar()
        const error_msg = new Div({ class: 'error-message' })

        container.add_element(toolbar)
        container.add_element(error_msg)

        if (this.edit_mode) {
            const editor_container = new Div({ class: 'split-view' })
            editor_container.add_elements(
                this.render_editor(),
                this.render_preview()
            )
            container.add_element(editor_container)
        } else {
            container.add_element(this.render_preview())
        }

        this.set_inner_html(container.html())
        this.add_css_rules(this.css_rules())
        this.add_event_handlers()
    }

    add_event_handlers() {
        if (this.edit_mode) {
            // Live preview on typing
            this.query_selector('.markdown-editor').addEventListener('input', (e) => {
                const preview = this.query_selector('.markdown-preview')
                preview.innerHTML = marked.marked(e.target.value)
            })

            // Save button
            this.query_selector('.save-btn').addEventListener('click', () => this.save_content())

            // Cancel button
            this.query_selector('.cancel-btn').addEventListener('click', () => this.toggle_edit_mode())
        } else {
            // Edit button
            this.query_selector('.edit-btn').addEventListener('click', () => this.toggle_edit_mode())
        }
    }

    css_rules() {
        return {
            ".markdown-container"  : { padding          : "1rem"                      ,
                                     backgroundColor   : "#fff"                      ,
                                     borderRadius      : "0.375rem"                  ,
                                     boxShadow         : "0 2px 4px rgba(0,0,0,0.1)" },

            ".editor-toolbar"      : { marginBottom     : "1rem"                      ,
                                     display           : "flex"                      ,
                                     gap              : "0.5rem"                     ,
                                     borderBottom      : "1px solid #dee2e6"         ,
                                     paddingBottom     : "1rem"                      },

            ".split-view"          : { display          : "grid"                      ,
                                     gridTemplateColumns: "1fr 1fr"                   ,
                                     gap              : "1rem"                       ,
                                     height            : "calc(100vh - 200px)"       ,
                                     minHeight         : "400px"                     },

            ".markdown-editor"     : { width            : "100%"                      ,
                                       //height            : "100%"                      ,
                                       padding          : "1rem"                       ,
                                       fontSize          : "0.875rem"                  ,
                                       fontFamily        : "monospace"                 ,
                                       lineHeight        : "1.5"                       ,
                                       border           : "1px solid #dee2e6"          ,
                                       borderRadius      : "0.375rem"                  ,
                                       resize           : "none"                       },

            ".markdown-preview"    : { //height           : "100%"                      ,
                                       padding          : "1rem"                       ,
                                       overflow          : "auto"                      ,
                                       fontSize          : "0.875rem"                  ,
                                       lineHeight        : "1.6"                       ,
                                       backgroundColor   : "#f8f9fa"                   ,
                                       borderRadius      : "0.375rem"                  },

            ".error-message"       : { color            : "#dc3545"                   ,
                                     marginBottom      : "1rem"                      ,
                                     fontSize          : "0.875rem"                  },

            // Markdown preview styling
            ".markdown-preview h1" : { fontSize         : "1.75rem"                   ,
                                     marginBottom      : "1rem"                      ,
                                     borderBottom      : "1px solid #dee2e6"         ,
                                     paddingBottom     : "0.5rem"                    },

            ".markdown-preview h2" : { fontSize         : "1.5rem"                    ,
                                     marginBottom      : "1rem"                      ,
                                     borderBottom      : "1px solid #dee2e6"         ,
                                     paddingBottom     : "0.5rem"                    },

            ".markdown-preview h3" : { fontSize         : "1.25rem"                   ,
                                     marginBottom      : "0.75rem"                   },

            ".markdown-preview p"  : { marginBottom     : "1rem"                      },

            ".markdown-preview code": { fontFamily      : "monospace"                 ,
                                      backgroundColor  : "#f1f3f5"                   ,
                                      padding          : "0.2em 0.4em"               ,
                                      borderRadius     : "0.25rem"                   },

            ".markdown-preview pre": { backgroundColor  : "#f8f9fa"                   ,
                                     padding          : "1rem"                       ,
                                     borderRadius     : "0.375rem"                   ,
                                     marginBottom     : "1rem"                       ,
                                     overflow         : "auto"                       },
            ".toolbar-spacer"       : { flex             : "1"                       },
        }
    }
}

WebC__User_Files__Markdown__Editor.define()