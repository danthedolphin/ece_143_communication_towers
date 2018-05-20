import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

WINDOW_SIZE = 10
#10 square units but zero-indexed so index goes up to nine

#create a generator that creates a rectangle every time we call it
def create_rectangle():
    '''
    A generator function that uses numpy to randomly generate a point, width, and height with uniform distribution
    :return: tuple of rectangle coordinates
    '''
    while True:
        bottom_left_x = np.random.randint(0,WINDOW_SIZE) #initialize the x and y coordinates anywhere 0-9
        bottom_left_y = np.random.randint(0, WINDOW_SIZE)
        width = np.random.randint(1,WINDOW_SIZE-bottom_left_x+1) #make the width a random integer from coordinate to max value
        height = np.random.randint(1,WINDOW_SIZE-bottom_left_y+1)

        rect_coord = (bottom_left_x, bottom_left_y, width, height)

        yield rect_coord


def max_area_rectangle(rect_area):
    '''
    Takes in a 2-D numpy array of a polygon and cuts it so it becomes a rectangle of the maximum area
    I take a histogram of the number of ones in each column. From there I can
    :param rect_area: 2-D array with the polygon indicated by ones
    :return: 2-D array that has a rectangle of maximum area
    '''
    max_rect = np.array(rect_area)
    #create a histogram of how many ones in each column
    area = -1
    max_width = None
    max_height = None
    index_x = None
    index_y = None

    #create an accumulating histogram top down of the input rect_area
    for a in range(0,len(max_rect)): #loop through each row of the input rect_area
        if a != 0:#we do not want to start the histogram at row 0
            for b in range(len(max_rect[0])): #loop through each column in the row a
                if max_rect[a][b] == 1: #if there is a 1 add the value above in the column
                    max_rect[a][b] += max_rect[a-1][b]


        #for each accumulating histogram row we want to calculate the area
        hist = max_rect[a]
        for i in range(len(hist)):
            width = 1
            #add to the width for every value that is greater than or equal to the right of the value hist[i]
            for g in range(i+1,len(hist)): #go down the histogram to the right
                if hist[g] >= hist[i]:
                    width += 1

                #break if there is a value less than hist[i] somewhere to the right
                else:
                    break

            #get the area by multiplying width and the height of and check if its greater than the current placeholder
            if width*hist[i]>area:
                area = hist[i]*width

                #update the values that acheived max area to put on graph
                max_height =int(hist[i])
                max_width = width
                index_y = a
                index_x = i
    #graph the largest area rectangle and return it
    max_rect = np.zeros_like(rect_area)
    max_rect[index_y-max_height+1:index_y+1,index_x:index_x+max_width] = 1

    return max_rect


def main(n = WINDOW_SIZE*WINDOW_SIZE+1):

    assert isinstance(n,int), 'Input must be an integer'
    assert n>0, 'Input must be greater than zero'

    generate_rectangle = create_rectangle() #call the generator to get random rectangle coordinates
    ims = []
    store_area = np.zeros((WINDOW_SIZE, WINDOW_SIZE)) #initialize the global 2-D numpy array that holds all of the communication coverage

    counter = 1 #initialize counter that keeeps track of how many communication towers are plotted

    while not store_area.all() and counter <= n: #while loop ends when there is no more area to cover
        rect_coord = next(generate_rectangle) #call the generator to get random coordinates

        #create the rectangle in the matrix space
        x,y,width,height = rect_coord
        rect_area = np.zeros((WINDOW_SIZE,WINDOW_SIZE))
        rect_area[x:x+width,y:y+height] = 1

        rect_area[store_area > 0] = 0 #trim the rectangle so there is no overlap

        max_rect = max_area_rectangle(rect_area) #get the largest area rectangle out of rect_area
        image = plt.imshow(max_rect, animated = True)
        ims.append([image])


        #if there is anything added to store_area increment the counter and update the graph
        if max_rect.any():

            store_area[max_rect > 0] = counter  # put rect_area onto store_area to graph


            counter += 1


        #time.sleep(0.1) #delay for graph update

    if counter == 2:
        print 'There is 1 communication tower covering {}% of the area.'.format(100. * np.count_nonzero(store_area)/(WINDOW_SIZE*WINDOW_SIZE))
    else:
        print 'There are {} communication towers covering {}% of the area.'.format(counter-1, 100. * np.count_nonzero(store_area)/(WINDOW_SIZE*WINDOW_SIZE))
    fig1 = plt.figure()  # initialize figure to visualize the coverage
    #fig1.add_subplot(111, aspect='equal')

    animation.ArtistAnimation(fig1, ims, interval = 500, repeat_delay=1000, blit = True)
    plt.show()

main(10)


