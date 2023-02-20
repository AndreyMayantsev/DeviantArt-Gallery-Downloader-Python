import eel


# EEL library
def start_eel_window(dartd_obj):

    dd = dartd_obj;
    eel.init("web")

    @eel.expose
    def start_form(username):
        dartd_obj.start(username)

    @eel.expose
    def start_download(username):
        dartd_obj.download_gallery(username)

    @eel.expose
    def abort_process():
        dartd_obj.IS_ABORT_PROCESS = True

    eel.start("main.html", size=(600, 500))

def interface_error_message(error):
    eel.errormsg(error)

def interface_user_info(username, maxposition):
    eel.download_start(username, maxposition)

def interface_preload():
    eel.jspreload(1)

def inteface_downloading_info(imagename, position, max):
    eel.downloading(imagename, position, max)

def inteface_set_num(num):
    eel.setnum(num)
