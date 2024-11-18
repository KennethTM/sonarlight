# sonarlight
The `sonarlight` package provides tools for working with Lowrance sonar data in the `.sl2` and `.sl3` formats. The package includes the `Sonar` class for reading and parsing these files, as well as methods for extracting various types of information from the data. 

Project home is [https://github.com/KennethTM/sonarlight](https://github.com/KennethTM/sonarlight).

## Installation
To install the `sonarlight` package, simply run:

```
pip install sonarlight
```

The package requires the `numpy` and `pandas` packages to be installed.

## Example data
Small example files of the `.sl2` and `.sl3` formats are provided in the `example_files` folder.

## Usage
Once installed, you can use the `Sonar` class to read and parse sonar data from a `.sl2` or `.sl3` file.

When reading a file with `Sonar()` with argument `clean=True` (default) some light data cleaning is performed including dropping unknown columns and rows and observation where the water depth is 0. Setting `augment_coords=True` performs augmentation of the recorded coordinates as implemented in [SL3Reader](https://github.com/halmaia/SL3Reader). Coordinate augmentation attempts to make up for the reduced precision in the recorded coordinates which are rounded to the nearest meter.

The class contains a few methods for extracting data:

* `Sonar.image()` method to extract the raw sonar image for a specific channel
* `Sonar.sidescan_xyz()` method to extract georeferenced sidescan data as XYZ coordinates
* `Sonar.water()` method to extract the water column part of the the raw sonar imagery for a specific channel
* `Sonar.bottom()` method to extract the bottom (sediment) part of the the raw sonar imagery for a specific channel
* `Sonar.bottom_intensity()` method to extract raw sonar intensity at the bottom

The functionality of the class is showcased below and included in the `example_notebook.ipynb`.

Example of reading a sonar file using the `example_files/example_sl2_file.sl2` file:

```python
from sonarlight import Sonar

#Read data from a '.sl2' or '.sl3' file
sl2 = Sonar('path/to/file.sl2')

#See summary of data and available channels
sl2

#Output:
'''
Summary of SL2 file:

- Primary channel with 3182 frames
- Secondary channel with 3182 frames
- Downscan channel with 3182 frames
- Sidescan channel with 3181 frames

Start time: 2023-09-13 08:20:36.840000
End time: 2023-09-13 08:22:52.770999808

File info: version 2, device 2, blocksize 3200, frame version 8
'''

#View raw data store in Pandas dataframe
sl2.df

#Each row contains metadata and pixel for each recorded frame.
#Pixels are stored in the "frames" column.
#The dataframe can be saved for further processing, 
#for example the Parquet file format that supports nested data structues.
sl2.df.to_parquet('sl2.parquet')

#Or to '.csv' file
sl2.df.to_csv("sl2.csv")

#Or to '.csv' file after dropping the "frames" column containing nested arrays
df_csv = sl2.df.copy().drop(["frames"], axis=1)
df_csv.to_csv("sl2.csv")
```

Examples of further processing and plotting (see also `example_notebook.ipynb`):

```python
import matplotlib.pyplot as plt

#Plot route and water depth (meters)
route = sl2.df.query("survey == 'primary'")
plt.scatter(route["longitude"], route["latitude"], c=route["water_depth"], s = 3)
plt.colorbar()
```

![](https://github.com/KennethTM/sonarlight/blob/main/images/example_notebook_route.png)

```python
#Plot primary channel
prim = sl2.image("primary")
plt.imshow(prim.transpose())
```

![](https://github.com/KennethTM/sonarlight/blob/main/images/example_notebook_image.png)

```python
#Plot water column (surface to water_depth) from downscan channel
#Individual frames are linearly interpolated of length 'pixels'
downscan_water = sl2.water("downscan", pixels=300)
plt.imshow(downscan_water.transpose())
```

![](https://github.com/KennethTM/sonarlight/blob/main/images/example_notebook_water.png)

```python
#Plot bottom column (water_depth to max sonar range) from primary channel
#Individual frames are subsetted to match the minimum length of the bottom frames
secondary_bottom = sl2.bottom("secondary")
plt.imshow(secondary_bottom.transpose())
```

![](https://github.com/KennethTM/sonarlight/blob/main/images/example_notebook_bottom.png)

```python
#Plot sidescan georeferenced points
#Convert sidescan imagery to XYZ point cloud
#Note that this can result in MANY points, every 10'th point are plotted here
mosaic=sl2.sidescan_xyz()
plt.scatter(mosaic.x[::10], 
            mosaic.y[::10], 
            c=mosaic.z[::10], 
            cmap="cividis", s=0.1)
```

![](https://github.com/KennethTM/sonarlight/blob/main/images/example_notebook_xyz.png)

## Ressources
The package is inspired by and builds upon other tools and descriptions for processing Lowrance sonar data, e.g. [SL3Reader](https://github.com/halmaia/SL3Reader) which includes a usefull paper, [python-sllib](https://github.com/opensounder/python-sllib), [sonaR](https://github.com/KennethTM/sonaR), [Navico_SLG_Format notes](https://www.memotech.franken.de/FileFormats/Navico_SLG_Format.pdf), older [blog post](https://www.datainwater.com/post/sonar_numpy/).

## Release notes

0.1.5 - Fixed offset error (off by 8 bytes) when reading frames.

## Other image examples

![](https://github.com/KennethTM/sonarlight/blob/main/images/primary_void.png)

![](https://github.com/KennethTM/sonarlight/blob/main/images/primary_plants.png)

![](https://github.com/KennethTM/sonarlight/blob/main/images/sidescan.png)

![](https://github.com/KennethTM/sonarlight/blob/main/images/route_cluster.png)
