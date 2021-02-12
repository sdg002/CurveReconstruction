# Getting back a smooth curve from a noisy background

## Overview
we have a picture with a smooth curve (circle, parabola) and dotted with salt pepper noise. We want to remove the noise and just get to the smooth curve.

## What was I thinking?
- Use sequential RANSAC and find all lines in small patches
- Eliminate all other points  -just keep the points in the vicnity of these small lines
- Test using 2 intersecting lines
- Good to have 1 more sample of intersecting curves. e.g. 2 circles side by side or 2 parabolas in a top-down manner



## Next steps
- Create a star shape
- Create a HTML result from independent picture output and another accompanying output JSON which contains the parameters used for the generator
- How do you read Matlab .MAT file (see read me)
- Consider using Normal distribution for determining the gap between 2 consecutive points

## Changes to algo
- Capture patch window size, 
- Capture line statistics
- Line quality - What is the max allowable separation of points in a RANSAC line - this determines the quality?
- Line quality - What is the average density of points along the line length?
- 



# References
- Dataset used for CONSAC paper https://github.com/trungtpham/RCMSA/tree/master/data/AdelaideRMF
