### About

Given a jenkins pipeline job, crawl all the jobs spawned by that pipeline, gather the testResults, and save them to `nightly-yyy-mm-dd.json`.

```
{
  "nightly": {
    "id": 16,
    "url": "job/xxx/job/Nightly/job/yyy/job/parent-job-zzzz/16/api/json/?depth=3",
    "timestamp": 1717345980084,
    "timestamp_human": "2024-06-02T16:33:00.084000",
    "failed": false
  },
  "scenario": [
    {
      "name": "xxx-devel-rhel8.9-scenariozzz",
      "id": "16",
      "url": "job/aaa/job/Nightly/job/bbb/job/xxx-devel-rhel8.9-scenariozzz/16/",
      "test_results": [
        {
          "age": 0,
          "className": "tests.api.execution_environments.test_ee_association.TestEEAssociation",
          "duration": 102.404,
          "errorDetails": null,
          "errorStackTrace": null,
          "failedSince": 0,
          "name": "test_ee_pull_registry_specified[always]",
          "properties": {},
          "skipped": false,
          "skippedMessage": null,
          "status": "PASSED",
          "stderr": null,
          "stdout": null
        },
        {
          "age": 0,
          "className": "tests.api.execution_environments.test_ee_association.TestEEAssociation",
          "duration": 79.463,
          "errorDetails": null,
          "errorStackTrace": null,
          "failedSince": 0,
          "name": "test_ee_pull_registry_specified[missing]",
          "properties": {},
          "skipped": false,
          "skippedMessage": null,
          "status": "PASSED",
          "stderr": null,
          "stdout": null
        },
    {
      "name": "xxx-devel-rhel8.9-scenarioyyy",
      "id": "16",
      "url": "job/aaa/job/Nightly/job/bbb/job/xxx-devel-rhel8.9-scenarioyyy/16/",
      "test_results": [
        {
          "age": 17,
          "className": "tests.api.execution_environments.test_ee_association.TestEEAssociation",
          "duration": 1.826,
          "errorDetails": null,
          "errorStackTrace": null,
          "failedSince": 0,
          "name": "test_ee_pull_registry_specified[always]",
          "properties": {},
          "skipped": true,
          "skippedMessage": "Test requires x86_64 install",
          "status": "SKIPPED",
          "stderr": null,
          "stdout": null
        },
        ...
      ]
   },
   ...
 ]
}

```

### Quickstart

Fill in `.env`

```
./crawl.py
cat nightly-*.json
```

### Misc

`s3.py` requires boto3 and AWS / S3 cred setup and bucket name(s) that are hard-coded
