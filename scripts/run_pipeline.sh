#!/bin/bash
set -e

# Step 1: Run the pipeline to generate recipes_merged.csv.gz
echo "Running the ETL pipeline..."
# python src/app/run_all.py

# Check if file is produced
if [ ! -f data/clustering/recipes_merged.csv.gz ]; then
    echo "ERROR: Output gzip not found: data/clustering/recipes_merged.csv.gz" >&2
    exit 1
fi

echo "Uploading data/clustering/recipes_merged.csv.gz to S3..."
aws s3 cp data/clustering/recipes_merged.csv.gz s3://mangetamain/recipes_merged.csv.gz.1

echo "Done. Uploaded to s3://mangetamain/recipes_merged.csv.gz"
