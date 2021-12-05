for f in `ls *.m4a`; do
    newf=${f%.m4a}.mp3
    ffmpeg -i $f -c:a libmp3lame -q:a 8 $newf
done