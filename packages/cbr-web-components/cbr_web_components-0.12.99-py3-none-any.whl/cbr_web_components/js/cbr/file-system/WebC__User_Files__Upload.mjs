import Web_Component  from '../../core/Web_Component.mjs'
import CSS__Forms     from '../../css/CSS__Forms.mjs'
import CSS__Cards     from '../../css/CSS__Cards.mjs'
import CSS__Icons     from '../../css/icons/CSS__Icons.mjs'
import API__Invoke    from '../../data/API__Invoke.mjs'
import Icon           from '../../css/icons/Icon.mjs'
import Div            from '../../core/Div.mjs'
import Button         from '../../core/Button.mjs'
import Input          from '../../core/Input.mjs'
import CSS__Buttons  from "../../css/CSS__Buttons.mjs";

export default class WebC__User_Files__Upload extends Web_Component {
    load_attributes() {
        new CSS__Buttons   (this).apply_framework()
        new CSS__Forms     (this).apply_framework()
        new CSS__Cards     (this).apply_framework()
        new CSS__Icons     (this).apply_framework()
        this.api_invoke     = new API__Invoke()
        this.current_folder = {
            node_id: null,
            name: 'root'
        }
    }

    connectedCallback() {
        super.connectedCallback()
        this.build()
        this.add_event_listeners()
    }

    add_event_listeners() {
        // Listen for folder selection
        document.addEventListener('folder-selected', (e) => {
            this.current_folder = e.detail
            this.update_folder_display()
        })

        // Set up drag and drop handlers
        const drop_zone = this.shadowRoot.querySelector('.drop-zone')
        if (!drop_zone) {
            console.log("BUG!!! Drop zone not found")
            return
        }
        drop_zone.addEventListener('dragover',  this.handle_dragover)
        drop_zone.addEventListener('drop',      this.handle_drop)
        drop_zone.addEventListener('dragenter', () => drop_zone.classList.add('drag-active'))
        drop_zone.addEventListener('dragover' , () => drop_zone.classList.add('drag-active'))
        drop_zone.addEventListener('dragleave', () => drop_zone.classList.remove('drag-active'))

        // Set up file input handler
        const file_input = this.shadowRoot.querySelector('#file-input')
        file_input.addEventListener('change', this.handle_file_select)

        // Set up paste handler for the whole component
        this.addEventListener('paste', this.handle_paste)
    }

    handle_dragover = (e) => {
        e.preventDefault()
        e.stopPropagation()
    }

    handle_drop = async (e) => {
        e.preventDefault()
        e.stopPropagation()

        const files = [...e.dataTransfer.files]
        for (const file of files) {
            await this.upload_file(file)
        }
    }

    handle_file_select = async (e) => {
        const files = [...e.target.files]
        for (const file of files) {
            await this.upload_file(file)
        }
    }

    handle_paste = async (e) => {
        const items = [...e.clipboardData.items]
        for (const item of items) {
            if (item.kind === 'file') {
                const file = item.getAsFile()
                await this.upload_file(file)
            }
        }
    }

    async upload_file(file) {
        try {
            const reader = new FileReader()
            reader.readAsDataURL(file)

            reader.onload = async () => {
                const base64_content = reader.result.split(',')[1]
                const post_data = { file_name          : file.name                        ,
                                    file_bytes__base64 : base64_content                   ,
                                    folder_id          : this.current_folder.node_id || ''}
                await this.api_invoke.invoke_api('/api/user-data/files/add-file', 'POST', post_data)

                this.raise_refresh_event()
                this.show_success_message(`File ${file.name} uploaded successfully`)
            }
        } catch (error) {
            console.error('Error uploading file:', error)
            this.show_error_message(`Failed to upload ${file.name}`)
        }
    }

    raise_refresh_event() {
        const event = new CustomEvent('files-refresh', {
            bubbles : true,
            composed: true
        })
        this.dispatchEvent(event)
    }

