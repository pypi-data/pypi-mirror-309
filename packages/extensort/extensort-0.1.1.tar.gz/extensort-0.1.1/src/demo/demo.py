import extensort
extensions={
            'JPG':'images',
            'jpeg':'images',
            'pptx':'slides',
            'zip':'compressed',
            'rar':'compressed',
            'pdf':'documents',
            'docx':'documents',
            'png':'images',
            'exe':'executables'  
            }

dirs="E:\\Misc"
types=extensort.find_extensions(dirs)
print(types)
res=extensort.sort_files(dir_to_sort=dirs,extensions=extensions)
print(f"Summary:{res}")