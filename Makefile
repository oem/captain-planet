.PHONY: publish
publish:
	docker build . -t oembot/captain-planet
	docker push oembot/captain-planet:latest
