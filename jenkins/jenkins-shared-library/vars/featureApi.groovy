String save(Map config){
    if (!config.fciApiUrl || !config.authCredentialsId || !config.payload || !config.endpoint) {
        error "save: Missing required parameters - fciApiUrl|authCredentialsId|payload|endpoint"
    }
    String token = getAuthToken(config)
    String url = "${config.fciApiUrl}/${config.endpoint}/"
    String httpMode = 'POST'
    if(config.targetId){
        url = "${config.fciApiUrl}/${config.endpoint}/${config.targetId}"
        httpMode = 'PUT'
    }
    def response = requests.doHttpRequest url: url,
                                        headers: [[name:'Authorization', value: "Token ${token}"]],
                                        httpMode: httpMode,
                                        data: config.payload
    echo response.content
    return response.content
}

String approve(Map config){
    if (!config.fciApiUrl || !config.authCredentialsId || !config.fciId) {
        error "approve: Missing required parameters - fciApiUrl|authCredentialsId|fciId"
    }
    String token = getAuthToken(config)
    def response = requests.doHttpRequest url: "${config.fciApiUrl}/features/${config.fciId}/",
                                        headers: [[name:'Authorization', value: "Token ${token}"]],
                                        httpMode: 'PATCH',
                                        data: [action: 'approve']
    echo response.content
    return response.content
}

String setStatus(Map config){
    if (!config.fciApiUrl || !config.authCredentialsId || !config.status || !config.fciId) {
        error "setStatus: Missing required parameters - fciApiUrl|authCredentialsId|status"
    }
    String token = getAuthToken(config)
    def response = requests.doHttpRequest url: "${config.fciApiUrl}/features/${config.fciId}/",
                                        headers: [[name:'Authorization', value: "Token ${token}"]],
                                        httpMode: 'PATCH',
                                        data: [status: config.status]
    echo response.content
    return response.content
}

String delete(Map config){
    if (!config.fciApiUrl || !config.authCredentialsId || !config.targetId || !config.endpoint) {
        error "delete: Missing required parameters - fciApiUrl|authCredentialsId|payload|endpoint"
    }
    String token = getAuthToken(config)
    def response = requests.doHttpRequest url: "${config.fciApiUrl}/${config.endpoint}/${config.targetId}/",
                                        headers: [[name:'Authorization', value: "Token ${token}"]],
                                        httpMode: 'DELETE'
    echo response.content
    return response.content
}

String getAuthToken(Map config){
    String token = ''
    if (!config.fciApiUrl || !config.authCredentialsId) {
        error "setStatus: Missing required parameters - fciApiUrl|authCredentialsId"
    }
    withCredentials([usernamePassword(credentialsId: config.authCredentialsId, usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
        def response = requests.doHttpRequest url: "${config.fciApiUrl}/auth/",
                                            httpMode: 'POST',
                                            data: [username: "${USERNAME}", password: "${PASSWORD}"]
        Map jsonContent = readJSON text: response.content
        if(!jsonContent.token){
            error "Failed to get token for user: ${USERNAME}"
        }
        token = jsonContent.token
    }
    return token
}
