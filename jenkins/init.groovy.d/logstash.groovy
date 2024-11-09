import jenkins.plugins.logstash.LogstashConfiguration
import jenkins.plugins.logstash.configuration.Logstash

String logstashHost = System.getenv('JENKINS_LOGSTASH_HOST') ?: ''
if (logstashHost) {
    Logstash logstash = new Logstash()
    logstash.host = logstashHost.split(':')[0]
    logstash.port = Integer.parseInt(logstashHost.split(':')[1])

    LogstashConfiguration conf = LogstashConfiguration.getInstance()
    conf.logstashIndexer = logstash
    conf.enabled = true
    conf.enableGlobally = true
    conf.save()
}
