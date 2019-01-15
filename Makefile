lint:
	@scripts/lint.sh

setup:
	scripts/setup.sh

unit-test:
	@scripts/unit-test.sh

test: unit-test

update:
	@scripts/update.sh