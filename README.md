
# 项目
git clone https://github.com/fishaudio/fish-speech.git

说明：
https://speech.fish.audio/inference/#_2


# 安装
## 环境 
python3.10 -m venv venv_fish 
source venv_fish/bin/activate


## cuda 121
#pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

## cuda 118
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu118


pip3 install ninja && MAX_JOBS=4 pip3 install flash-attn==2.4.2 --no-build-isolation


## 以下方法没法获得模型
```
https://hf-mirror.com/
HF_ENDPOINT=https://hf-mirror.com huggingface-cli login
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

git config --global http.proxy "http://192.168.0.77:18808"
git config --global https.proxy "http://192.168.0.77:18808"


git config --global --unset https.proxy
git config --global --unset http.proxy


huggingface-cli download fishaudio/speech-lm-v1 vqgan-v1.pth --local-dir checkpoints
huggingface-cli download fishaudio/speech-lm-v1 text2semantic-400m-v0.2-4k.pth --local-dir checkpoints
```

## 改为clone
```
#s机房，非 77 机器上
git config --global http.proxy "http://192.168.0.77:18808"
git config --global https.proxy "http://192.168.0.77:18808"

git lfs install
git clone https://huggingface.co/fishaudio/speech-lm-v1
用户名： 
daocode
秘钥：
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


# clone 完成后
git config --global --unset https.proxy
git config --global --unset http.proxy

mkdir -p fish-speech/checkpoints/
cp speech-lm-v1/vqgan-v1.pth  fish-speech/checkpoints/
cp speech-lm-v1/text2semantic-400m-v0.2-4k.pth fish-speech/checkpoints/

```

# 对外端口
```
cat /data/work/frp/frpc.ini 
vim /data/work/frp/frpc.ini 

[ssh-fish5001]
type = tcp
local_ip = 127.0.0.1
local_port = 5001
remote_port = 5001
use_encryption = false
use_compression = false


[ssh-fish8000]
type = tcp
local_ip = 127.0.0.1
local_port = 8000
remote_port = 5002
use_encryption = false
use_compression = false


# 重启frp
systemctl restart  supervisor
supervisorctl reload

```



# 启动
```
start.sh
```


source venv_fish/bin/activate  
cd /data/work/fish-speech && python -m zibai tools.api_server:app --listen 127.0.0.1:8000  
cd /data/work/fish-speech && python fish_speech/webui/app.py  

# 查看GPU
nvidia-smi dmon