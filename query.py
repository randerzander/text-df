from dask_sql import Context
from dask.distributed import Client
import dask_cudf as dd

data_dir = "/raid/chess/pq/"

if __name__ == "__main__":
  client = Client("localhost:8786")

  ddf = dd.read_parquet(data_dir)
  c = Context()
  c.create_table("chess", ddf)
