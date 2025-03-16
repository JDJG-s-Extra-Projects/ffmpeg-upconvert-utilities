## Useful information guide

# convert 30fps (python script)

- useful for converting the videos into a nivida format that kdenlive will accept (for whatever reason it doesn't accept nintendo switch captures which is grabbed from the micro sd card after I turn off the switch).

# upconvert (batch script)

- Basically it makes a version of the video higher quality with 1080p (if qp is lower it will have higher quality however it will be bigger in file size)


However,
``ffmpeg -i "test.mp4" -c:v hevc_nvenc -qp 17 -vf scale=1920x1080:flags=lanczos "output-1.mp4"``

will have a file size of 72.8 Mib on windows from my super mario 3d all stars test clip

However with the same input video but with qp 1:
``ffmpeg -i "test.mp4" -c:v hevc_nvenc -qp 1 -vf scale=1920x1080:flags=lanczos "output-2.mp4"``

this is instead 368 Mib, a huge increase

output-2 is about 5 times bigger than output-1

- No real results appear to be the case for -qp 1 and -qp 17

- The next step is doing a comparasion video between the two with the left being the original and the right being the higher quality clip.

# upconvert (python script)

- this about the same as the batch script except it takes all the videos in a directory and applies the effects of upconvert.bat onto of all them however this does not use the batch script as it instead runs the command itself.

- Essentially meaning it will run the upconvert and then the test.

