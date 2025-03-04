/*
Copyright (C) 2025 "IoT.bzh"
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package cmd

import (
	"bytes"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestRootCmd(t *testing.T) {
	cmd := NewRootCmd()
	buffer := new(bytes.Buffer)
	cmd.SetOut(buffer)
	err := cmd.Execute()
	assert.NoError(t, err)
	assert.Equal(t, "Hello World !\n", buffer.String())
}

func TestRootCmdWithArg(t *testing.T) {
	cmd := NewRootCmd()
	bufOut := new(bytes.Buffer)
	bufErr := new(bytes.Buffer)
	cmd.SetOut(bufOut)
	cmd.SetErr(bufErr)
	cmd.SetArgs([]string{"blabla", "ddd"})
	assert.Error(t, cmd.Execute())
	assert.Contains(t, bufOut.String(), "Usage:\n  hello [flags]\n\nFlags:\n  -h, --help")
	assert.Equal(t, "Error: no argument supported\n", bufErr.String())
}
