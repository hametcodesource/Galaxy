def transform(self,x,y):
    #return self.transform_2D(x,y)
    return self.transform_perspective(x,y)

def transform_2D(self,x,y):
    return int(x),int(y)

def transform_perspective(self,x,y):
    line_y=y*self.perspectiver_pont_y/self.height
    if line_y>self.perspectiver_pont_y:
        line_y=self.perspectiver_pont_y
        
    diff_x=x-self.perspectiver_pont_x
    diff_y=self.perspectiver_pont_y-line_y

    factor_y=diff_y/self.perspectiver_pont_y

    factor_y=pow(factor_y,2)


    offset_x=diff_x*factor_y

    tr_x=self.perspectiver_pont_x + offset_x
    tr_y=self.perspectiver_pont_y - factor_y*self.perspectiver_pont_y

    return int(tr_x),int(tr_y)