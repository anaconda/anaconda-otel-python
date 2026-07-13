.PHONY: test unit integration

test:
	./run-tests.sh

unit:
	@export OTEL_USE_CONSOLE_EXPORTER=TRUE && \
	pytest --color=yes --cov=./anaconda_opentelemetry --cov-report=html --cov-report=term-missing tests/unit_tests

integration:
	@export OTEL_USE_CONSOLE_EXPORTER=TRUE && \
	pytest --color=yes tests/integration_tests
