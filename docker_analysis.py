#!/usr/bin/python3

import docker
import json
import tarfile
import os
import cmd
import sys
import re
import io
from shutil import copy2

main_analysis = None

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class dockerAnalysis:

    container_name = None
    image = None
    archive_name = None
    folder_name = None
    container_config = None
    container_layers = None
    client_docker = None

    def __init__(self, container):
        self.client_docker = docker.from_env()
        self.container_name = container
        image = self.pull_without_auth()
        archive_name = self.save_container()
        self.untar()
        self.manifest_analysis() # config = str, layers = list
        #print(self.container_layers)
        #self.read_config()

    def systemexec(self, syscmd):
        os.system(syscmd)

    def get_layers(self):
        return self.container_layers
    
    def selectlayer(self, layer):
        print("todo")

    def pull_without_auth(self):
        #client = docker.from_env()
        self.client_docker.images.pull(self.container_name) # Download image
        self.image = self.client_docker.images.get(self.container_name)
        print("Image name: {}".format(self.image.tags[0]))
        print("Image SHA256: {}".format(self.image.id))

    def pull_with_auth(self):
        print("TODO")
        # https://docs.docker.com/engine/api/sdk/examples/#pull-an-image-with-authentication

    def get_locale_image(self):
        print("TODO")

    def save_container(self):
        #print(type(self.container_name))
        self.archive_name = self.image.tags[0].split('/')[0]+'.tar'
        save_image = self.client_docker.images.get(self.image.tags[0]).save()
        f = open(self.archive_name,"wb")
        for i in save_image:
            f.write(i)
        f.close()
        print("Image written in: {}".format(self.archive_name))

    def untar(self):
        self.folder = self.archive_name.split('.')[0]
        os.mkdir(self.folder)
        print("Folder {} created.".format(self.folder))
        copy2(self.archive_name, self.folder)
        print("{} copied in {}".format(self.archive_name, self.folder))
        os.chdir(self.folder)
        tar = tarfile.open(self.archive_name)
        tar.extractall()
        print("{} is extracted.".format(self.archive_name))
        tar.close()

    def manifest_analysis(self):
        with open("manifest.json", "r") as read_file:
            data = json.load(read_file)
        self.container_config = data[0]['Config']
        self.container_layers = data[0]['Layers']

    # read_config('ddde36e2209357c424cca26ac5a0b46c2f864be797c053bed700422177ba7261.json')
    def read_config(self):
        with open(self.container_config, "r") as read_file:
            docker_main_config = json.load(read_file)
        print("{}Architecture{}: {} {}\n"  \
                "{}Startup command{}: {}\n"             \
                "{}Entrypoint{}: {}\n"                  \
                "{}Volumes{}: {}\n"                     \
                "{}Working directory{}: {}\n"           \
                .format(bcolors.OKGREEN, bcolors.ENDC, docker_main_config['os'], docker_main_config['architecture'],     \
                        bcolors.OKGREEN, bcolors.ENDC, docker_main_config['config']['Cmd'],        \
                        bcolors.OKGREEN, bcolors.ENDC, docker_main_config['config']['Entrypoint'],    \
                        bcolors.OKGREEN, bcolors.ENDC, docker_main_config['config']['Volumes'],     \
                        bcolors.OKGREEN, bcolors.ENDC, docker_main_config['config']['WorkingDir']))
        for j in range(len(docker_main_config['config']['Env'])):
            print("{}Environment variable{} {}: {}".format(bcolors.OKGREEN, j, bcolors.ENDC, docker_main_config['config']['Env'][j]))
        for i in range(len(docker_main_config['history'])):
            print("\n{}Layer creation{}: {}{}{}\n{}"                                                      \
                .format(bcolors.OKGREEN, bcolors.ENDC, \
                        bcolors.OKBLUE, docker_main_config['history'][i]['created'].split('.')[0].replace('T',' '), bcolors.ENDC, \
                        docker_main_config['history'][i]['created_by'].replace('\t','')))      

    def search_items(self, item):
        all_files = []
        a = self.container_layers
        for i in a:
            old_stdout = sys.stdout
            result = io.StringIO()
            sys.stdout = result
            tarfile.open(i).list(verbose=True)
            sys.stdout = old_stdout
            tmp = list(filter(None, result.getvalue().split('\n')))
            for j in tmp:
                j = list(filter(None, j.split(' ')))
                all_files.append(dict([(i,j)]))
        #print(all_files)
        for k in all_files:
            if re.search(item, list(k.values())[0][-1]): # get last element of the list in the dictionnary
                print("\n\n{}{}{}\n\
Timestamp: {}{} {}{}\n\
Original file size: {}{}{}\n\
Filename: {}{}{}".format(bcolors.OKGREEN, list(k.keys())[0], bcolors.ENDC, \
                        bcolors.OKBLUE, list(k.values())[0][3], list(k.values())[0][4], bcolors.ENDC,\
                        bcolors.FAIL, list(k.values())[0][2], bcolors.ENDC, \
                        bcolors.WARNING, list(k.keys())[0].split('/')[0]+"/"+list(k.values())[0][-1], bcolors.ENDC))     

    def extract_file(self, path):
        tar_archive = path.split('/')[0]+"/layer.tar"
        print(tar_archive)
        tar_path = "/".join(path.split('/')[1:])
        print(tar_path)
        tmp_tar = tarfile.open(tar_archive)
        print(tmp_tar)
        tmp_tar.extract(tar_path)
