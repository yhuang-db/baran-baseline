python3.10 -m venv venv

source venv/bin/activate

python -m pip install wheel

python -m pip install --upgrade pip

python -m pip install --upgrade setuptools

python -m pip install -r requirements.txt

python main.py -t example_data.toml
