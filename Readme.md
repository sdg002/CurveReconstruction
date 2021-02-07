# Getting back a smooth curve from a noisy background

## Overview
we have a picture with a smooth curve (circle, parabola) and dotted with salt pepper noise. We want to remove the noise and just get to the smooth curve.


## Next steps
- Try reducing the since wave and extract patches
- Create a star shape
- Create a HTML result from independent picture output and another accompanying output JSON which contains the parameters used for the generator

## Changes to algo
- Capture patch window size, 
- Capture line statistics
- Line quality - What is the max allowable separation of points in a RANSAC line - this determines the quality?
- Line quality - What is the average density of points along the line length?
- 



# References
- Dataset used for CONSAC paper https://github.com/trungtpham/RCMSA/tree/master/data/AdelaideRMF