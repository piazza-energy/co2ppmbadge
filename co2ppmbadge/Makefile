CURRENT_DIR?=$(abspath .)
VOLUME_DIR?=co2ppmbadge
OUTFILE_LAYER?=layer-co2ppmbadge.zip
OUTFILE_LAMBDA_CREATE_BADGES?=lambda-create_badges.zip

pin_requirements:
	pipenv lock -r > requirements.txt

build_sam: pin_requirements
	# ouch! sam is painful... maybe we can just use terraform
	# pipenv run sam build --manifest requirements.txt

docker_shell:
	docker run --rm -ti -v ${CURRENT_DIR}:/${VOLUME_DIR} lambci/lambda:build-python3.6 bash

build_zips: pin_requirements
	docker run --rm -v ${CURRENT_DIR}:/${VOLUME_DIR} lambci/lambda:build-python3.6 bash -c \
		'cd /${VOLUME_DIR} && \
		make docker_build_layer && \
		make docker_build_lambda_create_badges'
	-mv -f ${OUTFILE_LAYER} ${CURRENT_DIR}/../infrastructure
	-mv -f ${OUTFILE_LAMBDA_CREATE_BADGES} ${CURRENT_DIR}/../infrastructure

docker_build_layer:
	# this is intended to run within the docker container
	cd ~ && virtualenv venv
	~/venv/bin/pip install -t ~/python -r /${VOLUME_DIR}/requirements.txt
	cp -a /${VOLUME_DIR} ~/python
	cd ~ && zip -r9 ~/${OUTFILE_LAYER} python -x *__pycache__* *.pyc* *awscli* *.aws-sam* *boto* *pip* *pylint* *pytest* *setuptools*
	mv ~/${OUTFILE_LAYER} /${VOLUME_DIR}

docker_build_lambda_create_badges:
	cd /${VOLUME_DIR}/serverless/create_badges && zip -r9 ~/${OUTFILE_LAMBDA_CREATE_BADGES} * .env -x *__pycache__* *.pyc*
	mv ~/${OUTFILE_LAMBDA_CREATE_BADGES} /${VOLUME_DIR}
