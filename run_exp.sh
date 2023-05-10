rm -rf venv

python3.10 -m venv venv

source venv/bin/activate

python -m pip install wheel

python -m pip install --upgrade pip

python -m pip install --upgrade setuptools

python -m pip install -r requirements.txt

if [ $# -eq 1 ]; then
  toml_file="$1"
fi

echo "BARAN: START exp $toml_file."

python main.py -t "$toml_file"
