from zipfile import ZipFile

url:str = "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip"
file_name = url.split('/')[-1]
file_name_exc = file_name.split('.')[0]

with ZipFile('downloads\Divvy_Trips_2018_Q4.zip') as myzip:
    lists = myzip.namelist()
    # print isi konten dari .zip
    print(lists)
    myzip.extract(f'{file_name_exc}.csv', path='downloads\\')
    