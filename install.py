#! /usr/bin/python3
"""
Install gnome dynamic backgrounds 

author: Martino Ferrari
email: manda.mgf@gmail.com
"""

import os
import argparse
from shutil import copyfile
from pathlib import Path   
import temply 


def __args__():
    parser = argparse.ArgumentParser(description='Install custom Gnome dynamic background')
    parser.add_argument('images_dir', type=str, help='Directory containing the background images')
    parser.add_argument('name', type=str, help='Name of the background')
    parser.add_argument('--start-time', default=0, type=int, help='Custom start time in 24h format (default 00)')
    parser.add_argument('--duration', type=int, help='Custom static image duration in seconds (otherwise autocomptued)')
    parser.add_argument('--transition', type=int, help='Custom transition duration in seconds (otherwise autocomptued)')
    return parser.parse_args()


def __files__(base_path):
    files = list(os.listdir(base_path))
    files.sort()
    return files


def main():
    args = __args__()
    name = args.name
    print(f'Installing dynamic background: `{name}`')
    user_home = str(Path.home())
    images = __files__(args.images_dir)
    background_dir = os.path.join(user_home, '.local/share/backgrounds/gnome', f'{name}-timed')
   
    print('Creating background folders...', flush=True, end='')
    if not os.path.exists(background_dir):
        os.makedirs(background_dir)
    
    setting_dir = os.path.join(user_home, '.local/share/gnome-background-properties/')
    if not os.path.exists(setting_dir):
        os.makedirs(setting_dir)

    print(' [OK]')

    print('Copying images...', flush=True, end='')
    for image in images:
        copyfile(os.path.join(args.images_dir, image), os.path.join(background_dir, image))
    print(' [OK]')
    print('Creating XML files...', flush=True, end='')


    duration = 24 * 3600 // (len(images)*2)
    if args.duration is not None:
        duration = args.duration 
    transition = (24 * 3600 - (duration * len(images))) // len(images)
    if args.transition is not None:
        transition = args.transition
    template_file = open('template-timed.xml', 'r')
    timed_template = temply.Template(template_file.read())
    template_file.close()

    images_struct = [{'current': image, 'next': images[(i+1) % len(images)]} 
                        for i, image in enumerate(images)]

    xml = timed_template.generate(
        name=name,
        user_home=user_home,
        duration= duration,
        transition_duration=transition,
        images=images_struct
    )

    with open(f'{background_dir}.xml', 'w') as file:
        file.write(xml)

    template_file = open('template.xml', 'r')
    propierty_template = temply.Template(template_file.read())
    template_file.close()

    xml = propierty_template.generate(
        name=name,
        user_home=user_home
    )
    with open(os.path.join(setting_dir, f'{name}.xml'), 'w') as file:
        file.write(xml)

    print(' [OK]')

if __name__ == '__main__':
    main()



