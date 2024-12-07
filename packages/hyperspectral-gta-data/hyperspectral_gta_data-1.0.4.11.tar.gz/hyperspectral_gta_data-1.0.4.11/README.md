# hyperspectral_gta_data
A simple package to access hyperspectral images and spectral libraries.

The data system is created by Geospatial Technology Associates (GTA).
[www.geospatialtech.com](https://www.geospatialtec.com/)

## Images Provided:

### WashingtonDC_Ref_156bands
Download command:
```
hyperspectral_gta_data.download('WashingtonDC')
fname = 'spectral_images/WashingtonDC_Ref_156bands/WashingtonDC_Ref_156bands'
```
![image](https://github.com/user-attachments/assets/c31e1796-c36a-4de2-ae90-deb8a6d04eb1)  
Sensor: HYDICE  
Units: Reflectance  
Collection Date: August 23, 1995  
Image Dimensions: 1280 rows, 307 columns, 156 bands  
Spectral Range: 401.2881 ~ 2473.16 nm   
Spatial Resolution: 3m GSD  
Publications:  
D. Landgrebe, "Hyperspectral image data analysis," in IEEE Signal Processing Magazine, vol. 19, no. 1, pp. 17-28, Jan. 2002, doi: [10.1109/79.974718](https://doi.org/10.1109/79.974718).   

### reflectance_image_polymers
Download command: 
```
hyperspectral_gta_data.download('MicroscenePolymers')
fname = 'spectral_images\Microscene_Polymers\reflectance_image_polymers'
```
![image](https://github.com/user-attachments/assets/ae4aef6e-16a5-4bf7-ac51-7d946d638134)  
Sensor: SPECIM FENIX  
Units: Reflectance  
Collection Date: July 7, 2018  
Image Dimensions: 852 rows, 384 columns, 452 bands  
Spectral Range: 378.6nm - 2500nm   
Spatial Resolution: 3mm GSD  
Publications:  
B. Basener, "Neural Network Learning Of Chemical Bond Representations In Spectral Indices And Features," 2022 12th Workshop on Hyperspectral Imaging and Signal Processing: Evolution in Remote Sensing (WHISPERS), Rome, Italy, 2022, pp. 1-9, doi: [10.1109/WHISPERS56178.2022.9955112](https://doi.org/10.1109/WHISPERS56178.2022.9955112)


### Morven_paint_samples_or_ref
Download command: 
```
hyperspectral_gta_data.download('PaintDetectionUPWINS')
fname = 'spectral_images/Vegetation_Baccharis_halmifolia_UPWINS/Morven_paint_samples_or_ref''
```
![image](https://github.com/user-attachments/assets/eeefa24c-3bf9-44b9-8442-d4eabb5bcf0b)



### Vegetation_Baccharis_halmifolia_UPWINS
Download command: 
```
hyperspectral_gta_data.download('VegBaccharisUPWINS')
fname = 'spectral_images/Vegetation_Baccharis_halmifolia_UPWINS/Morven_Baccharis_h_or_ref'
```
![image](https://github.com/user-attachments/assets/5e118b70-1aa6-4351-af9e-c65d3ae00e2f)
