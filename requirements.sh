#!/bin/bash
list='os sys csv datetime requests re bs4'
for lib in $list; do
	sudo pip3 install $lib
done;
