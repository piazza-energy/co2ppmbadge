CURRENT_DIR?=$(abspath .)
INFRASTRUCTURE_DIR=${CURRENT_DIR}/infrastructure
SOURCE_DIR=${CURRENT_DIR}/co2ppmbadge

help:
	@echo "make, list of available commands"
	@echo "--------------------------------"

test:
	pipenv run pytest co2ppmbadge/tests/

coveralls:
	# .env file exports COVERALLS_REPO_TOKEN
	source .env && pipenv run coveralls

notify_errs:
	# these 2 .env files export SNS_TOPIC_LAMBDA_ERRS and EMAIL_SUBS_ERRORS
	# source .env && source ./co2ppmbadge/mgmt/.env
	SNS_TOPIC_LAMBDA_ERRS=${SNS_TOPIC_LAMBDA_ERRS}
	EMAIL_SUBS_ERRORS=${EMAIL_SUBS_ERRORS}
	pipenv run aws sns subscribe \
		--topic-arn ${SNS_TOPIC_LAMBDA_ERRS} \
		--protocol email \
		--notification-endpoint ${EMAIL_SUBS_ERRORS}

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
