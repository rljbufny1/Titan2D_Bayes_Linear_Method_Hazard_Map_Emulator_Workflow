#!/bin/bash

echo "pegasus-s3-rm.sh: $@"

# Args:
# $1 - S3 URL Prefix
# $2 - S3 Bucket
# $3 - S3 Bucket Key

filelist=($(pegasus-s3 ls ${1}/${2}/${3}))

for file in "${filelist[@]}"
do
   #echo "$file"
   pegasus-s3 rm --force ${1}/${2}/$file
done

pegasus-s3 rm --force ${1}/${2}/${3}

:
