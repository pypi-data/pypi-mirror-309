from zipfile import ZipFile 
import gdown
import configparser
import os

# Issues:
#   1. The RIT data gets unzipped into an extra directory, for example:
#            C:\spectral_data\spectral_images\Detection_Imagery_Cooke_City_RIT\Detection_Imagery_Cooke_City_RIT/blind_test_refl
#      when it should be:
#            C:\spectral_data\spectral_images\Detection_Imagery_Cooke_City_RIT/blind_test_refl


image_dict = {
            'WashingtonDC': ['WashingtonDC_Ref_156bands', '13NGtcTWsViteI1J46IDXldlMPPOnTNLz', 'spectral_images', 'WashingtonDC_Ref_156bands/WashingtonDC_Ref_156bands'],
            'MicroscenePolymers': ['Microscene_Polymers', '1SjIToGJwkkWyBZER5Wv-1v1-I22Y-EBI', 'spectral_images', 'Microscene_Polymers/reflectance_image_polymers'],
            'DetectionImagery_CookeCity_RIT': ['Detection_Imagery_Cooke_City_RIT', '1S97FG9UKdT7QHtnTmyvBq2VMZL-pDYt7', 'spectral_images', 'Detection_Imagery_Cooke_City_RIT/self_test_refl'],
            'VegBaccharisUPWINS': ['Vegetation_Baccharis_halmifolia_UPWINS', '1e5SloCAzXGIfDRlzhqYcmQ5JUMC8DweC', 'spectral_images', 'Vegetation_Baccharis_halmifolia_UPWINS/Morven_Baccharis_h_or_ref'],
            'PaintDetectionUPWINS': ['Morven_paint_samples_or_ref', '1WX_efoG5iIIYjg5Juh9tDz-Tk1BrElrk', 'spectral_images', 'Morven_paint_samples_or_ref/Morven_paint_samples_or_ref'],
            'indian_pines': ['indian_pines', '1d_348BZxHhWWhwo3Rt7jIo-hemG-FuWB', 'spectral_images', 'indian_pines/indian_pines'],
            'pavia_centre': ['pavia_centre', '1x3RJ2J_FzX-1wkmtmga7BvAZEwYt0_EY', 'spectral_images', 'pavia_centre/pavia_centre'],
            'pavia_university': ['pavia_university', '1ohdtA-0XGKRVSb5L9HfNHonBlTal1dIG', 'spectral_images', 'pavia_university/pavia_university'],
            'AVIRIS_Cuprite': ['AVIRIS_Cuprite', '1vG3vWdTfaLkCIticV3M9KH0oUgewptr2', 'spectral_images', 'AVIRIS_Cuprite/AVIRIS_cuprite_ang20200712t201415_subset'],
            'ENMAP_Cuprite': ['ENMAP_Cuprite', '1LIBLgDHs1Ov2gSlOKOEtjeqso6xR7jHv', 'spectral_images', 'ENMAP_Cuprite/ENMAP01-____L2A-DT0000013089_20230409T191307Z_001_V010402_20240326T021429Z-SPECTRAL_IMAGE.TIF']
}


lib_dict = {
            'GHISACONUS_2008_001_speclib': ['GHISACONUS_2008_001_speclib', '1b6XvgY46n-Dm8Df2QRiC1vE9Z7PA0VIa', 'spectral_libraries', 'GHISACONUS_2008_001_speclib/GHISACONUS_2008_001_speclib_orig.csv'],
            'Microscene_Polymers_Library': ['Microscene_Polymers_Library', '1WbG1xCgs4mhNth30-IRinrGIzT1W_Anh', 'spectral_libraries', 'Microscene_Polymers_Library/Polymers Full.sli'],
            'UPWINS_4_16_2024': ['UPWINS_4_16_2024', '11Zn-DxlVevtg-KAKnDRiPEVxnLYXDl5h', 'spectral_libraries', 'UPWINS_4_16_2024/UPWINS_4_16_2024.sli'],
            'Detection_Library_Cooke_City_RIT': ['Detection_Library_Cooke_City_RIT', '1ekB8TGOuumTIz_gQ3CAeAZrDjgscIbkr', 'spectral_libraries', 'Detection_Library_Cooke_City_RIT/Cooke_City_Targets'],
            'USGS_splib07b': ['USGS_splib07b', '1BqCoqxhtMjNHBZAsoQt874u5w7sfRUPx', 'spectral_libraries', 'USGS_splib07b/splib07b_asdfr.sli']
}

data_dict = {**image_dict, **lib_dict}


