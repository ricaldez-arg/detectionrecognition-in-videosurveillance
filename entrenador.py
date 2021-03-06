#!/usr/bin/env python
import argparse

import cv2
import imutils
from deteccion_reconocimiento import DetectorRostro
from imutils.video import VideoStream

from deteccion_reconocimiento.reconocimiento import Generador


def init(camara, detectorR, generador, args):
    capturar = False
    while True:
        img = camara.read()
        if img is None:
            break
        img = imutils.resize(img, width=720)

        pts, imgs = detectorR.detectar(img)
        for (x,y,xf,yf) in pts:
            cv2.rectangle(img,(x,y),(xf,yf),(0,255,0),2)
        if capturar:
            for im in imgs:
                generador.guardar(args['usuario'],im)
                cv2.putText(img, '[CAPTURADO]', (270, ycord - (ycord/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
            capturar = False

        ayuda = "Captura la imagen con la tecla 'SPACE' o 'ENTER'"
        ycord = img.shape[0]
        cv2.putText(img, ayuda, (10, ycord - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(255,255,255), 1)
        cv2.imshow("ENTRENADOR", img)

        t = cv2.waitKey(20)
        tecla = t & 0xff
        if tecla == ord(' ') or tecla == 13:
            capturar = True

        if tecla == ord('q'):
            break

    camara.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--usuario", required=True, help="nombre del usuario")
    ap.add_argument("-f", "--fuente", default=0, help="fuente de video o camara")
    args = vars(ap.parse_args())

    src = args['fuente']

    camara = VideoStream(src).start()
    detectorR = DetectorRostro('./util/haarcascades/haarcascade_frontalface_default.xml')

    generador = Generador('./util/data/')
    if not generador.existe(args['usuario']):
        generador.crear_usuario(args['usuario'])

    init(camara, detectorR, generador, args)
