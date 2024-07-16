#!/usr/bin/bash

rm -f ci.db

scripts/iconv.py sample-data/jenkins_data.csv > sample-data/jenkins_data_a.csv
csvtool cat sample-data/jenkins_data_a.csv  > sample-data/jenkins_data_b.csv
sqlite-utils insert ci.db jenkins sample-data/jenkins_data_b.csv --csv --detect-types
csvsql -i postgresql sample-data/jenkins_data_b.csv > postgres-schema/jenkins.sql

scripts/iconv.py sample-data/junit_data.csv > sample-data/junit_data_a.csv
csvtool cat sample-data/junit_data_a.csv  > sample-data/junit_data_b.csv
csvsql -i postgresql sample-data/junit_data_b.csv > postgres-schema/junit.sql

rm -f ci.sql
