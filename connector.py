import requests
import log

logC = log.log("Connector")
proxy_use = False
proxy = {} """ {"http":"http://165.255.24.114:8080", "https":"206.189.131.53:443"} """


def get_request(url):

    try:
        if proxy_use:

            res = requests.get(url, proxies = proxy)

            if res.ok():
                return res
            else:
                return 'Error'

        else:

            res = requests.get(url)

            if res.ok:
                return res
            else:
                return 'Error'

    except BrokenPipeError:
        logC.writeLog(f"Connection error: proxy = {proxy}, Broken_Pipe")
        return 'Error'
    except ConnectionAbortedError:
        logC.writeLog(f"Connection error: proxy = {proxy}, Connection_Aborted")
        return 'Error'
    except ConnectionRefusedError:
        logC.writeLog(f"Connection error: proxy = {proxy}, Connection_Refused")
        return 'Error'
    except ConnectionResetError:
        logC.writeLog(f"Connection error: proxy = {proxy}, Connection_Reset")
        return 'Error'
    except Exception as error:
        logC.writeLog(f"Connection error: proxy = {proxy}, ERROR: {error}")
        return 'Error'


def proxy_init(url, proxy):

    try:

        res = requests.get(url, proxies = proxy)

        if res.ok:
            print(f'Proxy test complete: {res.status_code}')
        else:
            print(f'Proxy test ERROR: {res.status_code}')

        logC.writeLog(f"OK proxy settings! {proxy}, status = {res.status_code}")

    except BrokenPipeError:
        logC.writeLog(f"Connection error: proxy = {proxy}, Broken_Pipe")
        return 'Error'
    except ConnectionAbortedError:
        logC.writeLog(f"Connection error: proxy = {proxy}, Connection_Aborted")
        return 'Error'
    except ConnectionRefusedError:
        logC.writeLog(f"Connection error: proxy = {proxy}, Connection_Refused")
        return 'Error'
    except ConnectionResetError:
        logC.writeLog(f"Connection error: proxy = {proxy}, Connection_Reset")
        return 'Error'
    except Exception as error:
        logC.writeLog(f"Connection error: proxy = {proxy}, ERROR: {error}")
        return 'Error'
