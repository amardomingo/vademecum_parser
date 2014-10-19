#!/bin/bash

echo -n "Cleaning..."
rm -f vademecum.json vademecum_encoded.json dictionary.*
echo " done!"

echo -n "Getting the data..."
python parser.py >/dev/null
echo " done!"

echo -n "Encoding the data... "
native2ascii -encoding UTF-8 -reverse vademecum.json vademecum_encoded.json
echo " done!"
