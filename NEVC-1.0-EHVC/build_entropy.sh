# Copyright 2025 ByteDance Ltd. and/or its affiliates.
# All rights reserved.
# Licensed under the BSD 3-Clause Clear License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://choosealicense.com/licenses/bsd-3-clause-clear/
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
cd src
mkdir build
cd build
cmake ../cpp -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/home/tiger/.pyenv/versions/3.11.2/bin/python3.11
make -j
cd ../../