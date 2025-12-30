from PIL import Image, ImageDraw, ImageFont
import math
n = "a,10,b,20,c,30,d,40,50,90"
rawList = n.split(n)

if len(rawList % 2 != 0):
    await interaction.response.send_message(":potato: list of inputs must be pairs of values, in other words, list must have even length")
try:
    param = []
    for i in range(0, int(len(rawList)/2)):
        param+=[(str(rawList[2*i]), int(rawList[2*i+1]))]
except ValueError:
    await interaction.response.send_message(":crying: one of your scores isn't an integer")

color = (107, 0, 185)

scale = 4 # needed for antialiasing

thickness = 4*scale
width, height = 1280, 720
width, height = width*scale, height*scale
radius = height*0.4

def getCoords(x: list[tuple[str, int]], y = -1)->list[tuple[int, int]]:
    """
    Creates a list of tuples representing the coords from the parameter
    
    :param x: list of tuples (name, score)
    :param y: if passed, mult radius times y, disregarding score scaling
    """
    rad = math.radians(360/len(x))
    output = []
    for i in range(0,len(x)):
        if (y == -1):
            output+=[(width/2 +radius*(x[i][1]/100)*math.cos(i*rad-math.pi/2),
                      height/2+radius*(x[i][1]/100)*math.sin(i*rad-math.pi/2))]
        elif (y >= 0):
            output+=[(width/2 +radius*y*math.cos(i*rad-math.pi/2),
                      height/2+radius*y*math.sin(i*rad-math.pi/2))]
    return output

# create image
img = Image.new('RGBA', (width, height), color="black")
draw = ImageDraw.Draw(img)

# create coords for the stats, lines, and text 
coords = getCoords(param)
coords2 = getCoords(param, 1)
coords3 = getCoords(param, 1.2)
coords4 = getCoords(param, 0.99)

# bg + stats
draw.polygon(coords2, fill="grey")
draw.polygon(coords, fill=color, outline="black", width=thickness)

# draw the lines and text
font = ImageFont.truetype("COMIC.TTF", 40*scale)

for i in range(0, len(coords2)):
    # make the line
    draw.line([(width/2, height/2), (coords4[i][0], coords4[i][1])], fill="white", width=thickness)
    
    # figure out the anchoring of the text
    anchor = ""
    if coords3[i][0] > width/2: anchor+="l"
    else: anchor+="r"
    if coords3[i][1] > height/2: anchor+="d"
    else: anchor+="a"
    
    # slap on the text
    draw.text((coords3[i][0], coords3[i][1]), param[i][0], fill="white", font=font, anchor=anchor)

# fg
draw.polygon(coords2, outline="white", width=thickness)

# "antialiassing" 
widthNew, heightNew = int(width/4), int(height/4)
img = img.resize((widthNew, heightNew), resample=Image.Resampling.LANCZOS)

# save
img.save("img.png")
img.show()