#!/bin/bash

# to change:
#     bandwidth:         --bwlimit
#     my server ip:      ...
#     source directory:  .../a224/
#     destiny directory: ./

while [ 1 ]
do
    #Transfer to another tokyo instance
    #rsync --remove-source-files --progress -P   -havz  /mnt/ee/   ubuntu@54.249.146.239:/mnt/myvid/
    rsync  --progress -P   -havze "ssh -i /home/ubuntu/.ssh/ec2tokyo_kp.pem"  ubuntu@54.248.189.134:/media/my/cc/   /mnt/cc0405/

    #rsync --remove-source-files --progress -P   -havze "ssh -i /home/ubuntu/.ssh/ec2tokyo_kp.pem"    /mnt/dd/   ubuntu@54.249.146.239:/mnt/myvid/

    #rsync -avz --partial source 

    #rsync --remove-source-files --progress -P  --bwlimit=111 -avze "ssh -i /home/za/.ssh/ec2tokyo_kp.pem" ubuntu@54.248.189.134:/home/ubuntu/tmp/a224/   /home/za/Videos/materials/225/
    #rsync --remove-source-files --progress -P  --bwlimit=289 -avze "ssh -i /home/za/.ssh/ec2tokyo_kp.pem" ubuntu@54.248.189.134:/media/my/cc/   /home/za/Videos/materials/34/
    #no speed limit :
    #rsync --remove-source-files --progress -P   -havze "ssh -i /home/za/.ssh/ec2tokyo_kp.pem" ubuntu@54.248.189.134:/media/my/cc/   /home/za/Videos/materials/34/


    # == can be used samely?
    if [ "$?" = "0" ] ; then
        echo "rsync completed normally"
        exit
    else
        echo "Rsync failure. Backing off and retrying..."
        sleep 180
    fi
done