#!/usr/bin/env python
# coding: utf-8

# ## Preprocess_reviews_dataset
# 
# 
# 

# Import Required libraries
import os
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("TripAdvisorReviewsFilter")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

df = spark.read.load(os.environ['READ_CSV_PATH'], format='csv', header=True)

negative_df = df.where(df.sentiment == 'Negative')
positive_df = df.where(df.sentiment == 'Positive')

negative_row_count = negative_df.count()

positive_df_filtered = positive_df.limit(negative_row_count)

final_df = negative_df.union(positive_df_filtered)

final_df.write.option('header', True).mode('overwrite').csv(os.environ['WRITE_CSV_PATH'])