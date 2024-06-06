#!/usr/bin/bash

./crawl.py
echo "Done crawling"

R=`ls -t nightly-*.json | head -1`

echo "Latest file is $R"

echo "Failures"
cat $R | jq ".yolo_runs_failed[].name"

echo "Success"
cat $R | jq ".yolo_runs[].name"

./s3.py $R
echo "Done uploading $R to s3"

./json2csv.py $R
echo "Done with json->csv"

./s3.py $R.csv
echo "Done uploading $R.csv to s3"

sqlite-utils insert my.db runs $R.csv --csv
echo "Done loading csv into my.db"

sqlite3 my.db ".schema" > schema.txt

sqlite3 ./my.db "select job_date, job_name, status, count(*) from runs group by job_date, job_name, status"
echo "Done with sql query"

./s3.py my.db
echo "Done uploading my.db to s3"

./s3.py schema.txt
echo "Done uploading schema.txt to s3"
