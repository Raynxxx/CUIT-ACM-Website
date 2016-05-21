export function checkStatus(response) {
    if (response.status >= 200 && response.status < 300) {
        return response
    } else {
        let error = new Error(response.statusText)
        error.response = response
        throw error
    }
}

export function parseJSON(response) {
    return response.json()
}

export function withAuthHeader(params, token) {
    if (params.hasOwnProperty('headers')) {
        params.headers['Authorization'] = token
    } else {
        params.headers = {
            'Authorization': token
        }
    }
}