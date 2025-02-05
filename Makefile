###########################################################################
# Copyright (C) 2025 "IoT.bzh"
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###########################################################################

.PHONY: all
all: deps build

.PHONY: build
build:
	go build -v -o bin/helloworld-go .

.PHONY: deps
deps:
	go mod tidy

.PHONY: clean
clean:
	rm -rf bin

.PHONY: test
test:
	go test -v ./cmd/...

.PHONY: test.binary
test.binary:
	go test -v ./cmd/... -o bin/helloworld-go.test
