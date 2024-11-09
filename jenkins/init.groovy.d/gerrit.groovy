import com.sonyericsson.hudson.plugins.gerrit.trigger.config.Config
import com.sonyericsson.hudson.plugins.gerrit.trigger.GerritServer
import com.sonyericsson.hudson.plugins.gerrit.trigger.PluginImpl


System.getenv().findAll { it.key.startsWith('JENKINS_GERRIT_') }.each { item ->
    String name = item.value.split('@')[0]
    String host = item.value.split('@')[1]
    String sshPort = item.value.split('@')[2]
    String user = item.value.split('@')[3]
    String sshKey = item.value.split('@')[4]
    String frontendUrl = item.value.split('@')[5]

    GerritServer server = new GerritServer(name)
    Config config = server.getConfig()
    config.setGerritHostName(host)
    config.setGerritSshPort(Integer.parseInt(sshPort))
    config.setGerritUserName(user)
    config.setGerritFrontEndURL(frontendUrl)

    String sshKeyFileName = System.getenv('JENKINS_HOME') + "/gerrit.sshkey." + name
    File sshKeyFile = new File(sshKeyFileName)
    sshKeyFile.write(new String(sshKey.decodeBase64()))
    config.setGerritAuthKeyFile(sshKeyFile)

    PluginImpl.getInstance().addServer(server)
    server.start()
}
