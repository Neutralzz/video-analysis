#coding=utf-8
import sys,os

import redis
import base64,time

global redis_cli,cache_path,store_path,cookies_path,log_path

redis_cli = redis.StrictRedis(host='127.0.0.1',port='6379')
cookies_path = "../config/cookies.sqlite"
cache_path = "../static/cache"
store_path = "../static/video"
log_path = "../log"



def main():
    global redis_cli,cache_path,store_path,cookies_path,log_path
    while(True):
        task_queue,link = redis_cli.blpop('TASK')
        logfile = log_path + '/' + str(base64.b64encode(link),encoding='utf-8') + '.log'
        link = str(link,encoding='utf-8')
        #print("you-get --debug -c %s -o %s --format=mp4 \"%s\" > %s 2>&1"%(cookies_path,cache_path,link,logfile))
        return_code = os.system("you-get --debug -c %s -o %s --format=mp4 \"%s\" > %s 2>&1"%(cookies_path,cache_path,link,logfile))
        if return_code == 0:
            title = ""
            f = open(logfile,'r')
            for line in f:
                if 'title' in line:
                    flag = False
                    for i in range(6,len(line)):
                        if (not flag) and line[i] == ' ':
                            continue
                        else:
                            flag = True
                            if line[i] != '\n':
                                title += line[i]
                    break
            filename = title + '.mp4'
            print("filename = %s"%filename)
            f.close()

            mv_code = os.system('mv -f \"%s/%s\" \"%s/%s\"'%(cache_path,filename,store_path,filename))
            if mv_code == 0:
                print("%s process finished."%link)
            else:
                # complete it
                pass


        else:
            # complete it 
            pass


        time.sleep(5)



if __name__ == '__main__':
    main()
