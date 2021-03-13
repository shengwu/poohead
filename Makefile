.PHONY: test
test: check
	pytest

.PHONY: check
check:
	mypy poohead tests

.PHONY: fmt
fmt:
	black -S poohead tests
