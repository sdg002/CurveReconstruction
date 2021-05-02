# Motivation
The problem was to find the approximate regions in a dotted image where there might be a curve
Trying to find a way to reduce the image size by taking the mean of a patch
And, then apply some thresholding

# What are the sample files?
convolve-in folder


# What was the objective?
- Try to do a convolution with various sizes of kernel.
- Use a stride=kernel/2
- We want to reduce the image size
- Perform an averaging convolution operation
- We could then apply a thresholding to hide patches whose mean value falls below a certain threshold - thereby leaving us with crowded patches that would be of interest



# What was I thinking?
- Find the relevant regions. These are regions with higher density
- Do a strided convolution with an averaging filter
- Higher density patches will produce a higher value
- Apply a threshold and eliminate the weaker patches
- Whatever is left over are relevant regions for analysis


# Which is the working Python code?
Playground\Convolve.py

# What did I learn?
- None of the existing libraries do a strided convolution
- Some examples on SFO and Medium - but none worked for me
- I hand crafted my own function
- Works well
- Performance needs improvement
- 

# What images worked well?
Convolved-parabola.W=500.H=200.MAXD=5.SP=0.90.19.png-kernel-25

# What kernel worked well?
The kernel size is dependent on the MAXD parameter. 25 worked well. 5,10,15 gave bad results

