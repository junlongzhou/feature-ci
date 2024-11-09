import hudson.plugins.gearman.GearmanPluginConfig


String gerritHost = System.getenv('JENKINS_GEARMAN_HOST') ?: ''
if (gerritHost) {
    GearmanPluginConfig conf = GearmanPluginConfig.get()
    conf.host = gerritHost
    conf.port = Integer.parseInt((System.getenv('JENKINS_GEARMAN_PORT') ?: '4730'))
    conf.enablePlugin = Boolean.parseBoolean('true')
    conf.save()
}
