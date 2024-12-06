# Copyright 2024 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io


class FakeHost:
    def __init__(self):
        self.stderr = io.StringIO()
        self.stdin = io.StringIO()
        self.stdout = io.StringIO()
        self.files = {}
        self.written_files = {}

    def exists(self, path):
        return path in self.files

    def make_executable(self, path):
        pass

    def print(self, *args, end='\n', file=None):
        file = file or self.stdout
        print(*args, end=end, file=file, flush=True)

    def read_text_file(self, path):
        return self.files[path]

    def splitext(self, path):
        return path.rsplit('.')

    def write_text_file(self, path, contents):
        self.files[path] = contents
        self.written_files[path] = contents
