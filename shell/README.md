# USEFUL SHELL CMDS IN ML
## gpu/cuda related
- check cuda version
```
nvcc -V
cat /usr/local/cuda/version.txt
python3 -c "import torch;print(torch.version.cuda)"
```
- check gpu status
```
nvidia-smi #check once
#show gpu status until ctrl+c
nvidia-smi -l 
watch -n 1 nvidia-smi

#show free gpu in csv format
nvidia-smi --query-gpu=memory.free --format=csv

# show used gpu
nvidia-smi --query-gpu=memory.used --format=csv
nvidia-smi | grep MiB | awk '{print $9}' | sed -n '3p'

```

## docker related
```
docker build -t a-tag:v1 . #build an image from local Dockerfile
docker pull <image>
docker image ls
docker ps 

# start a container with gpu
docker run --gpus all/0/etc image cmd

# remove all stoped docker container with a filter
docker rm $(docker ps -a | grep xxx | awk '{print $1}')
```
- build seperated dev-env using docker

[https://www.yuque.com/docs/share/5591c84c-0907-4b65-b5b7-c3a327fbf214](https://www.yuque.com/docs/share/5591c84c-0907-4b65-b5b7-c3a327fbf214)