def doHttpRequest(Map callerParams) {
    if(!callerParams.url) {
        error "doHttpRequest: url missing -- callerParams=$callerParams"
    }
    Map defaultParams = [
        httpMode: 'GET',
        headers: [:],
        connectionTimeout: 60,
        retryCount: 3,
        acceptType: 'APPLICATION_JSON',
        contentType: 'APPLICATION_JSON',
        validResponseCodes: '100:399',
        maskValue: true
    ]
    callerParams = defaultParams + callerParams
    List customHeaders = callerParams.headers.findAll{ it.name!=null && it.value!=null }.collect{ Map header ->
        [name: header.name, value: header.value, maskValue: defaultParams.maskValue] 
    }
    Map httpRequestParams = [
        customHeaders: customHeaders ?: [],
        timeout: callerParams.connectionTimeout,
        httpMode: callerParams.httpMode,
        url: callerParams.url,
        acceptType: callerParams.acceptType,
        contentType: callerParams.contentType,
        validResponseCodes: callerParams.validResponseCodes
    ]
    if(callerParams.data instanceof Map){
        httpRequestParams = httpRequestParams + [requestBody: writeJSON(json: callerParams.data, returnText: true)]
    }
    if(callerParams.authCredentialsId){
        httpRequestParams = httpRequestParams + [authentication: callerParams.authCredentialsId]
    }
    def httpResponse = null
    retry(callerParams.retryCount) {
        httpResponse = httpRequest(httpRequestParams)
    }
    return httpResponse
}
