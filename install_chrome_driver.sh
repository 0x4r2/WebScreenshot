#!/bin/bash
# Chrome Driver Install Latest Version

chrome_url="http://chromedriver.storage.googleapis.com/"
last_version=$(curl -s   http://chromedriver.storage.googleapis.com/ | grep -oP "<Key>\K[^<]*chromedriver_linux64.zip" |sort -h |tail -1)
file="/tmp/chrome_driver.zip"
wget "$chrome_url$last_version" -O $file
sudo unzip -o -d /usr/local/bin  $file
rm -rf  $file
echo "Versión actualizada: $last_version"
