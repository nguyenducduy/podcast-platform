import os
from config import upload_dir, MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS
from datetime import datetime
from werkzeug.utils import secure_filename
from graphql import GraphQLError
import urllib.request
import re


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save(folder_name, fileObj):
    if fileObj and allowed_file(fileObj.filename):
        # get file info
        name = fileObj.filename.rsplit('.', 1)[0].lower()
        ext = fileObj.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(name) + '.' + ext

        # create upload folder
        currentDateDir = os.path.join(
            upload_dir,
            folder_name + '/' + datetime.today().strftime('%Y/%m')
        )
        os.makedirs(currentDateDir, exist_ok=True)

        # write file
        file_path = os.path.join(currentDateDir, filename)
        timestamp = int(datetime.now().timestamp())
        if os.path.isfile(file_path):
            now = datetime.now()
            filename = '%s_%s.%s' % (secure_filename(name), timestamp, ext)
            file_path = os.path.join(currentDateDir, filename)
        else:
            file_path = os.path.join(currentDateDir, filename)

        fileObj.save(file_path)

        return datetime.today().strftime('%Y/%m') + '/' + filename
    else:
        raise GraphQLError('File type not allowed')
        return False


def delete(folder_name, filePath):
    os.remove(os.path.join(upload_dir, folder_name + '/' + filePath))


def getPath(folder_name, filePath):
    return folder_name + '/' + filePath


def getRelativePath(folder_name, filePath):
    return os.path.join(
        upload_dir,
        folder_name + '/' + filePath
    )


def saveToFile(folder_name, name, ext, data):
    filename = secure_filename(name) + '.' + ext

    # create upload folder
    currentDateDir = os.path.join(
        upload_dir,
        folder_name + '/' + datetime.today().strftime('%Y/%m')
    )
    os.makedirs(currentDateDir, exist_ok=True)
    file_path = os.path.join(currentDateDir, filename)

    # write file
    file = open(file_path, "w")
    file.write(data)
    file.close()

    return datetime.today().strftime('%Y/%m') + '/' + filename


def downloadFromUrl(folder_name, dest_url):
    filename = secure_filename(dest_url)

    # create upload folder
    currentDateDir = os.path.join(
        upload_dir,
        folder_name + '/' + datetime.today().strftime('%Y/%m')
    )
    os.makedirs(currentDateDir, exist_ok=True)
    file_path = os.path.join(currentDateDir, filename)

    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(dest_url, file_path)
    except urllib.error.URLError as e:
        print(e.reason)
        pass
        # raise GraphQLError(e.reason)

    return datetime.today().strftime('%Y/%m') + '/' + filename
