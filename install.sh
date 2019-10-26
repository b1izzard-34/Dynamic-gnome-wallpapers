#! /bin/bash

echo "Adding $1 to wallpapers ..."
echo "Starting download ..."

svn checkout https://github.com/b1izzard-34/Dynamic-gnome-wallpapers/trunk/$1

cd $1
sudo mkdir /usr/share/backgrounds/gnome/$1-timed
sudo cp $1*.jpeg /usr/share/backgrounds/gnome/$1-timed
sudo cp $1-timed.xml /usr/share/backgrounds/gnome
sudo cp $1.xml /usr/share/gnome-background-properties
echo "Added $1 dynamic wallpaper!"

echo "Cleaning up ..."
rm -rf $1
