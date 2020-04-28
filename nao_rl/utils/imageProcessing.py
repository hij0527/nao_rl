import numpy as np
import time
import cv2 as cv

class ImageProcessor(object):

    @staticmethod
    def threshold(image, low, high):
        """
        Apply thresholding to an image
        """ 
        im = cv.cvtColor(np.asarray(im), cv.COLOR_RGB2BGR)
        retval, thresholded = cv.threshold(im, low, high, cv.THRESH_BINARY)
        return thresholded

    @staticmethod
    def resize(image, dim):
        """
        Resize an image
        """
        if not isinstance(dim, tuple):
            dim = tuple(dim)
        
        resized = cv.resize(image, dim)
        return resized

    @staticmethod
    def ball_tracking(im, display=None, draw=True, color='red'):
        """
        Locates a green object in an image and draws a circle around it
        """ 
        if im is None:
            print('image is None')
            return None, None

        # hsv range
        if color == 'green':
            lower = (50, 80, 40)
            upper = (70, 255, 255)
        elif color == 'blue':
            lower = (110, 80, 40)
            upper = (130, 255, 255)
        elif color == 'red':
            lower = (0, 80, 40)
            upper = (10, 255, 255)
        else:
            print('unknown color: {}'.format(color))
            return None, None

        im = np.asarray(im, dtype=np.uint8)

        scale = 1
        small = cv.resize(im, (0, 0), fx=scale, fy=scale)
        hsv = cv.cvtColor(small, cv.COLOR_RGB2HSV)

        mask = cv.inRange(hsv, lower, upper)
        # Erosion and dilation to remove imperfections in masking
        mask = cv.erode(mask, None, iterations=2)
        mask = cv.dilate(mask, None, iterations=2)

        # Find the contours of masked shapes

        contours = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = contours[-2]
        center = None

        # If there is a masked object
        if contours is None:
            print('contours is None!')
        elif len(contours) > 0:
            # Largest contour
            c = max(contours, key=cv.contourArea)
            # Radius
            ((x, y), radius) = cv.minEnclosingCircle(c)
            # Moments of the largest contour
            moments = cv.moments(c)
            center = (int(moments["m10"] / moments["m00"]),
                        int(moments["m01"] / moments["m00"]))

            if draw:
                # Draw appropriate circles
                if radius > 2:
                    cv.circle(im, (int(x/scale), int(y/scale)), int(radius*1.25), (0, 255, 255), 2)
                    cv.circle(im, (int(center[0]/scale), int(center[1]/scale)), 2, (0, 0, 255), -1)
        if display:
            if cv.getWindowProperty('Nao', 3) == -1:
                cv.namedWindow('Nao', cv.WINDOW_NORMAL)
                cv.resizeWindow('Nao', 300, 300)
            cv.imshow('Nao',  im)
            key = cv.waitKey(1) & 0xFF

        return im, center

