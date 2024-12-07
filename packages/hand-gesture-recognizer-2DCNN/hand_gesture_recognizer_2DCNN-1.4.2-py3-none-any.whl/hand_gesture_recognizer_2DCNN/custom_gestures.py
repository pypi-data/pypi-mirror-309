import cv2

def handle_fist(image):
    cv2.putText(
        image,
        "Fist",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        5,
        cv2.LINE_AA,
    )


def handle_open_palm(image):
    cv2.putText(
        image,
        "Open Palm",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        5,
        cv2.LINE_AA,
    )


def handle_two_fingers(image):
    cv2.putText(
        image,
        "Two Fingers",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        5,
        cv2.LINE_AA,
    )


def handle_three_fingers(image):
    cv2.putText(
        image,
        "Three Fingers",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        5,
        cv2.LINE_AA,
    )


def handle_four_fingers(image):
    cv2.putText(
        image,
        "Four Fingers",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 0),
        5,
        cv2.LINE_AA,
    )