def available_datasets():
    print('Available Images:')
    for key in image_dict.keys():
        print('   '+key)
    print('Available Spectral Libraries:')
    for key in lib_dict.keys():
        print('   '+key)
    
        

def get_fname(data_name):
    # get the main directory for storing data
    data_dir = get_data_dir()
    # read the information for the requested image from the dict
    fname, fid, file_type, data_fname = data_dict[data_name]
    # get the full filename with path
    data_fname = os.path.join(data_dir,file_type, data_fname)    
    # print and return the full filename
    print('Primary Image Filename:')
    print(data_fname)
    return data_fname

   
def get_data_dir():    
    # get the home directory for the user - this is the directory where config files are aved
    home_dir = os.environ.get('HOME')  # For Linux/macOS
    if home_dir is None:
        home_dir = os.environ.get('USERPROFILE')  # For Windows
    # set the fname for the config file
    fname_config = os.path.join(home_dir,'hsi_data_config.ini')
    
    # get the location for storing spectral data from the hsi_data_config.ini config file
    config = configparser.ConfigParser()
    # Read the configuration file
    if os.path.isfile(fname_config):
        config.read(fname_config)
    else:
        data_dir = os.path.join('C:','\\spectral_data')
        set_data_dir(data_dir)
        config.read(fname_config)
        print('')
        print(f'No config file was found.')
        print(f'A config file was created at {fname_config}.')
        print(f'The data directory has been set to {data_dir}.')
        print('Spectral data will be downloaded and saved to this directory.')
        print('You can change the directory using hyperspectral_gta_data.set_data_dir(dirname).')
        print('')
    # read the data dir value from the configuration file
    data_dir = config.get('General', 'data_dir')
    
    # create the data directory if ti does not exist
    if not os.path.exists(data_dir):       
        os.makedirs(data_dir) 
        
    return data_dir
    
                                
def set_data_dir(data_dir):
    home_dir = os.environ.get('HOME')  # For Linux/macOS
    if home_dir is None:
        home_dir = os.environ.get('USERPROFILE')  # For Windows
    fname_config = os.path.join(home_dir,'hsi_data_config.ini')
    
    try:
        config = configparser.ConfigParser()
        # Add sections and key-value pairs
        config['General'] = {'data_dir': data_dir}
        # Write the configuration to a file
        with open(fname_config, 'w') as configfile:
            config.write(configfile)   
    except: 
        print('Directory value not valid.')     
        data_dir = os.path.join('C:','\\spectral_data')   
        config = configparser.ConfigParser()
        # Add sections and key-value pairs
        config['General'] = {'data_dir': data_dir}
        # Write the configuration to a file
        with open(fname_config, 'w') as configfile:
            config.write(configfile)      
            
                                  
def download_all():
    # download all imagery data
    for key in image_dict.keys():
        download(key)
    # download all spectral library data
    for key in lib_dict.keys():
        download(key)
    
    
class download:
    def __init__(self, data_name):
        self.data_dict = data_dict        
        self.data_dir = get_data_dir()
        
        try:
            # determine the file information
            fname, fid, file_type, self.data_fname = self.data_dict[data_name]   
            
            # create the subdirectory for the filetype if needed
            self.subdir_filetype = os.path.join(self.data_dir,file_type)
            
            if not os.path.isdir(self.subdir_filetype):
                os.mkdir(self.subdir_filetype) 
            
            # create the name of the directory where this data wil lbe stored
            self.subdir_data = os.path.join(self.subdir_filetype,fname)
            
            self.download_unzip(fname, fid);
            
        except:
            print('No data downloaded.  Available datasets are:')
            available_datasets()
            
            
    def download_unzip(self, fname, fid):
        
        # download and unzip the files if the directory for these files does not exist
        if not os.path.isdir(self.subdir_data):
            # Download the zip files of the image into the  subdirectory for the filetype
            fnameZip = os.path.join(self.subdir_filetype, fname+'.zip')
            if not os.path.isfile(fnameZip):
                gdown.download(id=fid, output=fnameZip)
            else:
                print(f'File {fnameZip} exists.')
            
            # Unzip the images into the directory for this data
            with ZipFile(fnameZip, 'r') as zObject: 
                zipped_filenames = zObject.namelist()
                zObject.extractall( 
                    path=os.path.join(self.subdir_data) ) 
            for zfname in zipped_filenames:
                print(f'File saved as: {os.path.join(self.subdir_data,zfname)}')
            
            # Delete the zip file
            os.remove(fnameZip)
            print(' ')
        
        print('Available Files:')
        for dirpath,_,filenames in os.walk(self.subdir_data):
            for f in filenames:
                print(os.path.abspath(os.path.join(dirpath, f)))
        
    
