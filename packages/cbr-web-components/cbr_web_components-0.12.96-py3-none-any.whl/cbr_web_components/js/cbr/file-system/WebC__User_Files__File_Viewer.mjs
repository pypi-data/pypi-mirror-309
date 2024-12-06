import Web_Component  from '../../core/Web_Component.mjs'
import CSS__Cards     from '../../css/CSS__Cards.mjs'
import CSS__Forms     from '../../css/CSS__Forms.mjs'
import CSS__Icons     from '../../css/icons/CSS__Icons.mjs'
import API__Invoke    from '../../data/API__Invoke.mjs'
import Div            from '../../core/Div.mjs'
import Img            from '../../core/Img.mjs'
import Button         from '../../core/Button.mjs'
import Raw_Html       from "../../core/Raw_Html.mjs";
import CSS__Buttons   from "../../css/CSS__Buttons.mjs";

export default class WebC__User_Files__File_Viewer extends Web_Component {
    load_attributes() {
        new CSS__Buttons  (this).apply_framework()
        new CSS__Cards    (this).apply_framework()
        new CSS__Forms    (this).apply_framework()
        new CSS__Icons    (this).apply_framework()
        this.api_invoke   = new API__Invoke()
        this.current_file = null
        this.current_view = 'content'
    }

    connectedCallback() {
        super.connectedCallback()
        this.build()
        this.add_event_listeners()
    }

    add_event_listeners() {
        document.addEventListener('file-selected', async (e) => {
            this.current_file = e.detail
            await this.load_file_data()
            await this.render_file_viewer()
        })
    }

    add_event_handlers() {
        if (this.current_file) {
            // File action buttons
            const btn__delete         = this.query_selector('.delete-file')
            const btn__create_summary = this.query_selector('.create-summary')
            const btn__download       = this.query_selector('.download-file')
            const btn__rename         = this.query_selector('.rename-file')

            if (btn__create_summary) { btn__create_summary.addEventListener('click', () => this.on_current_file__create_summary(btn__create_summary)) }
            if (btn__delete)         { btn__delete.addEventListener('click', () => this.on_current_file__delete()) }
            if (btn__download)       { btn__download.addEventListener('click', () => this.on_current_file__create_download()) }
            if (btn__rename)         { btn__rename.addEventListener('click', () => this.on_current_file__rename()) }

            // View tabs
            const content_tab = this.query_selector('#content-tab')
            const chat_tab = this.query_selector('#chat-tab')

            if (content_tab) {
                content_tab.addEventListener('click', () => {
                    this.current_view = 'content'
                    this.render_file_viewer()
                })
            }

            if (chat_tab) {
                chat_tab.addEventListener('click', () => {
                    this.current_view = 'chat'
                    this.render_file_viewer()
                })
            }
        }
    }

    async load_file_data() {
        try {
            const response = await this.api_invoke.invoke_api(
                `/api/user-data/files/file-contents?file_id=${this.current_file.node_id}`
            )
            this.file_data          = response.data.file_data
            this.file_bytes__base64 = response.data.file_bytes__base64
            this.file_summary       = response.data.file_summary          // Store summary
        } catch (error) {
            console.error('Error loading file:', error)
            this.show_error_message('Failed to load file data')
        }
    }

    async on_current_file__create_summary(button) {
        if (!this.current_file?.node_id) {
            return
        }
        button.innerHTML = '...creating'                                // todo: find a better way to show progress
        const file_id      = this.current_file.node_id
        const path         = `/api/user-data/file-to-llms/file-summary?re_create=true&file_id=${file_id}`

        await this.api_invoke.invoke_api(path, 'POST')

        button.innerHTML = '...reloading data'
        await this.load_file_data()
        await this.render_file_viewer()
        button.innerHTML = '...all done'

    }
    async on_current_file__delete() {
        if (!this.current_file?.node_id) {
            return
        }

        if (confirm(`Are you sure you want to delete file "${this.file_data.file_name}"?`)) {
            try {
                const path = `/api/user-data/files/delete-file?file_id=${this.current_file.node_id}`
                await this.api_invoke.invoke_api(path, 'DELETE')
                this.raise_refresh_event()
                this.clear_viewer()
            } catch (error) {
                console.error('Error deleting file:', error)
                this.show_error_message('Failed to delete file')
            }
        }
    }

