# Data Engineering YouTube Analysis Project by Darshil Parmar

## Project Overview
This project is designed to effectively manage, streamline, and analyze structured and semi-structured YouTube video data based on categories and trending metrics.

## Project Goals
1. Data Ingestion — Create a mechanism to ingest data from various sources.
2. ETL System — Transform raw data into a usable format.
3. Data Lake — Centralize storage for data from multiple sources.
4. Scalability — Ensure the system can scale with increasing data size.
5. Cloud — Utilize AWS for processing large datasets.
6. Reporting — Develop a dashboard to analyze key questions.

## Services Used
1. Amazon S3: An object storage service offering scalability, availability, and security.
2. AWS IAM: Enables secure management of access to AWS services and resources.
3. QuickSight: A serverless, scalable BI service for analytics.
4. AWS Glue: A serverless data integration service for analytics and machine learning.
5. AWS Lambda: A computing service to run code without server management.
6. AWS Athena: An interactive query service for analyzing data in S3 without loading it.

## Dataset Used
This dataset includes statistics (CSV files) on daily trending YouTube videos over many months, with up to 200 videos published daily across various regions. The data includes video title, channel title, publication time, tags, views, likes, dislikes, descriptions, and comment counts, along with a category ID for each region.

Link to dataset: [Kaggle Dataset](https://www.kaggle.com/datasets/datasnaek/youtube-new)

## Architecture Diagram
<img src="architecture.jpeg">