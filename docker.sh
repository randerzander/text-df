CMD=$1
#CMD=${CMD:-bash}
CMD=${CMD:-/opt/conda/envs/dsql/bin/jupyter-lab --ip="0.0.0.0" --allow-root --NotebookApp.token=""}

IMAGE="randerzander/pynds"

project=${PWD##*/} 

docker run --rm --gpus all -it \
  -p 8888:8888 \
  -p 8787:8787 \
  -v /raid:/raid \
  -v $(pwd):/$project \
  --hostname $HOSTNAME \
  $IMAGE $CMD
