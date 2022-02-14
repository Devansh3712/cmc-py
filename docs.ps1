$ErrorActionPreference = "silentlyContinue"
rmdir ./docs
pdoc3 --html ./cmc --output-dir ./docs --force
mv ./docs/cmc/* ./docs
rmdir ./docs/cmc
