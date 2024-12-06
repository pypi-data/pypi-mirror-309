# -*- coding:utf-8 -*-
import os
import sys
import shutil
import subprocess
import argparse
import copy
import pathlib
import redis
import fsspec
import boto3
import botocore
import tempfile
import shlex
from tqdm import tqdm
from tqdm.utils import _screen_shape_wrapper
import time
import platform
import pickle
import yaml
import glob
import random
import msgpack
import importlib
from PIL import Image
from functools import partial
import urllib.request
from warnings import simplefilter
from datetime import timedelta, datetime
from timeit import default_timer
from configobj import ConfigObj
from io import BytesIO
import io
import requests
import psutil
import hashlib
import imageio
import math
import h5py
import csv
import collections
import json
import json_lines
import numpy as np
import pandas as pd
import torch
import torchvision
import torchdata
import torch.nn as nn
from torch.optim import Adam
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.datapipes.datapipe import IterDataPipe
from torch.utils.data.datapipes.iter import IterableWrapper
from einops import rearrange, repeat
import torch.distributed as dist
from torchvision import datasets, transforms, utils
from torch.utils.tensorboard.writer import SummaryWriter
from itertools import cycle
import wandb
import safetensors
from contextlib import nullcontext
import cv2
import av
import uuid
import base64
import tarfile
import warnings
import traceback
from torchdata.datapipes.utils.common import validate_pathname_binary_tuple
from torchdata.datapipes.utils import StreamWrapper
from typing import cast
import webdataset as wds
import pdb
from io import BufferedIOBase, RawIOBase
import gc
import re
from PIL import ImageSequence
import threading
from collections import OrderedDict
from dataclasses import is_dataclass, dataclass, fields
from typing import Callable
torch.backends.cuda.matmul.allow_bf16_reduced_precision_reduction = False
# Disable transformers outputs weights.
simplefilter(action='ignore', category=FutureWarning)


from loguru import logger
logger.remove()  
logger.level('CHECK', 30, color='<cyan><bold>')
logger.add(
    sink=sys.stderr,
    format=f"<level>[{{time:YYYY-MM-DD HH:mm:ss.SSS}}] [{{level}} {int(os.environ.get('RANK', 0))}/{int(os.environ.get('WORLD_SIZE', 1))}] [{{file}}:{{line}}:{{function}}] {{message}}</level>",
    filter=lambda record: record["level"].name != "INFO" or int(os.environ.get('RANK', '0')) == 0
)
logger.info("Deep Learning Utils @ Chenfei Wu & Shengming Yin & Zekai Zhang & Kun Yan")


class ForkedPdb(pdb.Pdb):
    # 用法：ForkedPdb().set_trace()
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin

class extending_tqdm(tqdm):

    def __init__(self, *args, desc="", **kwargs):
        
        super().__init__(*args, **kwargs)
        self.subbar = None
        self.set_description(desc)
        

    def set_description(self, desc=None, refresh=True):

        screen_width, _ = _screen_shape_wrapper()(sys.stdout)
        max_len = screen_width
        if len(desc) > max_len*.7:
            if not self.subbar:
                self.subbar = extending_tqdm(range(len(self)))
                self.subbar.n = self.n
                self.default_bar_format = self.bar_format
                self.bar_format = "{desc}"
            
            super().set_description_str(desc=desc[:screen_width], refresh=refresh)
            self.subbar.set_description(desc[screen_width:])
        else:
            if self.subbar:
                self.bar_format = self.default_bar_format
                self.subbar.leave = False
                self.subbar.close()
            
            super().set_description(desc=desc, refresh=refresh)
        
        
    def update(self, n=1):
        if self.subbar:
            self.subbar.update(n)
            self.last_print_n = self.subbar.last_print_n
            self.n = self.subbar.n
        else:
            super().update(n)

    def close(self):
        if self.subbar:
            self.subbar.leave = self.leave
            self.subbar.close()
        
        super().close()

def path_join(path, *paths):
    output = os.path.join(path, *paths).replace('\\', '/')
    return output


class Timer:
    def __init__(self):
        '''
        t = Timer()
        time.sleep(1)
        print(t.elapse())
        '''
        self.start = default_timer()

    def elapse(self, readable=False):
        seconds = default_timer() - self.start
        if readable:
            seconds = str(timedelta(seconds=seconds))
        return seconds

def get_timestr(precision='second', timezone='Asia/Shanghai'):  # zecheng note: 这里修改成北京时间，而不是世界时间
    import pytz
    tz_beijing = pytz.timezone(timezone)
    now_beijing = datetime.now(tz_beijing)

    if precision == 'second':
        timestr = now_beijing.strftime('%Y%m%d%H%M%S')
    elif precision == 'hour':
        timestr = now_beijing.strftime('%Y%m%d%H')
    elif precision == 'day':
        timestr = now_beijing.strftime('%Y%m%d')
    else:
        raise ValueError(f'precision must be second or day, but got {precision}')
    return timestr

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        logger.info('%s function took %0.3f ms' %
                    (f.__name__, (time2 - time1) * 1000.0))
        return ret
    return wrap

def identity(x):
    return x


def groupby(l, key=lambda x: x):
    d = collections.defaultdict(list)
    for item in l:
        d[key(item)].append(item)
    return dict(d.items())

def sliding_window(l, n):
    return [l[i:i+n] for i in range(len(l) - n + 1)]

