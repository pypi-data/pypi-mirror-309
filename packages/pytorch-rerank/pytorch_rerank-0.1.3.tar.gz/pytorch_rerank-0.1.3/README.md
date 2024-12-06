# PytorchRerank

在容器环境中动态替换原先注入的 `MASTER_ADDR` 和 `RANK` 环境变量，实现 `RANK` 重排，重排依据是交换机亲和性，保证相邻 `RANK` 优先在相同交换机下，进而提升 Pytorch NCCL 的通信效率。

## 使用方式

在用户启动脚本执行前加上以下 rerank 逻辑即可，代码会自动修改 `MASTER_ADDR` 和 `RANK` 环境变量，后续获取的 `MASTER_ADDR` 和 `RANK` 都是重排后的。

### 使用前
```shell
# 用户代码
pip install transformers
pip install diffusers
torchrun --nproc_per_node=$NPROC_PER_NODE --nnodes=$WORLD_SIZE --node_rank=$RANK --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT your_train_script.py

```

### 使用后
```shell
# 安装并执行 rerank
pip install pytorch-rerank -i https://mirrors.aliyun.com/pypi/simple/
torchrerank
source /tmp/pytorch_rerank_envs.sh

# 用户代码
pip install transformers
pip install diffusers
torchrun --nproc_per_node=$NPROC_PER_NODE --nnodes=$WORLD_SIZE --node_rank=$RANK --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT your_train_script.py
```

### 也可通过 clone 代码执行
```shell
# clone 代码 
git clone http://gitlab.alibaba-inc.com/tre-ai-infra/pytorch_rerank.git
cd pytorch_rerank
torchrerank
source /tmp/pytorch_rerank_envs.sh

# 用户代码
pip install transformers
pip install diffusers
torchrun --nproc_per_node=$NPROC_PER_NODE --nnodes=$WORLD_SIZE --node_rank=$RANK --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT your_train_script.py
```

### 其他
rerank 脚本默认按交换机亲和性重排 RANK，也支持按照 ip 进行重排，适用于某些特殊集群，执行时加上 ip 选项即可。
```shell
# 安装并执行 rerank
pip install pytorch-rerank -i https://mirrors.aliyun.com/pypi/simple
torchrerank ip
source /tmp/pytorch_rerank_envs.sh

# 用户代码
pip install transformers
pip install diffusers
torchrun --nproc_per_node=$NPROC_PER_NODE --nnodes=$WORLD_SIZE --node_rank=$RANK --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT your_train_script.py
```