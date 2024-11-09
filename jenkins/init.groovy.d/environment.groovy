import jenkins.model.Jenkins
import hudson.slaves.EnvironmentVariablesNodeProperty


def instance = Jenkins.getInstance()
def globalNodeProperties = instance.getGlobalNodeProperties()
def envVarsNodePropertyList = globalNodeProperties.getAll(EnvironmentVariablesNodeProperty.class)

def newEnvVarsNodeProperty = null
def envVars = null

if ( envVarsNodePropertyList == null || envVarsNodePropertyList.size() == 0 ) {
    newEnvVarsNodeProperty = new EnvironmentVariablesNodeProperty();
    globalNodeProperties.add(newEnvVarsNodeProperty)
    envVars = newEnvVarsNodeProperty.getEnvVars()
} else {
    envVars = envVarsNodePropertyList.get(0).getEnvVars()
}

System.getenv().findAll { it.key.startsWith('JENKINS_VARIABLE_') }.each { item ->
    envVars.put(item.key.replace('JENKINS_VARIABLE_', ''), item.value)
}

instance.save()
