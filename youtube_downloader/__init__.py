#encoding: utf-8
#Code by: Nguyễn Hồng Thắng
#Mail: thang1110@gmail.com
from __future__ import unicode_literals 
import youtube_dl
import re
DOMAIN = 'youtube_downloader'
CFG_URL = 'url'
CFG_SAVE_DIR = 'sub_dir'
CFG_ENTITY_ID = 'entity_id'
#Hàm loại bỏ dấu tiếng Việt
def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s
def setup(hass, config):
    def download_youtube(call):
        #Khai Báo Biến
        link = call.data.get(CFG_URL)
        subdir = call.data.get(CFG_SAVE_DIR)
        #Get link mp3 from youtube
        ydl_opts = {
                  'format': 'bestaudio/best',
              }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            link_mp3 = info['formats'][0]['url']
            file_name = no_accent_vietnamese(info.get('title', None)) + '.mp3'
        #Call service downloader
        Data_Hass = {'overwrite': 'false', 'url': link_mp3, 'subdir': subdir, 'filename': file_name}
        hass.services.call('downloader', 'download_file', Data_Hass)
    def play_youtube(call):
        #Khai Báo Biến
        link = call.data.get(CFG_URL)
        entityid = call.data.get(CFG_ENTITY_ID)
        #Get link mp3 from youtube
        ydl_opts = {
                  'format': 'bestaudio/best',
                  'postprocessors': [{
                      'key': 'FFmpegExtractAudio',
                      'preferredcodec': 'mp3',
                      'preferredquality': '192',
                  }],
              }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            link_mp3 = info['formats'][0]['url']
        #Call service media_player
        Data_Hass = {'entity_id': entityid, 'media_content_id': link_mp3, 'media_content_type': 'audio/mp3'}
        hass.services.call('media_player', 'play_media', Data_Hass)
    hass.services.register(DOMAIN, 'download_mp3', download_youtube)    
    hass.services.register(DOMAIN, 'play_mp3', play_youtube)
    return True
