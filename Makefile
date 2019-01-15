check:
	@scripts/check.sh

lint:
	@scripts/lint.sh

setup:
	scripts/setup.sh

test: check lint
	scripts/test.sh

update:
	@scripts/update.sh