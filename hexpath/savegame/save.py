import pickle


class GameData:
    def __init__(self):
        self.gems = 0
        self.upgrades = []

    def erase_game(self):
        self.gems = 0
        self.upgrades = []
        self.save_gamedata()

    def save_gamedata(self):
        with open("savegame.dat", "wb") as file:
            pickle.dump(self, file)
            file.close()
            print("Saved..")

    def load_game(self):
        try:
            with open("savegame.dat", "rb") as file:
                lg = pickle.load(file)
                print(lg.gems)
                self.gems = lg.gems
                self.upgrades = lg.upgrades
        except (FileNotFoundError, AttributeError, TypeError, EOFError)as ERR:
            print("No save state found, create new one.", ERR)

    def get_mapped_bonus_ids(self):
        bonus_ids = []
        for upgrade in self.upgrades:
            bonus_ids.append(self.get_mapped_bonus_id(upgrade))
        return bonus_ids

    def get_mapped_bonus_id(self, upgrade):
        upgrades = {
            "ATKA01" : "ATK_1",
            "ATKA02" : "ATK_1",
            "ATKA03" : "ATK_1",
            "ATKA04" : "ATK_1",
            "ATKA05" : "ATK_1",
            "SPECA01" : "PEN_5",
            "ACCA01": "ACC_1",
            "ACCA02": "ACC_1",
            "ACCA03": "ACC_1",
            "ACCA04": "ACC_1",
            "ACCA05": "ACC_1",
            "SPECB01": "PSN_5",
            "CRITA01": "CRITC_1",
            "CRITA02": "CRITC_1",
            "CRITA03": "CRITC_1",
            "CRITA04": "CRITC_1",
            "CRITA05": "CRITC_1",
            "SPECC01": "HST_5",
            "BUSPA01": "BULSP_1",
            "BUSPA02": "BULSP_1",
            "BUSPA03": "BULSP_1",
            "BUSPA04": "BULSP_1",
            "BUSPA05": "BULSP_1",
            "SPECD01": "FRG_5",

         }
        return upgrades[upgrade]