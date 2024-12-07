import cv2
import os
import time
import imageio
import numpy as np
import sys

__all__ = [
            "VideoCap",
            "FPS",
            "Timer",
            "Mp4toGif",
           ]

class VideoCap():
    """
    Customized Python video reading class
    """
    def __init__(self, mode=0, w=640, h=480, l=150):
        self.cap = cv2.VideoCapture(mode)
        self.cap.set(3, w)
        self.cap.set(4, h)
        self.cap.set(10, l)
        self.start_number = 0

    def read(self, flip=None):
        """
        :param flip: -1: Horizontal and vertical directions,
                      0: along the y-axis, vertical,
                      1: along the x-axis, horizontal
        """
        _, img = self.cap.read()
        if flip is not None:
            assert flip in [-1, 0, 1], f"VideoCap: The 'flip' parameter must be -1, 0, or 1."
            img = cv2.flip(img, flip)
        return img

    def free(self):
        """
        Release camera
        """
        self.cap.release()
        cv2.destroyAllWindows()

    def show(self,
             winname: str,
             src,
             base_name: str = './result.png',
             end_k=27,
             save_k=ord('s'),
             delay_t=1,
             extend_num=3
             ):
        """
        Window display. Press 's' to save, 'Esc' to end
        """
        image_path, ext = os.path.splitext(base_name)
        os.makedirs(os.path.dirname(base_name), exist_ok=True)
        if src is not None:
            cv2.imshow(winname, src)
            k = cv2.waitKey(delay_t) & 0xFF
            if k == end_k:
                self.free()
                sys.exit(0)
            elif k == save_k:
                self.start_number += 1
                file_number = str(self.start_number).zfill(extend_num)
                file_path = f"{image_path}_{file_number}{ext}"
                print(f"{self.start_number}  Image saved to {file_path}")
                cv2.imwrite(file_path, src)

class FPS:
    def __init__(self):
        self.pTime = time.time()

    def update(self, img=None, pos=(20, 50), color=(255, 0, 0), scale=3, thickness=3):
        """
        更新帧速率
        :param img: The displayed image can be left blank if only the fps value is needed
        :param pos: Position on FPS on image
        :param color: The color of the displayed FPS value
        :param scale: The proportion of displayed FPS values
        :param thickness: The thickness of the displayed FPS value
        :return:
        """
        cTime = time.time()
        try:
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            if img is None:
                return fps
            else:
                cv2.putText(img, f'FPS: {int(fps)}', pos, cv2.FONT_HERSHEY_PLAIN,
                            scale, color, thickness)
                return fps, img
        except:
            return 0

class Timer:
    def __init__(self):
        """Start is called upon creation"""
        self.times = []
        self.start()
    def start(self):
        """initial time"""
        self.gap = time.time()
    def stop(self):
        """The time interval from the start of timing to calling the stop method"""
        self.times.append(time.time() - self.gap)
        return self.times[-1]
    def avg(self):
        """Average time consumption"""
        return sum(self.times) / len(self.times)
    def total(self):
        """Total time consumption"""
        return sum(self.times)
    def cumsum(self):
        """Accumulated sum of time from the previous n runs"""
        return np.array(self.times).cumsum().tolist()


def Mp4toGif(mp4, name='result.gif', fps=10, start=None, end=None):
    cap = cv2.VideoCapture(mp4)
    all_images = []
    frame_count = 0

    while True:
        ret, img = cap.read()
        if ret is False:
            break
        if start is not None and frame_count < start:
            frame_count += 1
            continue
        if end is not None and frame_count >= end:
            break
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        all_images.append(img)
        frame_count += 1

    duration = int(1000 / fps)  # 将帧率转换为每帧之间的延迟时间（毫秒）
    imageio.mimsave(name, all_images, duration=duration)
    print("转换完成！")

if __name__ == "__main__":
    fpsReader = FPS()
    Vcap = VideoCap(mode=0)
    while True:
        img = Vcap.read()
        fps, img = fpsReader.update(img)
        Vcap.show("ss", img)