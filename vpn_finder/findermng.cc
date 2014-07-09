/*
 * =====================================================================================
 *
 *       Filename:  findermng.cc
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  2014年07月09日 14时19分48秒
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  tl
 *   Organization:  tl
 *
 * =====================================================================================
 */

#include <iostream>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <algorithm>
#include <vector>
#define UNUSED(x) (void)(x)

std::string &ltrim(std::string &s) {
    s.erase(s.begin(), 
            std::find_if(s.begin(), s.end(), 
                std::not1(std::ptr_fun<int, int>(std::isspace))));
    return s;
}

std::string &rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), 
                s.rend(), 
                std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s.end());
    return s;
}

std::string &trim(std::string &s) {
    return ltrim(rtrim(s));
}

bool cmpf(std::string e1, std::string e2) {
    int pose1 = 0;
    int pose2 = 0;
    pose1 = e1.find(":", 0);
    pose2 = e2.find(":", 0);

    std::string cmpstr1 = e1.substr(pose1 + 1, e1.size());
    std::string cmpstr2 = e2.substr(pose2 + 1, e2.size());

    cmpstr1 = trim(cmpstr1);
    cmpstr2 = trim(cmpstr2);
    //std::cout << cmpstr1 << std::endl;
    //std::cout << cmpstr2 << std::endl;
    if(std::atof(cmpstr1.c_str()) <= std::atof(cmpstr2.c_str()))
        return true;
    return false;
}


int main(int argc, char *argv[]) {
    UNUSED(argc);
    UNUSED(argv);

    FILE *pstream = popen("./finder", "r");
    char buf[1024];
    std::cout << "CAN YOU FUNCKING WAIT ME ?" << std::endl;
    std::vector<std::string> rvec;
    while(!feof(pstream)) {
        std::cout << ".";
        fflush(stdout);
        if(fgets(buf, 1024, pstream) == NULL) {
            std::cout << std::endl;
            break;
        } else {
            rvec.push_back(buf);
        }
    }

    pclose(pstream);

    std::cout << "VPN list by time: " << std::endl;

    std::sort(rvec.begin(), rvec.end(), cmpf);

    std::vector<std::string>::iterator it = rvec.begin();
    for(; it != rvec.end(); it++) {
        std::cout << (*it);
    }

    return 0;
}
