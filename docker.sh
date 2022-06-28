CMD=$1
CMD=${CMD:-bash}

IMAGE="randerzander/text-df"

project=${PWD##*/} 

docker run --rm --gpus all -it \
  -p 8888:8888 \
  -p 8787:8787 \
  -v /raid:/raid \
  -v $(pwd):/$project \
  --hostname $HOSTNAME \
  $IMAGE $CMD
