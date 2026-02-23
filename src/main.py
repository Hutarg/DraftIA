from src.model import *
from src.stats import getStats, getAccount

model = Model("../models/v1.h5")

puuid = getAccount("europe", "Hutarg", "EUW")["puuid"]
prediction = model.predict("top", ["Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Ambessa", "Amumu", "Anivia", "Annie", "Aphelios"],
                    ["Zyra", "Aurelion Sol", "Aurora", "Azir", "Bard", "Bel'Veth", "Blitzcrank", "Brand", "Braum"], getStats("europe", puuid))

index = np.argmax(prediction)

print(list(championsIndices.keys())[index + 1])