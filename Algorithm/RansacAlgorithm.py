from Common import Point
from typing import Union, Any, List, Optional, cast
from Common import RansacLineInfo
from Common import LineModel
from Common import Point
import math

class RansacAlgorithm(object):
    """implementation of Ransac algorithm"""
    def __init__(self,width:float, height:float,points:List[Point]):
        self.Points=points
        self.Width=float(width)
        self.Height=float(height)
        self.ThresholdDistance=float(10)
        
        pass

    def run(self)->List[RansacLineInfo]:
        if (len(self.Points)<2):
            return []

        pairs:List[PairOfPoints]=self.__create_pairs_of_points()
        temp_models:List[LineModelExtended]=self.__create_models_using2points(pairs)
        temp_models_with_high_inliers:List[LineModelExtended]=self.__get_good_temp_models(temp_models)
        expanded_models:List[LineModelExtended] = self.expand_models_using_inliers(temp_models_with_high_inliers)

        unique_models:List[LineModelExtended] = self.eliminate_duplicates_using_hough_accumulator(expanded_models)
        for unique_model in unique_models:
            new_ransac_line = RansacLineInfo()
            new_ransac_line.inliers=unique_model.Inliers #combine Inliers and Seed

        ##

        linePerp:RansacLineInfo=RansacLineInfo()
        linePerp.line = LineModel(1,0,-self.Width/2)
        linePerp.inliers=[Point(self.Width/2,0),Point(self.Width/2, self.Height)]

        lineHor=RansacLineInfo()
        lineHor.line = LineModel(0,1,-self.Height/3)
        lineHor.inliers = [Point(0,self.Height/3), Point(self.Width,self.Height/3)]
        return [linePerp,lineHor]

    def expand_models_using_inliers(self,line_models):
        """
        Improve the line model by recalculating a new best fit new line using the new inliers
        """
        results=[]
        line_model_ex:LineModelExtended
        for line_model_ex in line_models:
            all_inliers=[]
            all_inliers.extend(line_model_ex.SeedPoints)
            all_inliers.extend(line_model_ex.Inliers)
            expanded_model=self.create_least_square_model(all_inliers)
            new_inliers=self.__get_inliers(expanded_model,self.Points,self.ThresholdDistance)
            new_line=LineModelExtended(expanded_model,[],new_inliers)
            #line_ex=LineModelExtended(expanded_model,[line_model_ex.seed_points[0],line_model_ex.seed_points[1],new_inliers)
            results.append(new_line)
            pass
        return results

    def __get_inliers(self, line:LineModel, points, threshold:float):
        """
        Returns all points which are within the specified threshold distance of the specified line
        """
        results=[]
        for point in points:
            distance=line.compute_distance(point)
            if (distance> threshold):
                continue
            results.append(point)
        return results

    def eliminate_duplicates_using_hough_accumulator(self,expanded_models):
        pass

    def __create_pairs_of_points(self):
        """
        Creates all possible pairs from the given points
        """
        results=[]
        for index_outer in range(0,len(self.Points)):
            for index_inner in range(index_outer+1,len(self.Points)):
                point1=self.Points[index_outer]
                point2=self.Points[index_inner]
                pair = PairOfPoints(point1,point2)
                results.append(pair)
        return results

    #def __create_models_using2points(self, pairsofpoints:List[Point])->List[LineModelExtended]:
    def __create_models_using2points(self, pairsofpoints:List[Point]):
        """
        Creates Lines from the specified pairs of points
        """
        results=[]
        pair:PairOfPoints
        for pair in pairsofpoints:
            line=LineModel.create_line_from_2points(pair.Point1.X, pair.Point1.Y, pair.Point2.X, pair.Point2.Y)
            line_ex=LineModelExtended(line,[pair.Point1,pair.Point2],[])
            results.append(line_ex)
        return results

    #def __get_good_temp_models(self, line_models:List[LineModelExtended])->List[LineModelExtended]:
    def __get_good_temp_models(self, line_models):
        """
        Calculatates inliners for the specified models and returns those which exceed threshold
        """
        results:List[LineModelExtended]=[]
        for line_model_ex in line_models:
            inliers:List[Point]=[]
            for point in self.Points:
                if (point in line_model_ex.SeedPoints):
                    continue
                distance=line_model_ex.LineModel.compute_distance(point)
                if (distance > self.ThresholdDistance):
                    continue
                inliers.append(point)
            if (len(inliers)==0):
                continue
            good_model=LineModelExtended(line_model_ex.LineModel,line_model_ex.SeedPoints,inliers)
            results.append(good_model)
        return results

    #
    #Find the best line which fits the specified points
    #Use the least squares best fit
    #https://www.varsitytutors.com/hotmath/hotmath_help/topics/line-of-best-fit
    #
    def create_least_square_model(self,points:list)->LineModel:

        mean_x=0
        mean_y=0
        for p in points:
            mean_x+=p.X
            mean_y+=p.Y
        mean_x=mean_x/len(points)
        mean_y=mean_y/len(points)

        slope_numerator=0
        slope_denominator=0
        slope=0
        #use the formula for least squares
        for p in points:
            slope_numerator+=(p.X-mean_x)*(p.Y-mean_y)
            slope_denominator+=(p.X-mean_x)*(p.X-mean_x)

        if (math.fabs(slope_denominator) < 0.001):
            #perpendicular line
            x_intercept=mean_x
            #equation   (1)x + (0)y + (-xintercept) + 1
            vertical_line_a=1
            vertical_line_b=0
            vertical_line_c=-x_intercept
            model=LineModel(vertical_line_a,vertical_line_b,vertical_line_c)
            return model
        
        slope=slope_numerator/slope_denominator
        y_intercept=mean_y - (slope * mean_x)

        line_a=slope
        line_b=-1
        line_c=y_intercept
        #  standard form of line equation
        #  ------------------------------
        #   y=mx+c
        #   mx  -   y   +   c=0
        #   ax  +   by  +   c=0
        #   slope= -a/b
        #   yint= -c/b
        #        
        model=LineModel(line_a,line_b,line_c)
        return model


class PairOfPoints(object):
    """Represents 2 points"""
    def __init__(self, point1:Point, point2:Point):
        self.Point1:Point=point1
        self.Point2:Point=point2

class LineModelExtended(object):
    """Represents a line model along with all inliers."""
    def __init__(self, line:LineModel,seed_points:[],inliers:[]):
        self.LineModel:LineModel=line
        self.Inliers:List[Point]=inliers
        self.SeedPoints:List[Point]=seed_points

    def __repr__(self):
        display=("Seed points=%d Inlier points=%d, LineModel=%s")%(len(self.SeedPoints),len(self.Inliers),self.LineModel.__repr__())
        return display