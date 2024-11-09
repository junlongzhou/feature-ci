import jenkins.model.Jenkins
import org.csanchez.jenkins.plugins.kubernetes.*
import org.csanchez.jenkins.plugins.kubernetes.volumes.*


Map clouds = [:]

System.getenv().findAll { it.key.startsWith('JENKINS_KUBERNETES_POD_') }.each { item ->
    def kubeName = item.value.split('@')[0]
    def url = item.value.split('@')[1]
    def namespace = item.value.split('@')[2]
    def credential = item.value.split('@')[3]
    def podName = item.value.split('@')[4]
    def labels = item.value.split('@')[5]
    def volumes = item.value.split('@')[6]
    def containers = item.value.split('@')[7..-1].join('@')

    def p = new PodTemplate()
    p.setName(podName)
    p.setLabel(labels.replace(',', ' '))
    p.setNamespace(namespace)
    p.setHostNetwork(false)

    if (containers) {
        List podContainers = []
        containers.split('@').each { c ->
            def newContainer = new ContainerTemplate(c.split(',')[0], c.split(',')[1], c.split(',')[2], '')
            def workingDir = c.split(',')[3]
            def requestCpu = (c+',,0').split(',')[4]

            newContainer.setAlwaysPullImage(true)
            newContainer.setWorkingDir(workingDir)
            newContainer.setPrivileged(true)
            newContainer.setResourceRequestCpu(requestCpu)
            podContainers.add(newContainer)
        }
        p.setContainers(podContainers)
    }

    if (volumes) {
        def hostPathVolumes = []
        volumes.split(',').each { v ->
            hostPathVolumes << new HostPathVolume(v.split(':')[0], v.split(':')[1], false)
        }
        p.setVolumes(hostPathVolumes)
    }

    if (! clouds.containsKey(kubeName)) {
        def kube = new KubernetesCloud(kubeName, [], url, namespace, System.getenv('JENKINS_MASTER_LOCATION') ?: 'http://localhost:8080', '99999', 0, 0, 5)
        kube.setSkipTlsVerify(true)
        kube.setCredentialsId(credential)
        clouds[kubeName] = kube
    }

    clouds[kubeName].addTemplate(p)
}


if (clouds) {
    clouds.each{ k, v -> Jenkins.getInstance().clouds.add(v) }
    Jenkins.getInstance().save()
}
