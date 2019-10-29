SHELL := /bin/bash

venv:
	rm -rf ./venv; \
	python3 -m venv venv; \
	. venv/bin/activate

activate:
	. venv/bin/activate

install:
	. venv/bin/activate; \
	pip3 install -r requirements.txt

install-mirror:
	. venv/bin/activate; \
	pip3 install -r requirements.txt -i  https://mirrors.aliyun.com/pypi/simple

list:
	. venv/bin/activate; \
	pip3 list --format=columns

compile:
	mkdir build && cd build && mkdir contracts && cd ../; \
	cd contracts; \
	RUSTFLAGS="-C link-arg=-zstack-size=32768" cargo build --release --target wasm32-unknown-unknown; \
	cd target/wasm32-unknown-unknown/release; \
	ontio-wasm-build interplanetary_album_box.wasm interplanetary_album_box.wasm; \
	cp interplanetary_album_box.wasm ../../../../build/contracts/interplanetary_album_box.wasm; \
	cd ../../../; \
	rm -rf target/
