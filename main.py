import aiohttp
import asyncio
# from tqdm import tqdm
from contextlib import closing
import os

import mebar

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    # "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    # "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    # "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    # "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    # "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

CHUNK_SIZE = 4 * 1024 #kb

async def download_file(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            file_name = url.split('/')[-1]
            file_size = int(response.headers.get('Content-Length',0))
            
            try :
                os.mkdir('./downloads/')
            except Exception as E:
                pass

            with open(f'./downloads/{file_name}', 'wb') as f:
                bar = mebar.get_bar(file_name, file_size)
                async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                    if chunk:
                        size = f.write(chunk)
                        bar.update(size)

async def multiple(urls):
    tasks = [download_file(url) for url in urls]
    await asyncio.gather(*tasks)
        
asyncio.run(multiple(download_uris))