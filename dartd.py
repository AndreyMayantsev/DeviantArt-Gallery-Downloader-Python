import log
import os
import eelf
import connector
import downloader


class dartd:

    pics = []
    da_username = "username"
    log = log.log("mainLog")
    IS_ABORT_PROCESS = False
    downloader = None

    def __init__(self):
        self.log.writeLog('Start working:')

    def set_stop_work(self):
        self.downloader.set_stop_work()

    # DeviantArt composition
    # getting the url to download an avatar
    def get_avatar_url(self, name):
        return f"https://www.deviantart.com/_napi/da-user-profile/api/init/gallery?username={name}&deviations_limit=24&with_subfolders=true"

    # parsing info to get avatar image
    def parse_avatar_info(self, avatar):
        try:
            avatar_json = avatar.json()
            return avatar_json['pageData']['gruser']['usericon']
        except KeyError as ke:
            log.writeLog(f'Can not load avatar, KeyError: {ke}')
            return 'Error'

    # getting the url to download deviations list
    def get_deviations_url(self, name, offset):
        return f"https://www.deviantart.com/_napi/da-user-profile/api/gallery/contents?username={name}&offset={offset}&limit=10&all_folder=true&mode=newest"

    # getting deviations list with links to downloadable images - self.pics
    def get_deviation_list(self, res):
        res_json = res.json()
        offset = res_json['nextOffset']
        for a in res_json['results']:
            if self.IS_ABORT_PROCESS:
                break
            # search the list for links with the best image quality (8-1)
            quality_index = 8
            for x in range(8):
                try:
                    js_quality = a['deviation']['media']['types'][quality_index]['c']
                    break
                except Exception:
                    quality_index -= 1
            # creating an array for each image
            append_pic = {}
            try:
                append_pic['url'] = a['deviation']['media']['baseUri'] + "/" + js_quality + '?token=' + a['deviation']['media']['token'][0]
                append_pic['title'] = a['deviation']['title']
                append_pic['q'] = quality_index
                # update self.pics deviations list
                self.pics.append(append_pic)
                # View progress in interface EEL
                eelf.inteface_set_num(len(self.pics))
            except Exception as error:
                self.log.writeLog(f"USER: {self.da_username}, offset: {offset}: Error JSON parse: {error}\n\t--- [Data] ---\n\t {a} \n\t--- [End data] ---")
        return offset

    # DeviantArt interaction
    # getting an avatar image and saving it to a file _temp.jpg
    def get_avatar(self, name):
        url = self.get_avatar_url(name)
        avatar = connector.get_request(url)
        if avatar != 'Error':
            try:
                avatar_link = self.parse_avatar_info(avatar)
                if avatar_link != 'Error':
                    img = connector.get_request(avatar_link)
                    file = open('./web/_temp.jpg', 'wb')
                    file.write(img.content)
                    file.close()
                return True
            except KeyError as ex:
                return False
        else:
            self.log.writeLog(f'Can not connect to server and load avatar of user: {name}.')
            eelf.interface_error_message(f"User \"{name}\" was not found or there were problems with the internet connection!")

    # building a list of images
    def get_deviants_by_name(self, name):
        offset = 0
        while offset != None:
            if self.IS_ABORT_PROCESS:
                break
            # base url for load deviants by name and offset - limit = 10
            url = self.get_deviations_url(name, offset)
            res = connector.get_request(url)
            if res == 'Error':
                self.log.writeLog(f"User \"{name}\" was not found or there were problems with the internet connection!")
                eelf.interface_error_message(f"User \"{name}\" was not found or there were problems with the internet connection!")
            else:
                offset = self.get_deviation_list(res)

    # start gallery download
    def download_gallery(self, username):
        self.log.writeLog(f'Start downloading: User {username} image library length {len(self.pics)}')
        count = 0
        gallery_dir = './GALLERIES/' + username

        if self.folder_exists('./GALLERIES'):
            # check GALLERIES directory
            self.folder_exists(gallery_dir)

            self.downloader = downloader.Downloader(self.pics, username)

            count += 1
        else:
            print('Galleries folder does not exists and can not to be create!')
            self.log.writeLog(f'Galleries folder does not exists and can not to be create!')

    # System
    # check folder and make it if folder not exists
    def folder_exists(self, folder):
        if os.path.exists(folder):
            return True
        else:
            try:
                os.mkdir(folder)
                return True
            except PermissionError:
                print(f"Folder does not exists and can't be created! -> {folder} : Permission Denied!")
                return False
            except Exception as error:
                print(f"Folder does not exists and can't be created! -> {folder} : {error}")
                return False

    # file name corrector
    def filename(self, filename):
        bad_chars = [';', ':', '!', "*", "@", "#", ".", "^","/", "?", "=", "+", "|","<",">" ]
        readyname = filter(lambda i: i not in bad_chars, filename)
        readyname = "".join(readyname)
        return readyname

    # EEL self(
    def start(self, username):
        # clear list
        self.pics.clear()
        self.log.writeLog(f'Start work, username = {username}')

        if self.get_avatar(username):
            self.da_username = username
            # block start button in EEL form
            eelf.interface_preload()
            # get deviants list
            self.get_deviants_by_name(username);
            self.log.writeLog(f'Avatar and list loaded (username = {username}, size of list = {len(self.pics)})')
            maxposition = len(self.pics)

            if maxposition > 0:
                self.da_username = username
                # view downloading window in EEL form
                eelf.interface_user_info(username, maxposition)
            else:
                eelf.interface_error_message(f'User: {username} not found in DeviantArt!')
                self.da_username = ""

        else:
            print(f'Work Failed, list = {len(self.pics)}')
            self.log.writeLog(f'Work Failed, username = {username}, list size = {len(self.pics)}')

    def stop(self):
        print('Work aborted by user...')
        self.log.writeLog(f'Work forcibly stopped, username = {self.da_username}')
        self.da_username = ""
        self.IS_ABORT_PROCESS = False
