# Makefile to manage Python dependencies using pip-compile and pip
all: check

# The input requirements.in file
REQUIREMENTS_IN = requirements.in

# The generated requirements.txt file
REQUIREMENTS_TXT = requirements.txt

EB_ZIP := myapp.zip

.PHONY: compile install push format type build run package

format:
	ruff --fix .

type:
	mypy .

check: format type

compile: $(REQUIREMENTS_TXT)

install: compile
	pip install -r $(REQUIREMENTS_TXT)

$(REQUIREMENTS_TXT): $(REQUIREMENTS_IN)
	pip-compile $(REQUIREMENTS_IN) -o $(REQUIREMENTS_TXT)

push: check
	@if [ -z "$(message)" ]; then \
		echo "Please specify a commit message: make commit message='Your message here'"; \
		exit 1; \
	fi
	git add .
	git commit -m "$(message)"
	git push

build:
	@docker build -t gpt-crawler-backend .

run: build
	@docker run -p 8000:8000 gpt-crawler-backend


package:
	@echo "Creating application zip file for AWS Elastic Beanstalk deployment..."
	zip -r $(EB_ZIP) . -x *.git* -x *node_modules* -x *.idea* -x *.venv* -x *.devcontainer* -x *.DS_Store* -x *__pycache__* -x *.mypy_cache*
	@echo "Package $(EB_ZIP) created."
