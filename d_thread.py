import threading
import connector
import eelf


class DThread(threading.Thread):

    tquant = []
    gallery_dir = ''
    num = 0

    def __init__(self, dir, quant, num):
        threading.Thread.__init__(self)
        self.tquant = quant
        self.gallery_dir = dir
        self.num = num

    def run(self):
        self.quant_download(self. gallery_dir, self.num)

    def quant_download(self, dir, num):
        # try download and save image to local gallery
        try:
            img = connector.get_request(self.tquant['url'])
            if img != 'Error':
                title = self.filename(self.tquant['title'])
                quality = self.tquant['q']
                filename_out = f'/{num}-{title}_{quality}.jpg'
                file = open(dir + '/' + filename_out, 'wb')
                file.write(img.content)
                file.close()
                print(f"Downloading {filename_out}")
                #eelf.inteface_downloading_info(title, )
            else:
                print(f'Can not download image!')
        # if error
        except KeyError as ke:
            print(f'Error with parse JSON: {ke}')
        except PermissionError as pd:
            print(f'Can not download image {pd}, error: Permission Denied!')
        except Exception as error:
            print(f'Can not download image, error: {error}')

    def filename(self, filename):
        bad_chars = [';', ':', '!', "*", "@", "#", ".", "^", "/", "?", "=", "+", "|", "<", ">"]
        readyname = filter(lambda i: i not in bad_chars, filename)
        readyname = "".join(readyname)
        return readyname