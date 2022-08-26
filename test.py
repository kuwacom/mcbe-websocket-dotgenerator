import time
from multiprocessing import Process,Manager


process_worker_num = 4



def xLineLoad(process_worker_num,process_num,returned_dict):
    print("process : "+str(process_num)+" is START")
    out = []
    for i in range(0,100,1):
        time.sleep(0.1)
        # print("prcIN : "+str(process_num) + " h_ => "+str(i))
        out.append([])
        for l in range(0,4,1):
            out[i].append(l)
    returned_dict[process_num] = out
    


if __name__ == '__main__':
    print("create Manager")
    manager = Manager()
    print("DONE")

    print("create dict")
    returned_dict = manager.dict()
    print("DONE")

    print("create process loop")
    for process_num in range(0,process_worker_num,1):
        print("process : "+str(process_num)+" is ON")
        process = Process(
            target=xLineLoad,
            kwargs={
                'process_worker_num': process_worker_num,
                'process_num': process_num,
                'returned_dict': returned_dict,
            })
        process.start()
    process.join()

    print(returned_dict)