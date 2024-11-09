DOCKER_REGISTRY := docker.io
ALPINE_MIRROR := https://dl-cdn.alpinelinux.org
PYPI_INDEX := https://pypi.org/simple

CI_DOCKER_REGISTRY := localhost
IMAGE_TAG := latest
BUILD_ARGS := --build-arg no_proxy=localhost,127.,10., --build-arg DOCKER_REGISTRY=${DOCKER_REGISTRY} --build-arg ALPINE_MIRROR=${ALPINE_MIRROR} --build-arg PYPI_INDEX=${PYPI_INDEX}

package:
	podman build --tls-verify=false ${BUILD_ARGS} --target feature -t ${CI_DOCKER_REGISTRY}/scmci/feature:${IMAGE_TAG} .
	podman build --tls-verify=false ${BUILD_ARGS} --target jenkins -t ${CI_DOCKER_REGISTRY}/scmci/jenkins:${IMAGE_TAG} .

release:
	podman push --tls-verify=false ${CI_DOCKER_REGISTRY}/scmci/feature:${IMAGE_TAG}
	podman push --tls-verify=false ${CI_DOCKER_REGISTRY}/scmci/jenkins:${IMAGE_TAG}

all: package release

deploy:
	podman rm -f feature-ci_feature_1 feature-ci_jenkins_1 feature-ci_gerrit_1 feature-ci_postgres_1
	podman-compose up -d
	podman ps -a

clean:
	echo "no clean"
