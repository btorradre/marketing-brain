"""Reference-image face count guard.

If the reference image has more than one face we must STOP and ask which face to
lock before generating anything. Uses OpenCV's Haar cascade when cv2 is present;
if cv2 is unavailable we can't reliably count, so we proceed but warn.
"""
from util import log


def count_faces(image_path):
    """Return face count, or None if detection is unavailable."""
    try:
        import cv2
    except ImportError:
        return None
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(cascade_path)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    return len(faces)


def guard_single_face(image_path, *, face_index=None):
    """Raise SystemExit if multiple faces and the user hasn't chosen one."""
    n = count_faces(image_path)
    if n is None:
        log("face detection unavailable (install opencv-python to enable); proceeding.")
        return
    if n <= 1:
        return
    if face_index is None:
        raise SystemExit(
            f"[ugc-forge] Reference image has {n} faces. Re-run with "
            f"--face-index <0..{n-1}> to lock which face to keep before starting."
        )
    log(f"reference has {n} faces; locking face index {face_index} (per --face-index).")
