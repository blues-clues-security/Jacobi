#!/bin/bash

echo "[*] Welcome to Jacobi Viewer for Moloch"
echo "[*] Please select the query or queries you want to start analyzing"
echo "[*] Query 1" "Query Description 1" 
echo "[*] Query 2" "Query Description 2" 
echo "[*] Query 3" "Query Description 3"

if [ $? -eq "-h" ]
	then echo "Jacobi Viewer help file '\r\n' Next line"
fi

if [ $# -eq 0 ]
	then echo "You select no query, you get no results"
fi

if [ $# -eq 1 ]
	then echo "You've selected query 1"
fi


echo $#
