#!/usr/bin/python3

from pequod_database import *
from shutil import copy2
import docker
import json
import tarfile
import os

main_analysis = None

class DockerAnalysis:

    db = None
    container_name = None
    image = None
    archive_name = None
    folder_name = None
    container_config = None
    container_layers = None
    client_docker = None
    dbms = None
    dict_table = {}

    def __init__(self, container, db):
        """
        Class constructor, take container name as parameter (i.e. santactf/app)

        :param container: Name of the docker container.
        :type container: str
        """
        self.db = db
        self.container_name = container
        self.client_docker = docker.from_env()
        self.pull_without_auth()
        self.save_container()
        self.untar()
        self.manifest_analysis() # config = str, layers = list
        #self.fill_db()
        print("init done")

    def fill_db(self):
        for i in self.container_layers:
            f = open(i, "rb")
            tar = tarfile.open(fileobj=f, mode="r:")
            layer = i.split('/')[0]
            for j in tar:
                if j.isfile():
                    file_cont = str(tar.extractfile(j).read())[2:-1]
                else:
                    file_cont = "NOT A REGULAR FILE"
                new_file = Files(filename=j.name, \
                file_size=j.size, \
                file_perm=j.mode, \
                owner=j.uname, \
                timestamp=j.mtime, \
                file_content=file_cont, \
                layer=layer)
                self.db.session.add(new_file)
                self.db.session.commit()

    def pull_without_auth(self):
        """
        Download docker container on docker hub without authentication.
        """
        #client = docker.from_env()
        self.client_docker.images.pull(self.container_name) # Download image
        self.image = self.client_docker.images.get(self.container_name)
        print(f"Image name: {self.image.tags[0]}")
        print(f"Image SHA256: {self.image.id}")

    def save_container(self):
        """
        Save the docker container as a tar archive.
        """
        #print(type(self.container_name))
        self.archive_name = self.image.tags[0].split('/')[0]+'.tar'
        save_image = self.client_docker.images.get(self.image.tags[0]).save()
        f = open(self.archive_name,"wb")
        for i in save_image:
            f.write(i)
        f.close()
        print(f"Image written in: {self.archive_name}")

    def untar(self):
        """
        Uncompress the docker container tar archive.
        """
        self.folder = self.archive_name.split('.')[0]
        os.mkdir(self.folder)
        print(f"Folder {self.folder} created.")
        copy2(self.archive_name, self.folder)
        print(f"{self.archive_name} copied in {self.folder}")
        os.chdir(self.folder)
        tar = tarfile.open(self.archive_name)
        tar.extractall()
        print(f"{self.archive_name} is extracted.")
        tar.close()

    def manifest_analysis(self):
        """
        Get docker configuration in the "manifest.json" file.
        """
        with open("manifest.json", "r") as read_file:
            data = json.load(read_file)
        self.container_config = data[0]['Config']
        self.container_layers = data[0]['Layers']
