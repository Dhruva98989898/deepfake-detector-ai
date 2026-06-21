import cv2
import os


def extract_frames(video_path):

    frame_folder = "frames"

    os.makedirs(
        frame_folder,
        exist_ok=True
    )

    saved_frames = []

    cap = cv2.VideoCapture(
        video_path
    )

    frame_count = 0

    while True:

        success, frame = cap.read()

        if not success:

            break

        if frame_count % 30 == 0:

            filename = os.path.join(

                frame_folder,

                f"frame_{frame_count}.jpg"

            )

            cv2.imwrite(

                filename,

                frame

            )

            saved_frames.append(

                filename

            )

        frame_count += 1

    cap.release()

    return saved_frames