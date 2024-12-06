import os
import torch
import argparse
import subprocess
from typing import List
import torch.distributed as dist

HOST_INFO_BUFFER_SIZE=100
TAIL_DUMMY_CHAR=0
RESULT_FILE='/tmp/pytorch_rerank_envs.sh'
LOG_RESULT_PREFIX='TRE_ASI_RERANK_RESULT'


def do_all_gather(output_tensor_list: List, input_tensor: torch.CharTensor):
    dist.all_gather(output_tensor_list, input_tensor)


def get_ip():
    process_host = subprocess.Popen(['hostname', '-i'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_host, error_host = process_host.communicate()
    host_ip = output_host.strip().split(' ')[-1]
    info = host_ip
    return info


def convert_str_2_char_tensor(local_info_str):
    input_tensor = torch.zeros(HOST_INFO_BUFFER_SIZE, dtype=torch.int8)
    idx = 0
    for item in local_info_str:
        input_tensor[idx] = ord(item)
        idx += 1
    input_tensor[idx] = TAIL_DUMMY_CHAR
    return input_tensor


def convert_char_tensors_2_strs(output_list):
    result = []
    for item in output_list:
        temp_str = ''
        idx = 0
        while int(item[idx]) != 0:
            temp_str += chr(int(item[idx]))
            idx += 1
        result.append(temp_str)
    return result


def get_all_host_info():
    local_ip_info_str = get_ip()
    local_asw_info_str = os.getenv('ASW_ID', '')
    local_info_str = f"{local_ip_info_str},{local_asw_info_str}"
    output_list = [torch.zeros(HOST_INFO_BUFFER_SIZE, dtype=torch.int8) for _ in range(dist.get_world_size())]
    input_tensor = convert_str_2_char_tensor(local_info_str)
    do_all_gather(output_list, input_tensor)
    all_info_strs = convert_char_tensors_2_strs(output_list)
    unique_res = set()
    for item in all_info_strs:
        unique_res.add(item)
    return list(unique_res)


def init_result_file():
    with open(RESULT_FILE, 'w') as file:
        file.write("#!/bin/bash\n")


def write_result(str):
    with open(RESULT_FILE, 'a') as f:
        f.write(str)


def sort_host_info(all_info, use_ip=False, do_test=False):
    sorted_list = []
    local_ip = get_ip()
    all_ip_sw_list = [(_.split(',')[0], _.split(',')[1]) for _ in all_info]
    if use_ip:
        sorted_list = list(sorted(all_ip_sw_list, key=lambda x: int(x[0].split('.')[-1])))
    else:
        sorted_list = sorted(all_ip_sw_list, key=lambda x: (x[1], x[0]))

    if do_test:
        for item in sorted_list:
            print(item)
        print("\n")

    sorted_ip_list = [_[0] for _ in sorted_list]
    if local_ip in sorted_ip_list:
        print(f"{LOG_RESULT_PREFIX} MASTER_ADDR={sorted_ip_list[0]}")
        print(f"{LOG_RESULT_PREFIX} RANK={sorted_ip_list.index(local_ip)}")
        write_result(f"export MASTER_ADDR={sorted_ip_list[0]}\n")
        write_result(f"export RANK={sorted_ip_list.index(local_ip)}\n")


def test_sort_by_sw():
    all_info_list = [
        "33.195.58.19,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG3-S10-1.NA61",
        "33.198.98.20,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG8-S29-1.NA61",
        "33.195.58.1,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG3-S10-1.NA61",
        "33.195.58.123,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG3-S10-1.NA61",
        "33.198.98.16,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG8-S29-1.NA61",
        "33.195.58.193,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG3-S10-1.NA61",
        "33.198.98.20,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG7-S01-1.NA61",
        "33.198.98.12,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG7-S29-1.NA61",
        "33.198.98.45,ASW-MAN-EXCLUSIVE-G2-P2-P2-SG7-S01-1.NA61",
        "33.198.98.75,ASW-MAN-EXCLUSIVE-G2-P3-P3-SG7-S01-1.NA61",
        "33.198.98.32,ASW-MAN-EXCLUSIVE-G2-P2-P3-SG6-S29-1.NA61",
        "33.198.98.49,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG7-S23-1.NA61",
        "33.198.98.23,ASW-MAN-EXCLUSIVE-G2-P2-P2-SG7-S01-1.NA61",
        "33.198.98.21,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG7-S01-1.NA61",
    ]
    sort_host_info(all_info_list, do_test=True)


def test_sort_by_ip():
    all_info_list = [
        "33.195.58.19,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG3-S10-1.NA61",
        "33.198.98.20,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG8-S29-1.NA61",
        "33.195.58.1,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG3-S10-1.NA61",
        "33.195.58.123,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG3-S10-1.NA61",
        "33.198.98.16,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG8-S29-1.NA61",
        "33.195.58.193,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG3-S10-1.NA61",
        "33.198.98.20,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG7-S01-1.NA61",
        "33.198.98.12,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG7-S29-1.NA61",
        "33.198.98.45,ASW-MAN-EXCLUSIVE-G2-P2-P2-SG7-S01-1.NA61",
        "33.198.98.75,ASW-MAN-EXCLUSIVE-G2-P3-P3-SG7-S01-1.NA61",
        "33.198.98.32,ASW-MAN-EXCLUSIVE-G2-P2-P3-SG6-S29-1.NA61",
        "33.198.98.49,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG7-S23-1.NA61",
        "33.198.98.23,ASW-MAN-EXCLUSIVE-G2-P2-P2-SG7-S01-1.NA61",
        "33.198.98.21,ASW-MAN-EXCLUSIVE-G2-P2-P1-SG7-S01-1.NA61",
    ]
    sort_host_info(all_info_list, True, do_test=True)
  

def run_rerank(args):
    try:
        res = get_all_host_info()
        if int(os.getenv('LOCAL_RANK')) == 0:
            sort_host_info(res, args.use_ip_rerank)
    except Exception:
        if int(os.getenv('LOCAL_RANK')) == 0:
            print("rerank failed. Unknown Exception raised!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="pytorch reranker")
    parser.add_argument('--use-ip-rerank', action='store_true', help='use ip address to do rerank.')
    args = parser.parse_args()
    init_result_file()
    dist.init_process_group('gloo')
    run_rerank(args)
    # test_sort_by_sw()
    # test_sort_by_ip()
    

# torchrun --nproc_per_node=4 --nnodes=1 --node_rank=0 --master_addr=$MASTER_ADDR --master_port=23456 train.py

# torchrun --nproc_per_node=4 --nnodes=2 --node_rank=0 --master_addr=$MASTER_ADDR --master_port=23456 train.py
# torchrun --nproc_per_node=4 --nnodes=2 --node_rank=1 --master_addr=$MASTER_ADDR --master_port=23456 train.py

# torchrun --nproc_per_node=4 --nnodes=2 --rdzv_id=12345 --rdzv_backend=c10d --rdzv_endpoint=$MASTER_ADDR:23456 train.py
# torchrun --nproc_per_node=4 --nnodes=2 --rdzv_id=12345 --rdzv_backend=c10d --rdzv_endpoint=$MASTER_ADDR:23456 train.py