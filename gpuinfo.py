#!/usr/bin/env python
# gpuinfo.py [DELAY]
# dump gpu usage per user every 24 hours
# Thanks @matpalm for his code on https://gist.github.com/matpalm/9c0c7c6a6f3681a0d39d
# @author: Yuanwei Wang
# All Rights Reserved

import subprocess, json, time, sys
try:
    delay = int(sys.argv[1])
except:
    delay = 60  # second(s)

count = dict()

for i in range(60 * 24):
    cmd = ['nvidia-smi', 'pmon', '-c', '1']
    process_ids = subprocess.check_output(cmd).strip().split(b'\n')[2:]
    for id in process_ids:
        gpu, pid = id.strip().split()[:2]
        # print(int(gpu), str(pid))
        cmd1 = ['ps', '-u', '-p', pid.decode("utf-8")]
        ps_ids = subprocess.check_output(cmd1).strip().split(b'\n')[1].decode("utf-8")
        # print(ps_ids)
        ps_ids = ps_ids.split(maxsplit=10)
        user = ps_ids[0]
        args = ps_ids[-1]
        if user not in count:
            count[user] = {'time': 1, 'args': [args]}
        else:
            count[user]['time'] += 1
            if args not in count[user]['args']:
                count[user]['args'].append(args)
    time.sleep(delay)

with open('/var/log/gpuinfo/gpuinfo_{}.txt'.format(time.strftime('%Y%m%d')), 'w') as fw:
    json.dump(count, fw)
