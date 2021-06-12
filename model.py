"""
Random Forest Regressor model loaded from trained model data.
"""
import pickle
import requests
import json
import pandas as pd


class RFR_Model():
    RFR_MODEL = None
    DISTRICTS = []
    SOILS = []
    CROPS = []
    SEASONS = []
    COLS = []
    scaler = None

    def load_data(self):
        """Load Data from local store files into memory"""

        with open('store/model_dump.rfr', 'rb') as handle:
            self.RFR_MODEL = pickle.load(handle)

        with open('store/scaler.bin', 'rb') as handle:
            self.scaler = pickle.load(handle)

        with open('store/data.bin', 'r') as handle:
            all_data = handle.read()
            parts = all_data.split('|')
            self.DISTRICTS = parts[0].split(',')
            self.CROPS = parts[1].split(',')
            self.SEASONS = parts[2].split(',')
            self.SOILS = parts[3].split(',')
            self.COLS = parts[4].split(',')

    def structure_data(self, district, crop, soil, area, season):
        """
        Structure incoming data and scale to feed into models.\n  
        `returns` DataFrame to be fed into the regressor.
        """
        district = 'District:_' + district.upper()
        crop = 'Crop:_' + crop
        soil = 'Soil_type:_' + soil

        sx = [t for t in self.COLS if season in t]
        season = sx[0] if len(sx) > 0 else ''

        api_key = 'e618a01d6e94483a8a592355211106'
        try:
            response = requests.get(
                f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={district}&aqi=no')
            weather_data = json.loads(response.text)['current']
        except:
            return {'error': f'City {district} not found.'}

        preci = weather_data['precip_mm'] * 6
        humi = weather_data['humidity']
        temp = weather_data['temp_c']

        index_dict = dict(zip(self.COLS, range(len(self.COLS))))
        vect = {}
        for key, _ in index_dict.items():
            vect[key] = 0

        try:
            vect[district] = 1
        except:
            return {'error': 'Invalid District'}
        try:
            vect[crop] = 1
        except:
            return {'error': 'Invalid Crop'}
        try:
            vect[soil] = 1
        except:
            return {'error': 'Invalid Soil'}
        try:
            vect[season] = 1
        except:
            return {'error': 'Invalid Season'}
        try:
            vect['Area'] = area
        except:
            return {'error': 'Error in Area'}
        try:
            vect['Temperature'] = temp
        except:
            return {'error': 'Invalid Temperature'}
        try:
            vect['Precipitaion'] = preci
        except:
            return {'error': 'Invalid Precipitation'}
        try:
            vect['Humidity'] = humi
        except:
            return {'error': 'Invalid Humidity'}

        df = pd.DataFrame.from_records(vect, index=[0])
        # print(df.shape)
        df = self.scaler.transform(df)
        return df

    def predict(self, district, crop, soil, area, season):
        """Perform regression and generate output using provided data"""

        df = self.structure_data(district, crop, soil, area, season)
        crop_produce = self.RFR_MODEL.predict(df)
        # print(self.RFR_MODEL.get_params())
        return {
            'produce': crop_produce,
            'city': district,
            'crop': crop,
            'soil': soil,
            'area': int(area)
        }
