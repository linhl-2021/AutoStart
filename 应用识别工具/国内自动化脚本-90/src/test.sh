#!/bin/bash
bash update1.sh $1 $2 $3
python3 main.py $1 $2 $3
bash update2.sh $1 $2 $3
