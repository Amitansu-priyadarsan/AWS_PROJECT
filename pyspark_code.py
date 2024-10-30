import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

# parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize contexts
spark_context = SparkContext()
glue_context = GlueContext(spark_context)
spark_session = glue_context.spark_session
job_instance = Job(glue_context)
job_instance.init(args['JOB_NAME'], args)

# Define predicate for filtering
region_filter = "region IN ('ca', 'us', 'gb')"

# Load data from Glue Catalog
input_data = glue_context.create_dynamic_frame.from_catalog(
    database="db_youtube_raw",
    table_name="raw_statistics",
    transformation_ctx="input_data",
    push_down_predicate=region_filter
)

# Map columns
mapped_data = ApplyMapping.apply(
    frame=input_data,
    mappings=[
        ("video_id", "string", "video_id", "string"),
        ("trending_date", "string", "trending_date", "string"),
        ("title", "string", "title", "string"),
        ("channel_title", "string", "channel_title", "string"),
        ("category_id", "long", "category_id", "long"),
        ("publish_time", "string", "publish_time", "string"),
        ("tags", "string", "tags", "string"),
        ("views", "long", "views", "long"),
        ("likes", "long", "likes", "long"),
        ("dislikes", "long", "dislikes", "long"),
        ("comment_count", "long", "comment_count", "long"),
        ("thumbnail_link", "string", "thumbnail_link", "string"),
        ("comments_disabled", "boolean", "comments_disabled", "boolean"),
        ("ratings_disabled", "boolean", "ratings_disabled", "boolean"),
        ("video_error_or_removed", "boolean", "video_error_or_removed", "boolean"),
        ("description", "string", "description", "string"),
        ("region", "string", "region", "string")
    ],
    transformation_ctx="mapped_data"
)

# Resolve choices and drop null fields
resolved_data = ResolveChoice.apply(frame=mapped_data, choice="make_struct", transformation_ctx="resolved_data")
cleaned_data = DropNullFields.apply(frame=resolved_data, transformation_ctx="cleaned_data")

# Write cleaned data to S3
final_dynamic_frame = DynamicFrame.fromDF(cleaned_data.toDF().coalesce(1), glue_context, "final_dynamic_frame")
glue_context.write_dynamic_frame.from_options(
    frame=final_dynamic_frame,
    connection_type="s3",
    connection_options={"path": "s3://my-bucket/youtube/cleaned_data/", "partitionKeys": ["region"]},
    format="parquet",
    transformation_ctx="output_data"
)

job_instance.commit()
