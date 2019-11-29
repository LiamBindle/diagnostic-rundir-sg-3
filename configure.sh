#!/bin/bash

[ $# == 3 ] || exit

sed -i "s/^.*STRETCH_FACTOR\s*=\s*[0-9\.\-]*\s*$/STRETCH_FACTOR=${1}/g" runConfig.sh
sed -i "s/^.*TARGET_LAT\s*=\s*[0-9\.\-]*\s*$/TARGET_LAT=${2}/g"         runConfig.sh
sed -i "s/^.*TARGET_LON\s*=\s*[0-9\.\-]*\s*$/TARGET_LON=${3}/g"         runConfig.sh
