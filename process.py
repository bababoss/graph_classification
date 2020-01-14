from concurrent import futures
import os,glob,sys,requests
from pathlib import Path



    
save_path="/home/ubuntu/projects/continual/dataset/"
def download_file(url,cls):
    try:
        local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            save_path_cls=save_path+cls
            print(save_path_cls)
            Path(save_path_cls).mkdir(parents=True, exist_ok=True)
            with open(save_path_cls+"/"+local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        # f.flush()
        return [url,cls]
    except:
        return [None,url,cls]

    
with open("vis10cat.txt", "r") as f:
    data=f.readlines()
    
    wait_for = []
    with futures.ThreadPoolExecutor(max_workers=2) as ex:

        for d in data:
            url=d.split("\t")[-1].split("\n")[0]
            cls=d.split("\t")[0]
            w=ex.submit(download_file, url,cls)
            wait_for.append(w)

    f1 = open("processed_url.txt", "a")
    f2 = open("failed_url.txt", "a")

    for f in futures.as_completed(wait_for):
        if f.result()[0]:
            f1.write(f.result()[1]+"\t"+f.result()[0]+"\n")
        else:
            f2.write(f.result()[2]+"\t"+f.result()[1]+"\n")
        print('main: result: {}'.format(f.result()[0]))
    f1.close()
    f2.close()