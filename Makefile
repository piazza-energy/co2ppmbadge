CURRENT_DIR?=$(abspath .)
INFRASTRUCTURE_DIR=${CURRENT_DIR}/infrastructure
SOURCE_DIR=${CURRENT_DIR}/co2ppmbadge

help:
	@echo "make, list of available commands"
	@echo "--------------------------------"

test:
	pipenv run pytest co2ppmbadge/tests/

coveralls:
	# mh... don't really know what I'm doing wrong here
	source .env && pipenv run coveralls

build_zips:
	make -C ${SOURCE_DIR} build_zips

tf_init:
	cd ${INFRASTRUCTURE_DIR} && terraform init

tf_plan:
	cd ${INFRASTRUCTURE_DIR} && terraform plan

tf_apply:
	cd ${INFRASTRUCTURE_DIR} && terraform apply

tf_destroy:
	cd ${INFRASTRUCTURE_DIR} && terraform destroy
