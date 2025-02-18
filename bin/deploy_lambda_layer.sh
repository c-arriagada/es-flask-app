SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo $SCRIPT_DIR
pushd "$SCRIPT_DIR/.."
aws lambda publish-layer-version \
    --layer-name estilo-calico-deps \
    --description "Updated layer version" \
    --zip-file fileb://estilo-calico-deps-layer.zip \
    --compatible-runtimes python3.8 python3.9
popd