



# test_user = input("Print some\n")
# test_user = r"https://api.1xbet.et/MobileLiveBetX/MobileGetTax?partner=232&gr=307&country=213&betSum=50.0&cf=1.74&currencyId=117&lng=ru"
# test_user = r"https://zjumapxjws.com/paysystems/deposit?host=https://zjumapxjws.com&lng=ru&sub_id=619581839&type=2&whence=22&h_guid=4c8b5788c13be643_2&X-TMSessionId=a21fbad5eab6698934b17989e617fcc5"



def printInfo(str):
    print(str.split("MobileLiveBetX")[0])
    print("----"*10)
    print(str.split("&")[0].split("?")[1])
    for i in range(1, 10):
        try:
            print(str.split("&")[i])  
        except(IndexError):
            break



def getData():
    dbCountries = ['Кения',
                   'Танзания',
                   'Уганда',
                   'Эфиопия',
                   'Гвинея-Бисау',
                   'Замбия',
                   'Мозамбик']
    
    dbPartners = ['1xbet',
                  '22Bet',
                  '888starz',
                  'Melbet',
                  'Helabet',
                  'betwinner',
                  'paripesa'
                  ]
    
    dbMap = {
        dbCountries[0]:{
            dbPartners[0]:[7.5, 20], 
            dbPartners[1]:[7.5, 20],
            dbPartners[2]:[7.5, 20],
            dbPartners[3]:[7.5, 20],
            dbPartners[4]:[None, 20],
            dbPartners[5]:[None, 20]
        },
        
        dbCountries[1]:{
            dbPartners[1]:[None, 15],
            dbPartners[4]:[None, 10],
            dbPartners[5]:[None, 10],
        },
        
        dbCountries[2]:{
            '22Bet':[None, 15],
            'Helabet':[None, 10],
            'betwinner':[None, 10],
        },

        dbCountries[3]:{
            '22Bet':[None, 15],
            'Helabet':[None, 10],
            'betwinner':[None, 10],
        },
        dbCountries[4]:{
            '22Bet':[None, 15],
            'Helabet':[None, 10],
            'betwinner':[None, 10],
        },
        dbCountries[5]:{
            '22Bet':[None, 15],
            'Helabet':[None, 10],
            'betwinner':[None, 10],
        },
        dbCountries[6]:{
            '22Bet':[None, 15],
            'Helabet':[None, 10],
            'betwinner':[None, 10],
        }
    }
    return dbMap


# for country, partner in mmmap.items():
#     print(country)
#     for pKey, pValue in partner.items():
#         print(pKey, ' ', pValue)
#     print("---------")

