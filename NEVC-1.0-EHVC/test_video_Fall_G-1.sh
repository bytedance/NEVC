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

python3 test.py \
--i_frame_model_path $1 \
--p_frame_model_path $2 \
--rate_num 4 \
--test_config ./cfg/dataset_config_rgb_allF_IP-1.json \
--yuv420 0 \
--cuda 1 \
--output_frame_RD 1 \
--worker 1 \
--write_stream 1 \
--output_path ./results_FallG-1.json \
--stream_path ./bitstreams/