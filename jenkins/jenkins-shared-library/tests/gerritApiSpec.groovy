import com.lesfurets.jenkins.unit.BasePipelineTest
import org.junit.Before
import org.junit.Test

class GerritApiSpec extends BasePipelineTest {

    def gerritApi

    @Override
    @Before
    void setUp() {
        super.setUp()
        binding.setVariable('requests',[doHttpRequest: { Map args -> 
            if(args.url.contains('topic=my-topic')){
                return [content: """)]}' [{"id": "my-change-id", "status": "NEW"}] """]
            }else if(args.httpMode=='POST'){
                return [content: """)]}'{"change_id":"my-change-id"}"""]
            }else if(args.httpMode=='PUT'){
                return [content: """)]}'{"ref":"refs/tags/v0.0.0"}"""]
            }else{
                return [content: """)]}'"""]
            }
        }])
        gerritApi = loadScript('vars/gerritApi.groovy')
    }

    @Test
    void 'getChanges should return correct changes'() {
        List changes = [[id: 'my-change-id', status: 'NEW']]
        helper.registerAllowedMethod('readJSON', [Map]) { args ->
            assert args.text == """ [{"id": "my-change-id", "status": "NEW"}] """
            return changes
        }
        List foundChanges = gerritApi.getChanges gerritServer: 'https://my-gerrit.server.com',
                            authCredentialsId: 'my-credentials-id',
                            queryStr: 'topic=my-topic'
        helper.callStack.findAll{ call -> call.methodName == 'httpRequest'}.any{ call ->
            assert args.url == 'https://my-gerrit.server.com/a/changes/?q=topic=my-topic'
            assert args.authCredentialsId == 'my-credentials-id'
        }
        assert foundChanges == changes
    }

    @Test(expected = RuntimeException)
    void 'getChanges should fail when changes not found'() {
        helper.registerAllowedMethod('readJSON', [Map]) { args ->
            assert args.text == ' '
            return ''
        }
        Map callerParams = [gerritServer: 'https://my-gerrit.server.com',
                            authCredentialsId: 'my-credentials-id',
                            queryStr: 'message=my-feature'
                        ]
        helper.callStack.findAll{ call -> call.methodName == 'httpRequest'}.any{ call ->
            assert args.url == 'https://my-gerrit.server.com/a/changes/?q=message=my-feature'
            assert args.authCredentialsId == 'my-credentials-id'
        }
        assertThrows(RuntimeException, gerritApi.getChanges(callerParams))
    }

    @Test
    void 'createChange should be successfull'() {
        helper.registerAllowedMethod('readJSON', [Map]) { args ->
            assert args.text == '{"change_id":"my-change-id"}'
            return [change_id: 'my-change-id']
        }
        Map res = gerritApi.createChange gerritServer: 'https://my-gerrit.server.com',
                            authCredentialsId: 'my-credentials-id',
                            project: 'my-project',
                            branch: 'master',
                            subject: 'my-subject',
                            topic: 'my-topic',
                            isPrivate: true
        helper.callStack.findAll{ call -> call.methodName == 'httpRequest'}.any{ call ->
            assert args.url == 'https://my-gerrit.server.com/a/changes/'
            assert args.data == [
                project: 'my-project',
                branch: 'master',
                subject: 'my-subject',
                topic: 'my-topic',
                is_private: true,
                work_in_progress: false
            ]
            assert args.authCredentialsId == 'my-credentials-id'
        }
        assert res.change_id == 'my-change-id'
    }

    @Test
    void 'createTag should be successfull'() {
        helper.registerAllowedMethod('readJSON', [Map]) { args ->
            assert args.text == '{"ref":"refs/tags/v0.0.0"}'
            return [ref: 'refs/tags/v0.0.0']
        }
        Map res = gerritApi.createTag gerritServer: 'https://my-gerrit.server.com',
                            authCredentialsId: 'my-credentials-id',
                            project: 'my-group/my-project',
                            branch: 'master',
                            tag: 'v0.0.0',
                            tagMessage: 'my-init-tag'
        helper.callStack.findAll{ call -> call.methodName == 'httpRequest'}.any{ call ->
            assert args.url == 'https://my-gerrit.server.com/a/projects/my-group%2Fmy-project/tag/v0.0.0'
            assert args.data == [
                message: 'my-init-tag',
                revision: 'master'
            ]
            assert args.authCredentialsId == 'my-credentials-id'
        }
        assert res.ref == 'refs/tags/v0.0.0'
    }

    @Test
    void 'setReview should be successfull'() {
        helper.registerAllowedMethod('readJSON', [Map]) { args ->
             assert args.text == '{"change_id":"my-change-id"}'
            return [change_id: 'my-change-id']
        }
        Map res = gerritApi.setReview gerritServer: 'https://my-gerrit.server.com',
                            authCredentialsId: 'my-credentials-id',
                            changeId: 'my-change-id',
                            revision: 'my-revision',
                            message: 'Auto review',
                            labels: ['Code-Review': 2]
        helper.callStack.findAll{ call -> call.methodName == 'httpRequest'}.any{ call ->
            assert args.url == 'https://my-gerrit.server.com/a/changes/my-change-id/revisions/my-revision/review'
            assert args.data == [
                message: 'Auto review',
                labels: ['Code-Review': 2]
            ]
            assert args.authCredentialsId == 'my-credentials-id'
        }
        assert res.change_id == 'my-change-id'
    }

    @Test
    void 'submit should be successfull'() {
        helper.registerAllowedMethod('readJSON', [Map]) { args ->
            assert args.text == '{"change_id":"my-change-id"}'
            return [change_id: 'my-change-id']
        }
        Map res = gerritApi.submit gerritServer: 'https://my-gerrit.server.com',
                            authCredentialsId: 'my-credentials-id',
                            changeId: 'my-change-id'
        helper.callStack.findAll{ call -> call.methodName == 'httpRequest'}.any{ call ->
            assert args.url == 'https://my-gerrit.server.com/a/changes/my-change-id/submit'
            assert args.authCredentialsId == 'my-credentials-id'
        }
        assert res.change_id == 'my-change-id'
    }
}
