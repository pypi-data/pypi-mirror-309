import Web_Component from '../../core/Web_Component.mjs'
import CSS__Forms     from '../../css/CSS__Forms.mjs'
import CSS__Buttons   from '../../css/CSS__Buttons.mjs'
import CSS__Icons     from '../../css/icons/CSS__Icons.mjs'
import API__Invoke    from '../../data/API__Invoke.mjs'
import Div            from '../../core/Div.mjs'
import Button         from '../../core/Button.mjs'
import Raw_Html       from '../../core/Raw_Html.mjs'
import Textarea       from '../../core/Textarea.mjs'
import Icon          from '../../css/icons/Icon.mjs'

export default class WebC__User_Files__Markdown__Editor extends Web_Component {
    load_attributes() {
        new CSS__Forms   (this).apply_framework()
        new CSS__Buttons (this).apply_framework()
        new CSS__Icons   (this).apply_framework()
        
        this.api_invoke  = new API__Invoke()
        this.file_id     = this.getAttribute('file_id') || '970804a2-88d8-41d6-881e-e1c5910b80f8'
        this.edit_mode   = false
        this.view_mode   = 'content'  // 'content' or 'versions'
    }

    async connectedCallback() {
        this.load_attributes()
        await this.build()
    }

    async build() {
        await this.load_file_data()
        await this.load_versions()
        this.render()
        this.update_ui()
    }

    async load_file_data() {
        try {
            const response = await this.api_invoke.invoke_api(
                `/api/user-data/files/file-contents?file_id=${this.file_id}`
            )
            const base64Content = response.data.file_bytes__base64
            const binaryContent = atob(base64Content)
            const bytes = Uint8Array.from(binaryContent, char => char.charCodeAt(0))
            this.markdown_content = new TextDecoder('utf-8').decode(bytes)
            this.file_data = response.data.file_data
        } catch (error) {
            console.error('Error loading file:', error)
            this.show_error(error.message)
        }
    }

    async load_versions() {
        try {
            const response = await this.api_invoke.invoke_api(`/api/user-data/files/file-versions?file_id=${this.file_id}`)
            this.versions = response.data || []
        } catch (error) {
            console.error('Error loading versions:', error)
            this.versions = []
        }
    }

    async save_content() {
        try {
            const editor = this.query_selector('.markdown-editor')
            const content = editor.value

            const encoder = new TextEncoder()
            const utf8Bytes = encoder.encode(content)
            const base64Content = btoa(Array.from(utf8Bytes)
                .map(byte => String.fromCharCode(byte))
                .join(''))

            await this.api_invoke.invoke_api(
                '/api/user-data/files/update-file',
                'PUT',
                {
                    file_id: this.file_id,
                    file_bytes__base64: base64Content
                }
            )
            this.markdown_content = content
            this.edit_mode = false
            await this.load_versions()  // Reload versions after save
            this.render()
            this.raise_refresh_event()
            this.show_success('Changes saved successfully')
        } catch (error) {
            console.error('Error saving file:', error)
            this.show_error(error.message)
        }
    }

    async view_version(version_id) {
        try {
            const response = await this.api_invoke.invoke_api(
                `/api/user-data/files/file-bytes?file_id=${this.file_id}&version_id=${version_id}`
            )

            if (response.data?.file_bytes__base64) {
                const base64Content = response.data.file_bytes__base64
                const binaryContent = atob(base64Content)
                const bytes = Uint8Array.from(binaryContent, char => char.charCodeAt(0))

                this.temp_content    = this.markdown_content             // Store current content
                this.markdown_content = new TextDecoder('utf-8').decode(bytes)
                this.viewing_version = version_id
                this.edit_mode      = true
                this.view_mode      = 'content'                         // Switch to content view
                this.render()
            } else {
                this.show_error('Invalid version data received')
            }
        } catch (error) {
            console.error('Error viewing version:', error)
            this.show_error('Failed to load version')
        }
    }

