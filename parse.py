from dask_cuda import LocalCUDACluster
from dask.distributed import Client
import dask_cudf as dd

data_dir = "/raid/chess/"

if __name__ == "__main__":
  cluster = LocalCUDACluster(
    jit_unspill=True,
    rmm_pool_size="12GiB",
    device_memory_limit="14GiB"
  )
  client = Client(cluster)

  #ddf = dd.read_text(data_dir+"*_2014*.pgn", delimiter="\n\n[").to_frame()
  ddf = dd.read_text(data_dir+"*.pgn", delimiter="\n\n[").to_frame()
  ddf["header"] = ddf[0].str.split("]\n\n").list.get(0)
  ddf["game"] = ddf[0].str.split("]\n\n").list.get(1)
  ddf = ddf[["header", "game"]]

  for field in [
    "Event",
    "Site",
    "White",
    "Black",
    "Result",
    "WhiteElo",
    "BlackElo",
    "WhiteRatingDiff",
    "BlackRatingDiff",
    "ECO",
    "Opening",
    "TimeControl",
    "UTCDate",
    "UTCTime",
    "Termination",
    ]:
    ddf[field] = ddf["header"].str.split(field+" ").list.get(1)
    ddf[field] = ddf[field].str.split("\"").list.get(1)

  ddf = ddf.drop("header", axis=1)
  ddf["first_move"] = ddf["game"].str.split(" 2").list.get(0)

  move_count = ddf["game"].str.count(" ")/3
  ddf["move_count"] = move_count.astype("int")

  ddf["checks"] = ddf["game"].str.count("\+")
  print(ddf.head())

  ddf.repartition(partition_size="512MiB").to_parquet(data_dir+"pq/", overwrite=True)
