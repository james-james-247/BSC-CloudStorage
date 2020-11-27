import os
from flask import Flask, request, render_template, send_file
import shutil
app = Flask(__name__)






#This is simply the starting of the server the first file to be shown
@app.route('/')
def index():
    return render_template('index.html')






#This gets the preset username and password from the file they are stored
account = open("admin/account.txt", "r")
content = account.readlines() #returns an array of lines
username = content[0]
password = content[1]
account.close()






#This is for when the user attempts to login
@app.route('/loginAttempt', methods=['GET', 'POST'])
def loginAttempt():

    #This if statement is to prevent the user from inserting into the url and getting past the security
    if request.method == 'POST':

        #This is here to get the users input to query it
        usernameGuess = request.form["username"] + "\n"
        passwordGuess = request.form["password"]
        
        #Comparing it to the pre set username and password
        if usernameGuess == username and passwordGuess == password:

            file = open("./admin/folder.txt", "r")
            path = file.read()
            file.close()

            #This is the code to display the files
            files = os.listdir(path)
    
            return render_template('home.html', files=files, searched="File/Folder Has Not Been Found")
        else:
            return render_template('index.html', status="Login Failed! Either Your Username or Password is Incorrect!")
        
    else:
        return render_template('index.html', status="Incorrect Method Of Input")
    
    #Status is used to respond to the user with their current progress






#This section is for when the user uploads a file
@app.route('/fileUpload', methods=['POST'])
def fileUpload():

    file = open("./admin/folder.txt", "r")
    path = file.read()
    file.close()
    
    file = request.files['files']
    file.save(os.path.join(path, file.filename))

    #Find all the files in the home directory
    files = os.listdir(path)
    
    return render_template('home.html', files=files, searched="File/Folder Has Not Been Found")






#This section is for when the user creates a new folder
@app.route('/folderCreation', methods=['POST'])
def folderCreation():

    file = open("./admin/folder.txt", "r")
    path = file.read()
    file.close()

    folderName = request.form["folderName"]
    newPath = path + "/" + folderName

    #Checking to see if the folder already exists
    if not os.path.exists(newPath):
        os.makedirs(newPath)

        #Sending back all files
        files = os.listdir(path)
    
        return render_template('home.html',  files=files, searched="File/Folder Has Not Been Found")
    else:

        #Sending back all files
        files = os.listdir(path)
            
        return render_template('home.html', files=files, searched="File/Folder Has Not Been Found")






#This section is for when the user wants to delete a file or folder
@app.route('/delete', methods=["GET"])
def delete():

    file = open("./admin/folder.txt", "r")
    path = file.read()
    file.close()

    file = request.args.get('file', '')
    toDelete = path + file

    if request.args.get('file', '').find('.') == -1:
        shutil.rmtree(toDelete)
        
        #Sending back all files
        files = os.listdir(path)
        
        return render_template('home.html', files=files, searched="File/Folder Has Not Been Found")
        
    else:
        os.remove(toDelete)

        #Sending back all files
        files = os.listdir(path)
        
        return render_template('home.html', files=files, searched="File/Folder Has Not Been Found")





    
#This is the section that allows the user to download files
@app.route('/downloadFile', methods=['GET'])
def downloadFile():

    file = open("./admin/folder.txt", "r")
    path = file.read()
    file.close()

    selectedFile = path + request.args.get('file')

    if request.args.get('file', '').find('.') != -1:
        return send_file(selectedFile, as_attachment=True)
    else:
        #Sending back all files
        files = os.listdir(path)
        zipped = shutil.make_archive(selectedFile, 'zip', selectedFile)
    
        return render_template('home.html', files=files, searched="File/Folder Has Not Been Found")






#This is the section that allows the user to access sub-folders
@app.route('/subFolder', methods=["POST"])
def subFolder():

    file = open("./admin/folder.txt", "r")
    path = file.read()
    file.close()

    #Sending back all files
    newPath = path  + request.form["subFolder"] + "/"
    files = os.listdir(newPath)

    subFolder = open("./admin/folder.txt", "w")
    subFolder.write(newPath)
    subFolder.close()

    return render_template('home.html', files=files, searched="File/Folder Has Not Been Found")






#This is the section that allows the user to move 'back to the home directory
@app.route('/backFolder', methods=["POST"])
def backFolder():

    file = open("./admin/folder.txt", "r")
    path = file.read()
    file.close()

    split = path.split("/")
    
    status = ""
    if(len(split) == 4):

        return render_template("index.html")
    
    else:
        split.pop()
        split.pop()

        newPath = ""
        for val in split:
            newPath += val + "/"

        subFolder = open("./admin/folder.txt", "w")
        subFolder.write(newPath)
        subFolder.close()
    
        #Sending back all files
        files = os.listdir(newPath)
    
        return render_template('home.html', files=files, searched="File/Folder Has Not Been Found")







#This is the section for when the user wants to view their file
@app.route("/view", methods=["GET"])
def view():

    imgArray = ["jpg", "jpeg", "png", "svg", "gif", "bmp", "pdf"]
    vidArray = ["mkv", "mpeg", "mpg", "mp4"]
    textArray = ["txt"]

    file = request.args.get('file', '')
    
    find = file.find(".")
    length = len(file)
    ext = length - find - 1


    extension = ""  
    if ext == 3:
        extension += file[-3]
        extension += file[-2]
        extension += file[-1]
    elif ext == 4:
        extension += file[-4]
        extension += file[-3]
        extension += file[-2]
        extension += file[-1]

    readFile = open("./admin/folder.txt", "r")
    path = readFile.read()
    Path = path.lstrip(".")
    readFile.close()

    if extension in imgArray:
        
        finalPath = Path + "/" + file    
        return render_template('viewing/images.html', returnFile=finalPath, image=file)
    
    elif extension in vidArray:
        
        finalPath = Path + "/" + file    
        return render_template('viewing/video.html', returnFile=finalPath, image=file)

    elif extension in textArray:
        
        finalPath = "." + Path + "/" + file
        readFile = open(finalPath)
        value = readFile.readlines()
        values = ""
        for val in value:
            values += val
        readFile.close()
        return render_template('viewing/text.html', returnFile=finalPath, image=file, value=values)

    else:
        
        #Sending back all files
        files = os.listdir(path)
        return render_template('home.html', files=files, error="Unsupported File Format", searched="File/Folder Has Not Been Found")






#This section is for when the user returns from viewing a file
@app.route("/returning", methods=["POST"])
def returning():

    file = open("./admin/folder.txt", "r")
    path = file.read()
    file.close()
    
    #Sending back all files
    files = os.listdir(path)
    return render_template('home.html', files=files, error="Unsupported File Format", searched="File/Folder Has Not Been Found")













#This is the section that begins the server on the localhost on PORT 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
