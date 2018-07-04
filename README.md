# Why do people keep photographs?

Repository for the media-art project [whydopeoplekeepphotographs.net](http://whydopeoplekeepphotographs.net) 
by [Tessa Groenewoud](http://tessagroenewoud.nl).   
<br><br>

“Why do people keep photographs?”  
&nbsp;“Why? Goodness knows! Why do people keep things —  
junk — trash, bits and pieces. They do — that’s all there is to  
it!”  
&nbsp;“Up to a point I agree with you. Some people keep things.  
Some people throw everything away as soon as they have  
done with it. That, yes, it is a matter of temperament. But  
I speak now especially of photographs. Why do people keep,  
in particular, photographs?”  
<br><br>

Every day a video is automatically generated based on the above passage from Agatha Christie's crime novel ‘Mrs. McGinty’s Dead’ (1952).
 Each word from the fragment is used to randomly select the day’s highest ranking image result in the search engines of Bing, Google or Yahoo*.  
   
 The images are concatenated into a HD video through FFmpeg, with burned-in subtitles containing the matching words. 
 The time codes for each image/word are read from an external file. A title and a rolling credits screen, 
 with the source urls of the images, are also generated and merged into the video.  
 The project was launched in November 2016.  
 <br>
 See Tessa Groenewoud's [project description](https://tessagroenewoud.nl/works/Why-do-People-keep-Photographs) too.  


### Tech info

* Requires Python 3.4+
* Python dependencies: oauth2, dotenv
* Command-line dependencies: ffmpeg 3+, scp (OpenSSH)
* Configure through ``.env`` and ``/wdpkp/settings.py`` files
* Fonts in ``assets/fonts`` not included
* Renders a H264/mp4, 1920x1080 HD video


#### Docker build & run

```
docker build -t tessagroenewoud/wdpkp:latest .
docker run -d --name wdpkp \
  --restart=always \
  -v /host/dir/for/source/images:/root/wdpkp/data_tmp:rw \
  -v /host/dir/for/rendered/videos:/root/wdpkp/videos:rw \
  -v /host/.ssh:/root/.ssh:ro \
  tessagroenewoud/wdpkp
```


### license
GPL-3.0

<br><br>
<small>* Yahoo's API ceased to respond to queries on May 15, 2018 &mdash; yes, more than two years after the officially announced date.</small>