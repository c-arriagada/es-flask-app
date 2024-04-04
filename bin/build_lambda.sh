SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo $SCRIPT_DIR
pushd "$SCRIPT_DIR/.."
zip -r estilo_calico_backend_updated.zip app.py bios.py events.py db.py
popd