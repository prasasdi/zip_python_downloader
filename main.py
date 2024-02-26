import aiohttp
import asyncio
from tqdm import tqdm
from contextlib import closing
import os

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    # "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    # "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    # "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    # "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    # "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

r_semaphone = asyncio.Semaphore(10)

CHUNK_SIZE = 4 * 1024 #kb

async def download_file(url:str):
    filename = url.split('/')[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try :
                os.mkdir('./downloads/')
            except Exception as E:
                pass
            with open(f'./downloads/{filename}', 'wb') as f, tqdm(
                desc = filename,
                total = int(response.headers.get('Content-Length',0)),
                unit = 'iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                    if chunk:
                        size = f.write(chunk)
                        bar.update(size)

# [asyncio.run(download_file(uri)) for uri in download_uris]
async def multiple(urls):
    tasks = [download_file(url) for url in urls]
    await asyncio.gather(*tasks)
        
asyncio.run(multiple(download_uris))