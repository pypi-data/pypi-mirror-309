import io
import gridfs


def upload_file(data:io.BytesIO, db):
    fs = gridfs.GridFS(db)
    print(f"Upload file: start")
    file_id = fs.put(data)
    print(f"Upload file: success")
    print(f"- file_id: {file_id}")
    return file_id


def delete_file(file_id, db):
    fs = gridfs.GridFS(db)
    print(f"Remove file '{file_id}': start")
    fs.delete(file_id)
    print(f"Remove file '{file_id}': success")


def read_file_data(file_id, db):
    fs = gridfs.GridFS(db)
    grid_out = fs.get(file_id)
    return grid_out.read()


# def downloadFile(fileId, fileName, db=None):
#     if db == None:
#         db = getDb()
#     fs = gridfs.GridFS(db)
#     print("Downloading file " + fileId + "...")
#     folder = os.path.dirname(fileName)
#     data = fs.get(ObjectId(fileId))
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#     f = open(fileName, "wb")
#     f.write(data.read())
#     f.close()
#     print("File " + fileName + " downloaded")
