"""
Access HDFS like a normal filesystem using pyarrow and fsspec
"""

# Method 1: Using pyarrow.fs (Recommended)
import pyarrow.fs

# Connect to HDFS
hdfs = pyarrow.fs.HadoopFileSystem(host='namenode', port=8020, user='root')

# List directory (like os.listdir)
def listdir_hdfs(path: str):
    """List directory contents like os.listdir"""
    try:
        file_infos = hdfs.get_file_info(pyarrow.fs.FileSelector(path, recursive=False))
        return [info.path for info in file_infos]
    except Exception as e:
        print(f"Error: {e}")
        return []

# Read file (like open().read())
def read_file_hdfs(path: str):
    """Read file content like open().read()"""
    try:
        with hdfs.open_input_file(path) as f:
            return f.read().decode('utf-8')
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Write file (like open().write())
def write_file_hdfs(path: str, content: str):
    """Write file content like open().write()"""
    try:
        with hdfs.open_output_stream(path) as f:
            f.write(content.encode('utf-8'))
        print(f"File written: {path}")
    except Exception as e:
        print(f"Error writing file: {e}")

# Check if path exists (like os.path.exists())
def exists_hdfs(path: str):
    """Check if path exists like os.path.exists()"""
    try:
        info = hdfs.get_file_info(path)
        return True
    except:
        return False

# Check if directory (like os.path.isdir())
def isdir_hdfs(path: str):
    """Check if path is directory like os.path.isdir()"""
    try:
        info = hdfs.get_file_info(path)
        return info.type == pyarrow.fs.FileType.Directory
    except:
        return False

# Check if file (like os.path.isfile())
def isfile_hdfs(path: str):
    """Check if path is file like os.path.isfile()"""
    try:
        info = hdfs.get_file_info(path)
        return info.type == pyarrow.fs.FileType.File
    except:
        return False

# Create directory (like os.mkdir())
def mkdir_hdfs(path: str):
    """Create directory like os.mkdir()"""
    try:
        hdfs.create_dir(path)
        print(f"Directory created: {path}")
    except Exception as e:
        print(f"Error creating directory: {e}")

# Delete file/directory (like os.remove() / os.rmdir())
def remove_hdfs(path: str, recursive: bool = False):
    """Delete file or directory"""
    try:
        if isdir_hdfs(path):
            hdfs.delete_dir(path, recursive=recursive)
        else:
            hdfs.delete_file(path)
        print(f"Deleted: {path}")
    except Exception as e:
        print(f"Error deleting: {e}")

# Get file size (like os.path.getsize())
def getsize_hdfs(path: str):
    """Get file size like os.path.getsize()"""
    try:
        info = hdfs.get_file_info(path)
        return info.size
    except:
        return None


# Method 2: Using fsspec (Alternative approach)
import fsspec

# Create fsspec filesystem for HDFS
fs = fsspec.filesystem('hdfs', host='namenode', port=8020)

# Now you can use it like a normal filesystem
def listdir_fsspec(path: str):
    """List directory using fsspec"""
    try:
        return fs.ls(path)
    except Exception as e:
        print(f"Error: {e}")
        return []

def read_file_fsspec(path: str):
    """Read file using fsspec"""
    try:
        with fs.open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error: {e}")
        return None

def write_file_fsspec(path: str, content: str):
    """Write file using fsspec"""
    try:
        with fs.open(path, 'w') as f:
            f.write(content)
        print(f"File written: {path}")
    except Exception as e:
        print(f"Error: {e}")


# Method 3: Wrapper class to make HDFS feel like os/pathlib
class HDFSPath:
    """A pathlib-like interface for HDFS"""
    
    def __init__(self, path: str):
        self.path = path
        self.hdfs = pyarrow.fs.HadoopFileSystem(host='namenode', port=8020, user='root')
    
    def exists(self):
        try:
            self.hdfs.get_file_info(self.path)
            return True
        except:
            return False
    
    def is_dir(self):
        try:
            info = self.hdfs.get_file_info(self.path)
            return info.type == pyarrow.fs.FileType.Directory
        except:
            return False
    
    def is_file(self):
        try:
            info = self.hdfs.get_file_info(self.path)
            return info.type == pyarrow.fs.FileType.File
        except:
            return False
    
    def listdir(self):
        """List directory contents"""
        try:
            file_infos = self.hdfs.get_file_info(
                pyarrow.fs.FileSelector(self.path, recursive=False)
            )
            return [info.path for info in file_infos]
        except:
            return []
    
    def read_text(self):
        """Read file as text"""
        with self.hdfs.open_input_file(self.path) as f:
            return f.read().decode('utf-8')
    
    def write_text(self, content: str):
        """Write text to file"""
        with self.hdfs.open_output_stream(self.path) as f:
            f.write(content.encode('utf-8'))
    
    def mkdir(self):
        """Create directory"""
        self.hdfs.create_dir(self.path)
    
    def unlink(self):
        """Delete file"""
        self.hdfs.delete_file(self.path)
    
    def rmdir(self, recursive: bool = False):
        """Remove directory"""
        self.hdfs.delete_dir(self.path, recursive=recursive)
    
    def size(self):
        """Get file size"""
        info = self.hdfs.get_file_info(self.path)
        return info.size
    
    def __str__(self):
        return self.path
    
    def __repr__(self):
        return f"HDFSPath('{self.path}')"