    async restore_version(version_id) {
        try {
            const response = await this.api_invoke.invoke_api(
                `/api/user-data/files/file-bytes?file_id=${this.file_id}&version_id=${version_id}`
            )

            if (response.data?.file_bytes__base64) {
                const base64Content = response.data.file_bytes__base64
                const binaryContent = atob(base64Content)
                const bytes = Uint8Array.from(binaryContent, char => char.charCodeAt(0))

                this.markdown_content = new TextDecoder('utf-8').decode(bytes)
                await this.save_content()
                this.viewing_version = null
                this.view_mode      = 'content'                         // Switch to content view
                this.render()
                this.show_success('Version restored successfully')
            } else {
                this.show_error('Invalid version data received')
            }
        } catch (error) {
            console.error('Error restoring version:', error)
            this.show_error('Failed to restore version')
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
        const error = this.query_selector('.error-message')
        if (error) {
            error.textContent = message
            error.style.display = 'block'
            setTimeout(() => {
                error.style.display = 'none'
            }, 3000)
        }
    }

    show_success(message) {
        const success = new Div({ 
            class: 'success-message',
            value: message
        })
        const success_dom = success.dom_create()
        this.query_selector('.editor-container').prepend(success_dom)
        setTimeout(() => success_dom.remove(), 3000)
    }

    toggle_edit_mode() {
        this.edit_mode = !this.edit_mode
        this.render()
    }

    toggle_view_mode() {
        this.view_mode = this.view_mode === 'content' ? 'versions' : 'content'
        this.update_ui()
    }

    update_ui() {
        if (this.view_mode === 'versions') {
            this.query_selector('.versions-container').show()
            this.query_selector('.versions-btn'      ).innerText = 'Hide Versions'
        }
        else {
            this.query_selector('.versions-container').hide()
            this.query_selector('.versions-btn'      ).innerText = 'Show Versions'
        }
    }

    render_toolbar() {
        const toolbar = new Div({ class: 'editor-toolbar' })
        const left_group = new Div({ class: 'toolbar-group' })
        const right_group = new Div({ class: 'toolbar-group' })

        if (this.edit_mode) {
            const save_btn = new Button({
                class: 'btn btn-success save-btn',
                value: 'Save Changes'
            })
            save_btn.add_element(new Icon({
                icon: 'save',
                size: 'sm',
                spacing: 'right'
            }))

            const cancel_btn = new Button({
                class: 'btn btn-secondary cancel-btn',
                value: 'Cancel'
            })
            cancel_btn.add_element(new Icon({
                icon: 'cross',
                size: 'sm',
                spacing: 'right'
            }))

            left_group.add_elements(save_btn, cancel_btn)
        } else {
            const edit_btn = new Button({
                class: 'btn btn-primary edit-btn',
                value: 'Edit'
            })
            edit_btn.add_element(new Icon({
                icon: 'edit',
                size: 'sm',
                spacing: 'right'
            }))
            left_group.add_element(edit_btn)
        }

        const versions_btn = new Button({
            class: 'btn btn-outline-secondary versions-btn',
            value: this.view_mode === 'content' ? 'Show History' : 'Show Content'
        })
        versions_btn.add_element(new Icon({icon: 'history',  size: 'sm',  spacing: 'right'}))
        right_group.add_element(versions_btn)

        toolbar.add_elements(left_group, right_group)
        return toolbar
    }

    render_editor() {
        return new Textarea({
            class: 'markdown-editor',
            value: this.markdown_content,
            attributes: {
                spellcheck: false,
                'data-gramm': false
            }
        })
    }

    render_preview() {
        return new Raw_Html({
            class: 'markdown-preview',
            value: marked.marked(this.markdown_content || '')
        })
    }

    render_versions() {
        const versions_container = new Div({ class: 'versions-container' })
        const versions_list     = new Div({ class: 'versions-list'      })

        this.versions.forEach(version => {
            const version_item = new Div({
                class: `version-item ${this.viewing_version === version.version_id ? 'current' : ''}`
            })

            // Version info section
            const info = new Div({ class: 'version-info' })

            // Version number and date/time
            const version_header = new Div({ class: 'version-header' })
            version_header.add_elements(
                new Div({ class: 'version-number' , value: `Version ${version.version_number}`               }),
                new Div({ class: 'version-status' , value: version.is_latest_version ? '(Latest)' : ''      })
            )

            // Date and time
            const date_time = new Div({ class: 'version-datetime' })
            date_time.add_elements(
                new Div({ class: 'version-date'   , value: version.created_date                             }),
                new Div({ class: 'version-time'   , value: version.created_time                             })
            )

            // File size
            const size = new Div({
                class: 'version-size',
                value: `${(version.file_size / 1024).toFixed(1)} KB`
            })

            info.add_elements(version_header, date_time, size)

            // Version actions
            const actions = new Div({ class: 'version-actions' })

            const view_btn = new Button({
                class      : 'btn btn-sm btn-outline-primary view-btn',
                value      : 'View',
                attributes : { 'data-version': version.version_id }
            })
            view_btn.add_element(new Icon({ icon: 'eye'   , size: 'sm', spacing: 'right' }))

            const restore_btn = new Button({
                class      : 'btn btn-sm btn-outline-success restore-btn',
                value      : 'Restore',
                attributes : { 'data-version': version.version_id }
            })
            restore_btn.add_element(new Icon({ icon: 'history', size: 'sm', spacing: 'right' }))

            // Only add buttons if version_id is not null
            if (version.version_id !== 'null') {
                actions.add_elements(view_btn, restore_btn)
            }

            version_item.add_elements(info, actions)
            versions_list.add_element(version_item)
        })

        versions_container.add_element(versions_list)
        return versions_container
    }

    render() {
        const container        = new Div({ class: 'markdown-container' })
        const editor_container = new Div({ class: 'editor-container' })

        const toolbar = this.render_toolbar()
        const error_msg = new Div({ class: 'error-message' })
        editor_container.add_elements(toolbar, error_msg)
        const preview_and_versions       = new Div({ class: 'preview-and-versions' })
        const viewer_and_editor          = new Div({ class: 'viewer-and-editor' })
        //if (this.view_mode === 'content') {
        if (this.edit_mode) {
            const split_view = new Div({ class: 'split-view' })
            split_view.add_elements(
                this.render_editor(),
                this.render_preview()
            )
            viewer_and_editor.add_element(split_view)
        } else {

            if (this.viewing_version) {
                const version_bar = new Div({ class: 'version-bar' })
                version_bar.add_elements(
                    new Div({
                        class: 'version-message',
                        value: 'Viewing previous version'
                    }),
                    new Button({
                        class: 'btn btn-sm btn-success',
                        value: 'Restore This Version'
                    }),
                    new Button({
                        class: 'btn btn-sm btn-secondary',
                        value: 'Return to Current'
                    })
                )
                viewer_and_editor.add_element(version_bar)
            }
            viewer_and_editor.add_element(this.render_preview())
        }
        // } else {
        //     editor_container.add_element(this.render_versions())
        // }

        editor_container.add_element(preview_and_versions)
        preview_and_versions.add_element(viewer_and_editor)
        preview_and_versions.add_element(this.render_versions())

        container.add_element(editor_container)

        this.set_inner_html(container.html())
        this.add_css_rules(this.css_rules())
        this.add_event_handlers()
    }

    add_event_handlers() {
        if (this.edit_mode) {
            this.query_selector('.markdown-editor').addEventListener('input', (e) => {
                const preview = this.query_selector('.markdown-preview')
                preview.innerHTML = marked.marked(e.target.value)
            })

            this.query_selector('.save-btn').addEventListener('click', () => this.save_content())
            this.query_selector('.cancel-btn').addEventListener('click', () => this.toggle_edit_mode())
        } else {
            this.query_selector('.edit-btn')?.addEventListener('click', () => this.toggle_edit_mode())
        }

        this.query_selector('.versions-btn').addEventListener('click', () => this.toggle_view_mode())

        //if (this.view_mode === 'versions') {
        this.query_selector_all('.view-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.view_version(btn.dataset.version)
            })
        })

        this.query_selector_all('.restore-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.restore_version(btn.dataset.version)
            })
        })
        //}

        if (this.viewing_version) {
            this.query_selector('.btn-success')?.addEventListener('click', () => {
                this.restore_version(this.viewing_version)
            })

            this.query_selector('.btn-secondary')?.addEventListener('click', () => {
                this.markdown_content = this.temp_content
                this.viewing_version = null
                this.render()
            })
        }
    }

    css_rules() {
        return {
            ".markdown-container"  : { height           : "100%"                      ,
                                     display          : "flex"                      ,
                                     flexDirection    : "column"                    ,
                                     backgroundColor  : "#fff"                      ,
                                     borderRadius     : "0.375rem"                  ,
                                     boxShadow        : "0 2px 4px rgba(0,0,0,0.1)" },

            ".editor-container"   : { flex             : "1"                         ,
                                     display          : "flex"                      ,
                                     flexDirection    : "column"                    ,
                                     padding          : "1rem"                      ,
                                     gap              : "1rem"                      },

            ".editor-toolbar"     : { display          : "flex"                      ,
                                     justifyContent   : "space-between"             ,
                                     alignItems       : "center"                    ,
                                     padding          : "0.5rem 0"                  ,
                                     borderBottom     : "1px solid #dee2e6"         ,
                                     marginBottom     : "1rem"                      },

            ".toolbar-group"      : { display          : "flex"                      ,
                                     gap              : "0.5rem"                    },

            ".split-view"          : { display          : "grid"                      ,
                                     gridTemplateColumns: "1fr 1fr"                   ,
                                     gap              : "1rem"                       ,
                                     height           : "calc(100vh - 200px)"       ,
                                     minHeight        : "400px"                     },

            ".markdown-editor"     : { width            : "100%"                      ,
                                     padding          : "1rem"                       ,
                                     fontSize         : "0.875rem"                  ,
                                     fontFamily       : "monospace"                 ,
                                     lineHeight       : "1.5"                       ,
                                     border           : "1px solid #dee2e6"         ,
                                     borderRadius     : "0.375rem"                  ,
                                     resize           : "none"                      },

            ".markdown-preview"    : { padding          : "1rem"                      ,
                                     overflow         : "auto"                      ,
                                     fontSize         : "0.875rem"                  ,
                                     lineHeight       : "1.6"                       ,
                                     backgroundColor  : "#f8f9fa"                   ,
                                     borderRadius     : "0.375rem"                  },

            ".error-message"       : { display          : "none"                      ,
                                     color            : "#dc3545"                   ,
                                     padding          : "0.75rem"                   ,
                                     marginBottom     : "1rem"                      ,
                                     backgroundColor  : "#f8d7da"                   ,
                                     borderRadius     : "0.375rem"                  ,
                                     fontSize         : "0.875rem"                  },

            ".success-message"     : { color            : "#155724"                   ,
                                     backgroundColor  : "#d4edda"                   ,
                                     padding          : "0.75rem"                   ,
                                     marginBottom     : "1rem"                      ,
                                     borderRadius     : "0.375rem"                  ,
                                     fontSize         : "0.875rem"                  },


        ".version-header"     : { display         : "flex"                      ,
                                 alignItems      : "center"                    ,
                                 gap             : "0.5rem"                    ,
                                 marginBottom    : "0.25rem"                   },

        ".version-number"     : { fontWeight      : "600"                       ,
                                 color           : "#212529"                   },

        ".version-status"     : { fontSize        : "0.75rem"                   ,
                                 color           : "#198754"                   ,
                                 fontWeight      : "500"                       },

        ".version-datetime"   : { display         : "flex"                      ,
                                 gap             : "0.5rem"                    ,
                                 fontSize        : "0.875rem"                  ,
                                 color           : "#6c757d"                   ,
                                 marginBottom    : "0.25rem"                   },

        ".version-size"       : { fontSize        : "0.75rem"                   ,
                                 color           : "#6c757d"                   },


        ".version-item.current .version-number" : {
                                 color           : "#0d6efd"                   },

            ".versions-list"      : { display          : "flex"                      ,
                                     flexDirection    : "column"                    ,
                                     gap              : "0.75rem"                   },

            ".version-item"       : { padding          : "1rem"                      ,
                                     backgroundColor  : "#f8f9fa"                   ,
                                     borderRadius     : "0.375rem"                  ,
                                     border           : "1px solid #dee2e6"         ,
                                     display          : "flex"                      ,
                                     justifyContent   : "space-between"             ,
                                     alignItems       : "center"                    },

            ".version-item.current": { borderColor      : "#0d6efd"                   ,
                                     borderWidth      : "2px"                       },

            ".version-info"       : { fontSize         : "0.875rem"                  ,
                                     color            : "#6c757d"                   },

            ".version-date"       : { fontWeight       : "500"                       ,
                                     color            : "#212529"                   ,
                                     marginBottom     : "0.25rem"                   },

            // ".version-actions"    : { display          : "flex"                      ,
            //                          gap              : "0.5rem"                    },
            ".version-actions"    : { display         : "flex"                      ,
                                     gap             : "0.5rem"                    ,
                                     alignItems      : "center"                    },

            ".version-bar"        : { padding          : "0.75rem"                   ,
                                     backgroundColor  : "#fff3cd"                   ,
                                     borderRadius     : "0.375rem"                  ,
                                     display          : "flex"                      ,
                                     alignItems       : "center"                    ,
                                     justifyContent   : "space-between"             ,
                                     marginTop        : "1rem"                      },

            ".version-message"    : { fontSize         : "0.875rem"                  ,
                                     color            : "#856404"                   },

            // Markdown preview styling
            ".markdown-preview h1" : { fontSize         : "1.75rem"                   ,
                                     marginBottom     : "1rem"                      ,
                                     borderBottom     : "1px solid #dee2e6"         ,
                                     paddingBottom    : "0.5rem"                    },

            ".markdown-preview h2" : { fontSize         : "1.5rem"                    ,
                                     marginBottom     : "1rem"                      ,
                                     borderBottom     : "1px solid #dee2e6"         ,
                                     paddingBottom    : "0.5rem"                    },

            ".markdown-preview h3" : { fontSize         : "1.25rem"                   ,
                                     marginBottom     : "0.75rem"                   },

            ".markdown-preview p"  : { marginBottom     : "1rem"                      },

            ".markdown-preview code": { fontFamily      : "monospace"                 ,
                                      backgroundColor : "#f1f3f5"                   ,
                                      padding         : "0.2em 0.4em"               ,
                                      borderRadius    : "0.25rem"                   },

            ".markdown-preview pre": { backgroundColor  : "#f8f9fa"                   ,
                                     padding          : "1rem"                       ,
                                     borderRadius     : "0.375rem"                   ,
                                     marginBottom     : "1rem"                       ,
                                     overflow         : "auto"                       },

            ".preview-and-versions": { display        : "flex"                       ,
                                       flexDirection  : "row"                        ,
                                       padding        : "10px"                       },
            ".versions-container"  : { flex           : "1"                          ,
                                       overflow       : "auto"                       ,
                                       maxWidth       : "250px"                      ,
                                       padding        : "10px"                       },

            ".viewer-and-editor"   : { flex           : 1                            ,
                                       padding        : "10px"                       },
        }
    }
}

WebC__User_Files__Markdown__Editor.define()