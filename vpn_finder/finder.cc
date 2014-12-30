/*
 * =====================================================================================
 *
 *       Filename:  finder.cc
 *
 *    Description:  VPN ServerList finder 
 *
 *        Version:  1.0
 *        Created:  2014年07月09日 11时37分23秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  tl
 *   Organization:  tl
 *
 * =====================================================================================
 */

#include <iostream>
#include <stdlib.h>

#include <string>
#include <vector>

#include <errno.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>
#include <signal.h>
#include <fstream>

#define UNUSED(x) (void)(x)



pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

std::string gen_call_cmd(std::string site) {
    std::string cmd;
    cmd.append("echo ");
    cmd.append(site + " : ");
    cmd.append("`ping -c 3 " + site + " | " + "grep rtt" + " | ");
    cmd.append("awk -F \"=\" '{print $2}' | ");
    cmd.append("awk -F \"/\" '{print $2}'`");
    return cmd;
}



void *thr(void *args) {
    pthread_mutex_lock(&mutex);
    std::string server_name((char *)args);
    pthread_mutex_unlock(&mutex);
    system(gen_call_cmd(server_name).c_str());
#if 0
    system("echo thr1 : `ping -c 1 www.sina.com.cn | grep rtt | awk -F \"=\" '{print $2}' \
            | awk -F \"/\" '{print $2}'`");
#endif

    return NULL;

}

void init_server_list(std::vector<std::string> &vec) {
    vec.clear();
    std::string filename = "./vpnlist.txt";
    std::ifstream instream(filename.c_str());
    if(!instream.good()) {
        std::cout << "vpnlist.txt is not exists" << std::endl;
        exit(1);
    }
    std::string line;
    while(std::getline(instream, line)) {
        vec.push_back(line);
    }
    return;
}



int main(int argc, char *argv[]) {
    UNUSED(argc);
    UNUSED(argv);
    std::vector<std::string> vec;
    init_server_list(vec);
    int v_size = vec.size();
    pthread_t *p_arr = NULL;

    try {
        p_arr = new pthread_t[v_size];
    } catch (std::bad_alloc &e) {
        std::cout << " bad_alloc" << e.what();
    }

    for(int i = 0; i < v_size; i++) {
        pthread_create(p_arr + i, NULL, thr, (void *)(vec.at(i).c_str()));
        while(1) {
            if(pthread_kill(*(p_arr + i), 0) == 0) {
                break;
            }
        }
    }
    for(int i = 0 ;i < v_size; i++) {
        pthread_join(*(p_arr + i), NULL);
    }
    delete []p_arr;

    return 0;
}
