List getChanges(Map config){
    if (!config.gerritServer || !config.authCredentialsId || !config.queryStr) {
        error "getChanges: Missing required parameters - gerritServer|accessKeyCredentialsId|queryStr"
    }
    String queryUrl = "${config.gerritServer}/a/changes/?q=${config.queryStr}"
    def responseList
    String responseContent = requests.doHttpRequest(url: queryUrl, authCredentialsId: config.authCredentialsId).content
    echo responseContent
    responseList = readJSON text: responseContent.split('\\)\\]\\}\\\'').last()
    if (!(responseList instanceof List)) {
        error "Not map format: $responseList"
    }
    return responseList
}

Map createChange(Map config){
    if (!config.gerritServer || !config.authCredentialsId || !config.project || !config.branch || !config.subject || !config.topic) {
        error "createChange: Missing required parameters - gerritServer|accessKeyCredentialsId|project|branch|subject|topic"
    }
    String url = "${config.gerritServer}/a/changes/"
    def response = requests.doHttpRequest url: url,
                                            authCredentialsId: config.authCredentialsId,
                                            httpMode: 'POST',
                                            data: [
                                                project: config.project,
                                                branch: config.branch,
                                                subject: config.subject,
                                                topic: config.topic,
                                                is_private: config.isPrivate ?: false,
                                                work_in_progress: config.workInProgress ?: false
                                            ]
    echo response.content
    def responseMap = readJSON text: response.content.split('\\)\\]\\}\\\'').last()
    if (!(responseMap instanceof Map)) {
        error "Not map format: $responseMap"
    }
    return responseMap
}

Map createTag(Map config){
    if (!config.gerritServer || !config.authCredentialsId || !config.project || !config.branch || !config.tag || !config.tagMessage) {
        error "createTag: Missing required parameters - gerritServer|accessKeyCredentialsId|project|branch|tagMessage"
    }
    config.project = config.project.replace('/', '%2F')
    String url = "${config.gerritServer}/a/projects/${config.project}/tags/${config.tag}"
    def response = requests.doHttpRequest url: url,
                                            authCredentialsId: config.authCredentialsId,
                                            httpMode: 'PUT',
                                            data: [
                                                message: config.tagMessage,
                                                revision: config.branch
                                            ]
    echo response.content
    def responseMap = readJSON text: response.content.split('\\)\\]\\}\\\'').last()
    if (!(responseMap instanceof Map)) {
        error "Not map format: $responseMap"
    }
    return responseMap
}

Map setReview(Map config){
    if (!config.gerritServer || !config.authCredentialsId || !config.changeId || !config.revision || !config.message) {
        error "setReview: Missing required parameters - gerritServer|accessKeyCredentialsId|changeId|revision|message"
    }
    Map labels = config.labels ?: [:]
    String url = "${config.gerritServer}/a/changes/${config.changeId}/revisions/${config.revision}/review"
    def response = requests.doHttpRequest url: url,
                                            authCredentialsId: config.authCredentialsId,
                                            httpMode: 'POST',
                                            data: [
                                                message: config.message,
                                                labels: labels
                                            ]
    echo response.content
    def responseMap = readJSON text: response.content.split('\\)\\]\\}\\\'').last()
    if (!(responseMap instanceof Map)) {
        error "Not map format: $responseMap"
    }
    return responseMap
}

Map submit(Map config){
    if (!config.gerritServer || !config.authCredentialsId || !config.changeId) {
        error "submit: Missing required parameters - gerritServer|accessKeyCredentialsId|changeId"
    }
    String url = "${config.gerritServer}/a/changes/${config.changeId}/submit"
    def response = requests.doHttpRequest url: url,
                                            authCredentialsId: config.authCredentialsId,
                                            httpMode: 'POST',
                                            contentType: 'NOT_SET'
    echo response.content
    def responseMap = readJSON text: response.content.split('\\)\\]\\}\\\'').last()
    if (!(responseMap instanceof Map)) {
        error "Not map format: $responseMap"
    }
    return responseMap
}

void unmarkPrivate(Map config){
    if (!config.gerritServer || !config.authCredentialsId || !config.changeId) {
        error "unmarkPrivate: Missing required parameters - gerritServer|accessKeyCredentialsId|changeId"
    }
    Map labels = config.labels ?: [:]
    String url = "${config.gerritServer}/a/changes/${config.changeId}/private"
    def response = requests.doHttpRequest url: url,
                                            authCredentialsId: config.authCredentialsId,
                                            httpMode: 'DELETE',
                                            contentType: 'NOT_SET',
                                            acceptType: 'NOT_SET'
    echo response.content
}

void setReadyForReview(Map config){
    if (!config.gerritServer || !config.authCredentialsId || !config.changeId) {
        error "setReadyForReview: Missing required parameters - gerritServer|accessKeyCredentialsId|changeId"
    }
    Map labels = config.labels ?: [:]
    String url = "${config.gerritServer}/a/changes/${config.changeId}/ready"
    def response = requests.doHttpRequest url: url,
                                            authCredentialsId: config.authCredentialsId,
                                            httpMode: 'POST',
                                            acceptType: 'NOT_SET',
                                            contentType: 'NOT_SET'
    echo response.content
}

List getHashtags(Map config){
    if (!config.gerritServer || !config.authCredentialsId || !config.changeId) {
        error "getChanges: Missing required parameters - gerritServer|accessKeyCredentialsId|changeId"
    }
    String queryUrl = "${config.gerritServer}/a/changes/${config.changeId}/hashtags"
    def responseList
    String responseContent = requests.doHttpRequest(url: queryUrl, authCredentialsId: config.authCredentialsId).content
    echo responseContent
    responseList = readJSON text: responseContent.split('\\)\\]\\}\\\'').last()
    if (!(responseList instanceof List)) {
        error "Not map format: $responseList"
    }
    return responseList
}

List setHashtags(Map config){
    if (!config.gerritServer || !config.authCredentialsId || !config.changeId || !config.addedTags) {
        error "setHashtags: Missing required parameters - gerritServer|accessKeyCredentialsId|changeId|addedTags"
    }
    String url = "${config.gerritServer}/a/changes/${config.changeId}/hashtags"
    Map payload = [
        add: config.addedTags
    ]
    if(config.removedTags){
        payload = payload + [remove: config.removedTags]
    }
    def response = requests.doHttpRequest url: url,
                                            authCredentialsId: config.authCredentialsId,
                                            httpMode: 'POST',
                                            data: payload
    echo response.content
    def responseList = readJSON text: response.content.split('\\)\\]\\}\\\'').last()
    if (!(responseList instanceof List)) {
        error "Not map format: $responseList"
    }
    return responseList
}
