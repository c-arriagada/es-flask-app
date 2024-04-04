SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo $SCRIPT_DIR
pushd "$SCRIPT_DIR/.."
aws lambda update-function-code \
    --function-name  estilo_calico_backend \
    --zip-file fileb://estilo_calico_backend_updated.zip
popd