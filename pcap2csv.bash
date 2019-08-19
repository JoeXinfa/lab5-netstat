#!/bin/bash

dir='/home/joseph/Documents/uta/secu/lab5'

cd $dir/firefox
for filename in *.pcap
do
  echo $filename
  #tshark -r $filename > $filename.txt
  tshark -r $filename -T fields -e frame.number -e ip.src -e ip.dst -e frame.len -e ip.proto -E separator=, > $filename.csv
done

cd $dir/tor
for filename in *.pcap
do
  echo $filename
  tshark -r $filename -T fields -e frame.number -e ip.src -e ip.dst -e frame.len -e ip.proto -E separator=, > $filename.csv
done

cd $dir/vpn
for filename in *.pcap
do
  echo $filename
  tshark -r $filename -T fields -e frame.number -e ip.src -e ip.dst -e frame.len -e ip.proto -E separator=, > $filename.csv
done
