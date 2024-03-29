import aiohttp
import asyncio
from contextlib import closing
from zipfile import ZipFile
import os

import mebar

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]
# create chunk_size const for 4 * 1024 kbs
CHUNK_SIZE = 4 * 1024 #kb

async def download_file(url:str):
    async with aiohttp.ClientSession() as session:
        # set timeout to None
        async with session.get(url, timeout = None) as response:
            # get filename and it's extension by str.split() method
            file_name = url.split('/')[-1]
            # get file_size by looking at their header['Content-Length']
            file_size = int(response.headers.get('Content-Length',0))
            
            if (response.status != 200): 
                print(f'Won\'\\t download {file_name}: message {response.status}')
                return

            # force to create download directory
            try :
                os.mkdir('./downloads/')
            except Exception as E:
                # otherwise will throw Exception if download dir is already exist
                pass

            zip_file_path = f'./downloads/{file_name}'
            with open(zip_file_path, 'wb') as f:
                # would work as well with ... as .... Pass parameter such as file_name and file_size
                bar = mebar.get_bar(file_name, file_size)

                # iterate file by chunks
                async for chunk in response.content.iter_chunked(CHUNK_SIZE):
                    if chunk:
                        size = f.write(chunk)
                        bar.update(size)
                        bar.refresh()

                # make sure to close otherwize ZipFile won't able to read the final .zip
                f.close()

                # close the bar as well
                bar.clear()
                
                print()
                print(f'{file_name} extract to downloads')

                # create myzip instance by file_path
                with ZipFile(zip_file_path) as myzip:
                    # assume the csv file name is the zip file name as well
                    file_name_exc = file_name.split('.')[0]
                    myzip.extract(f'{file_name_exc}.csv', path='downloads\\')
                    print(f'{url} Complete')



# gather coroutine with asyncio.gather(coros)
async def multiple(urls):
    tasks = [download_file(url) for url in urls]
    await asyncio.gather(*tasks)
        
# run with prefered high-level method asyncio.run() 
asyncio.run(multiple(download_uris)) # uncomment this
    
# or, run with low-level method
# call the event loop
# loop = asyncio.get_event_loop()

# then run until complete
# loop.run_until_complete(multiple(download_uris))