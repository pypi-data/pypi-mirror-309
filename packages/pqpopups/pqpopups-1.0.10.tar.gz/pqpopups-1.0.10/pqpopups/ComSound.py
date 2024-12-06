
import os
import platform
#import _util.loggingUtil

# ----------------------------------------------------------------------------------------------------------------------
# Sound
# ----------------------------------------------------------------------------------------------------------------------
class enSoundType():
    EN_BUTTON_SOUND_TYPE = 0
    EN_START_SOUND_TYPE = 1
    EN_NOTICE_SOUND_TYPE = 2
    EN_SHUTDOWN_SOUND_TYPE = 3
    EN_ERROR_SOUND_TYPE = 3

class enSoundSourceKind():
    EN_START_SOUND_SOURCE_01 = 0
    EN_START_SOUND_SOURCE_02 = 1
    EN_START_SOUND_SOURCE_03 = 2
    EN_START_SOUND_SOURCE_04 = 3

    EN_BUTTON_SOUND_SOURCE_01 = 10
    EN_BUTTON_SOUND_SOURCE_02 = 11
    EN_BUTTON_SOUND_SOURCE_03 = 12
    EN_BUTTON_SOUND_SOURCE_04 = 13

    EN_SHUTDOWN_SOUND_SOURCE_01 = 20
    EN_SHUTDOWN_SOUND_SOURCE_02 = 21
    EN_SHUTDOWN_SOUND_SOURCE_03 = 22
    EN_SHUTDOWN_SOUND_SOURCE_04 = 23

    EN_NOTICE_SOUND_SOURCE_01 = 30
    EN_NOTICE_SOUND_SOURCE_02 = 31
    EN_NOTICE_SOUND_SOURCE_03 = 32
    EN_NOTICE_SOUND_SOURCE_04 = 33

    EN_ERROR_SOUND_SOURCE_01 = 60
    EN_ERROR_SOUND_SOURCE_02 = 61

class enSoundOnOffMode():
    EN_SOUND_ON_MODE = str('1')
    EN_SOUND_OFF_MODE = str('0')
    
strOS = platform.system()

DEF_SOUND_PLAY_LINUX_CMD = "aplay -Dplug:default -F 800 "
if strOS == "Linux":
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DEF_SOUND_PATH = CURRENT_DIR + "/sound/"
else:
    import winsound
    DEF_SOUND_PATH = os.getcwd() + "\\res\\sound\\"

DEF_SOUND_SOURCE_KIND_PATH = ["start_1.wav", "start_2.wav", "start_3.wav", "start_4.wav","","","","","","",
                              "button_1.wav", "button_2.wav", "button_3.wav", "button_4.wav","","","","","","",
                              "shutdown_1.wav", "shutdown_2.wav", "shutdown_3.wav", "shutdown_4.wav","","","","","","",
                              "Notice_1.wav", "Notice_2.wav", "Notice_3.wav", "Notice_4.wav","","","","","",""]
soundStart = enSoundSourceKind.EN_START_SOUND_SOURCE_02
soundButton = enSoundSourceKind.EN_BUTTON_SOUND_SOURCE_03
soundShutdown = enSoundSourceKind.EN_SHUTDOWN_SOUND_SOURCE_01
soundNotice = enSoundSourceKind.EN_NOTICE_SOUND_SOURCE_01

def play(sndType):
    # _util.loggingUtil.logger_info("play SoundOnOff:{0}, sndType:{1}".format(str(systemInfo.systemInfo.systemSetting.SoundOnOff), str(sndType)))
    #if str(systemInfo.systemInfo.systemSetting.SoundOnOff) == str(enSoundOnOffMode.EN_SOUND_ON_MODE):
    if sndType == enSoundType.EN_START_SOUND_TYPE:
        strSndFilePath = DEF_SOUND_PATH + DEF_SOUND_SOURCE_KIND_PATH[soundStart]
    elif sndType == enSoundType.EN_BUTTON_SOUND_TYPE:
        strSndFilePath = DEF_SOUND_PATH + DEF_SOUND_SOURCE_KIND_PATH[soundButton]
    elif sndType == enSoundType.EN_SHUTDOWN_SOUND_TYPE:
        strSndFilePath = DEF_SOUND_PATH + DEF_SOUND_SOURCE_KIND_PATH[soundShutdown]
    elif sndType == enSoundType.EN_NOTICE_SOUND_TYPE:
        strSndFilePath = DEF_SOUND_PATH + DEF_SOUND_SOURCE_KIND_PATH[soundNotice]
    if strOS == "Linux":
        os.system("pkill -9 aplay")
        cmd = DEF_SOUND_PLAY_LINUX_CMD + strSndFilePath + " &"
        os.system(cmd)
           # _util.loggingUtil.logger_info("play cmd:{0}".format(str(cmd)))
        # else:
        #     winsound.PlaySound(strSndFilePath, winsound.SND_FILENAME) # 음원이 너무 짧아서 확인 안됨 (긴파일로 확인함)


def playBarcodeSuccess():
    #if str(systemInfo.systemInfo.systemSetting.SoundOnOff) == str(enSoundOnOffMode.EN_SOUND_ON_MODE):
    if strOS == "Linux":
        cmd = DEF_SOUND_PLAY_LINUX_CMD + DEF_SOUND_PATH + "beep.wav &"
        os.system(cmd)
            #_util.loggingUtil.logger_info("play cmd:{0}".format(str(cmd)))

def playBarcodeTimeout():
    #if str(systemInfo.systemInfo.systemSetting.SoundOnOff) == str(enSoundOnOffMode.EN_SOUND_ON_MODE):
    if strOS == "Linux":
        cmd = DEF_SOUND_PLAY_LINUX_CMD + DEF_SOUND_PATH + "beep_beep_beep.wav &"
        os.system(cmd)
        #_util.loggingUtil.logger_info("play cmd:{0}".format(str(cmd)))
