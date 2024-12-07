import json

image_dict = {
            'WashingtonDC': ['WashingtonDC_Ref_156bands', '13NGtcTWsViteI1J46IDXldlMPPOnTNLz', 'spectral_images', 'WashingtonDC_Ref_156bands/WashingtonDC_Ref_156bands'],
            'MicroscenePolymers': ['Microscene_Polymers', '1SjIToGJwkkWyBZER5Wv-1v1-I22Y-EBI', 'spectral_images', 'Microscene_Polymers/reflectance_image_polymers'],
            'FabricVehicleDetectionRIT': ['Detection_Test_Cooke_City_RIT', '1TxTiM98Fc-D5_ZBFlOlceR0lXdH5qqEo', 'spectral_images', 'Detection_Test_Cooke_City_RIT/self_test/self_test/HyMap/self_test_refl.img'],
            'VegBaccharisUPWINS': ['Vegetation_Baccharis_halmifolia_UPWINS', '1e5SloCAzXGIfDRlzhqYcmQ5JUMC8DweC', 'spectral_images', 'Vegetation_Baccharis_halmifolia_UPWINS/Morven_Baccharis_h_or_ref'],
            'PaintDetectionUPWINS': ['Morven_paint_samples_or_ref', '1WX_efoG5iIIYjg5Juh9tDz-Tk1BrElrk', 'spectral_images', 'Morven_paint_samples_or_ref/Morven_paint_samples_or_ref'],
            'indian_pines': ['indian_pines', '1d_348BZxHhWWhwo3Rt7jIo-hemG-FuWB', 'spectral_images', 'indian_pines/indian_pines'],
            'pavia_centre': ['pavia_centre', '1x3RJ2J_FzX-1wkmtmga7BvAZEwYt0_EY', 'spectral_images', 'pavia_centre/pavia_centre'],
            'pavia_university': ['pavia_university', '1ohdtA-0XGKRVSb5L9HfNHonBlTal1dIG', 'spectral_images', 'pavia_university/pavia_university']
}

lib_dict = {
            'GHISACONUS_2008': ['GHISACONUS_2008_001_speclib', '1b6XvgY46n-Dm8Df2QRiC1vE9Z7PA0VIa', 'spectral_libraries', 'GHISACONUS_2008_001_speclib/GHISACONUS_2008_001_speclib_orig.csv'],
            'MicroscenePolymersLibrary': ['Microscene_Polymers_Library', '1WbG1xCgs4mhNth30-IRinrGIzT1W_Anh', 'spectral_libraries', 'Microscene_Polymers_Library/Polymers Full.sli'],
            'UPWINS_4_16_2024': ['UPWINS_4_16_2024', '11Zn-DxlVevtg-KAKnDRiPEVxnLYXDl5h', 'spectral_libraries', 'UPWINS_4_16_2024/UPWINS_4_16_2024.sli']
}

data_dict = {**image_dict, **lib_dict}

fname_json = 'data_dict_json.txt'
with open(fname_json, 'w') as data_dict_file: 
     data_dict_file.write(json.dumps(data_dict))