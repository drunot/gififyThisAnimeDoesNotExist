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

`gififyThisAnimeDoesNotExist.py` now takse a couple of optional arguments:

`-h`, `--help`: Print the help message.

`-o`, `--output`: The output file. This also sets the type mp4,avi or gif if an extension is given. If no extension is given the set type extension will be added to the output. If type is set. It will be saved with that type no matter the extension. If extension is not valid. The type will be set to gif. Default is output_gif_\<seed\>.gif

`-t`, `--type`:  The output type. (gif, avi or mp4). Default is gif. If this is set the defualt output string is changed acordingly.

`--reverse`, `--loop`, `-l`: Adds the reverse version of the pictures to the en of the video/gif to make a perfect loop.

`--fps`, `-f`: Sets the fps to export with. No interpolation is used. This in turn also sets the length of the whole video or gif. Default is 8.

`--random`, `-r`: Overwrites seed with a random seed. When this is set, seed is not needed.

`--interpolate`, `-i`: Makes interpolation of the frames. For interpolation to work please download [cain-ncnn-vulkan](https://github.com/nihui/cain-ncnn-vulkan) and place that in the same folder as the script.