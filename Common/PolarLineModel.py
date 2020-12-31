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
        acute_theta=math.atan(abs(point_closest_origin.Y)/abs(point_closest_origin.X))
        theta=0.0
        if (quadrant == 0):
            theta=acute_theta
        elif (quadrant == 1):
            theta=math.pi-acute_theta
        elif (quadrant == 2):
            theta=acute_theta+math.pi
        elif (quadrant == 3):
            theta=math.pi*2-acute_theta

        return PolarLineModel(abs(rho),theta)

    def __repr__(self):
        display=("rho=%f  theta=%f")%(self.rho,self.theta)
        return display

    def __str__(self):
        return self.__repr__()

    @classmethod
    def _calculate_point_closest_to_origin(cls,model:LineModel):
        s=model.A**2+model.B**2
        x=-model.A*model.C/s
        y=-model.B*model.C/s
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

    @classmethod
    def generate_polar_equation_hough(cls, model:LineModel):
        """ The values of theta will vary from +90 to -89  and rho varies from -R to +R"""
        distance_of_perp_from_origin:float =model.compute_distance(Point(0,0))
        point_closest_origin= PolarLineModel._calculate_point_closest_to_origin(model)
        
        rho:float=0
        if (point_closest_origin.Y > 0):
            rho=distance_of_perp_from_origin
        else:
            rho=-distance_of_perp_from_origin

        perp_model:LineModel=LineModel.compute_perpendicular_line_through_origin(model)

        theta:float=0
        if (abs(perp_model.B) < 0.001):
            theta=math.pi/2  #Line is nearly 90 degrees
        else:
            slope=-(perp_model.A/perp_model.B)
            if (slope > 0):
                theta=math.atan(slope)
            else:
                theta=math.atan(slope)
        return PolarLineModel(rho,theta)
