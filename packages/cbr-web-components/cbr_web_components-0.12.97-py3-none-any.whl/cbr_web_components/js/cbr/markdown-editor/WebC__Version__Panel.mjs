import Web_Component from '../../core/Web_Component.mjs'
import CSS__Cards    from '../../css/CSS__Cards.mjs'
import CSS__Buttons  from '../../css/CSS__Buttons.mjs'
import CSS__Icons    from '../../css/icons/CSS__Icons.mjs'
import Div           from '../../core/Div.mjs'
import Button        from '../../core/Button.mjs'
import Icon          from '../../css/icons/Icon.mjs'

export default class WebC__Version__Panel extends Web_Component {
    load_attributes() {
        new CSS__Cards   (this).apply_framework()
        new CSS__Buttons (this).apply_framework()
        new CSS__Icons   (this).apply_framework()

        this.file_id     = this.getAttribute('file_id')
        this.versions    = JSON.parse(this.getAttribute('versions') || '[]')
        this.on_view     = null
        this.on_restore  = null
    }

    format_date(timestamp) {
        return new Date(timestamp).toLocaleString()
    }

    format_size(bytes) {
        if (bytes === 0) return '0 B'
        const sizes = ['B', 'KB', 'MB', 'GB']
        const i = Math.floor(Math.log(bytes) / Math.log(1024))
        return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`
    }

    render() {
        const container = new Div({ class: 'version-panel card' })

        // Header
        const header = new Div({ class: 'version-header card-header' })
        header.add_elements(
            new Icon({ icon: 'history', size: 'sm', spacing: 'right' }),
            new Div({ class: 'version-title', value: 'Version History' })
        )

        // List of versions
        const list = new Div({ class: 'version-list card-body' })

        this.versions.forEach((version, index) => {
            const item = new Div({
                class: 'version-item',
                attributes: { 'data-version': version.version_id }
            })

            // Version info
            const info = new Div({ class: 'version-info' })
            info.add_elements(
                new Div({ class: 'version-number' , value: `v${index + 1}`                          }),
                new Div({ class: 'version-date'   , value: this.format_date(version.timestamp)      }),
                new Div({ class: 'version-size'   , value: this.format_size(version.size)           }),
                new Div({ class: 'version-author' , value: version.author || 'Unknown'              })
            )

            // Version actions
            const actions = new Div({ class: 'version-actions' })

            const view_btn = new Button({
                class: 'btn btn-sm btn-outline-primary view-btn',
                value: 'View'
            })
            view_btn.add_element(new Icon({ icon: 'eye', size: 'sm', spacing: 'right' }))

            const restore_btn = new Button({
                class: 'btn btn-sm btn-outline-success restore-btn',
                value: 'Restore'
            })
            restore_btn.add_element(new Icon({ icon: 'refresh', size: 'sm', spacing: 'right' }))

            actions.add_elements(view_btn, restore_btn)
            item.add_elements(info, actions)
            list.add_element(item)
        })

        container.add_elements(header, list)

        this.set_inner_html(container.html())
        this.add_css_rules(this.css_rules())
        this.add_event_handlers()
    }

    add_event_handlers() {
        this.query_selector_all('.view-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const version_id = e.target.closest('.version-item').dataset.version
                this.raise_event('version-view', { version_id })
            })
        })

        this.query_selector_all('.restore-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const version_id = e.target.closest('.version-item').dataset.version
                this.raise_event('version-restore', { version_id })
            })
        })
    }

    css_rules() {
        return {
            ".version-panel"       : { height           : "100%"                      ,
                                     display          : "flex"                      ,
                                     flexDirection    : "column"                    ,
                                     backgroundColor  : "#fff"                      },

            ".version-header"      : { display          : "flex"                      ,
                                     alignItems       : "center"                    ,
                                     gap              : "0.5rem"                    ,
                                     padding          : "1rem"                      ,
                                     backgroundColor  : "#f8f9fa"                   ,
                                     borderBottom     : "1px solid #dee2e6"         },

            ".version-title"       : { fontSize         : "0.875rem"                  ,
                                     fontWeight       : "500"                       ,
                                     color            : "#212529"                   },

            ".version-list"        : { flex             : "1"                         ,
                                     overflowY        : "auto"                      ,
                                     padding          : "1rem"                      ,
                                     display          : "flex"                      ,
                                     flexDirection    : "column"                    ,
                                     gap              : "0.75rem"                   },

            ".version-item"        : { padding          : "0.75rem"                   ,
                                     backgroundColor  : "#f8f9fa"                   ,
                                     borderRadius     : "0.375rem"                  ,
                                     border           : "1px solid #dee2e6"         ,
                                     display          : "flex"                      ,
                                     flexDirection    : "column"                    ,
                                     gap              : "0.75rem"                   },

            ".version-info"        : { display          : "grid"                      ,
                                     gap              : "0.25rem"                   ,
                                     fontSize         : "0.75rem"                   ,
                                     color            : "#6c757d"                   },

            ".version-number"      : { fontSize         : "0.875rem"                  ,
                                     fontWeight       : "500"                       ,
                                     color            : "#1a73e8"                   },

            ".version-date"        : { fontWeight       : "500"                       ,
                                     color            : "#212529"                   },

            ".version-author"      : { color            : "#6c757d"                   ,
                                     fontStyle        : "italic"                    },

            ".version-actions"     : { display          : "flex"                      ,
                                     gap              : "0.5rem"                    ,
                                     justifyContent   : "flex-end"                  },

            ".version-item:hover"  : { backgroundColor  : "#fff"                      ,
                                     boxShadow        : "0 2px 4px rgba(0,0,0,0.05)" },

            // Current version indicator
            ".version-item.current": { borderColor      : "#1a73e8"                   ,
                                     borderWidth      : "2px"                       }
        }
    }
}

WebC__Version__Panel.define()