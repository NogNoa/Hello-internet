from typing import Dict


class SaveNotFoundError(FileNotFoundError):
    pass


def Save(sav_nom):
    import pickle

    def back():
        return sav_nom

    def save_write(args: Dict[str, str]) -> Dict[str, str]:
        with open(sav_nom, "w+") as save:
            pickle.dump(args, save)
        return args

    def save_read() -> Dict[str, str]:
        try:
            with open(sav_nom, "r") as save:
                args = pickle.load(save)
        except (FileNotFoundError, pickle.UnpicklingError):
            raise SaveNotFoundError
        else:
            return args

    back.write, back.read = save_write, save_read
    return back
