# Gifify This Anime does not exist

This python script downloads and creates videos and gifs from [thisanimedoesnotexist.ai](https://thisanimedoesnotexist.ai).

The script donwloads the images at all creativity levels and makes them to a gif or video.

![Example for seed 65189](output_gif_65189.gif)

## Prerequisites

To get the script to work run:

```shell
python -m pip install -r requirenments.txt
```

## Running the script

You can just get the videos and gifs as showen below:

```shell
python gififyThisAnimeDoesNotExist.py <seed>
```

You can find the seeds from the web-page or just type somting random in between 0-99999.

`gififyThisAnimeDoesNotExist.py` takse a couple of optional arguments:

`-h`, `--help`: Print the help message.

`-o`, `--output`: The name of the output file. This also sets the type mp4,avi or gif if an extension is given. If no extension is given the type extension will be added to the output. If the `--type`-flag is set, the file will be saved with that type and the given extension no matter if they match. If extension is not valid and `-type` is not set the type will be set to gif, but the file will keep the given extension. Default output name is `output_gif_<seed>.gif`

`-t`, `--type`: The output type. (gif, avi or mp4). Default type is gif. If this is set the defualt output string is changed acordingly.

`--reverse`, `--loop`, `-l`: Adds the reverse version of the pictures to the en of the video/gif to make a perfect loop.

`--fps`, `-f`: Sets the fps to export with. No interpolation is used by default. This therefore also sets the length of the whole video or gif. Default is 8. If interpolation is used, the framerate will not change the video or gif will just get longer.

`--random`, `-r`: Overwrites seed with a random seed. When this is set, seed is not needed. If both is set, this takes precedence.

`--interpolate`, `-i`: Specifies the number of interpolations should run on the frame. Please note that this is exponential. A value of 3 e.g. means 8 times the frames. 0-3 is therefore recomended. For interpolation to work please download [cain-ncnn-vulkan](https://github.com/nihui/cain-ncnn-vulkan) and place the cain-ncnn-vulkan-YYYYDDMM-OS folder in the same folder as the script.

Example of how to download a random anime which loops and is interpolated 3 times with 30 fps and saved with the name `random.gif`.

```shell
python gififyThisAnimeDoesNotExist.py -r -i 3 -l -f 30 -o random.gif
```
