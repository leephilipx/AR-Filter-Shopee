# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 00:40:18 2021

@author: Philip
"""

import requests

with open('pic1.jpg', 'wb') as handle:
        response = requests.get('https://cf.shopee.sg/file/493e3c3eb6981e12ffb57981d9e5537b', stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)