import os

__author__ = 'AVPetrov'

import shutil, git

if shutil.which('git')==None:
    print("Error: Couldn't find git on machine")
else:
    if not os.path.exists('htm-core'):
        os.mkdir('htm-core')
        os.system('git clone https://github.com/cog-isa/htm-core htm-core')

    repo = git.Repo('htm-core/')
    origin = repo.remote()
    origin.pull()