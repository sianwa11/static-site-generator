import os
import shutil

def copy_dir(src, dest):
  if not os.path.exists(dest):
    os.mkdir(dest)
    print(f"Made directory: {dest}")
  else:
    for filename in os.listdir(dest):
      file_path = os.path.join(dest, filename)
      if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted file: {filename}")
      else:
        shutil.rmtree(file_path, ignore_errors=False)

  for filename in os.listdir(src):
    file_path = os.path.join(src, filename)
    if os.path.isfile(file_path):
      shutil.copy(file_path, dest)
    else:
      copy_dir(file_path, f"{dest}/{filename}")

  