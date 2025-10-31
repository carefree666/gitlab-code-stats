PROJECT_NAME=gitlab-code-stats
VERSION=1.0.0
PYTHON=python3
VENV_DIR=.venv
PACKAGE_FILE=$(PROJECT_NAME)-$(VERSION).tar.gz
IMAGE_NAME=$(PROJECT_NAME)
PLATFORMS=linux/amd64,linux/arm64
BUILDER_NAME=gitlab-code-stats-builder

install:
	@echo "🐍 Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "📦 Installing dependencies..."
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r requirements.txt

run:
	@echo "🚀 Running CLI..."
	$(VENV_DIR)/bin/python main.py

web:
	@echo "🌐 Running Web service..."
	$(VENV_DIR)/bin/python main.py --web

package:
	@echo "📦 Packaging..."
	@mkdir -p dist
	tar --exclude='./dist' --exclude='*.pyc' --exclude='__pycache__' -czf dist/$(PACKAGE_FILE) .
	@echo "✅ Package created: dist/$(PACKAGE_FILE)"

docker-build:
	docker buildx create --name $(BUILDER_NAME) --use || true
	docker buildx inspect --bootstrap
	docker buildx build \
		--platform $(PLATFORMS) \
		--tag $(IMAGE_NAME):$(VERSION) \
		--push \
		.
	docker buildx rm $(BUILDER_NAME) || true
	@echo "✅ Docker multi-arch image built and pushed: $(IMAGE_NAME):$(VERSION)"

clean:
	@echo "🧹 Cleaning..."
	rm -rf dist __pycache__ */__pycache__ build *.spec $(VENV_DIR)
	find . -name '*.pyc' -delete
	find . -name '*.csv' -delete
	@echo "✅ Clean complete!"
