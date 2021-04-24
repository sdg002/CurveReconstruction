# Getting back a smooth curve from a noisy background

## Overview
we have a picture with a smooth curve (circle, parabola) and dotted with salt pepper noise. We want to remove the noise and just get to the smooth curve.

## What was I thinking?
- Test the diagonal lines 
- Use sequential RANSAC and find all lines in small patches
- Eliminate all other points  -just keep the points in the vicnity of these small lines
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


# Ideas on the algorithm
- Image as an input
- Add some padding all over the original image
- Decide on a kernel size
- Extract patches with a stride
## How to handle the patches?
- Find the median nearest neighbour distance
- Use the median to do an adaptive RANSAC iteratively
- For every patch, generate a collection of lines (sequential ransac)
- Collect adjacent patches in 2X2 system
- You were here - think of a Relational model
## Relational model
-   Point
-   Patch
-   Line
-   2X2Clusters
-   Join lines from adjacent 2X2Clusters into something more continous
-   But, how do you decide to join 2 adjacent 2X2 Clusters when there are more than 1 overlapping clusters
-   Bottom line, preserve information at all stages
-   Quality of a line can be also judged by the uniformity of the distance betwen the projected points
-   What about symmetry
## How to save the final file? 
- Do this at the very endJust strip off the padding and you will get back the original image size


# Quality of a RANSAC line
RANSAC will give you a straight line by only considering the perpendicular distance of the inliers to the line.
What RANSAC does not take into account is the density of the projection of the points along the line.
Think of the following line:
    . . . . . .       .
The points are well aligned. The last point, even though a perfect inlier in RANSACA terms, might not be a good visual/logical candiate

## How to judge the quality of a line determined by RANSAC?
- Dvide the line into overlapping segments using a stride. 
- Count the number of points in every segment
- Use a threshold. Call this *line_density*
- Any segment less than *line_density* is eliminated
- Join the left over segments to produce new lines
- Another threshold to consider is the maximum gap between 2 adjacent lines. Call this *max_gap*
- Any 2 adjacent lines are considered separate lines if the gap between them exceeds this threshold *max_gap*


# Abandon the idea of Patches for now.
- Too difficult and not guaranteed to give results immediately
- Rather focus on a smaller image
Shrink the image 
## Consecutive RANSAC line 
- Use the mean nearest neighbour metric to determine threshold (use 0.5 to 1.5)
- Find the RANSAC lines
- Build an in-memory database of all such lines

## Consecutive RANSAC circle
- Use the mean nearest neighbour metric
- Does Scikit algo for Circles work?

## How to look for continuity?
- You now have a database of line segments and arcs
- Some spatial indexing will help here
- Pick the longest line or longest arc
- Should we pick the line/arc just on the merit of length. Why not pixel density also?
- Pick the first shape --> pick closest shape --> how good is the join between shape1 and shape2

## How to measure the goodness of a shape join?
 - Do sequential RANSAC on parabola
 - Use mean NND
 - Try sequential RANSAC Circles on parabola
 - Use mean NND
 

# Paper on J Linkage
This appears to be a very good one
http://www.diegm.uniud.it/fusiello/papers/eccv08.pdf

