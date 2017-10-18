from src.UI.ChooseMicrophoneView import ChooseMicrophoneView
from src.Commons.InputDeviceInfo import InputDeviceInfo as Idi

def showChooseMicrophoneDialog(mics: list) -> int:
    """
    :param mics: list of available microphones
    :return: choosen device nr.
    """
    window = ChooseMicrophoneView(list)
    window.show()
    window.exec_()