    async on_current_file__create_download(button) {
        if (!this.current_file?.node_id) {
            return
        }
        const file_id        = this.current_file.node_id
        const path           = `/api/user-data/files/file-download?file_id=${file_id}`
        window.location.href = path;
        // const file_contents = await this.api_invoke.invoke_api(path, 'POST')
        // console.log(file_contents)
    }

    async on_current_file__rename() {
        const new_file_name = prompt('Enter new name:', this.file_data.file_name)
        if (new_file_name && new_file_name !== this.file_data.file_name) {
            try {
                const path      = '/api/user-data/files/rename-file'
                const post_data = { file_id: this.current_file.node_id,  new_file_name: new_file_name}
                await this.api_invoke.invoke_api(path, 'PUT', post_data)

                this.raise_refresh_event()

                await this.load_file_data    ()
                await this.render_file_viewer()
            } catch (error) {
                console.error('Error renaming file:', error)
                this.show_error_message('Failed to rename file')
            }
        }
    }

    raise_refresh_event() {
        const event = new CustomEvent('files-refresh', {
            bubbles : true,
            composed: true
        })
        this.dispatchEvent(event)
    }

    format_date(date, time) {
        return `${date} ${time}`
    }

    format_size(size) {
        const units = ['B', 'KB', 'MB', 'GB']
        let size_num = size
        let unit_index = 0

        while (size_num >= 1024 && unit_index < units.length - 1) {
            size_num /= 1024
            unit_index++
        }

        return `${size_num.toFixed(1)} ${units[unit_index]}`
    }

    show_error_message(message) {
        const status = this.shadowRoot.querySelector('.viewer-status')
        if (status) {
            status.textContent = message
            status.className = 'viewer-status error'
            setTimeout(() => { status.textContent = '' }, 3000)
        }
    }

    clear_viewer() {
        this.current_file       = null
        this.file_data          = null
        this.file_bytes__base64 = null
        this.render_file_viewer()
    }


    async render_content_by_type() {
        if (!this.file_bytes__base64) return new Div()

        // Decode base64 content
        let decoded_content;
        try {
            decoded_content = atob(this.file_bytes__base64)
        } catch (error) {
            console.error('Error decoding base64:', error)
            return new Div({
                class: 'content-error',
                value: 'Error decoding file contents'
            })
        }

        switch(this.file_data.file_type.toLowerCase()) {            // todo: refactor each of these handlers into separate methods (if not classes)
            case '.md':
                const markdown_editor = new Div({ class: 'markdown-editor-container' })
                markdown_editor.add_tag({tag: 'webc-user-files-markdown-editor',
                                         attributes: { 'file_id': this.current_file.node_id } })
                return markdown_editor
            case '.txt':
            case '.json':
                try {                                                                           // For text files, convert decoded content to UTF-8
                    const decoded_text = new TextDecoder().decode(
                        new Uint8Array([...decoded_content].map(c => c.charCodeAt(0)))
                    )

                    if (this.file_data.file_type === '.json') {
                        try {
                            const formatted = JSON.stringify(JSON.parse(decoded_text), null, 2)
                            return new Raw_Html({   class: 'content-code',  value: `<pre>${formatted}</pre>` })
                        } catch {
                            return new Raw_Html({   class: 'content-text', value: decoded_text })
                        }
                    }

                    if (this.file_data.file_type === '.md') {
                        return new Raw_Html({ class: 'content-markdown', value: marked.marked(decoded_text) })
                    }

                    return new Raw_Html({ class: 'content-text',    value: decoded_text
                    })
                } catch (error) {
                    console.error('Error converting to text:', error)
                    return new Raw_Html({
                        class: 'content-error',
                        value: 'Error converting file contents'
                    })
                }
            case '.doc':
            case '.docx':
            case '.xls':
            case '.xlsx':
            case '.ppt':
            case '.pptx':
                return await this.render__using_google_viewer()

            case '.jpg':
            case '.jpeg':
            case '.png':
            case '.gif':
                const src = `data:image/${this.file_data.file_type.slice(1)};base64,${this.file_bytes__base64}`      // For images, we can use the base64 directly since it's already in the correct format
                return new Img({ class: 'content-image',  src: src })
            case '.pdf':
                return new Raw_Html({ class: 'content-pdf',
                                      value: `<embed src    = "data:application/pdf;base64,${this.file_bytes__base64}" 
                                                     type   = "application/pdf"
                                                     width  = "100%"
                                                     height = "600px"/>` })
            default:
                // For unknown types, try to display as text
                try {
                    const decoded_text = new TextDecoder().decode(
                        new Uint8Array([...decoded_content].map(c => c.charCodeAt(0)))
                    )
                    return new Raw_Html({ class: 'content-text',  value: decoded_text })
                } catch {
                    return new Div({
                        class: 'content-binary',
                        value: 'Binary file contents cannot be displayed'
                    })
                }
        }
    }

