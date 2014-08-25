#!/bin/bash

limit=$(rabbitmqctl status | grep vm_memory_limit,)
limit2=${limit:18}
limit_result=${limit2//\},/}


test=$(rabbitmqctl status | grep total,)
test2=${test:13}
result=${test2//\},/}

total_result=$(expr $result + 200000000)


if (($limit_result <= $total_result));
then
        echo "NOT OK"
        exit 1
else
        echo "Node is fine"
        exit 0
fi