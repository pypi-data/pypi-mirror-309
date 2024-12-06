# Download videos from toutiao.com

## Installation

```bash
python3 -m pip install toutiao-video
```

## Usage

### Use in CMD
```bash
toutiao --help

toutiao -u xxxxx -t xxxxx
toutiao -u xxxxx -t xxxxx -d output
toutiao -u xxxxx -t xxxxx -l 5
toutiao -u xxxxx -t xxxxx -l 1 -d 1080p
toutiao -u xxxxx -t xxxxx -l 10 --dryrun
```

### Use in Python

```python

from toutiao.core import TouTiao

toutiao = TouTiao(user_id='user_id', tt_webid='tt_webid')

for n, item in enumerate(toutiao.list_user_feed(), 1):
    if n > 5:
        break()
    print(item)        
```
