Prog image client 
------------------


A python client for the [prog image server API](https://github.com/tobey/progimage-server)

Using `python3.6+`

Installation 
------------

```
pip install git+https://github.com/Tobey/progimage-client.git@0.0.1#egg=progimage-client
```

Usage
-----

Initailize session with server url and token

```python

from progimage_client import ProgImageClient

progimage = ProgImageClient(
                server_host='http://localhost:8000',
                server_token='a secret token',
            )

```

Use methods to retrieve, upload and transform images

```python
from progimage_client import transforms

# Retrieving 
progimage.get_one(<image_id>)
progimage.get_many([<image_id>, <image_id>])


# Creating
progimage.upload_one(<path to file>)
progimage.upload_many([<path to file>, <path to file>])
progimage.upload_by_url([<image url>, <image url>])

# Transforming
progimage.get_many([<image_id>, <image_id>], transform=transforms.THUMBNAIL)
progimage.get_many([<image_id>, <image_id>], transform=transforms.INVERT)
progimage.get_many([<image_id>, <image_id>], transform=transforms.ROTATE)
progimage.get_many([<image_id>, <image_id>], transform=transforms.PNG)
progimage.get_many([<image_id>, <image_id>], transform=transforms.JPEG)
```
