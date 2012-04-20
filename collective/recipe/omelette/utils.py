import sys, os, shutil

WIN32 = False
if sys.platform[:3].lower() == "win":
    WIN32 = True

if WIN32:
    from jaraco.windows import filesystem
    
    def unlink(path):
        if not filesystem.islink(path):
            return
        os.rmdir(path)
    
    symlink = filesystem.symlink
    islink = filesystem.islink
    
    def rmtree(location, nonlinks=True):
        # Explicitly unlink all junction'd links
        for root, dirs, files in os.walk(location, topdown=False):
            for dir in dirs:
                path = os.path.join(root, dir)
                unlink(path)
        # Then get rid of everything else
        if nonlinks:
            shutil.rmtree(location)
        
else:
    symlink = os.symlink
    islink = os.path.islink
    rmtree = shutil.rmtree
    unlink = None
