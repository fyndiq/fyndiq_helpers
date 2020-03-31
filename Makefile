lint:
	@scripts/lint.sh

setup:
	scripts/setup.sh

unit-test:
	@scripts/unit-test.sh

test: unit-test

pip-update:
	@scripts/pip-update.sh

update:
	@scripts/update.sh
