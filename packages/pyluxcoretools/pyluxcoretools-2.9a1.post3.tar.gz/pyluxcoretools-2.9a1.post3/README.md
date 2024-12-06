A Python package to provide LuxCoreTools.

# LuxCoreRender
LuxCoreRender is a physically correct, unbiased rendering engine.
It is built on physically based equations that model the transportation of
light. This allows it to accurately capture a wide range of phenomena which
most other rendering programs are simply unable to reproduce.

You can find more information about at: https://www.luxcorerender.org

Sources can be found here: https://github.com/LuxCoreRender/LuxCore


# PyLuxCoreTools
PyLuxCoreTools are a set of command line tools available in the LuxCoreRender stand-alone version. They include
command line rendering, film merging and image conversion to tx format.

## PyLuxCoreConsole
Command line rendering.

```
usage: pyluxcoreconsole [-h] [-f FILE_NAME] [-w WIDTH] [-e HEIGHT] [-D PROP_NAME VALUE]
                        [-d DIR_NAME] [-c] [-t CAMERA_SHUTTER CAMERA_SHUTTER]
                        fileToRender

PyLuxCoreConsole

positional arguments:
  fileToRender          .cfg, .lxs, .bcf or .rsm file to render

options:
  -h, --help            show this help message and exit
  -f FILE_NAME, --scene FILE_NAME
                        scene file name
  -w WIDTH, --film-width WIDTH
                        film width
  -e HEIGHT, --film-height HEIGHT
                        film height
  -D PROP_NAME VALUE, --define PROP_NAME VALUE
                        assign a value to a property
  -d DIR_NAME, --current-dir DIR_NAME
                        current directory path
  -c, --remove-unused   remove all unused meshes, materials, textures and image maps
  -t CAMERA_SHUTTER CAMERA_SHUTTER, --camera-shutter CAMERA_SHUTTER CAMERA_SHUTTER
                        camera shutter open/close
```

## PyLuxCoreMerge
Film merging.


```
usage: pyluxcoremerge [-o FILE_NAME] [-f FILE_NAME] [-h] [-a AOV_NAME FILE_NAME]

PyLuxCoreMerge

options:
  -o FILE_NAME, --image-output FILE_NAME
                        Save the RGB_IMAGEPIPELINE film output to a file
  -f FILE_NAME, --film-output FILE_NAME
                        Save the merge film to a file
  -h, --help            Show this help message and exit
  -a AOV_NAME FILE_NAME, --aov-output AOV_NAME FILE_NAME
                        Save the merge film AOV to a file
usage: cmd.py [-p] [-s]
              [-r SRC_OFFSET_X SRC_OFFSET_Y SRC_WIDTH SRC_HEIGHT DST_OFFSET_X DST_OFFSET_Y]
              fileFilm

Film Options

positional arguments:
  fileFilm              .cfg, .flm or .rsm files with a film

options:
  -p, --pixel-normalized-channel
                        The film will have CHANNEL_RADIANCE_PER_PIXEL_NORMALIZED (required by
                        all render engines)
  -s, --screen-normalized-channel
                        The film will have CHANNEL_RADIANCE_PER_SCREEN_NORMALIZED (required
                        by BIDIRCPU and LIGHTCPU render engines)
  -r SRC_OFFSET_X SRC_OFFSET_Y SRC_WIDTH SRC_HEIGHT DST_OFFSET_X DST_OFFSET_Y, --region SRC_OFFSET_X SRC_OFFSET_Y SRC_WIDTH SRC_HEIGHT DST_OFFSET_X DST_OFFSET_Y
                        Define the origin and the size of the region in the source film and
                        the placement in the destination film where the it will be merged
```

## PyLuxCoreMakeTx
Image conversion to tx format.

```
usage: pyluxcoremaketx [-h] srcImageFileName dstImageFileName

PyLuxCoreMakeTx

positional arguments:
  srcImageFileName  source image file name to convert
  dstImageFileName  destination image TX file name

options:
  -h, --help        show this help message and exit
```


# Install

`pip install pyluxcoretools`

# License
This package is released under Apache 2.0 license.