def chunk_list(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def list_filenames(dirname, filter_fn=None, sort_fn=None, printable=True, fsspec_config=None):
    if dirname.startswith('s3://'):
        if not fsspec_config:
            raise ValueError("晨飞错误！要写s3路径，请直接加fsspec_config参数，不要用aws配置文件！")
        fs = fsspec.filesystem('s3', **fsspec_config)
        filename_list = fs.listdir(dirname, refresh=True)
        filenames = [os.path.join("s3://",filename['Key']) for filename in filename_list]
    else:
        dirname = os.path.abspath(dirname)
        filenames = os.listdir(dirname)
        filenames = [path_join(dirname, filename) for filename in filenames]
    if filter_fn:
        tmp = len(filenames)
        if printable:
            logger.info('Start filtering files in %s by %s.' %
                        (dirname, filter_fn))
        filenames = [e for e in filenames if filter_fn(e)]
        if printable:
            logger.info(
                'Detected %s files/dirs in %s, filtering to %s files.' % (tmp, dirname, len(filenames)))
    else:
        if printable:
            logger.info('Detected %s files/dirs in %s, No filtering.' %
                        (len(filenames), dirname))
    if sort_fn:
        filenames = sorted(filenames, key=sort_fn)

    return filenames


def listdict2dict2list(listdict, printable=True):
    tmp_dict = collections.defaultdict(list)
    for example_dict in listdict:
        for k, v in example_dict.items():
            tmp_dict[k].append(v)
    if printable:
        logger.info('%s' % tmp_dict.keys())
    return dict(tmp_dict)


def split_filename(filename):
    if filename.startswith('s3://'):
        absname = filename
    else:
        absname = os.path.abspath(filename)
    dirname, basename = os.path.split(absname)
    split_tmp = basename.rsplit('.', maxsplit=1)
    if len(split_tmp) == 2:
        rootname, extname = split_tmp
    elif len(split_tmp) == 1:
        rootname = split_tmp[0]
        extname = None
    else:
        raise ValueError("programming error!")
    dirname = dirname.replace('\\', '/')
    return dirname, rootname, extname


def add_suffix(file_or_dir, suffix):
    if file_or_dir.startswith('s3://'):
        if file_or_dir.endswith('/'):
            file_or_dir = file_or_dir[:-1]
    else:
        file_or_dir = os.path.abspath(file_or_dir)
    dirname, rootname, extname = split_filename(file_or_dir)
    ext_str = f".{extname}" if extname else ""
    new_file_or_dir = path_join(dirname, f"{rootname}{suffix}{ext_str}")
    return new_file_or_dir


def get_suffix(file_path):
    try:
        return os.path.splitext(file_path)[-1]
    except:
        raise ValueError(f"file_path:{file_path} error!")

def random_str(length=8):
    return uuid.uuid4().hex[:length]

def data2file_fsspec(data, filename, type=None, override=False, printable=False, **kwargs):
    # 请在kwargs中指定fsspec_config参数，示例如下：
    # fsspec_config = {'key':"AKLTxxxxxx",
    #                   'secret':"WVdVMUxxxxxx",
    #                   'endpoint_url':"https://tos-s3-cn-beijing2.ivolces.com",
    #                   'config_kwargs':{"s3": {"addressing_style": "virtual"}}}
    # data2file(["1","2"], filename, fsspec_config=fsspec_config)


    if 'fsspec_config' in kwargs:
        fsspec_config = kwargs.pop('fsspec_config')
    else:
        # fsspec_config = {}
        raise ValueError("晨飞错误！要写s3路径，请直接加fsspec_config参数，不要用aws配置文件！")

    dirname, rootname, extname = split_filename(filename)
    print_did_not_save_flag = True
    if type:
        extname = type
 
    if not path_exists(filename, fsspec_config=fsspec_config) or override:
        if extname == 'pkl':
            with fsspec.open(filename, 'wb', **fsspec_config) as f:
                pickle.dump(data, f)
        elif extname == 'msg':
            with fsspec.open(filename, 'wb', **fsspec_config) as f:
                msgpack.dump(data, f)
        elif extname == 'hy':
            # hy support 2 params: key and max_step
            # if key, then create group using key, else create group using index
            # if max_step, then the loop may early stopping, used for debug
            # Remove filename since h5py may corrupt.
            if override:
                remove_filename(filename)
            key_str = kwargs.pop('key_str', None)
            topk = kwargs.pop('topk', None)

            with h5py.File(filename, 'w') as f:
                for i, datum in enumerate(tqdm(data)):
                    if key_str:
                        grp = f.create_group(name=datum[key_str])
                    else:
                        grp = f.create_group(name=str(i))
                    for k in datum.keys():
                        grp[k] = datum[k]
                    if topk is not None and i + 1 == topk:
                        break
        elif extname == 'csv':
            with fsspec.open(filename, 'w', **fsspec_config) as f:
                writer = csv.writer(f)
                writer.writerows(data)
        elif extname == 'json':
            with fsspec.open(filename, 'w', **fsspec_config) as f:
                json.dump(data, f, ensure_ascii=False)
        elif extname == 'npy':
            with fsspec.open(filename, 'wb', **fsspec_config) as f:
                np.save(f, data)
        elif extname in ['jpg', 'png', 'jpeg']:
            with fsspec.open(filename, 'wb', **fsspec_config) as f:
                pil = Image.fromarray(data.astype('uint8'), 'RGB')
                pil.save(f, extname)
        elif extname == 'gif':
            with fsspec.open(filename, 'wb', **fsspec_config) as f:
                imageio.mimsave(f, data, format='GIF', duration=kwargs.get('duration', 1/24), loop=0, quality=kwargs.get('quality', 5))
        elif extname == 'pth' or extname == 'pt':
            with fsspec.open(filename, 'wb', **fsspec_config) as f:
                torch.save(data, f)
        elif extname == 'txt':
            if isinstance(data, list):
                pass
            elif isinstance(data, str):
                data = [data]
            else:
                raise ValueError('Unsupported data type %s' % type(data))
            if kwargs is None:
                kwargs = {}
            max_step = kwargs.get('max_step')
            if max_step is None:
                max_step = np.Infinity

            with fsspec.open(filename, 'w', encoding='utf-8', **fsspec_config) as f:
                for i, e in enumerate(data):
                    if i < max_step:
                        f.write(str(e) + '\n')
                    else:
                        break
        elif extname == 'mp4':
            fps = kwargs.get('fps', 24)
            with fsspec.open(filename, 'wb', **fsspec_config) as f:
                imageio.mimsave(f, data, format=pathlib.Path(filename).suffix, fps=fps, quality=kwargs.get('quality', 5))
        elif extname == 'html':
            with fsspec.open(filename, 'w', **fsspec_config) as f:
                f.write(data)
        else:
            raise ValueError(f'Unsupported {filename} with ext: {extname}')
        if printable:
            logger.info('Saved data to %s' % os.path.abspath(filename))
    else:
        if print_did_not_save_flag:
            logger.info(
                'Did not save data to %s because file exists and override is False' % os.path.abspath(
                    filename))



def data2file(data, filename, type=None, override=False, printable=False, **kwargs):
    if filename.startswith('s3://'):
        return data2file_fsspec(data, filename, type, override, printable, **kwargs)
    dirname, rootname, extname = split_filename(filename)
    print_did_not_save_flag = True
    if type:
        extname = type
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)

    if not os.path.exists(filename) or override:
        if extname == 'pkl':
            with open(filename, 'wb') as f:
                pickle.dump(data, f)
        elif extname == 'msg':
            with open(filename, 'wb') as f:
                msgpack.dump(data, f)
        elif extname == 'hy':
            # hy support 2 params: key and max_step
            # if key, then create group using key, else create group using index
            # if max_step, then the loop may early stopping, used for debug
            # Remove filename since h5py may corrupt.
            if override:
                remove_filename(filename)
            key_str = kwargs.pop('key_str', None)
            topk = kwargs.pop('topk', None)

            with h5py.File(filename, 'w') as f:
                for i, datum in enumerate(tqdm(data)):
                    if key_str:
                        grp = f.create_group(name=datum[key_str])
                    else:
                        grp = f.create_group(name=str(i))
                    for k in datum.keys():
                        grp[k] = datum[k]
                    if topk is not None and i + 1 == topk:
                        break
        elif extname == 'csv':
            with open(filename, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(data)
        elif extname == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
        elif extname == 'npy':
            np.save(filename, data)
        elif extname in ['jpg', 'png', 'jpeg']:
            # utils.save_image(data, filename, **kwargs)
            arr2image(data, filename)
        elif extname == 'gif':
            imageio.mimsave(filename, data, format='GIF', duration=kwargs.get('duration'), loop=0, quality=kwargs.get('quality', 5))
        elif extname == 'pth' or extname == 'pt':
            torch.save(data, filename)
        elif extname == 'txt':
            if isinstance(data, list):
                pass
            elif isinstance(data, str):
                data = [data]
            else:
                raise ValueError('Unsupported data type %s' % type(data))
            if kwargs is None:
                kwargs = {}
            max_step = kwargs.get('max_step')
            if max_step is None:
                max_step = np.Infinity

            with open(filename, 'w', encoding='utf-8') as f:
                for i, e in enumerate(data):
                    if i < max_step:
                        f.write(str(e) + '\n')
                    else:
                        break
        elif extname == 'mp4':
             fps = kwargs.get('fps', 24)
             imageio.mimsave(filename, data, format=pathlib.Path(filename).suffix, fps=fps, quality=kwargs.get('quality', 5))
        elif extname == 'html':
            with open(filename, 'w') as f:
                f.write(data)      
        else:
            raise ValueError(f'Unsupported {filename} with ext: {extname}')
        if printable:
            logger.info('Saved data to %s' % os.path.abspath(filename))
    else:
        if print_did_not_save_flag:
            logger.info(
                'Did not save data to %s because file exists and override is False' % os.path.abspath(
                    filename))


def file2data(filename, type=None, printable=True, **kwargs):
    if isinstance(filename, str):
        dirname, rootname, extname = split_filename(filename)
        cache_filename = filename
        if filename.startswith('s3://'):
            if 'fsspec_config' in kwargs:
                fsspec_config = kwargs.pop('fsspec_config')
            else:
                # fsspec_config = {}
                raise ValueError("晨飞错误！要写s3路径，请直接加fsspec_config参数，不要用aws配置文件！")   
                
            with fsspec.open(filename, 'rb', **fsspec_config) as f:
                filename = BytesIO(f.read())
    elif isinstance(filename, bytes):
        filename = BytesIO(filename)
        cache_filename = 'bytes_Filename'
    elif isinstance(filename, BytesIO):
        cache_filename = 'BytesIO_Filename'
    elif isinstance(filename, StreamWrapper):
        cache_filename = filename.name
        _, _, extname = split_filename(cache_filename)
    else:
        raise ValueError(f'Not supported filename isinstance {type(filename)}')
    if type:
        extname = type
    if not extname:
        extname = 'b'
        if printable: logger.critical(f'Auto extname b for {filename}')
    if extname == 'pkl':
        if isinstance(filename, BytesIO):
            data = pickle.load(filename)
        else:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
    elif extname == 'msg':
        with open(filename, 'rb') as f:
            data = msgpack.load(f, encoding="utf-8")
    elif extname == 'csv':
        data = pd.read_csv(filename)
    elif extname == 'hy':
        data = h5py.File(filename, 'r')
    elif extname in ['npy', 'npz']:
        try:
            data = np.load(filename, allow_pickle=True)
        except UnicodeError:
            logger.warning(
                '%s is python2 format, auto use latin1 encoding.' % os.path.abspath(cache_filename))
            data = np.load(filename, encoding='latin1', allow_pickle=True)
    elif extname == 'json':
        if isinstance(filename, BytesIO):
            try:
                data = json.load(filename)
            except json.decoder.JSONDecodeError as e:
                raise ValueError(
                    '[error] utils.file2data: failed to load json file %s' % cache_filename)
        elif isinstance(filename, StreamWrapper):
            try:
                data = json.loads(filename.read())
            except json.decoder.JSONDecodeError as e:
                raise ValueError(
                    '[error] utils.file2data: failed to load json file %s' % filename)
        else:
            with open(filename) as f:
                try:
                    data = json.load(f)
                except json.decoder.JSONDecodeError as e:
                    raise ValueError(
                        '[error] utils.file2data: failed to load json file %s' % cache_filename)
    elif extname == 'gif':
        gif = Image.open(filename)
        lst = []
        for frame in ImageSequence.Iterator(gif):
            frame_arr = np.array(frame.convert('RGB'))
            lst.append(frame_arr)
        return np.stack(lst)
    elif extname in ['png', 'jpg']:
        return image2arr(filename, **kwargs)
    elif extname == 'mp4':
        return video2arr(filename, **kwargs)
    elif extname == 'jsonl':
        with open(filename, 'rb') as f:
            data = [json.loads(e.decode('utf-8')) for e in f.readlines()]
    elif extname == 'ini':
        data = ConfigObj(filename, encoding='utf-8')
    elif extname in ['pth', 'ckpt', 'pt']:
        data = torch.load(filename, map_location=kwargs.get('map_location'))
    elif extname == 'txt':
        top = kwargs.get('top', None)
        encoding = kwargs.get('encoding', 'utf-8')
        if isinstance(filename, BytesIO):
            f = io.TextIOWrapper(filename, encoding=encoding)
            if top:
                data = [next(f) for _ in range(top)]
            else:
                data = [e.strip() for e in f if e]
        else:
            with open(filename, encoding=encoding) as f:
                if top:
                    data = [f.readline() for _ in range(top)]
                else:
                    data = [e for e in f.read().split('\n') if e]

    elif extname == 'yaml':
        with open(filename, 'r') as f:
            data = yaml.load(f)
    elif extname == "safetensors":
        if isinstance(filename, BytesIO):
            data = safetensors.torch.load(filename.read())
        else:
            checkpoint = {}
            with safetensors.safe_open(filename, framework="pt", device="cpu") as f:
                for key in f.keys():
                    checkpoint[key] = f.get_tensor(key)
            data = checkpoint
    elif extname == 'b':
        if isinstance(filename, io.BytesIO):
            data = filename.getvalue()
        else:
            with open(filename, 'rb') as f:
                data = f.read()
    else:
        raise ValueError(f'Unsupported {cache_filename} with ext: {extname}')
    if printable:
        if cache_filename.startswith('s3://'):
            logger.info('Loaded data from %s' % cache_filename)
        else:
            logger.info('Loaded data from %s' % os.path.abspath(cache_filename))
    return data


def path_exists(filename, fsspec_config=None):
    if filename.startswith('s3://'):
        if fsspec_config:
            fs = fsspec.filesystem('s3', **fsspec_config)
            return fs.exists(filename)
        else:
            raise ValueError("晨飞错误！要写s3路径，请直接加fsspec_config参数，不要用aws配置文件！")   
    else:
        return os.path.exists(filename)

def download_file(fileurl, filedir=None, progress_bar=True, override=False, fast=False, printable=True):
    if filedir:
        ensure_dirname(filedir)
        assert os.path.isdir(filedir)
    else:
        filedir = ''
    filename = os.path.abspath(os.path.join(filedir, fileurl.split('/')[-1]))
    # print(filename)
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        logger.info("%s not exist, automatic makedir." % dirname)
    if not os.path.exists(filename) or override:
        if fast:
            p = subprocess.Popen('axel -n 10 -o {0} {1}'.format(filename, fileurl), shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in iter(p.stdout.readline, ''):
                if line:
                    logger.info(line.decode('utf-8').replace('\n', ''))
                else:
                    p.kill()
                    break
        else:
            if progress_bar:
                def my_hook(t):
                    last_b = [0]

                    def inner(b=1, bsize=1, tsize=None):
                        if tsize is not None:
                            t.total = tsize
                        t.update((b - last_b[0]) * bsize)
                        last_b[0] = b

                    return inner

                with tqdm(unit='B', unit_scale=True, miniters=1,
                          desc=fileurl.split('/')[-1]) as t:
                    urllib.request.urlretrieve(fileurl, filename=filename,
                                               reporthook=my_hook(t), data=None)
            else:
                urllib.request.urlretrieve(fileurl, filename=filename)
        if printable:
            logger.info("%s downloaded sucessfully." % filename)
    else:
        if printable:
            logger.info("%s already existed" % filename)
    return filename


def copy_file(filename, targetname, override=False, printable=True):
    filename = os.path.abspath(filename)
    targetname = os.path.abspath(targetname)
    if not os.path.exists(targetname) or override:
        shutil.copy2(filename, targetname)
        if printable:
            logger.info('Copied %s to %s.' % (filename, targetname))
    else:
        if printable:
            logger.info('Did not copy because %s exists.' % targetname)


def ensure_dirname(dirname, override=False, printable=True):
    if dirname.startswith('s3://'):
        if printable: logger.warning(f"{dirname} is s3 dir, No ensure operation required.")
        return

    if os.path.exists(dirname) and override:
        if printable: logger.info('Removing dirname: %s' % os.path.abspath(dirname))
        try:
            shutil.rmtree(dirname)
        except OSError as e:
            raise ValueError('Failed to delete %s because %s' % (dirname, e))

    if not os.path.exists(dirname):
        if printable: logger.info('Making dirname: %s' % os.path.abspath(dirname))
        os.makedirs(dirname, exist_ok=True)


def ensure_filename(filename, override=False):
    if filename.startswith('s3://'):
        logger.warning(f"{filename} is s3 dir, No ensure operation required.")
        return

    dirname, rootname, extname = split_filename(filename)
    ensure_dirname(dirname, override=False)
    if os.path.exists(filename) and override:
        os.remove(filename)
        logger.info('Deleted filename %s' % filename)


def remove_filename(filename, printable=False):
    if os.path.isfile(filename) or os.path.islink(filename):
        os.remove(filename)
        if printable:
            logger.info('Deleted file %s.' % filename)
    elif os.path.isdir(filename):
        shutil.rmtree(filename)
        if printable:
            logger.info('Deleted dir %s.' % filename)
    else:
        raise ValueError("%s is not a file or dir." % filename)


def execute(cmd, wait=True, printable=True):
    if wait:
        if printable:
            logger.warning('Executing: '"%s"', waiting...' % cmd)
        try:
            output = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            logger.warning(e.output)
            output = None
            # sys.exit(-1)

        return output
    else:
        if platform.system() == 'Windows':
            black_hole = 'NUL'
        elif platform.system() == 'Linux':
            black_hole = '/dev/null'
        else:
            raise ValueError('Unsupported system %s' % platform.system())
        cmd = cmd + ' 1>%s 2>&1' % black_hole
        if printable:
            logger.info('Executing: '"%s"', not wait.' % cmd)
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)


def execute_cmd(cmd, input_data=None):
    process = subprocess.Popen(shlex.split(
        cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate(input=input_data)
    retcode = process.poll()
    if retcode:
        raise ValueError(err.decode('utf-8'))
    return out

def run_thread(threaded_function, *args, **kwargs):
    logger.warning('Running thread: %s' % threaded_function.__name__)
    thread = threading.Thread(target=threaded_function, args=args, kwargs=kwargs)
    thread.start()

def import_filename(filename, name="mymodule"):
    spec = importlib.util.spec_from_file_location(name, filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def pname2pid(str_proc_name):
    map_proc_info = {}
    for proc in psutil.process_iter():
        if proc.name() == str_proc_name:
            map_proc_info[proc.pid] = str_proc_name

    return map_proc_info


def get_parameters(net: torch.nn.Module) -> int:
    return sum(p.numel() for p in net.parameters() if p.requires_grad)


def adaptively_load_state_dict(target, state_dict, print_common_dict=False, ignore_prefixs=None, printable=True):
    # target: 被载入的模型的weight
    # state_dict: pretrained 的 weight文件
    target_dict = target.state_dict()
    
    if ignore_prefixs is not None:
        for ig_p in ignore_prefixs:
            state_dict = {
                k:v for k,v in state_dict.items() if not k.startswith(ig_p)
            }

    try:
        common_dict = {k: v for k, v in state_dict.items(
        ) if k in target_dict and v.size() == target_dict[k].size()}
    except Exception as e:
        if printable:
            logger.warning('load error %s', e)
            logger.warning(str(state_dict.keys()))
        common_dict = {k: v for k, v in state_dict.items() if k in target_dict}

    if 'param_groups' in common_dict and common_dict['param_groups'][0]['params'] != \
            target.state_dict()['param_groups'][0]['params']:
        if printable:
            logger.warning(
                'Detected mismatch params, auto adapte state_dict to current')
        common_dict['param_groups'][0]['params'] = target.state_dict()[
            'param_groups'][0]['params']
    target_dict.update(common_dict)
    target.load_state_dict(target_dict)

    missing_keys = [k for k in target_dict.keys() if k not in common_dict]
    unexpected_keys = [k for k in state_dict.keys() if k not in common_dict]

    if printable and int(os.getenv('RANK', '-1')) in [0, 1, -1]:
        if len(unexpected_keys) != 0:
            logger.warning(
                f"{len(unexpected_keys)} Weights in pretrained model, Not used in your model: {unexpected_keys}"
            )
        if len(missing_keys) != 0:
            logger.warning(
                f"{len(missing_keys)} Weights in your model, Not used in pretrained model: {missing_keys}"
            )
        if len(common_dict) != 0 and print_common_dict:
            logger.warning(
                f"{len(common_dict)} Weights in your model and pretrained model, successfully loaded: {list(common_dict.keys())}"
            )
        if len(unexpected_keys) == 0 and len(missing_keys) == 0:
            logger.warning("Strictly Loaded state_dict.")

def from_pretrained(model, pretrained_model):
    if hasattr(model, "module"):
        raise ValueError(
            "Please do not load pretrained models into wrapped models, ensure self.models is CPU.")
    if os.path.isdir(pretrained_model):
        logger.warning('Pretrained Model is a dir, will load the model later')
        return None
    if isinstance(pretrained_model, str):
        logger.warning('Loading Pretrained Model Path: %s...' %
                        pretrained_model)
        pretrained_dict = file2data(pretrained_model, map_location='cpu')
        if 'models' in pretrained_dict:
            pretrained_dict = pretrained_dict['models']
        if 'model' in pretrained_dict:
            pretrained_dict = pretrained_dict['model']
        if 'module' in pretrained_dict:
            pretrained_dict = pretrained_dict['module']
    else:
        logger.warning('Loading Given Pretrained Dict...')
        pretrained_dict = pretrained_model
    adaptively_load_state_dict(model, pretrained_dict, printable=True)


class Meter(object):
    def __init__(self):
        self.val = None
        self.avg = None
        self.sum = None
        self.count = None

    def update(self, val, n=1):
        if isinstance(val, torch.Tensor):
            val = val.item()
        if isinstance(val, (int, float)):
            self.val = val
            if self.sum:
                self.sum += val * n
            else:
                self.sum = val * n
            if self.count:
                self.count += n
            else:
                self.count = n
            self.avg = self.sum / self.count
        elif isinstance(val, dict):
            for k, v in val.items():
                if isinstance(v, torch.Tensor):
                    val[k] = v.item()
            if self.val:
                for k in val.keys():
                    self.val[k] = val[k]
            else:
                self.val = val
            if self.sum:
                for k in val.keys():
                    if k in self.sum:
                        self.sum[k] = self.sum[k] + val[k] * n
                    else:
                        self.sum[k] = val[k] * n
            else:
                self.sum = {k: val[k] * n for k in val.keys()}
            if self.count:
                for k in val.keys():
                    if k in self.count:
                        self.count[k] = self.count[k] + n
                    else:
                        self.count[k] = n
            else:
                self.count = {k: n for k in val.keys()}
            self.avg = {k: self.sum[k] / self.count[k]
                        for k in self.count.keys()}
        else:
            raise ValueError('Not supported type %s' % type(val))

    def __str__(self):
        if isinstance(self.avg, dict):
            outputs = {}
            for k, v in self.avg.items():
                if 'lr' in k:
                    outputs[k] = '%.3e' % v
                else:
                    outputs[k] = '%.4f' % v
            return str(outputs)
        else:
            return 'Nan'

    
def set_seed(seed=123, deterministic=False):
    random.seed(seed)
    os.environ['PYHTONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    if deterministic:
        torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def namespace_to_dict(namespace):
    return {
        k: namespace_to_dict(v) if isinstance(v, argparse.Namespace) else v
        for k, v in vars(namespace).items()
    }

def generate_run_id(exp_name):
    # https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits
    return str(int(hashlib.sha256(exp_name.encode('utf-8')).hexdigest(), 16) % 10 ** 8)

def initialize_wandb(args, exp_name, project_name):
    config_dict = namespace_to_dict(args)
    wandb.init(
        project=project_name,
        name=exp_name,
        config=config_dict,
        id=generate_run_id(exp_name),
        resume="allow",
    )
def log_wandb(stats, step=None):
    wandb.log({k: v for k, v in stats.items()}, step=step)

class TrainerDistributed:
    def __init__(self, args, model, optimizers=None, scheduler=None):
        # Basic Params
        self.args = args
        self.log_dir = args.log_dir
        self.model = model
        self.optimizers = optimizers
        self.scheduler = scheduler
        self.rank = int(os.getenv('RANK', '-1'))
        self.local_rank = int(os.getenv('LOCAL_RANK', '-1'))
        self.enable_write = (self.rank == 0)
        if self.enable_write:
            ensure_dirname(os.path.join(self.log_dir, 'log'), override=False)
            if self.args.enable_tb:
                self.writer = SummaryWriter(log_dir=os.path.join(self.log_dir, "log"))
            if self.args.enable_wandb:
                project_name, exp_name = os.path.abspath(self.log_dir).split('/')[-2:]
                exp_name = exp_name + '_' + get_timestr()
                initialize_wandb(self.args, exp_name=exp_name, project_name=project_name)
        self.global_step = 0
        self.n_gpu = torch.cuda.device_count()

    def save_fn(self, inputs, outputs):
        args = self.args
        pred_path = os.path.join(args.eval_dir, 'pred')
        ensure_dirname(pred_path, printable=False)
        dl = {**inputs, **outputs}
        ld = dl2ld(dl)

        for idx, sample in enumerate(ld):
            if 'txt' in sample:
                basename = ''.join([e.lower().capitalize() for e in re.sub('[^a-zA-Z]', ' ', sample['txt']).split(' ') if e][:4]) + '_' + random_str()
            else:
                basename = random_str()
            try:
                for k, v in sample.items():
                    if 'mp4' in k:
                        if isinstance(v, torch.Tensor):
                            assert v.dim() == 4 and v.size(1) == 3 # [L, c, h, w]
                            sample[k] = tensor2arr(sample[k], tensor_range=(-1, 1), permute=(0, 2, 3, 1))
                        elif isinstance(v, np.ndarray): # [L, h, w, c]
                            assert v.ndim == 4 and v.shape[3] == 3
                        data2file(sample[k], os.path.join(pred_path, f'{basename}.{k}'), printable=False, override=True,fsspec_config=args.fsspec_config)
                    elif 'png' in k:
                        if isinstance(v, torch.Tensor):
                            assert v.dim() == 3 and v.size(0) == 3 # [c, h, w]
                            sample[k] = tensor2arr(sample[k], tensor_range=(-1, 1), permute=(1, 2, 0))
                        elif isinstance(v, np.ndarray): # [h, w, c]
                            assert v.ndim == 3 and v.shape[2] == 3
                        data2file(sample[k], os.path.join(pred_path, f'{basename}.{k}'), printable=False, override=True,fsspec_config=args.fsspec_config)
                    elif 'pth' in k or 'txt' in k:
                        data2file(sample[k], os.path.join(pred_path, f'{basename}.{k}'), printable=False, override=True,fsspec_config=args.fsspec_config)
                    else:
                        pass
            except Exception as e:
                warn_and_continue_debug(f'Error happened when saving: {e}')    

    def reduce_mean(self, tensor):
        rt = tensor.clone()
        size = int(os.environ['WORLD_SIZE'])
        dist.all_reduce(rt, op=dist.ReduceOp.SUM)
        rt = rt / size
        return rt

    def wrap_model(self):
        if hasattr(self.model, 'module'):
            raise ValueError('You do not need to wrap a models with modules.')

        self.device = torch.device("cuda", self.local_rank)
        self.model.to(self.device)
        self.model = torch.nn.parallel.DistributedDataParallel(
            self.model, device_ids=[self.local_rank],
            output_device=self.local_rank,
            find_unused_parameters=getattr(self.args, "find_unused_parameters", True))

        # wrap_optimizers
        if self.optimizers:
            for i in range(len(self.optimizers)):
                self.optimizers[i].load_state_dict(
                    complex_to_device(self.optimizers[i].state_dict(), device=self.device))
                
    def check_outputs(self, outputs):
        error_message = 'Model output must be a dict. The key must be "class_subclass" format.' \
                        ' "class" can only be loss, metric, or logits. "subclass" should be a string.' \
                        ' But got an unexpected key %s'
        loss_total_list = [
            e for e in outputs.keys() if e.startswith('loss_total')]
        if not loss_total_list:
            raise ValueError(
                'Model output must contain a key startswith "loss_total"!')

    def train(self, train_loader):
        # 准备训练参数
        total_steps = getattr(self.args, 'total_steps', 10000000)
        resume = getattr(self.args, 'resume', True)
        save_step = getattr(self.args, 'save_step', 20)
        resume_idx = getattr(self.args, 'resume_ckpt', -1) # -1表示最后一个，其余表示对应checkpoint
        ltbs = getattr(self.args, 'ltbs', 1) #默认local train batch size为 1
        max_norm = getattr(self.args, 'max_norm', None)
        gradient_accumulate_steps = getattr(self.args, 'gradient_accumulate_steps', 1)

        if resume:
            self.load_checkpoint_for_resume(checkpoint_id=resume_idx)
        else:
            logger.warning('Dangerous! You set resume=False. Auto cleaning all the logs under %s' % self.log_dir)
            ensure_dirname(self.log_dir, override=True)
        self.wrap_model()
        logger.warning(f'Train total steps: {total_steps}, local_train_batch_size(ltbs): {ltbs}.')
        # Train phase
        self.save_settings(setting_dir=self.args.log_dir)
        self.model.train()
        train_meter = Meter()
        if self.enable_write:
            pbar = tqdm(total = total_steps)
            pbar.update(self.global_step)

        for step, inputs in enumerate(train_loader):
            if self.global_step >= total_steps:
                break
            self.global_step += 1
            for optimizer_idx in range(len(self.optimizers)):
                if not getattr(self.optimizers[optimizer_idx], 'is_enabled', lambda x: True)(self.global_step):
                    continue  # adjust to sdm KL-VAE

                with torch.autocast(device_type='cuda', dtype=torch.bfloat16, enabled=getattr(self.args, 'bf16', False)):
                    inputs = complex_to_device(inputs, self.device)
                    inputs['global_step'] = self.global_step
                    inputs['optimizer_idx'] = optimizer_idx
                    outputs = self.model(inputs)
                    self.check_outputs(outputs)

                if optimizer_idx == 0:
                    outputs['loss_total'].backward()
                else:
                    outputs['loss_total_%s' % optimizer_idx].backward()

                if (step + 1) % gradient_accumulate_steps == 0:
                    if max_norm:
                        nn.utils.clip_grad_norm_(
                            self.model.parameters(), max_norm)
                    self.optimizers[optimizer_idx].step()
                    self.optimizers[optimizer_idx].zero_grad()
                outputs[f'lr_{optimizer_idx}'] = self.optimizers[optimizer_idx].param_groups[0]['lr']
                metric_and_loss = {k: v for k, v in outputs.items() if k.split('_')[
                    0] in ['loss','lr']}
                for k, v in metric_and_loss.items():
                    if k.split('_')[0] in ['loss']:
                        metric_and_loss[k] = self.reduce_mean(v) 

                if self.enable_write:
                    if self.args.enable_tb:
                        for k, v in metric_and_loss.items():
                            if isinstance(v, torch.Tensor):
                                self.writer.add_scalar(k, v.float(), self.global_step)
                            else:
                                self.writer.add_scalar(k, v, self.global_step)
                    if self.args.enable_wandb:
                        wandb.log(metric_and_loss, step=self.global_step)

                train_meter.update(metric_and_loss)

                if self.scheduler:
                    self.scheduler.step()

            if self.global_step % save_step == 0 and self.enable_write:
                self.save_checkpoint(os.path.join(self.log_dir, str(self.global_step) + '.pth'))
            #     if self.args.enable_wandb:
            #         if 'logits_imgs' in outputs:
            #             video_logits = outputs['logits_imgs'][0]
            #             if video_logits.shape[1] > 3:
            #                 video_logits = rearrange(video_logits, 'c n ... -> n c ...')
            #             video_to_log = np.asarray([transforms.ToPILImage('RGB')(utils.make_grid(e.cpu(), normalize=True, value_range=(-1, 1))) for e in video_logits])
            #             video_to_log = video_to_log.transpose(0, 3, 1, 2)
            #             video_to_log = (video_to_log * 255).astype(np.uint8) 
            #             wandb.log({"video": wandb.Video(video_to_log, fps=4, format="gif")}, step=self.global_step)
            if self.enable_write:
                pbar.set_description("Metering:" + str(train_meter))
                pbar.update(1)

    def eval(self, eval_loader):
        self.wrap_model()
        self.save_settings(setting_dir=self.args.eval_dir)
        # TODO Note that eval_fn supports ddp. So we do not need to unwrap things here.
        model_to_eval = self.model
        model_to_eval.eval()
        with torch.no_grad():
            is_enable_bf16 = getattr(self.args, 'bf16', False)
            if is_enable_bf16:
                logger.warning('bf16 evaluation is enabled.')
                torch.backends.cuda.matmul.allow_bf16_reduced_precision_reduction = False
            else:
                logger.warning('bf16 is not enabled.')
            with torch.autocast(device_type='cuda', dtype=torch.bfloat16, enabled=is_enable_bf16):
                for inputs in tqdm(eval_loader):
                    inputs = complex_to_device(inputs, self.device)
                    outputs = model_to_eval(inputs)
                    self.save_fn(inputs, outputs)

    def load_checkpoint(self, checkpoint_filename):
        if hasattr(self.model, "module"):
            raise ValueError(
                "Please do not load checkpoint into wrapped models, ensure self.models is CPU.")
        checkpoint = file2data(checkpoint_filename, map_location='cpu')
        adaptively_load_state_dict(self.model, checkpoint['models'], ignore_prefixs = getattr(self.args, "resume_ignore_prefixs", None))
        if self.optimizers:
            if len(self.optimizers) > 1:
                for i, optimizer in enumerate(self.optimizers):
                    if isinstance(checkpoint['optimizer'], list) and i < len(checkpoint['optimizer']):
                        adaptively_load_state_dict(
                            self.optimizers[i], checkpoint['optimizer'][i])

            elif len(self.optimizers) == 1:
                adaptively_load_state_dict(
                    self.optimizers[0], checkpoint['optimizer'])

            else:
                raise ValueError
        if self.scheduler:
            adaptively_load_state_dict(self.scheduler, checkpoint['scheduler'])

        self.global_step = checkpoint['global_step']

        # IMPORTANT! The models will be wrapped automatically.
        logger.warning('Loaded checkpoint %s of global_step %s' %
                       (checkpoint_filename, checkpoint['global_step']))

    def load_checkpoint_for_resume(self, checkpoint_id=-1):
        if checkpoint_id == -1: 
            #载入最后一个checkpoint
            glob_filenames = glob.glob(os.path.join(self.log_dir, '*.pth'))
            if len(glob_filenames) == 0:
                logger.warning(f'No checkpoint found in {self.log_dir}, did not resume. This may happen during your first time train from scratch.')
            else:
                last_checkpoint_filename = sorted(glob_filenames,key=lambda x: x.split('/')[-1].split('.')[0].isnumeric()
                                            and int(x.split('/')[-1].split('.')[0]))[-1]
                self.load_checkpoint(last_checkpoint_filename)
                logger.warning(f'Resume from the last checkpoint {last_checkpoint_filename}.')
        else: 
            #载入特定的checkpoint
            specified_checkpoint_filename = os.path.join(self.log_dir, str(checkpoint_id) + '.pth')
            if not os.path.exists(specified_checkpoint_filename):
                raise ValueError(f"The specified checkpoint {specified_checkpoint_filename} does not exist.")
            else:
                self.load_checkpoint(specified_checkpoint_filename)
                logger.warning(f'Resume from the specified checkpoint {specified_checkpoint_filename}.')

    def save_checkpoint(self, checkpoint_filename):
        model_to_save = self.model.module if hasattr(
            self.model, 'module') else self.model
        if len(self.optimizers) > 1:
            optimizer_to_save = [optimizer.state_dict()
                                 for optimizer in self.optimizers]
        elif len(self.optimizers) == 1:
            optimizer_to_save = self.optimizers[0].state_dict()
        else:
            raise ValueError
        checkpoint = {
            'models': model_to_save.state_dict(),
            'optimizer': optimizer_to_save,
            'global_step': self.global_step,
        }
        if self.scheduler:
            checkpoint['scheduler'] = self.scheduler.state_dict()
        data2file(checkpoint, checkpoint_filename, override=True)
        logger.warning('Saved global_step %s to %s.' %
                       (checkpoint['global_step'], checkpoint_filename))

    def save_settings(self, setting_dir):
        # setting_dir: 
        if self.enable_write:
            ensure_dirname(setting_dir)
            setting_filename = os.path.join(setting_dir, f'settings{get_timestr()}.json')
            # Save Model Setting
            type_output = [int, float, str, bool, tuple, dict, type(None), ]
            setting_dict = {item: getattr(self.args, item) for item in dir(self.args) if
                            type(getattr(self.args, item)) in type_output and not item.startswith('__')}
            setting_dict['entry_cmd'] = ' '.join(sys.argv)
            data2file(setting_dict, setting_filename, fsspec_config=self.args.fsspec_config)
        
class TrainerDeepSpeed(TrainerDistributed):

    # def __init__(self, args, **kwargs):
    #     super(TrainerDeepSpeed, self).__init__(args, **kwargs)
    #     from deepspeed.utils.zero_to_fp32 import convert_zero_checkpoint_to_fp32_state_dict
    #     self.convert_zero_checkpoint_to_fp32_state_dict = convert_zero_checkpoint_to_fp32_state_dict

    def train(self, train_loader):
        # 准备训练参数
        total_steps = getattr(self.args, 'total_steps', 10000000)
        resume = getattr(self.args, 'resume', True)
        save_step = getattr(self.args, 'save_step', 20)
        resume_idx = getattr(self.args, 'resume_ckpt', -1) # -1表示最后一个，其余表示对应checkpoint
        ltbs = getattr(self.args, 'ltbs', 1) #默认local train batch size为 1
        if resume:
            self.load_checkpoint_for_resume(checkpoint_id=resume_idx)
        else:
            logger.warning('Dangerous! You set resume=False. Auto cleaning all the logs under %s' % self.log_dir)
            ensure_dirname(self.log_dir, override=True)
        # 注意，deepspeed不需要wrap model
        logger.warning(f'Train total steps: {total_steps}, local_train_batch_size(ltbs): {ltbs}.')
        # Train phase
        self.save_settings(setting_dir=self.args.log_dir)
        self.model.train()
        train_meter = Meter()
        if self.enable_write:
            pbar = tqdm(total = total_steps)
            pbar.update(self.global_step)

        for step, inputs in enumerate(train_loader):
            if self.global_step >= total_steps:
                break
            self.global_step += 1
            inputs = complex_to_device(inputs, self.model.device)
            inputs['global_step'] = self.global_step

            outputs = self.model(inputs)
            self.check_outputs(outputs)
            
            self.model.backward(outputs['loss_total'])
            loss_max = outputs['loss_total'].detach().clone()
            dist.all_reduce(loss_max, op=dist.ReduceOp.MAX)
            dist.all_reduce(outputs['loss_total'], op=dist.ReduceOp.AVG)
            loss_drop_thresh = getattr(self.args, 'loss_drop_thresh', 3)
            if loss_max > loss_drop_thresh:
                if self.enable_write:
                    logger.warning('Loss too large, skip this step')
                    with open(os.path.join(self.args.log_dir, 'loss_drop.txt'), 'a') as f:
                        f.write(f'{self.global_step}\n')
                for param_name, param in self.model.module.named_parameters():
                    if param.grad is not None:
                        param.grad.detach_()
                        param.grad.zero_()

            if outputs['loss_total'] != outputs['loss_total']:
                if self.enable_write:
                    logger.warning('Loss is nan, skip this step')
                    with open(os.path.join(self.args.log_dir, 'loss_nan_drop.txt'), 'a') as f:
                        f.write(f'{self.global_step}\n')
                for param_name, param in self.model.module.named_parameters():
                    if param.grad is not None:
                        param.grad.detach_()
                        param.grad.zero_()
            if getattr(self.args, 'find_nan_in_grad', False):
                nan_in_grad = False
                for param_name, param in self.model.module.named_parameters():
                    if param.grad is not None:
                        if torch.isnan(param.grad).any():
                            nan_in_grad = True
                            break
                print(f"Nan in Grad: {nan_in_grad}")
                if nan_in_grad:
                    if self.enable_write:
                        logger.warning('Grad is nan, skip this step')
                        with open(os.path.join(self.args.log_dir, 'loss_nan_drop.txt'), 'a') as f:
                            f.write(f'{self.global_step}\n')
                    for param_name, param in self.model.module.named_parameters():
                        if param.grad is not None:
                            param.grad.detach_()
                            param.grad.zero_() 
                        
            self.model.step()
            
            grad_norm = self.model.get_global_grad_norm()
            if isinstance(grad_norm, torch.Tensor):
                grad_norm = grad_norm.item()
            outputs[f'lr'] = self.optimizers[0].param_groups[0]['lr']
            metric_and_loss = {k: v for k, v in outputs.items() if k.split('_')[0] in ['loss', 'lr']}
            metric_and_loss['grad_norm'] = grad_norm
            metric_and_loss['loss_max'] = loss_max
            # deepspeed automatically reduce mean
            # for k, v in metric_and_loss.items():
            #     metric_and_loss[k] = self.reduce_mean(v)

            if self.enable_write:
                if self.args.enable_tb:
                    for k, v in metric_and_loss.items():
                        if isinstance(v, torch.Tensor):
                            self.writer.add_scalar(k, v.float(), self.global_step)
                        else:
                            self.writer.add_scalar(k, v, self.global_step)
                if self.args.enable_wandb:
                    wandb.log(metric_and_loss, step=self.global_step)

            train_meter.update(metric_and_loss)

            # if self.scheduler:
            #     self.scheduler.step()

            if self.global_step % save_step == 0:
                # if self.enable_write: # multinode sync to save checkpoint,
                self.save_checkpoint(str(self.global_step))
            if self.enable_write:
                pbar.set_description("Metering:" + str(train_meter))
                pbar.update(1)

    def eval(self, eval_loader):
        logger.warning(f'Start evaluating, eval_dir is {eval_loader}')
        self.save_settings(setting_dir=self.args.eval_dir)
        model_to_eval = self.model
        model_to_eval.eval()
        # total = self.args.max_eval_samples if self.args.max_eval_samples else 100
        with torch.no_grad():
            for inputs in tqdm(eval_loader):
                inputs = complex_to_device(inputs, self.model.device)
                outputs = model_to_eval(inputs)
                self.save_fn(inputs, outputs)




    def load_checkpoint_for_resume(self, checkpoint_id=-1):
        try:
            if checkpoint_id == -1: 
                #载入最后一个checkpoint
                _, client_sd = self.model.load_checkpoint(self.log_dir)  # automatically load latest checkpoint
                self.global_step = client_sd['global_step']
                logger.warning('Loaded latest checkpoint of global_step %s' %(client_sd['global_step']))
            else: 
                _, client_sd = self.model.load_checkpoint(self.log_dir, checkpoint_id)
                self.global_step = client_sd['global_step']
                logger.warning('Loaded checkpoint %s of global_step %s' % (os.path.join(self.log_dir, checkpoint_id), client_sd['global_step']))
        except Exception as e:
            logger.warning(f'Dit not load checkpoint because of {e}, Train from scratch.')

    def save_checkpoint(self, checkpoint_id):
        client_sd = {}
        client_sd = {
            'global_step': self.global_step,
        }
        ### DeepSpeed can automatically save and restore the model, optimizer, and the learning rate scheduler states
        self.model.save_checkpoint(self.log_dir, checkpoint_id, client_state=client_sd)
        # run_thread(self.convert_zero_checkpoint_to_fp32_state_dict, checkpoint_dir=self.log_dir, output_file=os.path.join(self.log_dir, f"{str(checkpoint_id)}.pth"), tag=str(checkpoint_id))
        logger.warning('Saved global_step %s to %s.' %(client_sd['global_step'], os.path.join(self.log_dir, checkpoint_id)))

def dl2ld(dl):
    return [dict(zip(dl, e)) for e in zip(*dl.values())]


def ld2dl(ld):
    return {k: [dic[k] for dic in ld] for k in ld[0]}


def complex_to_device(complex, device, non_blocking=False):
    if isinstance(complex, torch.Tensor):
        return complex.to(device, non_blocking=non_blocking)
    elif isinstance(complex, dict):
        return {k: complex_to_device(v, device, non_blocking=non_blocking) for k, v in complex.items()}
    elif isinstance(complex, list) or isinstance(complex, tuple):
        return [complex_to_device(e, device, non_blocking=non_blocking) for e in complex]
    elif isinstance(complex, str) or isinstance(complex, bytes) or \
            isinstance(complex, int) or isinstance(complex, float):
        return complex
    elif complex is None:
        return complex
    else:
        raise ValueError('Unsupported complex', complex)


'''
=====================================================================================================================
                                            Sync With Blob
=====================================================================================================================
'''


def azsync(path, local_rootdir, remote_rootdir='https://chenfei.blob.core.windows.net/data/'):
    if not local_rootdir:
        raise ValueError(
            'local_root_dir must be specified, i.e., /workspace/f_ndata')
        # r'D:\f_ndata' or /workspace/f_ndata
    else:
        local_rootdir = os.path.abspath(local_rootdir)
        print('Local Root Dir is %s' % local_rootdir)

    if path.startswith('https:'):
        local_path = None
        remote_path = path
    else:
        local_path = path
        remote_path = None
        if not os.path.exists(local_path):
            raise ValueError(
                f'The local_path {local_path} you specified does not exist or you have no permission!')

    if not os.environ.get('SAS'):
        raise ValueError('You must specify SAS as environment variable manually before using azsync.\n'
                         'Ask Chenfei Wu for this SAS')
    else:
        SAS = os.environ.get('SAS')
        # print("SAS is: ", SAS)

    if remote_path:
        if remote_path.startswith('https:'):
            target_remote_path = remote_path
        else:
            target_remote_path = os.path.join(remote_rootdir, remote_path)
        relative_path = target_remote_path.replace(remote_rootdir, "")
        target_local_path = os.path.join(local_rootdir, relative_path)
        if pathlib.Path(target_local_path).suffix:
            print('Detected file transfer R->L')
            method = "cp"
            if not os.path.exists(target_local_path):
                print('target_local_path: %s' % target_local_path)
                os.makedirs(os.path.dirname(target_local_path), exist_ok=True)

        else:
            print('Detected dir transfer R->L.')
            method = "sync"
            if not os.path.exists(target_local_path):
                os.makedirs(target_local_path, exist_ok=True)
        cmd = f'azcopy {method} {target_remote_path}"{SAS}" "{target_local_path}"'
        print(f'cmd is {cmd}')
        with subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                print(line, end='')

    if local_path:
        target_local_path = os.path.abspath(local_path)
        relative_path = os.path.relpath(target_local_path, local_rootdir)
        target_remote_path = os.path.join(
            remote_rootdir, relative_path).replace('\\', '/')
        if pathlib.Path(target_local_path).suffix:
            print('Detected file transfer L->R.')
            method = "copy"
        else:
            print('Detected dir transfer L->R.')
            method = "sync"
        cmd = f'azcopy {method} "{target_local_path}" {target_remote_path}"{SAS}"'
        print(f'cmd is {cmd}')
        with subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                print(line, end='')


class RedisDict:
    def __init__(self, type='dict'):
        if platform.system() == 'Windows':
            execute_path = 'redis-server.exe'
        elif platform.system() == 'Linux':
            execute_path = 'redis-server'
        else:
            raise ValueError('Not supported system.')
        pid = pname2pid(execute_path)
        if not pid:
            logger.warning('Cannot find pid, auto start redis-server...')
            tmp_dir = tempfile.TemporaryDirectory().name
            stdout_filename = os.path.join(
                tmp_dir, 'stdout.txt').replace('\\', '\\\\')
            config_filename = os.path.join(
                tmp_dir, 'redis.conf').replace('\\', '\\\\')
            config_content = '''
            daemonize yes\npidfile /var/run/redis.pid\nport 6379\ntimeout 0\nloglevel notice\ndatabases 16
            logfile %s\ndir %s
            save ""\nstop-writes-on-bgsave-error yes\nrdbcompression yes\nrdbchecksum yes\ndbfilename dump.rdb
            slave-serve-stale-data yes\nslave-read-only yes\nslave-priority 100\nappendonly no\nappendfsync everysec
            no-appendfsync-on-rewrite no\nauto-aof-rewrite-percentage 100\nauto-aof-rewrite-min-size 64mb\nlua-time-limit 5000
            slowlog-log-slower-than 10000\nslowlog-max-len 128\nhash-max-ziplist-entries 512\nhash-max-ziplist-value 64
            list-max-ziplist-entries 512\nlist-max-ziplist-value 64\nset-max-intset-entries 512\nzset-max-ziplist-entries 128
            zset-max-ziplist-value 64\nactiverehashing yes\nclient-output-buffer-limit normal 0 0 0
            client-output-buffer-limit slave 256mb 64mb 60\nclient-output-buffer-limit pubsub 32mb 8mb 60
            ''' % (stdout_filename, tmp_dir)
            data2file([e.strip() for e in config_content.split('\n')],
                      config_filename, type='txt', override=True)
            execute('%s %s' % (execute_path, config_filename),
                    wait=False, printable=True)
            time.sleep(3)
            pid = pname2pid(execute_path)
            if pid:
                logger.info(
                    'Successfully started redis-server, dirname is %s, pid is %s.' % (tmp_dir, pid))
            else:
                raise ValueError(
                    'Redis-server failed to start. Try sudo apt install redis-server')

        else:
            logger.info('Redis-server already started, pid is %s.' % pid)
        self.db = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.type = type

    def __setitem__(self, key, value):
        if isinstance(value, np.ndarray):
            value = value.tobytes()
        if isinstance(value, dict):
            value = pickle.dumps(value)
        if isinstance(value, str):
            value = value
        else:
            raise ValueError(f'Not supported type {type(value)}')
        self.db.set(key, value)

    def __getitem__(self, key):
        value = self.db.get(key)
        if self.type == 'dict':
            return pickle.loads(value)
        elif self.type == 'arr':
            return np.frombuffer(value)
        elif self.type == 'str':
            return value
        else:
            raise ValueError(f'Not supported type {self.type}')


    def __contains__(self, item):
        # return item.encode() in self.keys()
        return self.db.exists(item.encode())

    def __len__(self):
        return self.db.dbsize()

    def keys(self):
        return set(self.db.keys())


'''
=====================================================================================================================
                                            Common Transformations
=====================================================================================================================
'''


def npy2object(filename):
    try:
        data = np.load(filename, allow_pickle=True)
    except UnicodeError:
        logger.warning('%s is python2 format, auto use latin1 encoding.' %
                       os.path.abspath(filename))
        data = np.load(filename, encoding='latin1', allow_pickle=True)
    return data


def video2bytes(input_video):
    if isinstance(input_video, str) and input_video.startswith("s3://"):
        f = fsspec.open(input_video, 'rb')
    else:
        f = open(input_video, 'rb')
    data = f.read()
    f.close()
    return data


def video2meta(input_video, fsspec_config=None):
    if isinstance(input_video, str):
        if input_video.startswith("s3://"):
            if fsspec_config:
                with fsspec.open(input_video, 'rb', **fsspec_config) as f:
                    input_bytes = f.read()
                    return video2meta(input_bytes)
            else:
                raise ValueError("晨飞错误！要写s3路径，请直接加fsspec_config参数，不要用aws配置文件！")   
        else:
            out = execute_cmd(
                'ffprobe -i "%s" -print_format json -show_format -show_streams' % input_video)
    elif isinstance(input_video, bytes):
        out = execute_cmd(
            f'ffprobe -i pipe: -print_format json -show_streams', input_data=input_video)
    else:
        raise ValueError('Note supported input_video type %s' %
                         type(input_video))
    meta = json.loads(out.decode('utf-8'))
    try:
        res = {'width': meta['streams'][0]['width'],
            'height': meta['streams'][0]['height'],
            # 'duration': eval(meta['format']['duration']),
            'duration': eval(meta['streams'][0]['duration']),
            'fps': eval(meta['streams'][0]['r_frame_rate'])}
    except Exception as e:
        res = {'width': meta['streams'][0]['width'],
            'height': meta['streams'][0]['height'],
            'duration': eval(meta['format']['duration']),
            # 'duration': eval(meta['streams'][0]['duration']),
            'fps': eval(meta['streams'][0]['r_frame_rate'])}
    return res


def video2arr(input_video, start = None, span = None, whence='frame', fsspec_config=None):
    # 晨飞注：大家都使用这个新实现，支持快速seek，支持时间或帧选取
    if isinstance(input_video, str):
        if input_video.startswith("s3://"):
            if fsspec_config:
                with fsspec.open(input_video, 'rb', **fsspec_config) as f:
                    input_video = BytesIO(f.read())
            else:
                raise ValueError("晨飞错误！要写s3路径，请直接加fsspec_config参数，不要用aws配置文件！")   
    elif isinstance(input_video, bytes):
        input_video = BytesIO(input_video)
    elif isinstance(input_video, BytesIO):
        pass
    else:
        raise ValueError("Not supported input_video type %s" % type(input_video))

    container = av.open(input_video, mode='r')
    video_stream = container.streams.video[0]
    framerate = float(video_stream.guessed_rate)

    if not start: # start is None or start == 0
        decoder = container.decode(video_stream)
        if span:
            span_frame = span if whence == 'frame' else int(span * framerate)
        else:
            span_frame = np.Infinity
    else:
        time_base = container.streams.video[0].time_base 
        end = start + span
        if whence == 'frame':
            start_time, end_time = start / framerate, end / framerate
            start_frame, end_frame, span_frame = start, end, end-start
        elif whence == 'time':
            start_time, end_time = start, end
            start_frame, end_frame, span_frame = int(start * framerate), int(end * framerate), int((end-start) * framerate)
        else:
            raise ValueError(f"Invalid whence: {whence}")

        if container.format.variable_fps:
            start_pts = round(start_time / time_base)
            container.seek(start_pts, stream=video_stream)
            decoder = container.decode(video_stream)
        else:  # Automatic fast skip-seek by Chenfei
            start_frame = int (start_time * framerate)
            pts_delta = 1 / framerate / video_stream.time_base
            index_pts = int(start_frame * pts_delta)
            container.seek(index_pts, stream=video_stream)
            decoder = container.decode(video_stream)
            keyframe = next(decoder)
            container.seek(index_pts, stream=video_stream)
            frames_to_yield = start_frame - int(int(keyframe.pts * keyframe.time_base / time_base) / pts_delta)
            for _ in range(frames_to_yield):
                next(decoder)

    frames = []
    for i, frame in enumerate(decoder):
        if i >= span_frame:
            break
        frame_rgb24 = frame.to_ndarray(format='rgb24')
        frames.append(frame_rgb24)
    if not frames:
        raise ValueError(f"Empty video: {input_video}")
    video = np.array(frames)
    return video




def video2arr_opencv(video_path, fps=None):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
    if not fps:
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        video_array = np.array(frames)
        cap.release()
    else:
        ori_fps = cap.get(cv2.CAP_PROP_FPS)
        frames = []
        frame_count = 0
        cur_step = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if cur_step*fps/ori_fps > frame_count:
                frame_count += 1
                frames.append(frame)
            cur_step += 1
        #     frames.append(frame)
        # frame_indices = np.arange(0, len(frames)-1, step=ori_fps/fps)
        # frame_indices = np.ceil(frame_indices).astype(int)
        # video_array = np.array(frames)[frame_indices]
        video_array = np.array(frames)
        cap.release()
    return video_array

def arr2video(arr, filename, fps, quality=5, fsspec_config=None):
    if filename.startswith("s3://"):
        if not fsspec_config:
            raise ValueError("晨飞错误！要写s3路径，请直接加fsspec_config参数，不要用aws配置文件！")   
        with fsspec.open(filename, 'wb', **fsspec_config) as f:
            imageio.mimsave(f, arr, format=pathlib.Path(filename).suffix, fps=fps, quality=quality)
    else:
        imageio.mimsave(filename, arr, format=pathlib.Path(filename).suffix, fps=fps, quality=quality)



def pil2image(pil, filename):
    pil.save(filename)


def gif2arr(filename):
    gif = Image.open(filename)
    lst = []
    for frame in ImageSequence.Iterator(gif):
        frame_arr = np.array(frame.convert('RGB'))
        lst.append(frame_arr)
    return np.stack(lst)

def arr2image(arr, filename, fsspec_config=None):
    pil = arr2pil(arr)
    if filename.startswith("s3://"):
        if not fsspec_config:
            raise ValueError("晨飞错误！要写s3路径，请直接加fsspec_config参数，不要用aws配置文件！") 
        else:
            with fsspec.open(filename, 'wb', **fsspec_config) as f:
                pil.save(f, 'png')
    else:
        pil.save(filename)


def arr2gridimage(arr, filename, nrow=4):
    if arr.ndim != 4:
        raise ValueError("arr must has ndim of 4")
    torchvision.utils.save_image([transforms.ToTensor()(
        frame) for frame in arr], filename, nrow=nrow)


def image2pil(filename):
    return Image.open(filename)


def image2arr(filename, fsspec_config=None):
    if isinstance(filename, str):
        if filename.startswith("s3://"):
            if not fsspec_config:
                raise ValueError("晨飞错误！要写s3路径，请直接加fsspec_config参数，不要用aws配置文件！") 
            else:
                with fsspec.open(filename, 'rb', **fsspec_config) as f:
                    filename = BytesIO(f.read())
    elif isinstance(filename, bytes):
        filename = BytesIO(filename)
    elif isinstance(filename, BytesIO):
        pass
    else:
        raise ValueError("Not supported filename type %s" % type(filename))
    pil = image2pil(filename).convert('RGB')
    return pil2arr(pil)


# 格式转换
def pil2arr(pil):
    if isinstance(pil, list):
        arr = np.array(
            [np.array(e.convert('RGB').getdata(), dtype=np.uint8).reshape(e.size[1], e.size[0], 3) for e in pil])
    else:
        arr = np.array(pil)
    return arr

def arr2pil(arr):
    if arr.ndim == 3:
        return Image.fromarray(arr.astype('uint8'), 'RGB')
    elif arr.ndim == 4:
        return [Image.fromarray(e.astype('uint8'), 'RGB') for e in list(arr)]
    else:
        raise ValueError('arr must has ndim of 3 or 4, but got %s' % arr.ndim)

def tensor2arr(tensor, tensor_range=(-1, 1), permute=(0,2,3,1)):
    # 默认认为tensor为L, C, H, W, Permute为 L, H, W, C，方法为(0,2,3,1)
    # 或者tensor为C, H, W, Permute为 H, W, C，方法为(1,2,0)
    tensor = tensor.to('cpu').detach().float()
    if permute:
        tensor = tensor.permute(*permute)
    min_value, max_value = tensor_range
    tensor = tensor.clamp(min_value, max_value)

    scale_factor = 255 / (max_value - min_value) # 127.5
    scaled_tensor = (tensor - min_value) * scale_factor
    arr = scaled_tensor.numpy().astype(np.uint8)
    return arr

def arr2tensor(arr, tensor_range=(-1, 1), permute=(0,3,1,2)):
    tensor = torch.tensor(arr).float()
    if permute:
        tensor = tensor.permute(*permute)
    min_value, max_value = tensor_range
    output_tensor = (max_value-min_value)*tensor/255+min_value
    return output_tensor

def resize_and_crop_video_tensor(video_tensor, target_height, target_width, random=True):
    # video_tensor必须是 L, C, H, W
    # 如果是video2arr读出来的arr，建议torch.tensor(sample_arr).permute(0, 3, 1, 2)
    length, channel, height, width,  = video_tensor.size()
    if channel != 3:
        raise ValueError(f"Tensor should be L, C, H, W, but got {video_tensor.size()}")
    if target_height / height > target_width / width: # 嫌长
        resized_height = target_height
        resized_width = int(width * target_height / height)
        crop_top = 0
        if random:
            crop_left = np.random.randint(0, resized_width - target_width + 1)
        else:
            crop_left = (resized_width - target_width) // 2
    else:  # 嫌高
        resized_width = target_width
        resized_height = int(height * target_width / width)
        crop_left = 0
        if random:
            crop_top = np.random.randint(0, resized_height - target_height + 1)
        else:
            crop_top = (resized_height - target_height) // 2
    resize_crop_transform = transforms.Compose([
        transforms.Resize((resized_height, resized_width)),
        lambda x: transforms.functional.crop(x, crop_top, crop_left, target_height, target_width),
    ])
    resize_crop_frames = torch.stack([resize_crop_transform(frame) for frame in video_tensor], dim=0)

    return resize_crop_frames

def resize_and_crop_video(input_video, target_height, target_width, random=True):
    if isinstance(input_video, torch.Tensor):
        assert input_video.dim() == 4 and input_video.size(1) == 3 # [L, 3, H, W]
        video_tensor = input_video
    elif isinstance(input_video, np.ndarray):
        assert input_video.ndim == 4 and input_video.shape[3] == 3 # [L, H, W, 3]
        video_tensor = torch.tensor(input_video).permute(0, 3, 1, 2)
    else:
        raise ValueError("input_video must be np.ndarray or torch.Tensor")        
    length, channel, height, width = video_tensor.size()
    if target_height / height > target_width / width: # 嫌长
        resized_height = target_height
        resized_width = int(width * target_height / height)
        crop_top = 0
        if random:
            crop_left = np.random.randint(0, resized_width - target_width + 1)
        else:
            crop_left = (resized_width - target_width) // 2
    else:  # 嫌高
        resized_width = target_width
        resized_height = int(height * target_width / width)
        crop_left = 0
        if random:
            crop_top = np.random.randint(0, resized_height - target_height + 1)
        else:
            crop_top = (resized_height - target_height) // 2
    resize_crop_transform = transforms.Compose([
        transforms.Resize((resized_height, resized_width)),
        lambda x: transforms.functional.crop(x, crop_top, crop_left, target_height, target_width),
    ])
    resize_crop_frames = torch.stack([resize_crop_transform(frame) for frame in video_tensor], dim=0)
    if isinstance(input_video, np.ndarray):
        resize_crop_frames = resize_crop_frames.permute(0, 2, 3, 1).numpy()
    return resize_crop_frames

def resize_and_crop_image(input_image, target_height, target_width, random=True):
    if isinstance(input_image, torch.Tensor):
        assert input_image.dim() == 3 and input_image.size(0) == 3 # [3, H, W]
        image_tensor = input_video
    elif isinstance(input_image, np.ndarray):
        assert input_image.ndim == 3 and input_image.shape[2] == 3 # [H, W, 3]
        image_tensor = torch.tensor(input_image).permute(2, 0, 1)
    else:
        raise ValueError("input_image must be np.ndarray or torch.Tensor")    

    channel, height, width  = image_tensor.size()
    if target_height / height > target_width / width: # 嫌长
        resized_height = target_height
        resized_width = int(width * target_height / height)
        crop_top = 0
        if random:
            crop_left = np.random.randint(0, resized_width - target_width + 1)
        else:
            crop_left = (resized_width - target_width) // 2
    else:  # 嫌高
        resized_width = target_width
        resized_height = int(height * target_width / width)
        crop_left = 0
        if random:
            crop_top = np.random.randint(0, resized_height - target_height + 1)
        else:
            crop_top = (resized_height - target_height) // 2
    resize_crop_transform = transforms.Compose([
        transforms.Resize((resized_height, resized_width)),
        lambda x: transforms.functional.crop(x, crop_top, crop_left, target_height, target_width),
    ])
    resize_crop_frames = resize_crop_transform(image_tensor)
    if isinstance(input_image, np.ndarray):
        resize_crop_frames = resize_crop_frames.permute(1, 2, 0).numpy()
    return resize_crop_frames

def resize_and_crop_image_tensor(image_tensor, target_height, target_width, random=True):
    # video_tensor必须是 L, C, H, W
    # 如果是video2arr读出来的arr，建议torch.tensor(sample_arr).permute(0, 3, 1, 2)
    channel, height, width,  = image_tensor.size()
    if channel != 3:
        raise ValueError(f"Tensor should be L, C, H, W, but got {image_tensor.size()}")
    if target_height / height > target_width / width: # 嫌长
        resized_height = target_height
        resized_width = int(width * target_height / height)
        crop_top = 0
        if random:
            crop_left = np.random.randint(0, resized_width - target_width + 1)
        else:
            crop_left = (resized_width - target_width) // 2
    else:  # 嫌高
        resized_width = target_width
        resized_height = int(height * target_width / width)
        crop_left = 0
        if random:
            crop_top = np.random.randint(0, resized_height - target_height + 1)
        else:
            crop_top = (resized_height - target_height) // 2
    resize_crop_transform = transforms.Compose([
        transforms.Resize((resized_height, resized_width)),
        lambda x: transforms.functional.crop(x, crop_top, crop_left, target_height, target_width),
    ])
    resize_crop_frames = resize_crop_transform(image_tensor)
    return resize_crop_frames



'''
=====================================================================================================================
                                            Debugs
=====================================================================================================================
'''


def compare(x, y, threshold=1e-2):
    def _get_compare(data):
        added = []
        def add_compare(data):
            if isinstance(data, list):
                for x in data:
                    add_compare(x)
            elif isinstance(data, dict) or isinstance(data, OrderedDict):
                for k, v in data.items():
                    add_compare(v)
            elif isinstance(data, set):
                for item in data:
                    add_compare(item)
            elif is_dataclass(data):
                for field in fields(data):
                    value = getattr(data, field.name)
                    add_compare(value)
            elif isinstance(data, tuple):
                for item in data:
                    add_compare(item)
            elif isinstance(data, str):
                pass
            elif isinstance(data, torch.Tensor):
                added.append(data)
            elif isinstance(data, np.ndarray):
                pass
            elif data is None:
                pass
            elif isinstance(data, (int, float)):
                added.append(data)
            else:
                pass
        add_compare(data)
        return added

    compare_x = _get_compare(x)
    compare_y = _get_compare(y)
    # 比较数值个数：
    if not len(compare_x) == len(compare_y):
        logger.critial(f'x has {len(compare_x)} values but y has {len(compare_y)} values!')
    else:
        # 如果个数相同，就分别比较数值是否接近
        for i in range(len(compare_x)):
            res = torch.allclose(compare_x[i], compare_y[i], atol=threshold, rtol=threshold)
            logger.warning(res)


def compare_tensor(x, mgt_x, k=50):
    difference = mgt_x - x
    abs_difference = torch.abs(difference)
    flat_abs_diff = abs_difference.flatten()
    top_50_indices = torch.topk(flat_abs_diff, k).indices
    original_indices = [torch.unravel_index(idx, abs_difference.shape) for idx in top_50_indices]
    original_values = [x[idx].item() for idx in original_indices]
    original_mgt_values = [mgt_x[idx].item() for idx in original_indices]
    differences_at_indices = [difference[idx].item() for idx in original_indices]

    for i, (diff, v, mgt_v) in enumerate(zip(differences_at_indices, original_values, original_mgt_values)):
        logger.info(f"Diff:{diff}, X: {v}, MGT_X:{mgt_v}, Ratio: {abs(diff)/v*100}%")



'''
=====================================================================================================================
                                            Jupyter Notebooks
=====================================================================================================================
'''


# def notebook_show(*images):
#     from IPython.display import Image
#     from IPython.display import display
#     display(*[Image(e) for e in images])


def show_video(video, fps=24, message=None):
    from IPython.display import Video
    from IPython.display import display
    from IPython.core.display import HTML
    if isinstance(video, str):
        if message:
            display(HTML(f'<div>{message}</div>'),Video(video))
        else:
            display(Video(video))
        return video
    elif isinstance(video, np.ndarray):
        video_arr = video
        L, h, w, c = video_arr.shape
        if c != 3:
            raise ValueError(f"video_arr should be [l, h, w, c], but got shape: {video_arr.shape}")

        tmp_filename = os.path.abspath(os.path.join('tmp',random_str() + '.mp4'))
        ensure_filename(tmp_filename)
        arr2video(video_arr, tmp_filename, fps=fps)
        print(f"Video size is {video_arr.shape}, Saving to {tmp_filename}")
        if message:
            display(HTML(f'<div>{message}</div>'),Video(tmp_filename))
        else:
            display(Video(tmp_filename))
    else:
        raise ValueError
    return tmp_filename


def show_image(image_arr):
    h, w, c = image_arr.shape
    if c != 3:
        raise ValueError(f"image_arr should be [h, w, c], but got shape: {image_arr.shape}")
    from IPython.display import Image
    from IPython.display import display
    tmp_filename = os.path.join('tmp',random_str() + '.png')
    ensure_filename(tmp_filename)
    arr2image(image_arr, tmp_filename)
    print(f"Image size is {image_arr.shape}")
    display(Image(tmp_filename))
    return tmp_filename

'''
=====================================================================================================================
                                            Auto Fix
=====================================================================================================================
'''
def fix_library(library_name, relative_path, line_number, new_code):
    # fix_library(library_name="pytorchvideo", relative_path="transforms/augmentations.py", line_number=9, new_code="import torchvision.transforms.functional as F_t")
    try:
        library_path = os.path.dirname(os.path.realpath(__import__(library_name).__file__))
    except ImportError:
        return f"找不到库函数 {library_name}"
    absolute_path = pathlib.Path(library_path) / relative_path
    if not absolute_path.is_file():
        return f"文件 {absolute_path} 不存在"
    with open(absolute_path, 'r') as file:
        lines = file.readlines()
    if 0 < line_number <= len(lines):
        lines[line_number - 1] = new_code + '\n'
    else:
        return f"指定的行数 {line_number} 超出文件范围"
    with open(absolute_path, 'w') as file:
        file.writelines(lines)
    return f"已成功修改文件 {absolute_path} 的第 {line_number} 行为：\n{new_code}"


def fix_library_by_file(library_name, relative_path, replace_filename):
    try:
        library_path = os.path.dirname(os.path.realpath(__import__(library_name).__file__))
    except ImportError:
        return f"找不到库 {library_name}"
    target_file_path = pathlib.Path(library_path) / relative_path
    if not target_file_path.is_file():
        return f"文件 {target_file_path} 不存在"
    replace_file_path = pathlib.Path(replace_filename).resolve()
    if not replace_file_path.is_file():
        return f"替换文件 {replace_file_path} 不存在"
    with open(replace_file_path, 'r') as file:
        new_content = file.read()
    with open(target_file_path, 'w') as file:
        file.write(new_content)
    return f"已成功将文件 {target_file_path} 替换为 {replace_file_path} 的内容"



'''
=====================================================================================================================
                                            APIs
=====================================================================================================================
'''


def step_api(question, video_arr=None, model_name=None, api_base="http://10.154.192.2:8000/v1",  temperature=0.2, top_p=0.9, frequency_penalty=0.0, max_tokens=1024):
    if video_arr is not None:
        if len(video_arr) > 15:
            raise ValueError('only support max 15 frames.')
        if not model_name:
            model_name = 'step1p5c-hqlcode-video-10k-vl8k-5c5-0416-mlp'

            frame_base64_list = []
            for frame in video_arr:
                _, buffer = cv2.imencode('.jpg', frame[:,:,::-1])
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                frame_base64_list.append(frame_base64)

    else:
        if not model_name:
            model_name = "step1p5c-hqlcode-video-25k-vl8k-5d-0516-1a-0520"
            # model_name = "release-step2-merged-ppo-4in1-2022-post-ppo"

    content = [{"type": "text", "text": "USER:"}]
    if video_arr is not None:
        for frame in frame_base64_list:
            content.append({"type": "image_b64", "image_b64": {"b64_json": frame}})
    content += [{"type": "text", "text": '\n' + question}] + [{"type": "text", "text": " ASSISTANT: "}]
    messages = [{"role": "user", "content": content}]

    import openai
    openai.api_key = "EMPTY"
    openai.api_base = api_base

    k = 0
    while True:
        try:
            infer_start = time.time()
            print("Start reasoning")
            completion = openai.ChatCompletion.create(
                model=model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                frequency_penalty=frequency_penalty,
                top_p=top_p,
            )
            print("The reasoning spends {:.2f}s in total".format(time.time()-infer_start))
            return completion["choices"][0]["message"]["content"]
        except Exception as e:
            print(e)
            time.sleep(random.randint(3, 5))
            print(f'Retrying for {k} times')
            k += 1


'''
=====================================================================================================================
                                           Monitors
=====================================================================================================================
'''

def monitor_variable(variable_fn, total=10000000):
    last_length = 0
    start_rd_len = variable_fn()
    pbar = tqdm(total=total - start_rd_len)

    try:
        while True:
            current_length = variable_fn()-start_rd_len
            length_difference = current_length - last_length
            pbar.update(length_difference)
            pbar.refresh()
            last_length = current_length
            time.sleep(1) 
            if current_length >= pbar.total:
                break 
    except KeyboardInterrupt:
        print("\n中断执行。")
    finally:
        pbar.close() 

'''
=====================================================================================================================
                                            Multi Processing
=====================================================================================================================
'''

def dist_info(printable=False, return_dict = True):
    n_gpu = torch.cuda.device_count()
    local_rank = int(os.environ.get('LOCAL_RANK', 0))
    world_size = int(os.environ.get('WORLD_SIZE', 1))
    rank = int(os.environ.get('RANK', 0))
    nodes = int(world_size / n_gpu)
    node_id = int(rank / n_gpu)
    if printable:
        logger.info('dist_info: [rank:{}/{} local_rank:{}/{} node:{}/{}]'.format(node_id, nodes, rank, world_size, local_rank, n_gpu))
    if return_dict:
        return {'n_gpu': n_gpu, 'local_rank': local_rank, 'world_size': world_size, 'rank': rank, 'nodes': nodes, 'node_id': node_id}
    else:
        return rank, world_size, local_rank, n_gpu, node_id, nodes


def shard_list(all_files):
    world_size = int(os.environ.get("WORLD_SIZE", 1))
    rank = int(os.environ.get("RANK", 0))
    total = len(all_files)
    shard_len = total // world_size
    st = shard_len * rank
    ed = shard_len * (rank + 1)
    if rank == world_size - 1:
        ed = total
    assigned_total = ed-st
    all_files = copy.deepcopy(all_files[st:ed])
    gc.collect()
    logger.warning(f'Rank {rank}/{world_size} assigned {assigned_total}/{total}')
    return all_files


'''
=====================================================================================================================
                                            Data Pipelines
=====================================================================================================================
'''
class FilterException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"FilterException: {self.message}"

def warn_and_continue_debug(e):
    if 'aws' in repr(e):
        time.sleep(1)
        return True
    else:
        logger.warning("Exception: %s" % e)
        traceback.print_exc()

def warn_and_continue(e):
    if 'aws' in repr(e):
        time.sleep(1)
        return True
    else:
        logger.warning("Exception: %s" % e)
        # try:
        #     logger.exception(e)
        # except:
        #     pass
        # return True

def direct_continue(e):
    if 'aws' in repr(e):
        time.sleep(1)
        return True
    else:
        pass
        # try:
        #     logger.exception(e)
        # except:
        #     pass
        # return True

class CustomDecoderDataPipe(IterDataPipe):
    def __init__(self, datapipe, decode_fn, log_filename=None,except_handler= warn_and_continue):
        super().__init__()
        self.datapipe = datapipe
        self.decode_fn = decode_fn
        self.exception_handler = except_handler
        self.log_filename = log_filename
        if log_filename:
            # self.log_dir = log_dir
            ensure_filename(log_filename)
        self.cnt_success = 0
        self.cnt_failed = 0

    def __iter__(self):
        for data in self.datapipe:
            try:
                sample = self.decode_fn(data)
                if self.log_filename:
                    with open(self.log_filename, 'a', encoding='utf-8') as f:
                        log_str = get_timestr() + '\t' + 'rank_' + str(os.environ.get('RANK', 0)) + '\t' + str(list(sample['mp4'].shape)) + '\t' + sample['url']+'\n'
                        f.write(log_str)
                yield sample
                self.cnt_success += 1  
            except Exception as e:
                self.cnt_failed += 1
                e = str(e) + f' [URL: {data["__url__"]}, Success: {self.cnt_success}, Failed: {self.cnt_failed}, Sucess Rate: {self.cnt_success/(self.cnt_success+self.cnt_failed):.2f}]'
                self.exception_handler(e)



def generate_html(pred_dirname, s3_dir='s3://wcf-shared-bj3-volcecloud/G/share/tmp/', override=False, fsspec_config = None, printable=True):
    if not pred_dirname.startswith('s3'):
        raise ValueError('pred_dirname must start with s3.')
    if not os.path.basename(pred_dirname) == 'pred':
        raise ValueError('pred dirname must endwith pred')
    project_name, method_name, eval_name = pred_dirname.split('/')[-4:-1]
    html_filename = path_join(s3_dir, 'gather', f'{project_name}_{method_name}_{eval_name}.html')
    if printable: logger.info(f'html_filename is {html_filename}')
    if not path_exists(html_filename, fsspec_config=fsspec_config) or override:
        filename_list = list_filenames(pred_dirname, fsspec_config = fsspec_config, printable=printable)
        pairs = groupby(filename_list, key=lambda x: pathlib.Path(x).stem.split('.')[0]).values()
        max_len = max([len(pair) for pair in pairs])
        pairs = [pair for pair in pairs if len(pair) == max_len]
        if printable: logger.info(f"pairs: {pairs}", )
        html = ""
        iter_func = tqdm(range(len(pairs))) if printable else range(len(pairs))
        for pair_index in iter_func:
            filenames = sorted(pairs[pair_index])
            for filename in filenames:
                suffix = pathlib.Path(filename).suffix
                if suffix == '.txt':
                    txt = file2data(filename, fsspec_config = fsspec_config, printable=printable)
                    html += f"<p>{txt}</p>"
                elif suffix == '.mp4':
                    mp4 = filename.replace('s3://wcf-shared-bj3-volcecloud', 'https://wcf-shared-bj3-volcecloud.tos-cn-beijing2.volces.com')
                    # html += f'<video controls autoplay muted loop><source src="{mp4}" type="video/mp4"></video>'
                    html += f'<video controls loop><source src="{mp4}" type="video/mp4"></video>'
                elif suffix == '.png':
                    png = filename.replace('s3://wcf-shared-bj3-volcecloud', 'https://wcf-shared-bj3-volcecloud.tos-cn-beijing2.volces.com')
                    html += f'<img src="{png}">'
                
        data2file(html, html_filename, fsspec_config = fsspec_config, override=True, printable=printable)
        logger.info(f'Succssfully wrote file to {html_filename}')
    else:
        logger.info(f"HTML Gather file {html_filename} already exisits. skipping convert...")

class CustomFileListerDataPipe(torchdata.datapipes.iter.IterDataPipe):
    # 晨飞注：支持fs和本地读取，支持任意嵌套路径
    # 注意，分布式读取由于boto3不能pickle，建议使用CustomFileListerCacheDataPipe
    def __init__(self, root, fsspec_config=None,  except_handler = warn_and_continue):
        if isinstance(root, str):
            root = [root, ]
        if not isinstance(root, IterDataPipe):
            root = IterableWrapper(root)        
        self.datapipe = root
        self.fsspec_config= fsspec_config


    def __iter__(self):
        for path in self.datapipe:
            try:
                if path.startswith('s3://'):
                    boto3_config = {
                        'aws_access_key_id': self.fsspec_config['key'],
                        'aws_secret_access_key': self.fsspec_config['secret'],
                        'endpoint_url': self.fsspec_config['endpoint_url'],
                        'config': botocore.config.Config(**self.fsspec_config['config_kwargs'])
                    }            
                    boto3_client = boto3.client('s3', **boto3_config)
                    self.boto3_paginator = boto3_client.get_paginator('list_objects_v2')
                    s = path.replace('s3://', '').split('/')
                    pages = self.boto3_paginator.paginate(Bucket=s[0], Prefix='/'.join(s[1:]))                
                    for page in pages:
                        filenames = [os.path.join("s3://", s[0], obj['Key']) for obj in page['Contents']]
                        filenames = [e for e in filenames if e not in self.used_data]
                        if len(filenames) == 0:
                            continue
                        yield from filenames
                else:
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            filepath = os.path.join(root, file)
                            if filepath not in self.used_data:
                                yield filepath
            except Exception as e:
                    self.except_handler(e)            

@logger.catch(reraise=True)
def cache_filelists(urls, override=False, fsspec_config=None, filter_fn=None):  
    # 晨飞注：支持fs和本地读取，支持任意嵌套路径，支持多进程读取
    #     cache_filelists(args.urls, override=True, fsspec_config=args.fsspec_config,
    #                     filter_fn=lambda x: x.endswith(".tar"))
    if isinstance(urls, str):
        urls = [urls]
    if int(os.environ.get("RANK", 0)) == 0:
        for path in urls:
            cache_filename = add_suffix(path, '.txt')
            if not path_exists(cache_filename, fsspec_config=fsspec_config) or override:
                logger.info(f'Auto create cache_filename: {cache_filename}...')
                filename_list = []
                if path.startswith('s3://'):
                    if 'config_kwargs' in fsspec_config:
                        boto3_config = {
                            'aws_access_key_id': fsspec_config['key'],
                            'aws_secret_access_key': fsspec_config['secret'],
                            'endpoint_url': fsspec_config['endpoint_url'],
                            'config': botocore.config.Config(**fsspec_config['config_kwargs'])
                        }
                    else:
                        boto3_config = {
                            'aws_access_key_id': fsspec_config['key'],
                            'aws_secret_access_key': fsspec_config['secret'],
                            'endpoint_url': fsspec_config['endpoint_url'],
                        }
                    boto3_client = boto3.client('s3', **boto3_config)
                    boto3_paginator = boto3_client.get_paginator('list_objects_v2')
                    s = path.replace('s3://', '').split('/')
                    pages = boto3_paginator.paginate(Bucket=s[0], Prefix='/'.join(s[1:]))                
                    for page in tqdm(pages):
                        try:
                            filenames = [os.path.join("s3://", s[0], obj['Key']) for obj in page['Contents']]
                            filename_list.extend(filenames)
                        except Exception as e:
                            logger.warning('Failed to read page...')
                            traceback.print_exc()
                else:
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            filename_list.append(os.path.join(root, file))
                if filter_fn:
                    filename_list = [e for e in filename_list if filter_fn(e)]
                data2file(filename_list, cache_filename, fsspec_config=fsspec_config, override=override)
                logger.info(f'Cache file {cache_filename} has been created with {len(filename_list)} lines.')
            else:
                logger.info(f'Cache file {cache_filename} exists, skip it...')
    if torch.distributed.is_initialized():
        torch.distributed.barrier()
    cache_list = []
    for url in urls:
        cache_filename = add_suffix(url, '.txt')
        cache_list.extend(safe_file2data(cache_filename, fsspec_config=fsspec_config))
    return cache_list


def list_filenames_recursive(path, fsspec_config=None, filter_fn=None):  
    # 晨飞注：支持fs和本地读取，支持任意嵌套路径，常见用法
    #     cache_filelists(args.urls, override=True, fsspec_config=args.fsspec_config,
    #                     filter_fn=lambda x: x.endswith(".tar"))
    filename_list = []
    if path.startswith('s3://'):
        if 'config_kwargs' in fsspec_config:
            boto3_config = {
                'aws_access_key_id': fsspec_config['key'],
                'aws_secret_access_key': fsspec_config['secret'],
                'endpoint_url': fsspec_config['endpoint_url'],
                'config': botocore.config.Config(**fsspec_config['config_kwargs'])
            }
        else:
            boto3_config = {
                'aws_access_key_id': fsspec_config['key'],
                'aws_secret_access_key': fsspec_config['secret'],
                'endpoint_url': fsspec_config['endpoint_url'],
            }              
        boto3_client = boto3.client('s3', **boto3_config)
        boto3_paginator = boto3_client.get_paginator('list_objects_v2')
        s = path.replace('s3://', '').split('/')
        pages = boto3_paginator.paginate(Bucket=s[0], Prefix='/'.join(s[1:]))                
        for page in tqdm(pages):
            filenames = [os.path.join("s3://", s[0], obj['Key']) for obj in page['Contents']]
            filename_list.extend(filenames)
    else:
        for root, dirs, files in os.walk(path):
            for file in files:
                filename_list.append(os.path.join(root, file))
    if filter_fn:
        filename_list = [e for e in filename_list if filter_fn(e)]
    return filename_list



def safe_file2data(path, max_retries=100, sleep_interval=1, **kwargs):
    """尝试多次读取文件，直到成功或达到最大重试次数。

    Args:
        path (str): 要读取的文件路径。
        max_retries (int): 最大重试次数。
        sleep_interval (float): 重试之间的等待时间（秒）。
        **kwargs: 传递给 file2data 函数的其他关键字参数。

    Returns:
        file data if successful, None otherwise
    """
    retries = 0
    while retries < max_retries:
        try:
            # 尝试读取文件
            data = file2data(path, **kwargs)
            return data
        except OSError as e:
            # 如果发生OS错误，打印错误并等待，然后重试
            logger.warning(f"OS Error occurred: {e}. Retrying {retries + 1}/{max_retries}...")
            time.sleep(sleep_interval)
            retries += 1
    raise SystemError(f"Failed to read the file after {max_retries} attempts.")

class CustomStreamOpenerDataPipe(torchdata.datapipes.iter.IterDataPipe):
    def __init__(self,source_datapipe,mode='rb',retry=3,fsspec_config = None, except_handler=warn_and_continue, use_fscs=False):
        if not isinstance(source_datapipe, IterDataPipe):
            self.source_datapipe = IterableWrapper(source_datapipe)  
        else:
            self.source_datapipe = source_datapipe
        self.mode = mode
        self.retry = retry
        self.fsspec_config = fsspec_config
        self.except_handler = except_handler
        self.use_fscs = use_fscs
        
    def __iter__(self):

        for url in self.source_datapipe:
            if url.startswith('s3'):
                # TODO 去掉对~/.aws/credentials的依赖
                if url.startswith('s3://vdata-shared-bj3-volcecloud') and self.use_fscs:
                    pipeurl = url.replace('s3://vdata-shared-bj3-volcecloud', '/vdata-shared-bj3-volcecloud')
                else:
                    endpoint_url, key, secret = self.fsspec_config['endpoint_url'], self.fsspec_config['key'], self.fsspec_config['secret']
                pipeurl = f'pipe: AWS_ACCESS_KEY_ID={key} AWS_SECRET_ACCESS_KEY={secret} aws --endpoint-url={endpoint_url} s3 cp "{url}" -'
            else:
                pipeurl = url
            sw = None
            for _ in range(self.retry):
                try:
                    sw = StreamWrapper(wds.gopen(pipeurl, mode=self.mode))
                    break
                except Exception as exn:
                    print(exn)
                    print("retrying...in 1 sec")
                    time.sleep(1)
                    continue
            if sw is None:
                self.except_handler(ValueError("Failed to open {pipeurl} after {self.retry} retries"))
            yield url, sw

    def __len__(self) -> int:
        return len(self.source_datapipe) 
    
class CustomMaxSamplesDataPipe(IterDataPipe):
    def __init__(self, source_datapipe, max_samples):
        self.source_datapipe = source_datapipe
        self.max_samples = max_samples

    def __iter__(self):
        sample_count = 0
        for sample in self.source_datapipe:
            if sample_count >= self.max_samples:
                break
            yield sample
            sample_count += 1

class CustomTar2SampleDataPipe(IterDataPipe):
    def __init__(self, source_datapipe, except_handler = warn_and_continue):
        self.source_datapipe = source_datapipe
        self.except_handler = except_handler
    def __iter__(self):
        sample= {}
        current = ""
        for path, data in self.source_datapipe:
            try:
                assert isinstance(path, str), path
                _, prefix, suffix = split_filename(path)
                if suffix == "":
                    continue
                if prefix != current:
                    if current != "":
                        yield sample
                    sample = {}
                    current = prefix
                    sample["__key__"] = current
                    sample["__url__"] = path
                sample[suffix] = data
            except Exception as e:
                self.except_handler(e)
                
        if sample != {}:
            yield sample

def _is_stream_handle(data):
    obj_to_check = data.file_obj if isinstance(data, StreamWrapper) else data
    return isinstance(obj_to_check, (BufferedIOBase, RawIOBase))

class CustomTarArchiveLoaderDataPipe(IterDataPipe):

    def __init__(self, datapipe, mode  = "r:*",length: int = -1, except_handler = warn_and_continue):
        super().__init__()
        self.datapipe=datapipe
        self.mode=mode
        self.length=length
        self.except_handler = except_handler

    def __iter__(self):
        for data in self.datapipe:
            try:
                validate_pathname_binary_tuple(data)
                pathname, data_stream = data
                if isinstance(data_stream, StreamWrapper) and isinstance(data_stream.file_obj, tarfile.TarFile):
                    tar = data_stream.file_obj
                else:
                    reading_mode = (
                        self.mode
                        if hasattr(data_stream, "seekable") and data_stream.seekable()
                        else self.mode.replace(":", "|")
                    )
                    # typing.cast is used here to silence mypy's type checker
                    tar = tarfile.open(fileobj=cast(bytes, data_stream), mode=reading_mode)
                try:
                    for tarinfo in tar:
                        if not tarinfo.isfile():
                            continue
                        extracted_fobj = tar.extractfile(tarinfo)
                        if extracted_fobj is None:
                            logger.warning(f"failed to extract file {tarinfo.name} from source tarfile {pathname}")
                            raise tarfile.ExtractError
                        inner_pathname = os.path.normpath(os.path.join(pathname, tarinfo.name))
                        sw = StreamWrapper(io.BytesIO(extracted_fobj.read()), data_stream, name=inner_pathname)  # type: ignore[misc]
                        yield inner_pathname, sw
                        # sw.autoclose()
                        del sw
                    # close tarfile after it's been exceeded
                finally:
                    tar.close()
                    del tar
                    del tarinfo

                    if _is_stream_handle(data_stream):
                        data_stream.autoclose()
                    del data_stream
                    gc.collect()
            except Exception as e:
                self.except_handler(e)
                logger.warning(f"Unable to extract files from corrupted tarfile stream {pathname} due to: {e}, abort!")

    def __len__(self) -> int:
        if self.length == -1:
            raise TypeError(f"{type(self).__name__} instance doesn't have valid length")
        return self.length


def datapipe2tardir(datapipe, tar_dir, max_size=50, fsspec_config=None):
    def open_random_tar_writer(tar_dir):
        filename = os.path.join(tar_dir, f'{str(uuid.uuid4())}.tar')
        if filename.startswith("s3://"):
            f = fsspec.open(filename, 'wb',**fsspec_config).open()
            dst = wds.TarWriter(f)
        else:
            dst = wds.TarWriter(filename)
        return dst

    tar_writer = open_random_tar_writer(tar_dir)
    total_cnt = 0
    for item in tqdm(datapipe):
        tar_writer.write(item)
        total_cnt += 1
        if total_cnt % max_size == 0:
            tar_writer.close()
            tar_writer = open_random_tar_writer(tar_dir)
    if total_cnt % max_size != 0:
        tar_writer.close()


def tarlist2datapipe(tarlist, map_fn=None, fsspec_config=None, except_handler=warn_and_continue):
    logger.info(f'Detected {len(tarlist)} tars.')
    main_datapipe = CustomStreamOpenerDataPipe(tarlist, mode="rb", fsspec_config=fsspec_config) # [c_stream, a_stream]
    main_datapipe = CustomTarArchiveLoaderDataPipe(main_datapipe) # [c_extracted_stream_1_good.mp4,c_extracted_stream_2_bad.json, c_extracted_stream_3_good.json,c_extracted_stream_4_bad.mp4,a_extracted_stream_1, a_extracted_stream_2, xxx]
    main_datapipe = CustomTar2SampleDataPipe(main_datapipe) # {'good':{'mp4':c_extracted_stream_1_good, 'jso[n':c_extracted_stream_1_good}, 'bad':xxx}

    if map_fn:
        main_datapipe = CustomDecoderDataPipe(main_datapipe, map_fn, except_handler=except_handler)
    return main_datapipe

def tar2list(tarfile, top=None, decode=True, fsspec_config=None):
    def _simple_decode(sample):
        if 'json' in sample:
            sample['json'] = json.loads(sample['json'].read())
        if 'mp4' in sample:
            sample['mp4'] = video2arr(sample['mp4'].read())
        if 'txt' in sample:
            sample['txt'] = sample['txt'].read().decode('utf-8')
        if 'png' in sample:
            sample['png'] = image2arr(sample['png'].read())
        return sample
    if isinstance(tarfile, str):
        if tarfile.startswith("s3://") and not fsspec_config:
            raise ValueError(f"fsspec_config is required for {tarfile}")
    else:
        raise ValueError(f"tarfile should be str, but got {type(tarfile)}")

    main_datapipe = CustomStreamOpenerDataPipe([tarfile], mode="rb", fsspec_config=fsspec_config) # [c_stream, a_stream]
    main_datapipe = CustomTarArchiveLoaderDataPipe(main_datapipe) # [c_extracted_stream_1_good.mp4,c_extracted_stream_2_bad.json, c_extracted_stream_3_good.json,c_extracted_stream_4_bad.mp4,a_extracted_stream_1, a_extracted_stream_2, xxx]
    main_datapipe = CustomTar2SampleDataPipe(main_datapipe) # {'good':{'mp4':c_extracted_stream_1_good, 'json':c_extracted_stream_1_good}, 'bad':xxx}
    if top is not None:
        main_datapipe = CustomMaxSamplesDataPipe(main_datapipe, top)
    if decode:
        main_datapipe = CustomDecoderDataPipe(main_datapipe, decode_fn=_simple_decode) # {'good':{'mp4':c_extracted_stream_1_good, 'json':c_extracted_stream_1_good}, 'bad':xxx}
    output_list = [sample for sample in main_datapipe]
    return output_list



def numpy_to_tensor(datadict):
    for k, v in datadict.items():
        if isinstance(v, np.ndarray):
            datadict[k] = torch.from_numpy(v)
    return datadict



if __name__ == '__main__':
    if len(sys.argv) == 1:
        logger.warning('Usage: python3 -m utils <function_name> <args>')
        func_str = ', '.join([e for e in dir() if not e.startswith('_') and callable(getattr(sys.modules[__name__], e))])
        logger.info(f'Available functions are:\n{func_str}')
    else:
        function = getattr(sys.modules[__name__], sys.argv[1])
        function(*sys.argv[2:])


