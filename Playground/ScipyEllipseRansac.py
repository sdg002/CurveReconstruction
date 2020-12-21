#
#RANSAC sample from Scikit
#https://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.ransac
#

import numpy as np
from skimage.measure import EllipseModel
from skimage.measure import ransac
from array import array




#Generate ellipse data without tilt and add noise
t = np.linspace(0, 2 * np.pi, 50)
xc, yc = 20, 30
a, b = 5, 10
x = xc + a * np.cos(t)
y = yc + b * np.sin(t)
data = np.column_stack([x, y])
np.random.seed(seed=1234)
data += np.random.normal(size=data.shape)

#Add some faulty data
data[0] = (100, 100)
data[1] = (110, 120)
data[2] = (120, 130)
data[3] = (140, 130)

#Estimate ellipse model using all available data:
model = EllipseModel()
model.estimate(data)

np.round(model.params)  


#Estimate ellipse model using RANSAC:
ransac_model, inliers = ransac(data, EllipseModel, 20, 3, max_trials=50)
print("ransac complete")
abs(np.round(ransac_model.params))
print("inliers below")
print(inliers)
sum(inliers) > 40
