#!/bin/bash

for f in rat-vanilla.png rat-splines.png; do
    convert -crop 480x250+250+250 $f $f
done
