#!/bin/bash

time for i in $(seq 1 15); do python3.7 ./test.py & ; done
