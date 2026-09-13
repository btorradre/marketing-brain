"""Localized thin-strand cleanup on video frames; diagnostic output before production."""
import argparse, json
from pathlib import Path
import cv2
import numpy as np

def clean(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    smooth = cv2.GaussianBlur(gray, (0, 0), 3.5)
    structure = cv2.Canny(smooth, 16, 40)
    protect = cv2.dilate(structure, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))) > 0
    f = gray.astype(np.float32)
    mean = cv2.GaussianBlur(f, (0, 0), 6)
    variance = np.maximum(cv2.GaussianBlur(f*f, (0, 0), 6) - mean*mean, 1)
    detail = cv2.subtract(gray, cv2.medianBlur(gray, 7)).astype(np.float32)
    candidates = ((detail > 18) & ((f-mean) / np.sqrt(variance) > 2) & ~protect).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(candidates, 8)
    mask = np.zeros(gray.shape, np.uint8)
    for label in range(1, count):
        x, y, w, h, area = stats[label]
        if area < 7 or area > 1500 or max(w, h) < 8:
            continue
        yy, xx = np.where(labels[y:y+h, x:x+w] == label)
        covariance = np.cov(np.vstack([xx, yy]))
        eigen = np.linalg.eigvalsh(covariance)
        if eigen[-1] / max(eigen[0], .1) < 3.5:
            continue
        mask[y:y+h, x:x+w][labels[y:y+h, x:x+w] == label] = 255
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    mask[protect] = 0
    result = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)
    return result, mask

def main():
    p = argparse.ArgumentParser()
    p.add_argument('video'); p.add_argument('output'); p.add_argument('--at', type=float, default=8.9)
    args = p.parse_args()
    video = cv2.VideoCapture(args.video)
    video.set(cv2.CAP_PROP_POS_MSEC, args.at * 1000)
    ok, frame = video.read(); video.release()
    if not ok: raise RuntimeError('Frame could not be decoded')
    result, mask = clean(frame)
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out / 'before.png'), frame)
    cv2.imwrite(str(out / 'after.png'), result)
    cv2.imwrite(str(out / 'mask.png'), mask)
    overlay = frame.copy(); overlay[mask > 0] = (0, 0, 255)
    cv2.imwrite(str(out / 'mask-overlay.png'), overlay)
    crop = [650, 260, 1360, 790]
    x1,y1,x2,y2 = crop
    pair = np.hstack([frame[y1:y2,x1:x2], result[y1:y2,x1:x2]])
    cv2.imwrite(str(out / 'comparison.png'), pair)
    print(json.dumps({'at': args.at, 'altered_pixel_fraction': float((mask > 0).mean()), 'comparison': str(out/'comparison.png')}))

if __name__ == '__main__': main()
