# Copyright (c) 2024 Microsoft Corporation.
# Copyright (c) 2025 ByteDance Ltd. and/or its affiliates.
#
# This file has been modified by ByteDance Ltd. and/or its affiliates. on 2025
#
# Original file was released under MIT License, with the full license text
# available at https://github.com/microsoft/DCVC/blob/main/LICENSE.txt.
#
# The modified part from ByteDance Ltd. and/or its affiliates. is released under the BSD 3-Clause Clear License.

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

import json
import os
from unittest.mock import patch

import numpy as np


def str2bool(v):
    return str(v).lower() in ("yes", "y", "true", "t", "1")


def scale_list_to_str(scales):
    s = ''
    for scale in scales:
        s += f'{scale:.2f} '

    return s


def create_folder(path, print_if_create=False):
    if not os.path.exists(path):
        os.makedirs(path)
        if print_if_create:
            print(f"created folder: {path}")


@patch('json.encoder.c_make_encoder', None)
def dump_json(obj, fid, float_digits=-1, **kwargs):
    of = json.encoder._make_iterencode  # pylint: disable=W0212

    def inner(*args, **kwargs):
        args = list(args)
        # fifth argument is float formater which we will replace
        args[4] = lambda o: format(o, '.%df' % float_digits)
        return of(*args, **kwargs)

    with patch('json.encoder._make_iterencode', wraps=inner):
        json.dump(obj, fid, **kwargs)


