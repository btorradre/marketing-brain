.PHONY: venv test check dr gen workers
venv:
	cd services/engine && uv venv .venv && uv pip install -p .venv/bin/python -r requirements.txt pytest
test:
	services/engine/.venv/bin/python -m pytest -q services/engine/tests
check:
	scripts/phase0_check.sh
dr:
	ADENGINE_PACKAGES_DIR=$(PWD)/packages services/engine/.venv/bin/python -m adengine.dr --http 8770
gen:
	ADENGINE_PACKAGES_DIR=$(PWD)/packages services/engine/.venv/bin/python -m adengine.gen --http 8771
workers:
	ADENGINE_PACKAGES_DIR=$(PWD)/packages services/engine/.venv/bin/python -m adengine.workers
