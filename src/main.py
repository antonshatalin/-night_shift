import imaplib
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import yaml
from time import sleep
import sys
import datetime
from os import system

try:
    with open('config.yaml','r' ) as config:
        CONFIG = yaml.safe_load(config)
except FileNotFoundError:
    print('config file not found')
    sys.exit(1)

def check_unseen_messages(imap) -> tuple:
    letters_uid = imap.uid('search','UNSEEN')
    if letters_uid[1][0] != b'' and letters_uid[0] == 'OK':
        return (True, letters_uid)
    else: return (False, None)

def parse_mail(letters_uids:dict, imap):
    count = 0
    for letter_uid in (letters_uids[1][0].split()):
        res, msg = imap.uid('fetch', letter_uid, '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])
        subject = decode_header(msg["Subject"])[0][0].decode('utf-8')
        if msg.is_multipart():
            count+=1
            # print(f'is multi {letter_uid}, subject {subject}')
            for part in msg.walk():
                pass
                # print(part.get_content_type())
                if (part.get_content_maintype() == 'text') and (part.get_content_subtype() == 'plain'):
                    # print(base64.b64decode(part.get_payload()).decode())
                    print(count)
                    pass

                # if (part.get_content_maintype() == 'text') and (part.get_content_subtype() == 'html'):
                #     # print(part.get_payload())
                #     # print(base64.b64decode(part.get_payload()).decode())
                #     print(2)
                #     pass
                # if (part.get_content_maintype() == 'text') and (part.get_content_subtype() == 'html') and (part.get_content_subtype() == 'plain'):
                #     # print(part.get_payload())
                #     # print(base64.b64decode(part.get_payload()).decode())
                #     print(3)
                #     pass

        else:
            count+=1
            payload = base64.b64decode(msg.get_payload()).decode('utf-8')
            for part in msg.walk():
                # print(part.get_content_type())
            # print(f'isnt multi {letter_uid} ,subject {subject}',
            #       f' payload {payload}',
            #       sep= '\n'
            # )
                print(f'{count}')  

def send_message_to_chat():
    pass

def main(argv):
        try:
            while True:
                try:
                    imap = imaplib.IMAP4_SSL(CONFIG['imap_server'])
                    imap.login(CONFIG['email'], CONFIG['password'])
                    imap.select(f'INBOX/{CONFIG['mail_folder']}')
                    check_response = check_unseen_messages(imap)
                    if check_response[0] and check_response[1] != None:
                        print(datetime.datetime.now())
                        print('new_message/messages')
                        system('vlc.exe --play-and-exit  src/music/alarm.mp3')
                        #parse_mail(check_response[1], imap)
                    else:
                        print(datetime.datetime.now())
                        print('no new messages')
                        # for i in letters_uid[0].split():
                        #     res, msg = imap.uid('fetch',i, '(RFC822)')
                        #     msg = email.message_from_bytes(msg[0][1])
                        #     if msg.is_multipart():
                        #         print('multi')
                        #     else:
                        #         print('no multi')
                            # print(decode_header(msg['Subject'])[0][0].decode('utf-8'))
                            # payload = msg.get_payload()
                            # print(
                            #     payload
                            # )
                            # print(
                            #     payload.is_multipart()
                            # )
                            # for part in payload:
                            #     print(part.get_content_type)
                            # for i in payload:
                            # print(dir(msg))
                            # for part in payload:
                            #     print(part.get_content_type())
                    sleep(float(CONFIG['check_delay_m'])*60)
                except KeyboardInterrupt as e:
                    sys.exit(e.args)
        except KeyboardInterrupt as e:
            print(e.args)

main(sys.argv)
