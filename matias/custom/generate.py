import glob, os


dataset_path = '/media/matias/3335-3231/DCIM/100D5300/'

# Percentage of images to be used for the test set
percentage_test = 12;

# Create and/or truncate train.txt and test.txt
file_train = open('train.txt', 'w')  
file_test = open('test.txt', 'w')

# Populate train.txt and test.txt
counter = 1  
index_test = round(100 / percentage_test)  
for pathAndFilename in glob.iglob(os.path.join(dataset_path, "*.jpg")):  
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test+1:
        counter = 1
        file_test.write(dataset_path + title + '.jpg' + "\n")
    else:
        file_train.write(dataset_path + title + '.jpg' + "\n")
counter = counter + 1
