# install & run api server.
```bash
virtualenv myenv
source myenv/bin/activate
pip install -r requirements.txt
python app.py
```

# Run flask CLI
```bash
FLASK_APP=cli.py flask <command-name>
```

# format to mp3
```bash
ffmpeg -y -i end_music.wav -filter_complex "[0:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[a0]" -map [a0] -ar 44100 -ac 2 -b:a 128k -acodec libmp3lame -f mp3 end_music.mp3
```

# mix from intro_music.wav to clip.wav (trim first then add (atrim -> adelay))
```bash
ffmpeg -y -i clip.wav -i intro_music.wav -filter_complex "[0:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[a0];[1:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[a1];[a1]atrim=5.0:20.0[a1trim];[a1trim]adelay=5000|5000[aud1];[aud1]amix=1,apad[a];[a0][a]amerge[a]" -map "[a]" -ar 44100 -ac 2 -b:a 128k -acodec libmp3lame -f mp3 mix01.mp3
```

- format to 2 channel
- get from 5s - 20s of intro_music.wav
- add this to clip.wav at 5s
- format to mp3 output

# crossfade audio 1,2 then mix 3 to [1,2]
```bash
ffmpeg -y -i intro_music.wav -i clip.wav -i end_music.wav -i effect_1.mp3 -i effect_2.mp3 -filter_complex "[1]acrossfade=d=10:c1=tri:c2=tri[aud1];[aud1][2]acrossfade=d=10:c1=tri:c2=tri[aud2];[3]adelay=5000|5000[aud3];[aud3]amix=1,apad[mixed];[aud2][mixed]amerge[mixed]" -map "[mixed]" -ar 44100 -ac 2 -b:a 128k -acodec libmp3lame -f mp3 mix01.mp3
```

# crossfade audio 1,2 then mix 3 at 5sec, 4 at 10sec
```bash
ffmpeg -y 
-i intro_music.wav -i clip.wav -i end_music.wav -i effect_1.mp3 -i effect_2.mp3 
-filter_complex 
"[1]acrossfade=d=10:c1=tri:c2=tri[aud1];[aud1][2]acrossfade=d=10:c1=tri:c2=tri[aud2];[3]adelay=5000|5000[aud3];[4]adelay=10000|10000[aud4];[aud3][aud4]amix=2,apad[final];[aud2][final]amerge[final]" 
-map "[final]" 
-ar 44100 -ac 2 -b:a 128k -acodec libmp3lame -f mp3 mix01.mp3
```
```bash
[
  {
    "color" : "rgba(88, 196, 145, 0.44)",
    "end" : 33.529600000000002,
    "fdId" : 14,
    "label" : "intro_music.wav",
    "start" : 0,
    "type" : "crossfade"
  },
  {
    "color" : "rgba(167, 243, 110, 0.44)",
    "end" : 213.06326530612245,
    "fdId" : 16,
    "label" : "clip.wav",
    "start" : 33.529600000000002,
    "type" : "crossfade"
  },
  {
    "color" : "rgba(31, 108, 205, 0.44)",
    "end" : 226.89532879818591,
    "fdId" : 15,
    "label" : "end_music.wav",
    "start" : 213.06299999999999,
    "type" : "crossfade"
  },
  {
    "color" : "rgba(220, 169, 127, 0.44)",
    "end" : 90,
    "fdId" : 13,
    "label" : "effect_1.mp3",
    "start" : 89.859454999999997,
    "type" : "mix"
  },
  {
    "color" : "rgba(175, 144, 255, 0.44)",
    "end" : 32,
    "fdId" : 12,
    "label" : "effect_2.mp3",
    "start" : 15.458893,
    "type" : "mix"
  },
  {
    "color" : "rgba(203, 81, 127, 0.44)",
    "end" : 258.42496598639457,
    "fdId" : 14,
    "label" : "intro_music.wav",
    "start" : 226.89500000000001,
    "type" : "crossfade"
  }
]
```


# Documentation
https://docs.graphene-python.org/en/latest/, https://github.com/graphql-python/flask-graphql
https://vuejs.org/v2/guide/typescript.html

### key must declare = with key list item to breadcrum root link

Suite (Audio tool):
* merge track
* mix track
* trim silence
* reduce background noise
* generate transcript (for better SEO & socical)
* 1-1 interview

Podcast:
* create podcast from scratch
* import from existing podcast platform like Apple podcast, Soundcloud, AudioBoom, Spreaker, ...
* RSS feed for podcast
* Schedule Episode
* Podcast distribution to Apple podcast, Spotify, Google Music, TuneIn, Amazon Alexa, ...
* Audio search based on transcript, caption based on WebVTT format
* External player inject to any webpage, blog platform, ....
* Podcast producer page/blog
* Podcast analytisc with basic metric like Unique user listen, location, browser/device, referal site, ...

## Fix GCE utf8 encode
```
echo "LC_ALL=en_US.UTF-8" >> /etc/environment
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
```

## Frontend setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
