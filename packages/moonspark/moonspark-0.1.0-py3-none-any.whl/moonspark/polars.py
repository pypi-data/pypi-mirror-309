import pyarrow as pa
import polars as pl

def spark_to_polars(dataf):
    return pl.from_arrow(pa.Table.from_batches(dataf._collect_as_arrow()))

