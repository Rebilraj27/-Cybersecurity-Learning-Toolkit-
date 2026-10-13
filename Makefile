# =============================================================================
# Cyber Toolkit — Makefile
# Created by: Rebilraj
# =============================================================================

IMAGE_NAME  := cyber-toolkit
IMAGE_TAG   := 1.0.0
CONTAINER   := cyber-toolkit

.PHONY: help build run shell test lint clean lab lab-down pcap

help:  ## Show this help
	@echo "Cyber Toolkit — Docker commands"
	@echo "----------------------------------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build:  ## Build the Docker image
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -t $(IMAGE_NAME):latest .

run:  ## Run the CLI with --help
	docker run --rm -it $(IMAGE_NAME):latest --help

shell:  ## Open an interactive bash shell in the container
	docker run --rm -it --entrypoint bash $(IMAGE_NAME):latest

test:  ## Run pytest inside the container
	docker run --rm $(IMAGE_NAME):latest --help >/dev/null
	docker run --rm -v $$PWD:/app $(IMAGE_NAME):latest test 2>/dev/null || \
		docker run --rm --entrypoint pytest $(IMAGE_NAME):latest -v

lint:  ## Run black + flake8 inside a temp container
	docker run --rm -v $$PWD:/app --entrypoint sh $(IMAGE_NAME):latest -c \
		"black --check toolkit/ cli.py && flake8 toolkit/ cli.py"

scan-demo:  ## Demo: scan a local host's top ports
	docker run --rm --network host $(IMAGE_NAME):latest portscan 127.0.0.1 --ports 1-100

sniff:  ## Sniff packets (requires host network + NET_RAW)
	docker run --rm -it --network host --cap-add NET_RAW --cap-add NET_ADMIN \
		$(IMAGE_NAME):latest sniff --list

lab:  ## Start practice lab (Juice Shop + DVWA)
	docker compose --profile lab up -d
	@echo "✅ Juice Shop: http://localhost:3000"
	@echo "✅ DVWA:      http://localhost:8080  (admin/password)"

lab-down:  ## Stop the practice lab
	docker compose --profile lab down

pcap:  ## Analyze all pcaps in ./captures
	@for f in captures/*.pcap; do \
		echo "── Analyzing $$f ──"; \
		docker run --rm -v $$PWD/captures:/app/captures $(IMAGE_NAME):latest \
			sniff --pcap /app/captures/$$(basename $$f); \
	done

clean:  ## Remove image + dangling layers
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) $(IMAGE_NAME):latest 2>/dev/null || true
	docker system prune -f

logs:  ## Show lab container logs
	docker compose --profile lab logs -f