    async render__using_google_viewer() {                           // todo: a) see if this is the best way to handle these docs, and b) debug the multiple file formats supported
        try {
            const response      = await this.api_invoke.invoke_api(`/api/user-data/files/file-temp-signed-url?file_id=${this.current_file.node_id}`, 'GET')
            const presigned_url = response.data
            return new Raw_Html({
                class: 'content-document-viewer',
                value: `<iframe
                            src="https://docs.google.com/viewer?embedded=true&url=${encodeURIComponent(presigned_url)}"
                            width="100%"
                            height="600px"
                            frameborder="0">
                        </iframe>`
            })
        } catch (error) {
            console.error('Error getting presigned URL:', error)
            return new Raw_Html({
                class: 'content-error',
                value: 'Error loading document preview'
            })
        }
    }

    render_summary_section() {
        if (!this.file_summary) {
            return new Div()
        }


        let processed_summary
        try {
            processed_summary = JSON.parse(this.file_summary)
        } catch (error) {
            console.error('Error processing summary:', error)
            processed_summary = this.file_summary                        // Fallback to original if parsing fails
        }


        const summary_container = new Div({ class: 'summary-container'                                })
        const summary_header    = new Div({ class: 'summary-header'                                   })
        const summary_title     = new Div({ class: 'summary-title'    ,  value: 'File Summary'        })
        const summary_content   = new Raw_Html({
            class: 'summary-content',
            value: marked.marked(processed_summary)
        })

        summary_header.add_element(summary_title)
        summary_container.add_elements(summary_header, summary_content)

        return summary_container
    }

    render_view_tabs() {
        const tabs = new Div({ class: 'view-tabs' })
        const content_tab = new Button({
            class : `btn ${this.current_view === 'content' ? 'btn-primary' : 'btn-outline-primary'}`,
            value : 'Content View',
            id    : 'content-tab'
        })
        const chat_tab = new Button({
            class : `btn ${this.current_view === 'chat' ? 'btn-primary' : 'btn-outline-primary'}`,
            value : 'Chat View',
            id    : 'chat-tab'
        })
        tabs.add_elements(content_tab, chat_tab)
        return tabs
    }

    async render_file_viewer() {
        const container = new Div({ class: 'viewer-container' })

        if (!this.current_file || !this.file_data) {
            container.add_element(
                new Div({
                    class: 'viewer-empty',
                    value: 'Select a file to view its contents'
                })
            )
        } else {
            // Header section with file info and actions
            const header = new Div({ class: 'file-header' })
            const info = new Div({ class: 'file-info' })

            info.add_elements(
                new Div({ class: 'file-name', value: this.file_data.file_name }),
                new Div({ class: 'file-meta', value: `Last updated: ${this.format_date(this.file_data.updated__date, this.file_data.updated__time)}` }),
                new Div({ class: 'file-meta', value: `Size: ${this.format_size(this.file_data.file_size)}` }),
                new Div({ class: 'file-meta', value: `File id: ${this.current_file.node_id}` })
            )

            const actions = this.render_file_actions()
            header.add_elements(info, actions)

            // Add view tabs
            const tabs = this.render_view_tabs()

            // Content View
            const content_view = new Div({
                class : 'content-view',
                style : this.current_view === 'content' ? '' : 'display: none;'
            })

            const summary_section = this.render_summary_section()
            const content = new Div({ class: 'content-container' })
            content.add_element(await this.render_content_by_type())
            content_view.add_elements(summary_section, content)

            // Chat View
            const chat_view = new Div({
                class : 'chat-view',
                style : this.current_view === 'chat' ? '' : 'display: none;'
            })
            chat_view.add_tag({
                tag: 'webc-user-files-content-chat',
                attributes: { 'file_id': this.current_file.node_id }
            })

            const status = new Div({ class: 'viewer-status' })

            container.add_elements(header, tabs, content_view, chat_view, status)
        }

        this.set_inner_html(container.html())
        this.add_css_rules(this.css_rules())
        this.add_event_handlers()
    }

