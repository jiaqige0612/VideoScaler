import os
import cv2
import time
from PIL import Image
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import multiprocessing

os.environ["TFHUB_DOWNLOAD_PROGRESS"] = "True"

SAVED_MODEL_PATH = "https://tfhub.dev/captain-pool/esrgan-tf2/1"

def capture_frames(video_path, frame_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Read the video
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frame_count = 0
    while True:
        # Read a frame from the video
        ret, frame = video.read()

        # If the frame was not successfully read, we have reached the end of the video
        if not ret:
            break

        # Save the frame as an image
        frame_filename = f"{frame_count}.jpg"  # Specify the frame filename
        frame_filepath = f"{frame_path}/{frame_filename}"  # Specify the frame file path
        cv2.imwrite(frame_filepath, frame)

        # Write the frame to the output video
        # output_video.write(frame)

        frame_count += 1

    video.release()
    cv2.destroyAllWindows()


def create_video_from_frames(frame_path, output_path, fps):
    # Get the list of frame filenames in the frame path
    frame_filenames = os.listdir(frame_path)
    # frame_filenames.sort(key = extract_frame_number)
    # Read the first frame to get its properties
    first_frame = cv2.imread(os.path.join(frame_path, frame_filenames[0]))
    height, width, _ = first_frame.shape
    # Create a VideoWriter object to save the frames as a video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Specify the codec (e.g., XVID, MJPG, mp4v)
    output_video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Loop through each frame file and write it to the output video
    for i in range(0,len(frame_filenames)):
        filename = str(i)+'.jpg'
        frame_filepath = os.path.join(frame_path,filename)
        # frame_filepath = os.path.join(frame_path, frame_filename)
        frame = cv2.imread(frame_filepath)
        output_video.write(frame)

    # Release the resources
    output_video.release()
    cv2.destroyAllWindows()

def preprocess_image(image_path):
  """ Loads image from path and preprocesses to make it model ready
      Args:
        image_path: Path to the image file
  """
  hr_image = tf.image.decode_image(tf.io.read_file(image_path))
  # If PNG, remove the alpha channel. The model only supports
  # images with 3 color channels.
  if hr_image.shape[-1] == 4:
    hr_image = hr_image[...,:-1]
  hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
  hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
  hr_image = tf.cast(hr_image, tf.float32)
  return tf.expand_dims(hr_image, 0)

def save_image(image, filename):
  """
    Saves unscaled Tensor Images.
    Args:
      image: 3D image tensor. [height, width, channels]
      filename: Name of the file to save.
  """
  if not isinstance(image, Image.Image):
    image = tf.clip_by_value(image, 0, 255)
    image = Image.fromarray(tf.cast(image, tf.uint8).numpy())
  image.save("%s" % filename)
  print("Saved as %s" % filename)

def preprocess_image(image_path):
  """ Loads image from path and preprocesses to make it model ready
      Args:
        image_path: Path to the image file
  """
  hr_image = tf.image.decode_image(tf.io.read_file(image_path))
  # If PNG, remove the alpha channel. The model only supports
  # images with 3 color channels.
  if hr_image.shape[-1] == 4:
    hr_image = hr_image[...,:-1]
  hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
  hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
  hr_image = tf.cast(hr_image, tf.float32)
  return tf.expand_dims(hr_image, 0)

def preprocess_image_cv2(hr_image):
  """ Loads image from path and preprocesses to make it model ready
      Args:
        image_path: Path to the image file
  """
  # If PNG, remove the alpha channel. The model only supports
  # images with 3 color channels.
  if hr_image.shape[-1] == 4:
    hr_image = hr_image[...,:-1]
  hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
  hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
  hr_image = tf.cast(hr_image, tf.float32)
  return tf.expand_dims(hr_image, 0)

def save_image(image, filename):
  """
    Saves unscaled Tensor Images.
    Args:
      image: 3D image tensor. [height, width, channels]
      filename: Name of the file to save.
  """
  if not isinstance(image, Image.Image):
    image = tf.clip_by_value(image, 0, 255)
    image = Image.fromarray(tf.cast(image, tf.uint8).numpy())
  image.save("%s.jpg" % filename)
  print("Saved as %s.jpg" % filename)

model = hub.load(SAVED_MODEL_PATH)

def output_frame(frame):
    #video_path = r'D:\GUI\leaf.mp4'
    #frame_path = r'C:\Users\jiaqi\PycharmProjects\pythonProject\frame_path'
    #sr_frame_path = r'C:\Users\jiaqi\PycharmProjects\pythonProject\sr_frame_path'
    output_path = r'C:\Users\jiaqi\PycharmProjects\pythonProject\output.mp4'


    start = time.time()
    tensor = tf.convert_to_tensor(frame, dtype=tf.float32)
    tensor = tf.expand_dims(tensor, 0)

    #tmp_image = preprocess_image_cv2(tensor)
    fake_image = model(tmp_image)
    fake_image = tf.squeeze(fake_image)
    sr_frame_name = f"{frame_index}"
    sr_save_path = os.path.join(sr_frame_path,sr_frame_name)
    save_image(fake_image, sr_save_path)

    print("Time Taken: %f" % (time.time() - start))

    return fake_image.numpy()


def output_video(video_path = r'D:\GUI\leaf.mp4', fps = 60, startframeindex = 0, endframeindex = 0):
    #video_path = r'D:\GUI\leaf.mp4'
    frame_path = r'C:\Users\jiaqi\PycharmProjects\pythonProject\frame_path'
    sr_frame_path = r'C:\Users\jiaqi\PycharmProjects\pythonProject\sr_frame_path'
    output_path = r'C:\Users\jiaqi\PycharmProjects\pythonProject\output.mp4'

    # os.makedirs(frame_path)
    # os.makedirs(sr_frame_path)


    start = time.time()
    capture_frames(video_path,frame_path)

    lr_frame = os.listdir(frame_path)


    for i in range(startframeindex, endframeindex):
        lr_framepath = str(i)+'.jpg'
        tmp_path = os.path.join(frame_path,lr_framepath)
        tmp_image = preprocess_image(tmp_path)
        fake_image = model(tmp_image)
        fake_image = tf.squeeze(fake_image)
        sr_frame_name = f"{i}"
        sr_save_path = os.path.join(sr_frame_path,sr_frame_name)
        save_image(fake_image,sr_save_path)


    create_video_from_frames(sr_frame_path, output_path, fps)

    print("Time Taken: %f" % (time.time() - start))



    frame_path = '/content/sr_frame_path'
    output_path = '/content/drive/MyDrive/SR_consulting_project/output1.mp4'

    frame_filenames = os.listdir(frame_path)
    first_frame = cv2.imread(os.path.join(frame_path, frame_filenames[0]))
    height, width, _ = first_frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec (e.g., XVID, MJPG, mp4v)
    output_video = cv2.VideoWriter(output_path, fourcc, 30.0, (width, height))

    # Loop through each frame file and write it to the output video
    for i in range(0,315):
        filename = str(i)+'.jpg'
        frame_filepath = os.path.join(frame_path, filename)
        # frame = cv2.imread(frame_filepath)
        output_video.write(cv2.imread(frame_filepath))
        print('Frame written:', str(i),'.jpg')

    # Release the resources
    cv2.destroyAllWindows()
    output_video.release()


