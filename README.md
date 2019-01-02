# Example using scrapy to scrape [fara.gov](https://efile.fara.gov/pls/apex/f?p=185:130:0::NO:RP,130:P130_DATERANGE:N)


## Getting started

### Sample test data
Sample test data is in the root project directory in a file named `data.json`

### System requirements
[Python 3.6+](https://www.python.org/)

[pip](https://pip.pypa.io/en/stable/installing/)  - Already installed in the required Python version

### Setting up local environment
Run these commands in order from the project root:
```
python3 -m venv .
source bin/activate
pip install -r requirements.txt
```

### Running tests
Run `pytest simulation -v -s` to run tests


### Starting the crawler
Run the following command to start crawling:

`python run.py`

**_Notes_**: 
1. Download delay has been set to 2 so you may need to grab some coffee when waiting for the crawling to finish.

2. When the crawler is done, the crawled principals data is saved in `principals_data.json` in the root directory.

3. Foregin principal Registration dates are set to use `US/Eastern` timezone
