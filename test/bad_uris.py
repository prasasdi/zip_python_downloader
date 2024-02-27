import aiohttp
import asyncio


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

# try to get file_size from their header
async def get_header(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as r:
            print(f'header for {url} ----->')
            print(f'{r}\nResponse Status: {r.status}')
            print()


async def gather_uris(urls):
    coros = [get_header(url) for url in urls]
    await asyncio.gather(*coros)

asyncio.run(gather_uris(download_uris))