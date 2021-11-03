import glob
import pprint
import os
import re
import pathlib

mp4_path = ""

img_path = ""


def get_mp4_list():
    print('get mp4 list')
    mp4_files_full = glob.glob(mp4_path + "*.mp4")

    mp4_files = [os.path.split(f)[-1] for f in mp4_files_full]
    mp4_files = [f.split(' ')[0] for f in mp4_files]
    
    mp4_files = [re.sub('CD[0-9]*', '', f) for f in mp4_files]
    mp4_files = [re.sub('-', '', f) for f in mp4_files]
    mp4_files = [f.replace('[モザイク破壊]', '') for f in mp4_files]
    
    print(mp4_files)
    print(len(mp4_files))
    return mp4_files_full, mp4_files


def search_image(mp4_files):
    print('search image from mp4 title')

    img_folder = glob.glob(img_path + '*')
    img_folder_name = [os.path.split(f)[-1] for f in img_folder]

    search_result = []

    for i_mp4, mp4 in enumerate(mp4_files):
        for i_img, img in enumerate(img_folder_name):
            if mp4 in img:
                img_file = img_folder[i_img] + '\\' + img + '_0.jpg'
                break
            else:
                img_file = None
        
        if img_file is None:
            search_result.append("")
        else:
            search_result.append(img_file)
    
    print(search_result)
    print(len(search_result))
    
    # for file in search_result:
    #     print('exist: {}, path: '.format(os.path.exists(file)))
    return search_result


def main():
    mp4_files_full, mp4_files = get_mp4_list()
    img_files_full = search_image(mp4_files)

    # ps_tmp = "powershell -Command "
    output_path = mp4_path + 'output\\'
    pathlib.Path(output_path).mkdir(exist_ok=True, parents=True)
    mp4_names = [os.path.split(f)[-1] for f in mp4_files_full]

    for path_set in list(zip(mp4_files_full, img_files_full, mp4_names)):
        if path_set[1] == "":
            continue
        
        p_cmd = "atomicparsley "
        p_cmd += "\"" + path_set[0] + "\"" + ' --artwork '
        p_cmd += "\"" + path_set[1] + "\" "
        p_cmd += "-o " + "\"" + output_path + path_set[2] + "\""

        with open('./command.txt', 'a') as f:
            f.write(p_cmd + '\n')


if __name__ == "__main__":
    main()