def generate_log_json(frame_num, frame_pixel_num, test_time, frame_types, bits, psnrs_rgb,psnrs_yuv, ssims_rgb,ssims_yuv,
                      psnrs_y=None, psnrs_u=None, psnrs_v=None,
                      ssims_y=None, ssims_u=None, ssims_v=None, verbose=False):
    include_yuv = psnrs_y is not None
    if include_yuv:
        assert psnrs_u is not None
        assert psnrs_v is not None
        assert ssims_y is not None
        assert ssims_u is not None
        assert ssims_v is not None
    i_bits = 0
    i_psnr_rgb = 0
    # Line 76 is modified by ByteDance
    i_psnr_yuv=0
    i_psnr_y = 0
    i_psnr_u = 0
    i_psnr_v = 0
    i_ssim_rgb = 0
    # Line 82 is modified by ByteDance
    i_ssim_yuv=0
    i_ssim_y = 0
    i_ssim_u = 0
    i_ssim_v = 0
    p_bits = 0
    p_psnr_rgb = 0
    # Line 89 is modified by ByteDance
    p_psnr_yuv=0
    p_psnr_y = 0
    p_psnr_u = 0
    p_psnr_v = 0
    p_ssim_rgb = 0
    # Line 95 is modified by ByteDance
    p_ssim_yuv=0
    p_ssim_y = 0
    p_ssim_u = 0
    p_ssim_v = 0
    i_num = 0
    p_num = 0
    for idx in range(frame_num):
        if frame_types[idx] == 0:
            i_bits += bits[idx]
            i_psnr_rgb += psnrs_rgb[idx]
            i_ssim_rgb += ssims_rgb[idx]
            i_num += 1
            if include_yuv:
                # Line 109 is modified by ByteDance
                i_psnr_yuv+=psnrs_yuv[idx]
                i_psnr_y += psnrs_y[idx]
                i_psnr_u += psnrs_u[idx]
                i_psnr_v += psnrs_v[idx]
                # Line 114 is modified by ByteDance
                i_ssim_yuv=+ssims_yuv[idx]
                i_ssim_y += ssims_y[idx]
                i_ssim_u += ssims_u[idx]
                i_ssim_v += ssims_v[idx]
        else:
            p_bits += bits[idx]
            p_psnr_rgb += psnrs_rgb[idx]
            p_ssim_rgb += ssims_rgb[idx]
            p_num += 1
            if include_yuv:
                # Line 125 is modified by ByteDance
                p_psnr_yuv += psnrs_yuv[idx]
                p_psnr_y   += psnrs_y[idx]
                p_psnr_u   += psnrs_u[idx]
                p_psnr_v   += psnrs_v[idx]
                # Line 130 is modified by ByteDance
                p_ssim_yuv += ssims_yuv[idx]
                p_ssim_y   += ssims_y[idx]
                p_ssim_u   += ssims_u[idx]
                p_ssim_v   += ssims_v[idx]

    log_result = {}
    log_result['frame_pixel_num'] = frame_pixel_num
    log_result['i_frame_num'] = i_num
    log_result['p_frame_num'] = p_num
    log_result['ave_i_frame_bpp'] = i_bits / i_num / frame_pixel_num
    log_result['ave_i_frame_psnr_rgb'] = i_psnr_rgb / i_num
    log_result['ave_i_frame_msssim_rgb'] = i_ssim_rgb / i_num
    if include_yuv:
        # Line 144 is modified by ByteDance
        log_result['ave_i_frame_psnr_yuv'] = i_psnr_yuv / i_num
        log_result['ave_i_frame_psnr_y'] = i_psnr_y / i_num
        log_result['ave_i_frame_psnr_u'] = i_psnr_u / i_num
        log_result['ave_i_frame_psnr_v'] = i_psnr_v / i_num
        # Line 149 is modified by ByteDance
        log_result['ave_i_frame_msssim'] = i_ssim_yuv / i_num
        log_result['ave_i_frame_msssim_y'] = i_ssim_y / i_num
        log_result['ave_i_frame_msssim_u'] = i_ssim_u / i_num
        log_result['ave_i_frame_msssim_v'] = i_ssim_v / i_num
    if verbose:
        log_result['frame_bpp'] = list(np.array(bits) / frame_pixel_num)
        log_result['frame_psnr_rgb'] = psnrs_rgb
        log_result['frame_msssim_rgb'] = ssims_rgb
        log_result['frame_type'] = frame_types
        if include_yuv:
            # Line 160 is modified by ByteDance
            log_result['frame_psnr_yuv'] = psnrs_yuv
            log_result['frame_psnr_y'] = psnrs_y
            log_result['frame_psnr_u'] = psnrs_u
            log_result['frame_psnr_v'] = psnrs_v
            # Line 165 is modified by ByteDance
            log_result['frame_msssim_yuv'] = ssims_yuv
            log_result['frame_msssim_y'] = ssims_y
            log_result['frame_msssim_u'] = ssims_u
            log_result['frame_msssim_v'] = ssims_v
    log_result['test_time'] = test_time
    if p_num > 0:
        total_p_pixel_num = p_num * frame_pixel_num
        log_result['ave_p_frame_bpp'] = p_bits / total_p_pixel_num
        log_result['ave_p_frame_psnr_rgb'] = p_psnr_rgb / p_num
        log_result['ave_p_frame_msssim_rgb'] = p_ssim_rgb / p_num
        if include_yuv:
            # Line 177 is modified by ByteDance
            log_result['ave_p_frame_psnr_yuv'] = p_psnr_yuv / p_num
            log_result['ave_p_frame_psnr_y'] = p_psnr_y / p_num
            log_result['ave_p_frame_psnr_u'] = p_psnr_u / p_num
            log_result['ave_p_frame_psnr_v'] = p_psnr_v / p_num
            # Line 182 is modified by ByteDance
            log_result['ave_p_frame_msssim_y'] = p_ssim_yuv / p_num
            log_result['ave_p_frame_msssim_y'] = p_ssim_y / p_num
            log_result['ave_p_frame_msssim_u'] = p_ssim_u / p_num
            log_result['ave_p_frame_msssim_v'] = p_ssim_v / p_num
    else:
        log_result['ave_p_frame_bpp'] = 0
        log_result['ave_p_frame_psnr_rgb'] = 0
        log_result['ave_p_frame_msssim_rgb'] = 0
        if include_yuv:
            # Line 192 is modified by ByteDance
            log_result['ave_p_frame_psnr_yuv'] = 0
            log_result['ave_p_frame_psnr_y'] = 0
            log_result['ave_p_frame_psnr_u'] = 0
            log_result['ave_p_frame_psnr_v'] = 0
            # Line 197 is modified by ByteDance
            log_result['ave_p_frame_msssim_yuv'] = 0
            log_result['ave_p_frame_msssim_y'] = 0
            log_result['ave_p_frame_msssim_u'] = 0
            log_result['ave_p_frame_msssim_v'] = 0
    log_result['ave_all_frame_bpp'] = (i_bits + p_bits) / (frame_num * frame_pixel_num)
    log_result['ave_all_frame_psnr_rgb'] = (i_psnr_rgb + p_psnr_rgb) / frame_num
    log_result['ave_all_frame_msssim_rgb'] = (i_ssim_rgb + p_ssim_rgb) / frame_num
    if include_yuv:
        # Line 206 is modified by ByteDance
        log_result['ave_all_frame_psnr_yuv'] = (i_psnr_yuv + p_psnr_yuv) / frame_num
        log_result['ave_all_frame_psnr_y'] = (i_psnr_y + p_psnr_y) / frame_num
        log_result['ave_all_frame_psnr_u'] = (i_psnr_u + p_psnr_u) / frame_num
        log_result['ave_all_frame_psnr_v'] = (i_psnr_v + p_psnr_v) / frame_num
        # Line 211 is modified by ByteDance
        log_result['ave_all_frame_msssim_yuv'] = (i_ssim_yuv + p_ssim_yuv) / frame_num
        log_result['ave_all_frame_msssim_y'] = (i_ssim_y + p_ssim_y) / frame_num
        log_result['ave_all_frame_msssim_u'] = (i_ssim_u + p_ssim_u) / frame_num
        log_result['ave_all_frame_msssim_v'] = (i_ssim_v + p_ssim_v) / frame_num

    return log_result