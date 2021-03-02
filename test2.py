import yfinance as yf
import pandas as pd



tickers_CAC40_dict = {'Accor': 'AC.PA', 'Air Liquide': 'AI.PA',
                      'Airbus': 'AIR.PA', 'ArcelorMittal': 'MT.AS',
                      'Atos': 'ATO.PA', 'AXA': 'CS.PA',
                      'BNP Paribas': 'BNP.PA', 'Bouygues': 'EN.PA',
                      'Capgemini': 'CAP.PA', 'Carrefour': 'CA.PA',
                      'Crédit Agricole': 'ACA.PA', 'Danone': 'BN.PA',
                      'Dassault Systèmes': 'DSY.PA', 'Engie': 'ENGI.PA',
                      'Essilor': 'EL.PA', 'Hermès': 'RMS.PA',
                      'Kering': 'KER.PA', "L'Oréal": 'OR.PA',
                      'Legrand': 'LR.PA', 'LVMH': 'MC.PA',
                      'Michelin': 'ML.PA', 'Orange': 'ORA.PA',
                      'Pernod Ricard': 'RI.PA', 'PSA': 'UG.PA',
                      'Publicis': 'PUB.PA', 'Renault': 'RNO.PA',
                      'Safran': 'SAF.PA', 'Saint-Gobain': 'SGO.PA',
                      'Sanofi': 'SAN.PA', 'Schneider Electric': 'SU.PA', 'Société Générale': 'GLE.PA',
                      'Sodexo': 'SW.PA', 'STMicroelectronics': 'STM.PA', 'Thales': 'HO.PA', 'Total': 'FP.PA',
                      'Unibail-Rodamco-Westfield': 'URW.AS', 'Veolia': 'VIE.PA', 'Vinci': 'DG.PA',
                      'Vivendi': 'VIV.PA', 'Worldline': 'WLN.PA', 'CAC40': '^FCHI'}
tickers_CAC40_dict={'Air Liquide': 'AI.PA', 'Airbus': 'AIR.PA', 'Alstom': 'ALO.PA', 'ArcelorMittal': 'MT.AS', 'Atos': 'ATO.PA', 'AXA': 'CS.PA', 'BNP Paribas': 'BNP.PA', 'Bouygues': 'EN.PA', 'Capgemini': 'CAP.PA', 'Carrefour': 'CA.PA', 'Crédit Agricole': 'ACA.PA', 'Danone': 'BN.PA', 'Dassault Systèmes': 'DSY.PA', 'Engie': 'ENGI.PA', 'EssilorLuxottica': 'EL.PA', 'Hermès': 'RMS.PA', 'Kering': 'KER.PA', "L'Oréal": 'OR.PA', 'Legrand': 'LR.PA', 'LVMH': 'MC.PA', 'Michelin': 'ML.PA', 'Orange': 'ORA.PA', 'Pernod Ricard': 'RI.PA', 'Publicis': 'PUB.PA', 'Renault': 'RNO.PA', 'Safran': 'SAF.PA', 'Saint-Gobain': 'SGO.PA', 'Sanofi': 'SAN.PA', 'Schneider Electric': 'SU.PA', 'Société Générale': 'GLE.PA', 'Stellantis': 'STLA.PA', 'STMicroelectronics': 'STM.PA', 'Teleperformance': 'TEP.PA', 'Thales': 'HO.PA', 'Total': 'FP.PA', 'Unibail-Rodamco-Westfield': 'URW.AS', 'Veolia': 'VIE.PA', 'Vinci': 'DG.PA', 'Vivendi': 'VIV.PA', 'Worldline': 'WLN.PA'}

df = pd.DataFrame()
print(tickers_CAC40_dict)
for key, value in tickers_CAC40_dict.items():
    data = yf.Ticker(value).history(period='5d')["Close"]
    data = data.pct_change()

    try:
        df[key]=data
    except:
        print('key {} value {}'.format(key, value))

print(df.shape[1])
