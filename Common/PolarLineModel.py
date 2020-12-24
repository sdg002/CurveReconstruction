from .LineModel import LineModel
from .Point import Point
import math

class PolarLineModel(object):
    """Describes a 2d line using polar coordinates - pho and theta"""
    def __init__(self, distance:float, theta:float):
        self.rho = float(distance)
        self.theta=float(theta)
        

    @classmethod
    def generate_polar_equation(cls, model:LineModel):
        """
        Converts a line equation in the form ax+by+c into polar model
        """
        rho=model.C/math.sqrt(model.A**2 + model.B**2)
        point_closest_origin= PolarLineModel._calculate_point_closest_to_origin(model)
        quadrant=PolarLineModel._get_quadrant(point_closest_origin.X, point_closest_origin.Y)
        acute_theta=math.atan(abs(model.A)/abs(model.B))
        theta=0.0
        if (quadrant == 0):
            theta=acute_theta
        elif (quadrant == 1):
            theta=math.pi-acute_theta
        elif (quadrant == 2):
            theta=acute_theta+math.pi
        elif (quadrant == 3):
            theta=math.pi*2-acute_theta

        # if (abs(model.A) < 0.001):
        #     theta=math.pi/4.0
        # else:
        #     theta=math.atan(-model.B/model.A)
        return PolarLineModel(abs(rho),theta)

    def __repr__(self):
        display=("rho=%f  theta=%f")%(self.rho,self.theta)
        return display

    @classmethod
    def _calculate_point_closest_to_origin(cls,model:LineModel):
        x=-model.C/model.A/2
        y=-model.C/model.B/2
        return Point(x,y)

    @classmethod
    def _get_quadrant(cls,x:float, y:float)->int:
        """Returns the quadrant index of the specified point. 0,1,2,3"""
        if (x >=0 ) and ( y>=0):
            return 0
        elif (x <=0 ) and ( y>=0):
            return 1
        elif ( x <=0) and (y<=0):
            return 2
        else:
            return 3
