#!/bin/bash

limit=$(rabbitmqctl status | grep disk_free_limit,)
limit2=${limit:18}
limit_result=${limit2//\},/}


test=$(rabbitmqctl status | grep disk_free,)
test2=${test:12}
result=${test2//\},/}

total_limit_result=$(expr $limit_result + 500000000)



if (($total_limit_result >= $result));
then
        echo "NOT OK"
        exit 1
else
        echo "Node is fine"
        exit 0
fi
