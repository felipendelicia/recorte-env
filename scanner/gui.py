import cv2
from tkinter import Tk, filedialog
import numpy as np


def seleccionar_carpeta():
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Seleccionar carpeta de imágenes")
    return folder

def abrir_ventana_maximized(nombre, imagen, screen_size):
    cv2.namedWindow(nombre, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(nombre, screen_size[0], screen_size[1])
    cv2.imshow(nombre, imagen)

def rotar_libre(img, angle):
    h, w = img.shape[:2]
    centro = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(centro, angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

def warp_cuadrilatero(img, pts):
    pts = np.array(pts, dtype="float32")
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)
    rect = np.array([
        pts[np.argmin(s)],
        pts[np.argmin(diff)],
        pts[np.argmax(s)],
        pts[np.argmax(diff)]
    ], dtype="float32")

    (tl, tr, br, bl) = rect
    width = int(max(np.linalg.norm(br - bl), np.linalg.norm(tr - tl)))
    height = int(max(np.linalg.norm(tr - br), np.linalg.norm(tl - bl)))
    dst = np.array([
        [0, 0],
        [width-1, 0],
        [width-1, height-1],
        [0, height-1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(img, M, (width, height))

def seleccionar_4_puntos(img, screen_size):
    puntos = []

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(puntos) < 4:
            puntos.append((x, y))

    ventana = "Seleccionar 4 puntos"
    cv2.namedWindow(ventana, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(ventana, *screen_size)
    cv2.setMouseCallback(ventana, click_event)

    while True:
        tmp = img.copy()
        for p in puntos:
            cv2.circle(tmp, p, 5, (0, 255, 0), -1)
        cv2.imshow(ventana, tmp)
        k = cv2.waitKey(1) & 0xFF
        if k == ord("q"):  # cancelar
            cv2.destroyWindow(ventana)
            return None
        if len(puntos) == 4:
            cv2.destroyWindow(ventana)
            return puntos

def ajustar_manual(img, screen_size):
    manual = img.copy()
    angle = 0

    while True:
        display = rotar_libre(manual, angle) if angle != 0 else manual.copy()
        abrir_ventana_maximized("Ajuste manual", display, screen_size)
        k = cv2.waitKey(0) & 0xFF

        if k == ord("c"):  # Selección ROI rectangular
            roi = cv2.selectROI("Ajuste manual", display, fromCenter=False)
            cv2.destroyWindow("Ajuste manual")
            x, y, w, h = roi
            if w > 0 and h > 0:
                manual = display[y:y+h, x:x+w]
                angle = 0  # reiniciamos rotación
            continue

        elif k == ord("p"):  # Perspectiva: seleccionar 4 puntos
            puntos = seleccionar_4_puntos(display, screen_size)
            if puntos:
                manual = warp_cuadrilatero(display, puntos)
                angle = 0  # reiniciamos rotación
            continue  # seguir editando

        elif k == ord("q"):
            cv2.destroyWindow("Ajuste manual")
            return manual

        elif k == ord("l"):
            manual = cv2.rotate(manual, cv2.ROTATE_90_CLOCKWISE)
            angle = 0
        elif k == ord("j"):
            manual = cv2.rotate(manual, cv2.ROTATE_90_COUNTERCLOCKWISE)
            angle = 0
        elif k == ord("f"):
            manual = cv2.flip(manual, 1)
            angle = 0
        elif k == ord("v"):
            manual = cv2.flip(manual, 0)
            angle = 0
        elif k == ord("i"):
            angle += 1
        elif k == ord("u"):
            angle -= 1

        # La imagen final editada es siempre `manual`