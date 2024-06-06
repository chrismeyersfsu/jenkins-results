#!/usr/bin/env python3

import sys

from common.s3 import upload_to_s3

upload_to_s3(sys.argv[1])

