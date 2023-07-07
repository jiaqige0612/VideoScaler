# Pixel Perfect Video Upscaler
This repository is created for intel video scaler project.

Our design project aims to explore and compare different video upscaling algorithms, with the objective of identifying one that produces satisfactory output quality with acceptable speed, and potentially suitable for implementation on Field-Programmable Gate Arrays (FPGAs) for real-time upscaling. As the designed product of this project, the "Pixel Perfect" video upscaler application software is developed to showcase and apply our research outcomes.

## Application Preview
<img width="1280" alt="GUI2" src="https://github.com/jiaqige0612/VideoScaler/assets/43089087/7417db21-74b1-45f9-9246-4aec7ab45c76">

## Flow Chart
![app](https://github.com/jiaqige0612/VideoScaler/assets/43089087/b2397904-ea57-465b-bf2a-2591eb7e6f4b)

## Functions and Features
The edge adaptive video up-scaler is an application software that upscales videos with 5 encapsulated super-resolution algorithm, with varied cost and performance. The 5 algorithms are bicubic interpolation, local structure, DTCWT, Improved NEDI and ESRGAN. The software can support up-scaling of 2x, 4x, 6x and 8x. The supported input and output video formats include MP4, AVI and MOV; supported output image formats include PNG, JPG and BMP.

In the user interface, the software first takes the chosen video in the direct folder user picked and read in. There is an section, in which the user can choose desired start and end video frame index, the scaling ratio and pick one of the five super-resolution methods which will be performed on the video, as well as the output formats. All the parameters have default values that prevent the application from crashing if the user does not input anything. After the user press "Produce Super-resolved Video" or "Produce Super-resolved Frame", a reminder window would pop up to notify the user that the video is being processed. The frame data is passed from the front-end to the back-end algorithm modules; the upscaled frame data is passed back to the front-end, for outputting directly or converting to a video with other frames. After the upscaling process is completed, a reminder window would pop up, indicating the directory in which super-resolved video or image has been saved and showing a preview of the result. The process flowchart for the video upscaler application software is shown above.

## System Requirements
Using the edge adaptive video upscaler application software requires a local installation of Python and MATLAB. The application is designed for running on Windows. 

## Intended Users
Our project focuses on video and image upscaling and we have implemented various methods into a user interface. Intel is the client that starts the whole project and is considered as the main target. Despite our supported company, the video upscaler software application is also designed for individuals or professionals involved in media production, content creation, or digital imaging tasks. For example, video, image editors or graphic designers may find our product available as they often encounter the need to upscale content for various purposes, such as adapting lower-resolution footage to higher-resolution formats, enhancing image quality or improving the resolution and quality of graphics, illustrations, and other visual elements. Photographer or even general user who have interest and wish to improve the quality of their personal photos and videos can also get what they need with the help of our product. The range of varied cost and performance of the encapsulated upscaling algorithms, with the flexibility provided by the several adjustable settings, should satisfy the needs of both professional and individual users.
 
We do our best to create a good user experience as our first priority, ensuring ease of use, accessibility, and user-friendly design in the GUI to accommodate both professional users and those with limited technical expertise.

## Evaluation Metrics and Performance Considerations
There are several common performance measurement scales that are used to evaluate the quality and effectiveness of up-scaling algorithms and of the application software. In this project, PSNR(Peak Signal-to-Noise Ratio) and SSIM(Structural Similarity Index) metrics are used. 

PSNR measures the ratio between the maximum possible power of a signal (the original image) and the power of the noise (the difference between the original and up-scaled images). While SSIM compares the structural information of the original and up-scaled images. It takes brightness, contrast, and structural similarity into account and ranges from -1 to 1, with 1 indicating identical images. The higher these two scales are usually indicates the better of image similarities and performance the method is. However, it is possible to have algorithms which achieve high scores on objective metrics but still produce visually unsatisfactory results.

Other scales such as execution time, as well as estimated number of ALM (Adaptive Logic Module) needed for implementing the algorithms on FPGA are also taken into consideration.

## Documentation
[Literature Review](https://github.com/jiaqige0612/VideoScaler/blob/fe14c9c78f00beb09cf45b8afa01cfd411ac443b/Literature%20Review/Literature_Review.pdf)

[Design Process Outline](https://github.com/jiaqige0612/VideoScaler/blob/fe14c9c78f00beb09cf45b8afa01cfd411ac443b/Documentation/Gantt%20Graph.png)

[Meeting and Decision Record](Documentation)

[Implemented Algorithms](Algorithms)

[Graphical User Interface](GUI/mainfinal.py)

[Complete Application Software](https://github.com/jiaqige0612/VideoScaler/tree/fe14c9c78f00beb09cf45b8afa01cfd411ac443b/Final%20Application%20Software)

[Test Results](https://github.com/jiaqige0612/VideoScaler/tree/fe14c9c78f00beb09cf45b8afa01cfd411ac443b/Test%20Results)

[Complete Design History File](https://github.com/jiaqige0612/VideoScaler/blob/fe14c9c78f00beb09cf45b8afa01cfd411ac443b/Documentation/Documentation.pdf)
