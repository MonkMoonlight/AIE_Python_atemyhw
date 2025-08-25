# AI Image Processing and Classification Project

This project is designed to give you hands-on experience working with an image classifier and enhancing your programming skills using AI assistance. The project has two parts, each focused on different aspects of image classification and processing. By the end, you'll have explored fundamental concepts like Grad-CAM, image classification, and creative image filtering.

# Part 1
This program is a simple interactive image classifier. It loads a pre-trained MobileNetV2 model, asks the user for an image path, processes the image, runs it through the model, and prints out the top 3 predicted labels with confidence scores—until the user types "exit".

It basically takes an image and identifies with loop logic and gives you 3 possible things that it could be. It uses the import to pull from the appropriate databases, and the logic is straight forward from the def, loop logic, and print.

Top 3 Predictions for rogue.jpg
  1: bow (0.16)
  2: cuirass (0.09)
  3: breastplate (0.08)

It heavly focus on area they are not located at, but it got a lot more color scattered throughout the image with the focus on weapon armor. With very little not being selected.

#Part 2
AI Explanation Summary
This program is an interactive image blur tool. It:
1.	Lets you type in an image filename.
2.	Loads and resizes the image to 128×128.
3.	Applies a Gaussian blur filter.
4.	Saves the processed image with "_blurred" appended to the filename.
5.	Loops until you type "exit".

I don’t have much to add because that is the basic process of the process it would go through in its logic to produce a new image with the blur filter.

The image (rogue_blurred.jpg) looks kind of distorted after it has been blurred. You can clearly tell it about a person with some kind of white stick in their hand and it almost looks like they’re kneeling. It is very hard to decern what the image is other than a person holding something.

# Final Report:
The classifier is basically a search program to identify what it is looking for and what it found it looks like. Adding in the heat map just tells you more where the focus was at. The basic filters and enhanced filters are designed to modify the image and save a new copy with those modifications.

The black and white filter does just that, but the lighting of an object or lighting determines what will be more white than black. As well as the color of something.

Ripple causes ripples in the image distorting it.

Sketch removes colors and focuses more on the details of stuff and the lines.

Posterize basically distorts the lighting and colors but may not always distort the image like in the rogue_posterize.jpg only the background is affected and for the most part whereas the knight_posterize.jpg everything is affected.

Sepia would be more like the old black and white photos. Playing more in the grey scale of colors vs the pure black and white filter.

I found it very educational and learned a lot about python. Having AI help build the code made it easier for me to see why things were put in a certain way or structured in a certain way. It allowed me to improve my understanding of python.

