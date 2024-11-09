import jenkins.model.Jenkins
import jenkins.model.JenkinsLocationConfiguration
import hudson.model.ListView

def instance = Jenkins.getInstance()

String masterLocation = System.getenv('JENKINS_MASTER_LOCATION') ?: ''
if (masterLocation) {
    JenkinsLocationConfiguration.get().setUrl(masterLocation)
}

String masterExecutor = System.getenv('JENKINS_MASTER_EXECUTOR') ?: ''
if (masterExecutor) {
    instance.setNumExecutors(Integer.valueOf(masterExecutor))
}

System.getenv().findAll { it.key.startsWith('JENKINS_VIEW_') }.each { item ->
    String name = item.value.split('@')[0]
    String regex = item.value.split('@')[1]

    ListView view = new ListView(name)
    view.setIncludeRegex(regex)
    instance.addView(view)
    if (item.key == 'JENKINS_VIEW_PRIMARY') { instance.setPrimaryView(view) }
}

instance.save()
