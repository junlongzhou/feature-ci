ARG DOCKER_REGISTRY=docker.io

#######################################################################################################################
FROM ${DOCKER_REGISTRY}/library/alpine:3.19 AS feature

ARG ALPINE_MIRROR=https://dl-cdn.alpinelinux.org
ARG PYPI_INDEX=https://pypi.org/simple

RUN echo ${ALPINE_MIRROR}/alpine/v3.19/main >/etc/apk/repositories &&\
    echo ${ALPINE_MIRROR}/alpine/v3.19/community >>/etc/apk/repositories &&\
    apk add python3-dev py3-pip git gcc g++ linux-headers openldap-dev nginx

ADD apps/requirements.txt /tmp/requirements.txt
RUN python3 -m venv /tmp/pyenv && . /tmp/pyenv/bin/activate && pip3 --no-cache-dir install -i ${PYPI_INDEX} -r /tmp/requirements.txt

COPY dashboard /opt/dashboard
RUN cd /opt/dashboard && mkdir -p /usr/share/nginx/html && cp -r dist/* /usr/share/nginx/html

COPY apps /opt/apps
RUN cp -f /opt/apps/nginx.conf /etc/nginx/nginx.conf && dos2unix /opt/apps/run.sh && chmod a+x /opt/apps/run.sh

COPY cli /opt/cli
ADD fci.sh /opt/fci.sh
RUN chmod +x /opt/fci.sh

EXPOSE 80

ENTRYPOINT ["/opt/fci.sh"]


#######################################################################################################################
FROM ${DOCKER_REGISTRY}/jenkins/jenkins:2.452.2-alpine-jdk17 AS jenkins

ARG ALPINE_MIRROR=https://dl-cdn.alpinelinux.org
ARG PYPI_INDEX=https://pypi.org/simple

USER root
RUN echo ${ALPINE_MIRROR}/alpine/v3.19/main >/etc/apk/repositories &&\
    echo ${ALPINE_MIRROR}/alpine/v3.19/community >>/etc/apk/repositories &&\
    apk add jq make python3 py-pip &&\
    sed -i '2 a /tmp/startup.sh' /usr/local/bin/jenkins.sh
USER jenkins

COPY jenkins/plugins.txt /tmp/plugins.txt
RUN jenkins-plugin-cli -f /tmp/plugins.txt

RUN python3 -m venv /tmp/pyenv && . /tmp/pyenv/bin/activate && pip3 --no-cache-dir install -i ${PYPI_INDEX} jenkins-job-builder==6.2.0
COPY --chown=jenkins:jenkins jenkins/jenkins-jobs /tmp/jenkins-jobs
COPY --chmod=755 jenkins/startup.sh /tmp/startup.sh

COPY jenkins/jenkins-shared-library /tmp/jenkins-shared-library
RUN git init --initial-branch master --bare /usr/share/jenkins/ref/jenkins-shared-library.git -b master &&\
    git clone /usr/share/jenkins/ref/jenkins-shared-library.git /tmp/my-local-repo &&\
    cd /tmp/my-local-repo &&\
    cp -rf /tmp/jenkins-shared-library/* . &&\
    git config --global user.name jenkins &&\
    git config --global user.email jenkins@jenkins.com.not.available &&\
    git config --global http.sslVerify false &&\
    git add . &&\
    git commit -am "Add local jenkins-shared-library" &&\
    git push origin master &&\
    cd && rm -rf /tmp/my-local-repo

COPY jenkins/log /usr/share/jenkins/ref/log
COPY jenkins/init.groovy.d /usr/share/jenkins/ref/init.groovy.d
COPY jenkins/config/* /usr/share/jenkins/ref/
