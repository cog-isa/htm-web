__author__ = 'AVPetrov'

import shutil, git

if shutil.which('git')==None:
    print("Error: Couldn't find git on machine")
else:
    repo = git.Repo('C:/htm-core2')
    repo.remotes.origin.pull(repo.remotes.origin.refs[0].remote_head)
    print("---- PULL HAVE DONE ----")