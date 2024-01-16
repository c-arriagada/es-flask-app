#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "$SCRIPT_DIR"
# p="$1" # First argument "archive prefix directory name"
# d="$2" # Second argument "source directory name"
# z="$3" # Third argument "result ZIP archive name without .zip"
# [ -e "$p" -o -e "${z}.zip" ] && return "Prefix directory name: $p Or target zip file name: ${z}.zip exist in PWD, cannot continue"
tmp="$(mktemp)" 

echo "Creating temporary folder: $tmp"
echo "Creating temporary 'es-flask-app/python' directory where all Python deps will be placed."

gtar cf "$tmp" -C "$SCRIPT_DIR/../.venv/lib/python3.9/site-packages" --transform "s|^|python/|" "."
gtar xf "$tmp"

## BEFORE YOU ZIP THIS FILE AND UPLOAD TO AWS
# When you are running the estilo-calico app locally, you'll need a version of psycopg2
# that is compatible with the arm64 architecture that Mac machines use (assuming you're on a Mac laptop).
#
# However, in the cloud, AWS needs a version of psycopg2 that is compatible with x86_64 architectures, 
# (Intel chips have x86_64 instruction sets).
#
# So the problem is, we need to run one version of the app on a Mac, and we need to build and upload
# a different version to the cloud. So in our build script, we will have to override the pip installed
# psycopg binaries before we push to AWS.
echo "Removing psycopg2 binary and replacing with AWS-compatible psycopg2"
rm -r "$SCRIPT_DIR/../python/psycopg2"
cp -r ~/code/awslambda-psycopg2/psycopg2-3.9 "$SCRIPT_DIR/../python/psycopg2/"

echo "Zipping python folder to create lambda layer archive"
zip -rq "$SCRIPT_DIR/../estilo-calico-deps-layer.zip" "python"

# Cleanup 

echo "Cleaning up - removing temporary folders"
rm "$tmp"
rm -r "python"
