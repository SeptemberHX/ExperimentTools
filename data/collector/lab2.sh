#!/bin/bash

 ip_array=('144.34.160.60'  '144.34.214.165' '144.34.172.167' '104.225.148.205' '66.42.98.44' '8.3.29.104' '144.202.113.140' '149.28.80.33' '140.82.20.242' '144.34.200.189')
#ip_array=('104.225.148.205' '8.3.29.104' '144.34.200.189')


mkdir result
cd result

for ip in "${ip_array[@]}"
do
  echo $ip
  sshpass -p HIT-ices-511 scp -P 22333 root@$ip:/root/ExperimentTools/log.log ./"${ip}"_log.log
done
sshpass -p tianjianshan scp -P 22333 hexiang@192.168.1.102:/home/hexiang/workspace/pycharm/ExperimentTools/utils/Lab2/log.log ./system.log