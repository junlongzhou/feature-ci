import jenkins.model.Jenkins
import jenkins.security.ApiTokenProperty
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.GlobalMatrixAuthorizationStrategy
import org.jenkinsci.plugins.matrixauth.AuthorizationType
import org.jenkinsci.plugins.matrixauth.PermissionEntry
import com.cloudbees.plugins.credentials.CredentialsScope
import com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl


def adminUsername = System.getenv('JENKINS_ADMIN_USER') ?: 'admin'
def adminPassword = System.getenv('JENKINS_ADMIN_PASS') ?: 'admin123'
def instance = Jenkins.getInstance()
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
def adminUser = hudsonRealm.createAccount(adminUsername, adminPassword)
instance.setSecurityRealm(hudsonRealm)

def strategy = new GlobalMatrixAuthorizationStrategy()
strategy.add(hudson.model.Hudson.READ, new PermissionEntry(AuthorizationType.USER, 'anonymous'))
strategy.add(hudson.model.Item.READ, new PermissionEntry(AuthorizationType.USER, 'anonymous'))
strategy.add(hudson.model.View.READ, new PermissionEntry(AuthorizationType.USER, 'anonymous'))
strategy.add(Jenkins.ADMINISTER, new PermissionEntry(AuthorizationType.USER, adminUsername))
instance.setAuthorizationStrategy(strategy)
instance.save()

def apiTokenProperty = adminUser.getProperty(ApiTokenProperty.class)
def result = apiTokenProperty.tokenStore.generateNewToken('admin')
adminUser.save()

//append jenkins credentials
Map adminCredential = ["JENKINS_CREDENTIAL_ADMIN": "pw@jenkins@admin@" + result.plainValue]

def domain = com.cloudbees.plugins.credentials.domains.Domain.global()
def store = Jenkins.instance.getExtensionList('com.cloudbees.plugins.credentials.SystemCredentialsProvider')[0].getStore()
(System.getenv().findAll { it.key.startsWith('JENKINS_CREDENTIAL_') } << adminCredential).each { item ->
    def type = item.value.split('@')[0]
    def id = item.value.split('@')[1]
    def user = item.value.split('@')[2]
    def password = item.value.split('@')[3..-1].join('@')

    if (type == 'ssh'){
        credential = new com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey(CredentialsScope.GLOBAL, id, user, new com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey.DirectEntryPrivateKeySource(new String(password.decodeBase64())), '', '')
    } else if (type == 'gitlab'){
        credential = new com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl(CredentialsScope.GLOBAL, id, '', hudson.util.Secret.fromString(password))
    } else if (type == 'string'){
        credential = new org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl(CredentialsScope.GLOBAL, id, '', hudson.util.Secret.fromString(password))
    } else if (type == 'pw'){
        credential = new UsernamePasswordCredentialsImpl(CredentialsScope.GLOBAL, id, '', user, password)
    }
    store.addCredentials(domain, credential)
}
