Service cho phép download file mp3 từ link youtube và lưu vào thư mục local trên homeassistant
Khai báo trong configuration.yaml như sau:

downloader:
  download_dir: /config/www/media #thư mục local trên homeassistant

youtube_downloader:

Khai báo gọi dịch vụ như sau:

service: youtube_downloader.download
  data:
    message: 'link youtube muốn download'
    save_dir: 'music'   #thư mục con muốn lưu trữ trên hass (là subdir của thư mục download_dir khai báo trong file configuration.yaml