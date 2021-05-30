#!/bin/bash
list='datetime requests bs4'
for lib in $list; do
	sudo pip3 install $lib
done;
