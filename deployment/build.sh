#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
WORK_DIR=$(mktemp -d -p "$DIR")

IMAGE_NAME="deloinst/$(poetry version --no-interaction | sed 's| |:|g')"
export IMAGE_NAME
DOCKERFILE="${DIR}/deployment/Dockerfile"

if [[ ! "$WORK_DIR" || ! -d "$WORK_DIR" ]]; then
	echo "Could not create temp dir"
	exit 1
fi

# deletes the temp directory
function cleanup {
	rm -rf "$WORK_DIR"
	echo "Deleted temp working directory $WORK_DIR"
}

trap cleanup EXIT

export DOCKER_BUILDKIT=1
docker build -t "${IMAGE_NAME}" --ssh default -f "${DOCKERFILE}" "${DIR}"
