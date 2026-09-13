"""Track a GPT Image 2 surface retouch through an existing video shot.

Uses original-to-original motion correspondence, never an invented camera move.
The original source and generated retouch remain immutable. Output is a derived
video plate to place on the original frame-exact HyperFrames timeline.
"""
import argparse
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np

cv2.setNumThreads(4)

def read_frame(cap, index):
    cap.set(cv2.CAP_PROP_POS_FRAMES, index)
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError(f"Cannot read original frame {index}")
    return frame

def flow_to(a, b, scale=.5, blur=0):
    h, w = a.shape[:2]
    size = (round(w * scale), round(h * scale))
    def prep(im):
        g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        if blur:
            g = cv2.GaussianBlur(g, (0, 0), blur)
        return cv2.resize(g, size, interpolation=cv2.INTER_AREA)
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    dis.setFinestScale(0)
    dis.setGradientDescentIterations(25)
    f = dis.calc(prep(a), prep(b), None)
    return cv2.resize(f, (w, h), interpolation=cv2.INTER_LINEAR) / scale

def remap(im, flow, border=cv2.BORDER_REFLECT_101):
    h, w = im.shape[:2]
    xx, yy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    return cv2.remap(im, xx + flow[:, :, 0], yy + flow[:, :, 1], cv2.INTER_LINEAR, borderMode=border)

