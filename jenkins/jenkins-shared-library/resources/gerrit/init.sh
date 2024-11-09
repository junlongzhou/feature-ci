#!/bin/bash


GERRIT_USER=${GERRIT_USER:-admin}
GERRIT_PASSWORD=${GERRIT_PASSWORD:-secret}
GERRIT_LABELS=${GERRIT_LABELS:-Verified}
GERRIT_PROJECTS=${GERRIT_PROJECTS:-scmci/feature-ci}
GERRIT_PLUGINS=${GERRIT_PLUGINS:-checks-jenkins.jar}
GERRIT_CHECKS="${JENKINS_URL}"
GERRIT_URL_WITH_AUTH=`echo ${GERRIT_URL} |sed "s#://#://${GERRIT_USER}:${GERRIT_PASSWORD}@#"`


function gerrit_online() {
    echo "waiting gerrit service ready ..."
    while true;do curl -k -u ${GERRIT_USER}:${GERRIT_PASSWORD} ${GERRIT_URL}/a/groups/ && break ||sleep 10;done;
    echo "waiting gerrit API ready ..."
    while true;do curl -k -u ${GERRIT_USER}:${GERRIT_PASSWORD} ${GERRIT_URL}/a/groups/ |sed "s/)]}'//" |jq .Administrators && break ||sleep 10;done;
	sleep 5
}


function gerrit_new_plugins() {
    for plugin in `echo ${GERRIT_PLUGINS} |tr ',' ' '`;do
        echo "creating gerrit plugin ${plugin} ..."
        curl -k -u ${GERRIT_USER}:${GERRIT_PASSWORD} -X PUT -H "Content-Type:application/octet-stream" --data-binary @${plugin} ${GERRIT_URL}/a/plugins/${plugin} ||:
    done
}


function gerrit_new_accounts() {
    for account in `env |grep -e "^GERRIT_ACCOUNT_"`;do
        account_name=`echo ${account} |cut -d= -f2- |cut -d, -f1`
        account_pass=`echo ${account} |cut -d= -f2- |cut -d, -f2`
        account_sshpubkey=`echo ${account} |cut -d= -f2- |cut -d, -f3- |base64 -d`

        echo "creating gerrit user ${account_name} ..."
        echo "{'name': '${account_name}', 'display_name': '${account_name}', 'http_password': '${account_pass}', 'ssh_key': '${account_sshpubkey}', 'email': '${account_name}@do.not.available.com', 'groups': ['Administrators']}" >/tmp/account.json
        curl -k -u ${GERRIT_USER}:${GERRIT_PASSWORD} -X PUT -H "Content-Type: application/json" -d @/tmp/account.json ${GERRIT_URL}/a/accounts/${account_name} ||:
        curl -k -u ${GERRIT_USER}:${GERRIT_PASSWORD} -X PUT ${GERRIT_URL}/a/groups/Service%20Users/members/${account_name} ||:
    done
}


function gerrit_new_projects() {
    for project in `echo ${GERRIT_PROJECTS} |tr ',' ' '`;do
        echo "creating gerrit project ${project} ..."
        echo "{'description': '', 'submit_type': 'INHERIT', 'create_empty_commit': 'true', 'owners': ['Administrators']}" >/tmp/project.json
        curl -k -u ${GERRIT_USER}:${GERRIT_PASSWORD} -X PUT -H "Content-Type: application/json" -d @/tmp/project.json ${GERRIT_URL}/a/projects/${project//\//%2F} ||:

        echo "set gerrit checks UI for ${project} ..."
        cd /tmp
        rm -rf repo && git -c http.sslVerify=false clone ${GERRIT_URL_WITH_AUTH}/a/${project} repo && cd repo && git -c http.sslVerify=false fetch origin refs/meta/config && git checkout FETCH_HEAD
        rm -f checks-jenkins.config
        git config user.email "admin@example.com" && git config user.name "admin" && git config http.sslVerify false

        id=0
        for check in `echo ${GERRIT_CHECKS} |tr ',' ' '`;do
            id=$(($id+1))
            echo "[jenkins \"checks-${id}\"]" >>checks-jenkins.config && echo "        url = ${check}" >>checks-jenkins.config
            git add . && git commit -am "Add checks-jenkins.config" && git push origin HEAD:refs/meta/config
        done

    done
}


function gerrit_new_labels() {
    for label in `echo ${GERRIT_LABELS} |tr ',' ' '`;do
        echo "creating gerrit label ${label} ..."
        echo "{'commit_message': 'Create Label ${label}', 'values': {'0': 'No score', '-1': 'Fails', '+1': '${label}'}}" >/tmp/labels.json
        cat >/tmp/access.json <<EOF
        {
            "add": {
                "refs/*": {
                    "permissions": {
                        "create": {"rules": {"global:Registered-Users": {"action": "ALLOW"}}},
                        "push": {"rules": {"global:Registered-Users": {"action": "ALLOW","force": true}}},
                        "forgeAuthor": {"rules": {"global:Registered-Users": {"action": "ALLOW"}}},
                        "forgeCommitter": {"rules": {"global:Registered-Users": {"action": "ALLOW"}}},
                        "label-Verified": {"rules": {"global:Registered-Users": {"action": "ALLOW","min": "-1","max": "1"}}}
                    }
                }
            }
        }
EOF
		curl -k -u ${GERRIT_USER}:${GERRIT_PASSWORD} -X PUT  -H "Content-Type: application/json" -d @/tmp/labels.json ${GERRIT_URL}/a/projects/All-Projects/labels/${label} ||:
		curl -k -u ${GERRIT_USER}:${GERRIT_PASSWORD} -X POST -H "Content-Type: application/json" -d @/tmp/access.json ${GERRIT_URL}/a/projects/All-Projects/access ||:

    done
}


gerrit_online
gerrit_new_plugins
gerrit_new_accounts
gerrit_new_projects
gerrit_new_labels
