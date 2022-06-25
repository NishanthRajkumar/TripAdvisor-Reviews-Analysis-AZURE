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

conf = SparkConf().setAppName("TripAdvisorReviews")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

df = spark.read.load(os.environ['READ_CSV_PATH'], format='csv', header=True)

columns_to_drop = ['sno', 'parse_count', 'review_id', 'title_review', 'review_preview', 'date', 'url_restaurant', 'author_id']
new_df = df.drop(*columns_to_drop)

final_df = new_df.filter(df.sample.isin(['Positive', 'Negative']))

final_df.write.option('header', True).mode('overwrite').csv(os.environ['WRITE_CSV_PATH'])