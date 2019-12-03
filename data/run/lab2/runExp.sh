#!/bin/bash

if [ $# -ne 4 ]; then
  echo "$0 JAVA_PATH JAR_FILE_PATH DATA_DIR ALGO"
  exit
fi

DATA_DIR=$3
JAVA_PATH=$1
JAR_FILE_PATH=$2
ALGO_TYPE=$4

ROUND=400
POPULATION=200
COMP="false"
VERIFY="false"

for size in `ls $DATA_DIR`
do
  echo "calculate $size ..."
  $JAVA_PATH -jar $JAR_FILE_PATH $DATA_DIR/$size $ALGO_TYPE $ROUND $POPULATION $COMP $VERIFY > ./$ALGO_TYPE-$size-$ROUND-$POPULATION-$COMP-$VERIFY.log
  echo "calculate $size ends"
done