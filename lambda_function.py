import awswrangler as wr
import pandas as pd
import urllib.parse
import os

# Load environment variables
s3_cleansed_path = os.environ['S3_CLEANSED_PATH']
glue_db_name = os.environ['GLUE_DATABASE_NAME']
glue_table_name = os.environ['GLUE_TABLE_NAME']
write_mode = os.environ['WRITE_MODE']

def lambda_handler(event, context):
    # Extract bucket and key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        # Read JSON file from S3
        raw_df = wr.s3.read_json(f's3://{bucket_name}/{object_key}')

        # Normalize the JSON data
        normalized_df = pd.json_normalize(raw_df['items'])

        # Write normalized DataFrame to S3 in Parquet format
        response = wr.s3.to_parquet(
            df=normalized_df,
            path=s3_cleansed_path,
            dataset=True,
            database=glue_db_name,
            table=glue_table_name,
            mode=write_mode
        )

        return response
    except Exception as error:
        print(f"Error processing object {object_key} from bucket {bucket_name}. Error: {error}")
        raise error
