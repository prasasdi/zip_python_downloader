import aiohttp
import asyncio
import os

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

CHUNK_SIZE = 4 * 1024 #kb

async def download_file(url:str):
    filename = url.split('/')[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try :
                os.mkdir('./downloads/')
            except Exception as E:
                pass
            with open(f'./downloads/{filename}', 'wb') as f:
                async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

asyncio.run(download_file(download_uris[0]))