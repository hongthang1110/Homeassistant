#!/bin/bash
echo 'Script fix loi cho file youtube.py - thang1110@gmail.com'
echo 'https://github.com/hongthang1110/homeassistant/tree/main/youtube_downloader'
echo '------------------'
youtube_py=$(find /var/lib/docker/ -name youtube.py|grep extractor/youtube.py|grep merged)
if [ "$youtube_py" != "" ]
then
        echo 'Tim thay file youtube.py:'
	echo $youtube_py
	find_code=$(grep "if owner_profile_url else None" $youtube_py)
	if [ "$find_code" != "" ]
	then
		echo '------------------'
		echo 'Tim thay code loi:'
		echo $find_code
		echo '------------------'
		echo 'Thay the bang code dung:'
		echo "'uploader_id': self._search_regex(r'/(?:channel|user)/([^/?&#]+)', owner_profile_url, 'uploader id') if owner_profile_url else None,"
	        sed -i 's/\x27uploader_id\x27: self\._search_regex(r\x27\/(?:channel|user)\/(\[\^\/?\&#\]+)\x27, owner_profile_url, \x27uploader id\x27) if owner_profile_url else None,/\x27uploader_id\x27: self\._search_regex(r\x27\/(?:channel\/|user\/|(?=@))(\[\^\/?\&#\]+)\x27, owner_profile_url, \x27uploader id\x27, default=None),/g' $youtube_py
		echo 'Sua loi thanh cong.'
		echo 'Restart lai device sau 3 giay'
		echo 'Thanks!'
		sleep 3
		reboot
	else
		echo '------------------'
		echo 'Khong tim thay code loi.'
	fi
else
	echo 'Khong tim thay file youtube.py'
fi
