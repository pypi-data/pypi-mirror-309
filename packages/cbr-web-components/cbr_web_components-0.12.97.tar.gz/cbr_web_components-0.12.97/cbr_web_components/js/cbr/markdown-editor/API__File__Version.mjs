export default class API__File__Version {
    constructor(api_invoke) {
        this.api_invoke = api_invoke
    }

    async get_versions(file_id) {
        return await this.api_invoke.invoke_api(
            `/api/user-data/files/file-versions?file_id=${file_id}`,
            'GET'
        )
    }

    async get_version_content(file_id, version_id) {
        return await this.api_invoke.invoke_api(
            `/api/user-data/files/file--bytes?file_id=${file_id}&version_id=${version_id}`,
            'GET'
        )
    }
}