import com.lesfurets.jenkins.unit.BasePipelineTest
import org.junit.Before
import org.junit.Test

class FeatureApiSpec extends BasePipelineTest {

    def featureApi

    @Override
    @Before
    void setUp() {
        super.setUp()
        binding.setVariable('requests',[doHttpRequest: { Map args -> 
            if(args.data.status == 'MERGED'){
                return [content: '{"status": "MERGED"}']
            }else if(args.url.contains('/auth/')){
                return [content: '{"token": "f6d2698e646cf6599d4f5785eafc7b73bf92db24"}']
            }else if(['PUT', 'POST'].contains(args.httpMode)){
                return [content: """{"name": "${args.data.name}"}"""]
            }else if(args.data.containsKey('action')){
                return [content: """{"action": "${args.data.action}"}"""]
            }
        }])
        featureApi = loadScript('vars/featureApi.groovy')
        binding.setVariable('accessKey', 'my-token')
    }

    @Test
    void 'save should be successful when targetId is given'() {
        helper.registerAllowedMethod('readJSON', [Map]) { args ->
            assert args.text == '{"token": "f6d2698e646cf6599d4f5785eafc7b73bf92db24"}'
            return [token: 'f6d2698e646cf6599d4f5785eafc7b73bf92db24']
        }
        String response = featureApi.save fciApiUrl: 'https://my-fci.server.com/api/v1',
                            authCredentialsId: 'access-token',
                            endpoint: 'features',
                            targetId: 'FCI000000001',
                            payload: [name: 'my-feature', description: 'My demo feature', changes:[]]
        helper.callStack.findAll{ call -> call.methodName == 'httpRequest'}.any{ call ->
            assert args.url == 'https://my-fci.server.com/api/v1/features/FCI000000001/'
            assert args.headers == [[name: 'Authorization', value: 'f6d2698e646cf6599d4f5785eafc7b73bf92db24']]
            assert args.data == [name: 'my-feature', description: 'My demo feature', changes:[]]
            assert args.httpMode == 'PUT'
        }
        assert response == '{"name": "my-feature"}'
    }

    @Test
    void 'save should create new feature when fciId is not given'() {
        helper.registerAllowedMethod('readJSON', [Map]) { args ->
            assert args.text == '{"token": "f6d2698e646cf6599d4f5785eafc7b73bf92db24"}'
            return [token: 'f6d2698e646cf6599d4f5785eafc7b73bf92db24']
        }
        String response = featureApi.save fciApiUrl: 'https://my-fci.server.com/api/v1',
                            authCredentialsId: 'access-token',
                            endpoint: 'features',
                            payload: [name: 'my-feature', description: 'My demo feature', changes:[]]
        helper.callStack.findAll{ call -> call.methodName == 'httpRequest'}.any{ call ->
            assert args.url == 'https://my-fci.server.com/api/v1/features/FCI000000001/'
            assert args.headers == [[name: 'Authorization', value: 'f6d2698e646cf6599d4f5785eafc7b73bf92db24']]
            assert args.data == [name: 'my-feature', description: 'My demo feature', changes:[]]
            assert args.httpMode == 'POST'
        }
        assert response == '{"name": "my-feature"}'
    }

    @Test
    void 'setStatus should be successful with correct status is given'() {
        helper.registerAllowedMethod('readJSON', [Map]) { args ->
            assert args.text == '{"token": "f6d2698e646cf6599d4f5785eafc7b73bf92db24"}'
            return [token: 'f6d2698e646cf6599d4f5785eafc7b73bf92db24']
        }
        String res = featureApi.setStatus fciApiUrl: 'https://my-fci.server.com/api/v1',
                            authCredentialsId: 'access-token',
                            fciId: 'FCI000000001',
                            status: 'MERGED'
        helper.callStack.findAll{ call -> call.methodName == 'httpRequest'}.any{ call ->
            assert args.url == 'https://my-fci.server.com/api/v1/features/FCI000000001/'
            assert args.headers == [[name: 'Authorization', value: 'f6d2698e646cf6599d4f5785eafc7b73bf92db24']]
            assert args.data == [status: 'MERGED']
        }
        assert res == '{"status": "MERGED"}'
    }

    @Test
    void 'approve should be successfull when required params are given'() {
        helper.registerAllowedMethod('readJSON', [Map]) { args ->
            assert args.text == '{"token": "f6d2698e646cf6599d4f5785eafc7b73bf92db24"}'
            return [token: 'f6d2698e646cf6599d4f5785eafc7b73bf92db24']
        }
        String res = featureApi.approve fciApiUrl: 'https://my-fci.server.com/api/v1',
                            authCredentialsId: 'access-token',
                            fciId: 'FCI000000001'
        helper.callStack.findAll{ call -> call.methodName == 'httpRequest'}.any{ call ->
            assert args.url == 'https://my-fci.server.com/api/v1/features/FCI000000001/'
            assert args.headers == [[name: 'Authorization', value: 'f6d2698e646cf6599d4f5785eafc7b73bf92db24']]
            assert args.data == [action: 'approve']
        }
        assert res == '{"action": "approve"}'
    }
}
