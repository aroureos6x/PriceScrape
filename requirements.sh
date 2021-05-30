#!/bin/bash
list='os sys getpass csv datetime requests re bs4'
for lib in $list; do
	sudo pip3 install $lib
done;