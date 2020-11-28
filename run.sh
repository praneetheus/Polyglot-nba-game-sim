#!/bin/bash
npm install
pip3 install -r requirements.txt

swig -c++ -python -py3 predict.i 
g++ -c -fpic predict.cpp predict_wrap.cxx -I/usr/include/python3.6
g++ -shared predict.o predict_wrap.o -o _predict.so -lstdc++

g++ -O3 -Wall main.cpp loadfiles.cpp nb.cpp -o gnb

npm start