    render_file_actions() {
        const actions = new Div({ class: 'file-actions' })

        // const create_summary_btn = new Button({ class: 'btn btn-primary create-summary', value: 'Create Summary' })
        // const delete_btn         = new Button({ class: 'btn btn-danger  delete-file'   , value: 'Delete File'    })
        // const download_btn       = new Button({ class: 'btn btn-success download-file' , value: 'Download'       })

        const rename_btn   = new Button({ class: 'btn btn-outline-primary rename-file'    , value: 'Rename'         })
        const summary_btn  = new Button({ class: 'btn btn-primary         create-summary' , value: 'Create Summary' })
        const download_btn = new Button({ class: 'btn btn-success         download-file'  , value: 'Download'       })
        const delete_btn   = new Button({ class: 'btn btn-danger          delete-file'    , value: 'Delete File'    })

        actions.add_elements(rename_btn, summary_btn, download_btn, delete_btn)
        return actions
    }

    build() {
        this.render_file_viewer()
    }


    css_rules() {
        return {
            ".viewer-container"    : { padding          : "1.5rem"                    ,
                                     backgroundColor   : "#fff"                      ,
                                     borderRadius      : "0.5rem"                    ,
                                     boxShadow         : "0 2px 4px rgba(0,0,0,0.1)" ,
                                     minHeight         : "300px"                     },

            ".viewer-empty"        : { display          : "flex"                      ,
                                     alignItems        : "center"                    ,
                                     justifyContent    : "center"                    ,
                                     height            : "300px"                     ,
                                     color             : "#6c757d"                   },

            ".file-header"         : { display          : "flex"                      ,
                                     alignItems        : "center"                    ,
                                     justifyContent    : "space-between"             ,
                                     marginBottom      : "1rem"                      ,
                                     padding          : "0.5rem 0"                  ,
                                     borderBottom     : "1px solid #dee2e6"         },

            ".file-info"           : { display          : "flex"                      ,
                                     flexDirection     : "column"                    ,
                                     gap              : "0.25rem"                    },

            ".file-name"           : { fontSize         : "1.25rem"                   ,
                                     fontWeight        : "600"                       ,
                                     color             : "#212529"                   },

            ".file-meta"           : { fontSize         : "0.875rem"                  ,
                                     color             : "#6c757d"                   },

            ".content-container"   : { marginTop        : "1rem"                      ,
                                     padding          : "1rem"                       ,
                                     backgroundColor   : "#f8f9fa"                   ,
                                     borderRadius      : "0.375rem"                  ,
                                     minHeight         : "200px"                     },

            // ".content-markdown"    : { fontFamily       : "system-ui, sans-serif"     ,
            //                          lineHeight        : "1.5"                       },

            ".content-code"        : { fontFamily       : "monospace"                 ,
                                     whiteSpace       : "pre-wrap"                  ,
                                     fontSize         : "0.875rem"                  },

            ".content-text"        : { whiteSpace       : "pre-wrap"                  ,
                                     fontFamily       : "system-ui, sans-serif"     },

            ".content-image"       : { maxWidth         : "1024px"                   },
            ".content-image img"   : { maxWidth         : "100%"                      ,
                                       height            : "auto"                      },

            ".viewer-status"       : { marginTop        : "1rem"                      ,
                                     padding          : "0.5rem"                     ,
                                     borderRadius     : "0.25rem"                    ,
                                     textAlign        : "center"                     },

            ".error"              : { backgroundColor   : "#f8d7da"                    ,
                                      color             : "#842029"                    },
            ".content-pdf"        : { width            : "100%"                        ,
                                      height           : "600px"                       ,
                                      border           : "1px solid #dee2e6"           ,
                                      borderRadius     : "0.375rem"                    ,
                                      overflow         : "hidden"                      },

            ".content-pdf embed"  : { border           : "none"                        },

            ".content-markdown"    : { fontFamily       : "system-ui, sans-serif"     ,
                                       lineHeight        : "1.6"                        ,
                                       padding          : "1rem"                       },

            ".content-markdown h1" : { fontSize         : "2rem"                      ,
                                     marginBottom     : "1rem"                       ,
                                     borderBottom     : "1px solid #dee2e6"         ,
                                     paddingBottom    : "0.5rem"                    },

            ".content-markdown h2" : { fontSize         : "1.5rem"                    ,
                                     marginBottom     : "1rem"                       ,
                                     borderBottom     : "1px solid #dee2e6"         ,
                                     paddingBottom    : "0.5rem"                    },

            ".content-markdown h3" : { fontSize         : "1.25rem"                   ,
                                     marginBottom     : "0.75rem"                   },

            ".content-markdown p"  : { marginBottom     : "1rem"                      },

            ".content-markdown code": { fontFamily      : "monospace"                 ,
                                     backgroundColor  : "#f8f9fa"                   ,
                                     padding          : "0.2em 0.4em"               ,
                                     borderRadius     : "0.25rem"                   },

            ".content-markdown pre": { backgroundColor  : "#f8f9fa"                   ,
                                     padding          : "1rem"                       ,
                                     borderRadius     : "0.375rem"                  ,
                                     marginBottom     : "1rem"                       ,
                                     overflow         : "auto"                       },

            ".content-markdown pre code": {
                                     padding          : "0"                          ,
                                     backgroundColor  : "transparent"               },

            ".content-markdown ul" : { marginBottom     : "1rem"                      ,
                                     paddingLeft      : "1.5rem"                    },

            ".content-markdown li" : { marginBottom     : "0.5rem"                    },

            ".content-markdown blockquote"    : { borderLeft       : "4px solid #dee2e6"         ,
                                                  paddingLeft      : "1rem"                      ,
                                                  marginLeft       : "0"                         ,
                                                  marginBottom     : "1rem"                      ,
                                                  color            : "#6c757d"                   },

            ".content-document-viewer"        : { width            : "100%"                       ,
                                                  height           : "600px"                       ,
                                                  border           : "1px solid #dee2e6"          ,
                                                  borderRadius     : "0.375rem"                    ,
                                                  overflow         : "hidden"                      },

            ".content-document-viewer iframe" : { border           : "none"                 ,
                                                  width            : "100%"                 ,
                                                  height           : "100%"                 },
            // Add to css_rules()
            ".summary-container"   : { marginTop        : "1rem"                      ,            // Space above summary
                                      padding          : "1rem"                      ,            // Inner spacing
                                      backgroundColor  : "#fff"                      ,            // White background
                                      borderRadius     : "0.375rem"                  ,            // Rounded corners
                                      border          : "1px solid #e9ecef"         ,            // Subtle border
                                      marginBottom     : "1rem"                      },           // Space below

            ".summary-header"      : { display          : "flex"                      ,            // Flex container
                                      alignItems       : "center"                    ,            // Center items vertically
                                      marginBottom     : "0.75rem"                   ,            // Space below header
                                      paddingBottom    : "0.5rem"                    ,            // Padding below
                                      borderBottom     : "1px solid #e9ecef"         },           // Bottom border

            ".summary-title"       : { fontSize         : "1rem"                      ,            // Title size
                                      fontWeight       : "600"                       ,            // Bold weight
                                      color           : "#495057"                    },           // Dark gray color

            ".summary-content"     : { fontSize         : "0.875rem"                  ,            // Smaller text
                                      lineHeight       : "1.6"                       ,            // Line spacing
                                      color           : "#495057"                    },           // Text color

            ".file-actions"        : { display          : "flex"                      ,
                                       gap              : "0.5rem"                    ,
                                       marginLeft       : "auto"                      },

            ".error-message"       : { color            : "#dc3545"                   ,
                                       fontSize         : "0.875rem"                  ,
                                       marginTop        : "0.5rem"                    },
                        ".view-tabs"             : { display          : "flex"                      ,
                                       gap              : "0.5rem"                     ,
                                       marginBottom      : "1rem"                      ,
                                       padding          : "0.5rem 0"                   ,
                                       borderBottom      : "1px solid #dee2e6"         },

            ".content-view"          : { flex             : "1"                         ,
                                       display           : "flex"                      ,
                                       flexDirection     : "column"                    ,
                                       gap              : "1rem"                      },

            ".chat-view"             : { flex             : "1"                         ,
                                       display           : "flex"                      ,
                                       flexDirection     : "column"                    ,
                                       minHeight         : "400px"                     },

            }
    }
}

WebC__User_Files__File_Viewer.define()