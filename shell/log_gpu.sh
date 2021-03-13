#/bin/bash
while true; do
sleep 1
echo "`date +%Y-%m-%d/%H:%M:%S` `nvidia-smi | grep MiB | awk '{print $9}' | sed -n '1p'`" >> $1
done
# usage: bash log_gpu.sh >> xx.log