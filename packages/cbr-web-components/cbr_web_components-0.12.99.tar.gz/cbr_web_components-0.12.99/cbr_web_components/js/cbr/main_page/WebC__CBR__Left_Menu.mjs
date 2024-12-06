import Web_Component        from '../../core/Web_Component.mjs'
import CSS__Alerts          from "../../css/CSS__Alerts.mjs";
import CSS__Side_Menu       from "../../css/menus/CSS__Side_Menu.mjs"
import CSS__Typography      from '../../css/CSS__Typography.mjs'
import Left_Menu            from "../../css/menus/Left_Menu.mjs"
import Div                  from "../../core/Div.mjs"
import Button               from "../../core/Button.mjs"
import CBR__Left_Logo       from "./CBR__Left_Logo.mjs"
import CBR__Important_Alert from "./CBR__Important_Alert.mjs"
import WebC__Resize_Button from "../../elements/ui/WebC__Resize_Button.mjs";


export default class WebC__CBR__Left_Menu extends Web_Component {

    left_menu__resize__breakpoint = 768
    left_menu__resize__event_name = 'left-menu-toggle'

    load_attributes() {
        new CSS__Alerts    (this).apply_framework()
        new CSS__Side_Menu (this).apply_framework()
        new CSS__Typography(this).apply_framework()

        this.add_css_rules(CBR__Left_Logo      .css_rules())
        this.add_css_rules(CBR__Important_Alert.css_rules())
        this.add_css_rules(this.css_rules())
    }

    get div__left_menu_main() {
        return this.query_selector('.left-menu-main')
    }

    add_web_components() {
        let params = { resize_breakpoint : this.left_menu__resize__breakpoint ,
                       resize_event_name : this.left_menu__resize__event_name }
        this.add_web_component(WebC__Resize_Button, params )
    }

    add_event_listeners() {
        this.addEventListener('left-menu-toggle', (event) => this.on_left_menu_toggle(event))
    }

    on_left_menu_toggle (event) {
        const minimized = event.detail.minimized
        if (minimized) {
            this.div__left_menu_main.add_class   ('left-menu-minimized')
        } else {
            this.div__left_menu_main.remove_class('left-menu-minimized')
        }
    }

    html() {
        const div_left_menu       = new Div       ({ class: 'left-menu-main'       })
        const cbr_left_menu       = new Left_Menu ({ menu_items: this.menu_items() })
        const cbr_left_logo       = new CBR__Left_Logo()
        const cbr_important_alert = new CBR__Important_Alert()

        div_left_menu.add_elements(cbr_left_logo, cbr_left_menu, cbr_important_alert)
        return div_left_menu
    }

    menu_items() {
        return [
            { icon: 'home'    , label: 'Home'          , href: '/webc/cbr-webc-dev/home/index'       },
            { icon: 'robot'   , label: 'Athena'        , href: '/webc/cbr-webc-dev/athena/index'     },
            { icon: 'profile' , label: 'Profile'       , href: '/webc/cbr-webc-dev/profile/index'    },
            { icon: 'history' , label: 'Past Chats'    , href: '/webc/cbr-webc-dev/past-chats/index' },
            { icon: 'file'    , label: 'Files'         , href: '/webc/cbr-webc-dev/files/index'      },
            { icon: 'person'  , label: 'Personas'      , href: '/webc/cbr-webc-dev/personas/index'   },
            { icon: 'chat'    , label: 'Chat with LLMs', href: '/webc/cbr-webc-dev/chat/index'       },
            { icon: 'docs'    , label: 'Docs'          , href: '/webc/cbr-webc-dev/docs/index'       }
        ]
    }

    css_rules() {
        return {
            ".left-menu-main"                       : { transition : "width 0.3s ease-in-out"    ,
                                                        position   : "relative"                  },
            ".left-menu-minimized"                  : { width      : "60px"                      ,
                                                        paddingTop : "10px"                      ,
                                                        overflow   : "hidden"                    },
            ".left-menu-minimized .logo-container"  : { display    : "none"                      },
            ".left-menu-minimized .important-alert" : { display    : "none"                      },
        }
    }
}

WebC__CBR__Left_Menu.define()