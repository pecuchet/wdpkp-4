# Why do people keep photographs?

Repository for the media art project [whydopeoplekeepphotographs.net](http://whydopeoplekeepphotographs.net) (v4) 
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

Every day a video is automatically generated based on the above passage from the crime novel ‘Mrs. McGinty’s Dead’ (1952) by Agatha Christie.
 Each word from the fragment is used to select the day’s highest ranking image result in the search engines of Bing, Google or Yahoo.  
   
 The images are concatenated into a HD video through FFmpeg, with burned-in subtitles containing the matching words. 
 The time codes for each image/word are read in from an external file. A title and a rolling credits screen, 
 with the source urls of the images, are also generated and merged into the video (H264/mp4; 1920x1080).


### info

* Python3.4+
* Dependencies: oauth2, ffmpeg
* Project website: [whydopeoplekeepphotographs.net](http://whydopeoplekeepphotographs.net)

### (debug) settings

* /wdpkp/settings.py

### license
GPL-3.0
