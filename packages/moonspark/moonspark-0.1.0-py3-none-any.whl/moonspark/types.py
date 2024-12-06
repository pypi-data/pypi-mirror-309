import pyspark.sql.dataframe as SparkDataFrame

SparkDataFrame.len = property(lambda x: x.count())
SparkDataFrame.shape = property(lambda x: (x.count(), len(x.columns)))
SparkDataFrame.pipe = lambda x, func, *args, **kwargs: func(x, *args, **kwargs)
