import sys, os, shutil

WIN32 = False
if sys.platform[:3].lower() == "win":
    WIN32 = True

if WIN32:
    import ntfsutils.junction
    
    islink = ntfsutils.junction.isjunction
    
    def symlink(source, link_name):
        if not os.path.isdir(source):
            return
        ntfsutils.junction.create(source, link_name)
    
    def unlink(path):
        if not ntfsutils.junction.isjunction(path):
            return False
        ntfsutils.junction.unlink(path)
        return True
    
    def rmtree(location, nonlinks=True):
        # Explicitly unlink all junction'd links
        names = os.listdir(location)
        for dir in names:
            path = os.path.join(location, dir)
            if unlink(path):
                continue
            if os.path.isdir(path):
                rmtree(path)
        # Then get rid of everything else
        if nonlinks:
            shutil.rmtree(location)
        
else:
    symlink = os.symlink
    islink = os.path.islink
    rmtree = shutil.rmtree
    unlink = None