    update_folder_display() {
        const folder_name = this.shadowRoot.querySelector('.current-folder')
        if (folder_name) {
            folder_name.textContent = `Current folder: ${this.current_folder.name}`
        }
    }

    show_success_message(message) {
        const status = this.shadowRoot.querySelector('.upload-status')
        status.textContent = message
        status.className = 'upload-status success'
        setTimeout(() => { status.textContent = '' }, 3000)
    }

    show_error_message(message) {
        const status = this.shadowRoot.querySelector('.upload-status')
        status.textContent = message
        status.className = 'upload-status error'
        setTimeout(() => { status.textContent = '' }, 3000)
    }

    css_rules() {
        return {
            ".upload-container"    : { padding          : "1.5rem"                     ,
                                     backgroundColor   : "#fff"                        ,
                                     borderRadius      : "0.5rem"                      ,
                                     boxShadow         : "2px 2px 4px rgba(0,0,0,0.2)" },

            ".current-folder"      : { fontSize         : "0.875rem"                  ,
                                     color            : "#6c757d"                    ,
                                     marginBottom     : "1rem"                       },

            ".drop-zone"          : { border           : "2px dashed #dee2e6"        ,
                                     borderRadius      : "0.375rem"                   ,
                                     padding          : "2rem"                       ,
                                     textAlign        : "center"                     ,
                                     cursor           : "pointer"                    ,
                                     transition       : "all 0.2s ease-in-out"       },

            ".drag-active"        : { borderColor      : "#0d6efd"                   ,
                                     backgroundColor   : "rgba(13,110,253,0.05)"     },

            ".upload-icon"        : { fontSize         : "2rem"                      ,
                                     color            : "#6c757d"                    ,
                                     marginBottom     : "1rem"                       },

            ".upload-text"        : { color            : "#6c757d"                   ,
                                     marginBottom     : "1rem"                       },

            ".upload-methods"     : { display          : "flex"                      ,
                                     flexDirection    : "column"                     ,
                                     gap              : "0.5rem"                     ,
                                     alignItems       : "center"                     },

            ".upload-status"      : { marginTop        : "1rem"                      ,
                                     padding          : "0.5rem"                     ,
                                     borderRadius     : "0.25rem"                    ,
                                     textAlign        : "center"                     },

            ".success"            : { backgroundColor   : "#d1e7dd"                   ,
                                     color            : "#0f5132"                    },

            ".error"              : { backgroundColor   : "#f8d7da"                   ,
                                     color            : "#842029"                    },

            "#file-input"         : { display          : "none"                      }
        }
    }

    build() {
        const container = new Div({ class: 'upload-container' })
        const folder    = new Div({ class: 'current-folder', value: `Current folder: ${this.current_folder.name}` })
        const drop_zone = new Div({ class: 'drop-zone' })

        const upload_icon = new Icon({ icon: 'upload', class: 'upload-icon' })
        const text       = new Div({ class: 'upload-text', value: 'Drag and drop files here or:' })
        const methods    = new Div({ class: 'upload-methods' })

        // File input for selection dialog
        const file_input = new Input({
            id         : 'file-input',
            attributes : { type: 'file', multiple: true }
        })

        const select_button = new Button({
            class : 'btn btn-primary',
            value : 'Select Files',
            id    : 'select-files-btn'            // Added ID for querySelector
        })

        // Status display
        const status = new Div({ class: 'upload-status' })

        methods.add_elements(file_input, select_button)
        drop_zone.add_elements(upload_icon, text, methods)
        container.add_elements(folder, drop_zone, status)

        this.set_inner_html(container.html())
        this.add_css_rules(this.css_rules())

        // Add click handler after elements are in DOM
        const btn = this.shadowRoot.querySelector('#select-files-btn')
        const input = this.shadowRoot.querySelector('#file-input')
        if (btn && input) {
            btn.addEventListener('click', () => input.click())
        }
    }
}

WebC__User_Files__Upload.define()