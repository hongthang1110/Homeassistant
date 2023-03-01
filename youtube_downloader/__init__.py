#encoding: utf-8
#Code by: Nguyễn Hồng Thắng
#Mail: thang1110@gmail.com
from __future__ import unicode_literals 
import youtube_dl
import re
DOMAIN = 'youtube_downloader'
CFG_URL = 'message'
CFG_SAVE_DIR = 'save_dir'
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
        message = call.data.get(CFG_URL)
        save_dir = call.data.get(CFG_SAVE_DIR)
        #Lọc Lấy ID của link
        match = re.search(r'(?<=v=)[\w-]+', message)
        if match:
            video_id = "https://www.youtube.com/watch?v="+match.group(0)
        else:
            video_id = message
        #Download file mp3
        ydl_opts = {
                  'format': 'bestaudio/best',
                  'postprocessors': [{
                      'key': 'FFmpegExtractAudio',
                      'preferredcodec': 'mp3',
                      'preferredquality': '192',
                  }],
              }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_id, download=False)
            show_link = info['formats'][0]['url']
            file_name = no_accent_vietnamese(info.get('title', None)) + '.mp3'
        #Hass Send Data
        Data_Hass = {'overwrite': 'false', 'url': show_link, 'subdir': save_dir, 'filename': file_name}
        hass.services.call('downloader', 'download_file', Data_Hass)
    hass.services.register(DOMAIN, 'download', download_youtube)
    return True
