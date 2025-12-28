docker-build:
	docker buildx build --platform linux/arm64 --build-arg ARCH=linux/arm64 -t ai-product-research:latest .

docker-build-push:
	docker buildx build --push --platform linux/arm64 --build-arg ARCH=linux/arm64 -t weaxme/pet-project:ai-product-research-latest .

release: docker-build-push
	ssh hetzner-mvp "docker compose pull"
	ssh hetzner-mvp "docker compose stop ai_product_research; docker compose up -d ai_product_research"