import jenkins.model.Jenkins


String initJobs = System.getenv('JENKINS_INIT_JOBS') ?: ''
if (initJobs) {
    for (jobName in initJobs.split(',')) {
        def job = Jenkins.instance.getAllItems( hudson.model.Job.class ).find { it.fullName == jobName}
        job.scheduleBuild2(1);
    }
}