def planar_flow(a,b,return_matrix=False):
    """A single tracked affine map keeps a close-up's regular weave undistorted."""
    h,w=a.shape[:2];size=(w//2,h//2)
    ga=cv2.resize(cv2.cvtColor(a,cv2.COLOR_BGR2GRAY),size)
    gb=cv2.resize(cv2.cvtColor(b,cv2.COLOR_BGR2GRAY),size)
    sift=cv2.SIFT_create(nfeatures=3000,contrastThreshold=.015)
    ka,da=sift.detectAndCompute(ga,None);kb,db=sift.detectAndCompute(gb,None)
    good=[]
    if da is not None and db is not None:
        pairs=cv2.BFMatcher().knnMatch(da,db,k=2)
        good=[m for m,n in pairs if m.distance<.72*n.distance]
    matrix=None
    if len(good)>=12:
        pa=np.float32([ka[m.queryIdx].pt for m in good])*2
        pb=np.float32([kb[m.trainIdx].pt for m in good])*2
        matrix,inliers=cv2.estimateAffine2D(pa,pb,method=cv2.RANSAC,ransacReprojThreshold=4,maxIters=4000)
        if matrix is None or inliers.sum()<10:matrix=None
    if matrix is None:
        rough=flow_to(a,b,scale=.25,blur=2)
        dx,dy=np.median(rough.reshape(-1,2),axis=0)
        matrix=np.array([[1,0,dx],[0,1,dy]],np.float32)
    if return_matrix:return matrix
    return matrix_flow(matrix,w,h)

def matrix_flow(matrix,w,h):
    xx,yy=np.meshgrid(np.arange(w,dtype=np.float32),np.arange(h,dtype=np.float32))
    return np.stack([(matrix[0,0]-1)*xx+matrix[0,1]*yy+matrix[0,2],
        matrix[1,0]*xx+(matrix[1,1]-1)*yy+matrix[1,2]],axis=-1).astype(np.float32)

def align_clean(anchor, clean):
    h, w = anchor.shape[:2]
    clean = cv2.resize(clean, (w, h), interpolation=cv2.INTER_LANCZOS4)
    # A rigid registration cannot ripple newly repaired fabric weave.
    def gray_small(im):
        return cv2.resize(cv2.GaussianBlur(cv2.cvtColor(im,cv2.COLOR_BGR2GRAY),(0,0),3),(w//2,h//2))
    transform=np.eye(2,3,dtype=np.float32)
    try:
        _, transform=cv2.findTransformECC(gray_small(anchor),gray_small(clean),transform,
            cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,150,1e-5))
        transform[:,2]*=2
        if np.max(np.abs(transform[:,:2]-np.eye(2)))>.025 or np.max(np.abs(transform[:,2]))>15:
            transform=np.eye(2,3,dtype=np.float32)
    except cv2.error:
        transform=np.eye(2,3,dtype=np.float32)
    aligned=cv2.warpAffine(clean,transform,(w,h),flags=cv2.INTER_LANCZOS4|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REFLECT_101)
    # Keep the original shot's color and broad lighting while adopting repaired texture.
    difference = anchor.astype(np.float32) - aligned.astype(np.float32)
    aligned = np.clip(aligned.astype(np.float32) + cv2.GaussianBlur(difference, (0, 0), 18), 0, 255)
    return aligned.astype(np.uint8)

def process(video, clean_path, start, end, anchor_index, output, extra_references=None, surface_only=False, plate_only=False, smooth_planar=False, polish_surface=False):
    surface_only = surface_only or plate_only
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS)
    anchor = read_frame(cap, anchor_index)
    clean = cv2.imread(str(clean_path))
    if clean is None:
        raise RuntimeError(f"Missing generated reference {clean_path}")
    plate = align_clean(anchor, clean)
    references=[(anchor_index,anchor,plate)]
    for ref_index,ref_path in (extra_references or []):
        old=read_frame(cap,ref_index)
        references.append((ref_index,old,align_clean(old,cv2.imread(str(ref_path)))))
    cv2.imwrite(str(output / 'anchor-original.png'), anchor)
    cv2.imwrite(str(output / 'anchor-aligned.png'), plate)
    h,w = anchor.shape[:2]
    encoder = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24',
        '-s',f'{w}x{h}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','slow',
        '-crf','14','-pix_fmt','yuv420p','-movflags','+faststart',str(output / 'shot.mp4')], stdin=subprocess.PIPE)
    samples=[]
    smooth_maps={}
    if smooth_planar:
        # Fit the measured camera path robustly; individual SIFT failures must
        # not produce a one-frame jump of an otherwise stationary handle.
        time=np.linspace(-1,1,end-start)
        design=np.stack([np.ones_like(time),time,time*time],axis=1)
        for ref_index,old,_ in references:
            matrices=[]
            cap.set(cv2.CAP_PROP_POS_FRAMES,start)
            for index in range(start,end):
                ok,frame=cap.read();assert ok
                matrices.append(planar_flow(frame,old,return_matrix=True))
            values=np.asarray(matrices).reshape(-1,6)
            weights=np.ones(end-start)
            for _ in range(6):
                coef=np.linalg.lstsq(design*weights[:,None],values*weights[:,None],rcond=None)[0]
                fitted=design@coef
                error=np.linalg.norm((values-fitted)*np.array([w,h,1,w,h,1]),axis=1)
                scale=max(2,float(np.median(error))*1.4826)
                weights=np.minimum(1,2.5*scale/np.maximum(error,1e-6))**2
            smooth_maps[ref_index]=fitted.reshape(-1,2,3)
    cap.set(cv2.CAP_PROP_POS_FRAMES,start)
    for index in range(start,end):
        ok, frame = cap.read()
        if not ok: raise RuntimeError(f"Cannot decode frame {index}")
        # Keep original seams, hardware, silhouette, and newly revealed areas.
        gray=cv2.GaussianBlur(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),(0,0),5)
        edges=cv2.Canny(gray,18,42)
        protected=cv2.dilate(edges,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13)))
        structural=1-cv2.GaussianBlur(protected.astype(np.float32)/255,(0,0),3)
        if surface_only:structural[:]=1
        candidates=[]
        for ref_index,old,ref_plate in references:
            flow=matrix_flow(smooth_maps[ref_index][index-start],w,h) if smooth_planar else (planar_flow(frame,old) if surface_only else flow_to(frame,old,scale=.5,blur=1))
            if not surface_only:flow=cv2.GaussianBlur(flow,(0,0),5)
            tracked=remap(ref_plate,flow);old_tracked=remap(old,flow)
            illumination=cv2.GaussianBlur(frame.astype(np.float32)-old_tracked.astype(np.float32),(0,0),12)
            repaired=np.clip(tracked.astype(np.float32)+(0 if plate_only else illumination),0,255)
            residual=cv2.GaussianBlur(np.mean(np.abs(frame.astype(np.float32)-old_tracked.astype(np.float32)),axis=2),(0,0),5)
            confidence=np.clip((25-residual)/12,0,1)
            yy,xx=np.indices((h,w),dtype=np.float32)
            distance=np.minimum.reduce([xx+flow[:,:,0],yy+flow[:,:,1],w-1-xx-flow[:,:,0],h-1-yy-flow[:,:,1]])
            valid=np.clip(distance/12,0,1)
            if surface_only:
                confidence[:]=1
                if not plate_only:valid[:]=1
            candidates.append((repaired,confidence*valid,1/(1+(abs(index-ref_index)/12)**2)))
        denominator=sum(c*t for _,c,t in candidates)+1e-8
        repaired=sum(r*(c*t)[:,:,None] for r,c,t in candidates)/denominator[:,:,None]
        coverage=np.maximum.reduce([c for _,c,_ in candidates])
        alpha=(structural*coverage)[:,:,None]
        if not surface_only:
            saturation=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)[:,:,1].astype(np.float32)
            material=cv2.GaussianBlur(np.clip((saturation-15)/15,0,1),(0,0),3)
            alpha*=material[:,:,None]
        result=np.clip(frame*(1-alpha)+repaired*alpha,0,255).astype(np.uint8)
        if polish_surface:
            # Suppress residual low-contrast etched microtexture in the moving
            # repair. High-contrast seams and hardware boundaries remain sharp.
            result=cv2.fastNlMeansDenoisingColored(result,None,22,18,7,35)
        if index in {start,(start+end)//2,end-1,anchor_index}:
            cv2.imwrite(str(output/f'frame-{index:04d}.png'),result)
            cv2.imwrite(str(output/f'before-{index:04d}.png'),frame)
            samples.append(index)
        encoder.stdin.write(result.tobytes())
    cap.release(); encoder.stdin.close()
    if encoder.wait(): raise RuntimeError('Video encoding failed')
    receipt={'source':str(video),'generated_reference':str(clean_path),'start_frame':start,
        'end_frame_exclusive':end,'anchor_frame':anchor_index,'frames':end-start,'fps':fps,
        'samples':samples,'surface_polish':polish_surface,'status':'awaiting_visual_review'}
    (output/'tracking.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('video');p.add_argument('clean');p.add_argument('output')
    p.add_argument('--start',type=int,required=True);p.add_argument('--end',type=int,required=True)
    p.add_argument('--anchor',type=int,required=True)
    p.add_argument('--extra',action='append',default=[],help='FRAME=PATH')
    p.add_argument('--surface-only',action='store_true')
    p.add_argument('--plate-only',action='store_true',help='Use tracked clean plate without copying source transition ghosts or texture edges')
    p.add_argument('--smooth-planar',action='store_true')
    p.add_argument('--polish-surface',action='store_true')
    a=p.parse_args();process(a.video,a.clean,a.start,a.end,a.anchor,a.output,[(int(x.split('=',1)[0]),x.split('=',1)[1]) for x in a.extra],a.surface_only,a.plate_only,a.smooth_planar,a.polish_surface)
