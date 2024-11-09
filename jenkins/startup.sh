#!/bin/bash


if [ "${JENKINS_JOBS_GIT_REPO}" ];then
  git clone ${JENKINS_JOBS_GIT_REPO} /tmp/tmp-jobs -b ${JENKINS_JOBS_GIT_BRANCH:-master} --depth 1
  mkdir -p /tmp/jenkins-jobs
  for dir in `echo ${JENKINS_JOBS_DIRS:-.} |sed 's/,/ /g'`;do cp -rf /tmp/tmp-jobs/${dir}/* /tmp/jenkins-jobs/ ;done;
fi

if [ -d /tmp/jenkins-jobs ];then
    #workaround for JENKINS-JOB-BUILDER
    for variable in `env | grep -E "^(JJB_)" |sed 's/ /@!#/g'`;do
       key=`echo $variable |cut -d= -f1`
        value=`echo $variable |cut -d= -f2- |sed 's/@!#/ /g'`
        sed -i "s#${key}#${value}#g" /tmp/jenkins-jobs/*/*.yml
        sed -i "s#${key}#${value}#g" /tmp/jenkins-jobs/*/Jenkinsfile
    done

    #run JENKINS-JOB-BUILDER
    . /tmp/pyenv/bin/activate
    jenkins-jobs test --config-xml -r /tmp/jenkins-jobs -o /usr/share/jenkins/ref/jobs
    deactivate

    #workaround for jobs with folder
    for config_file in `find /usr/share/jenkins/ref/jobs -name config.xml |sort -r`;do
        if grep -q cloudbees-folder ${config_file};then
            config_dir=`dirname $config_file`
            echo "workaround for folder: ${config_dir}"
            for f in `ls -F ${config_dir} |grep "/$" |cut -d/ -f1`;do
                mkdir -p ${config_dir}/jobs
                echo mv ${config_dir}/$f ${config_dir}/jobs
                mv ${config_dir}/$f ${config_dir}/jobs
            done
        fi
    done
fi
