import jenkins.model.Jenkins
import jenkins.plugins.git.GitSCMSource;
import org.jenkinsci.plugins.workflow.libs.SCMSourceRetriever;
import org.jenkinsci.plugins.workflow.libs.LibraryConfiguration;


Map localLibraries = [:]
String localDir = System.getenv('JENKINS_HOME') + "/jenkins-shared-library.git"
if (new File(localDir).exists()) {
    localLibraries["JENKINS_LIBRARY_LOCAL"] = "local@@" + localDir + "@master"
}

List libraries = []
(System.getenv().findAll { it.key.startsWith('JENKINS_LIBRARY_') } << localLibraries).each { item ->
    def name = item.value.split('@')[0]
    def credential = item.value.split('@')[1]
    def repo = item.value.split('@')[2]
    def version = item.value.split('@')[3]

    SCMSourceRetriever retriever = new SCMSourceRetriever(new GitSCMSource(name, repo, credential, '*', '', false))
    LibraryConfiguration pipeline = new LibraryConfiguration(name, retriever)
    pipeline.setDefaultVersion(version)
    libraries.add(pipeline)
}

if (libraries) {
    def globalLibsDesc = Jenkins.getInstance().getDescriptor('org.jenkinsci.plugins.workflow.libs.GlobalLibraries')
    globalLibsDesc.get().setLibraries(libraries)
}
