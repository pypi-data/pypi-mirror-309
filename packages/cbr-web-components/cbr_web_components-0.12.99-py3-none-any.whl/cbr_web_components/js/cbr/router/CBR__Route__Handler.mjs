import Raw_Html from "../../core/Raw_Html.mjs";

export default class CBR__Route__Handler {

    base_path = '/webc/cbr-webc-dev'

    constructor(component) {
        this.component = component
        this.setupEventListeners()
    }

    setupEventListeners() {
        // Listen for popstate events (browser back/forward)
        window.addEventListener('popstate', (event) => {
            this.handleRoute(window.location.pathname)
        })

        // Intercept navigation clicks
        document.addEventListener('click', (event) => {
            const path = event.composedPath();
            const link = path.find(el => el.tagName === 'A');

            if (link && link.href.startsWith(window.location.origin)) {
                if (link.href.includes('/web/') || link.href.includes('/athena/index#' )) {           // don't intercept links to other pages
                    return
                }
                event.preventDefault()
                const path = link.href.replace(window.location.origin, '')
                this.navigate(path)
            }
        })
    }

    navigate(path) {
        window.history.pushState({}, '', path)
        this.handleRoute(path)
    }

    async handleRoute(path) {
        const contentEl = this.component.query_selector('#content')
        if (!contentEl) return

        const placeholder = contentEl


        const routePath = path.replace(this.base_path, '').replace(/^\/+/, '') || 'home'                // Get the route path without the base path

        const pathSegments = routePath.split('/').filter(segment => segment)                     // Create navigation classes from the path segments
        const navClasses = pathSegments.map((segment, index) => {
            const subPath = pathSegments.slice(0, index + 1).join('-')                                  // Build cumulative path for each level
            return `nav-${subPath}`
        })

        const div_classes = `nav-content ${navClasses.join(' ')}`
        const wrapperDiv = new Raw_Html({class: div_classes })                                               // Create wrapper div with all navigation classes



        try {
            const content         = await this.component.routeContent.fetch_content(routePath)
            wrapperDiv.raw_html      = content
            placeholder.innerHTML = wrapperDiv.html()
        } catch (error) {
            console.error('Error loading content:', error)
            wrapperDiv.value = '<div class="content-error">Error loading content. Please try again.</div>'
            placeholder.innerHTML = wrapperDiv.html()
        }
    }
}