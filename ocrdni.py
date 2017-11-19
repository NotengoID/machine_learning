import os
import numpy as np
import cv2

path = os.path.dirname(os.path.realpath('__file__'))

def leerImagenDeRequest(file=None):
    datos = []

    img = leerImagen(file)
    img_pre = preProcesarImagen(img)

    for n, xr, yr, wr, hr in getRegiones():
        region = img_pre[yr:yr + hr, xr:xr + wr]
        datos.append(getDato(region))

    return datos

def leerImagen(file):
    if (file is None):
        with open(getAbsPath('test/test0002.png'), 'rb') as infile:
            file = infile.read()

    file = np.fromstring(file, dtype='uint8')
    return cv2.imdecode(file, cv2.IMREAD_UNCHANGED)

def getAbsPath(dir):
    return os.path.join(path, dir)

def getRegiones():
    regiones = []
    x1 = 281 * 2
    h1 = 50 * 2
    h2 = 44 * 2
    regiones.append(['primer apellido', x1, 121 * 2, 141 * 2, h1])
    regiones.append(['segundo apellido', x1, 187 * 2, 310, h1])
    regiones.append(['prenombres', x1, 252 * 2, 184 * 2, h1])
    regiones.append(['sexo', x1, 322 * 2, 144 * 2, h2])
    regiones.append(['estado civil', 469 * 2, 322 * 2, 141 * 2, h2])
    regiones.append(['fecha de nacimiento', x1, 368 * 2, 141 * 2, h2])
    regiones.append(['dni', 120, 300, 300, 66])
    return regiones


def preProcesarImagen(img):
    img_std = cv2.resize(img, (1858, 1180))
    gray = cv2.cvtColor(img_std, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)
    return blur

def getModelos():
    modelos = []
    modelos.append(['R', (255, 255, 0), cv2.CascadeClassifier(getAbsPath('model/ml_R/cascade.xml'))])
    modelos.append(['A', (255, 0, 255), cv2.CascadeClassifier(getAbsPath('model/ml_A/cascade.xml'))])
    modelos.append(['C', (0, 255, 255), cv2.CascadeClassifier(getAbsPath('model/ml_C/cascade.xml'))])
    modelos.append(['E', (255, 100, 100), cv2.CascadeClassifier(getAbsPath('model/ml_E/cascade.xml'))])
    return modelos

def getDato(region):
    dato = ''
    letras = []
    regionx = region
    for letter, color, model in getModelos():
        for (x, y, w, h) in model.detectMultiScale(region):
            # print letter+'-'+str(x)+','+str(y)+'-'+str(w)+','+str(h)
            if (w > 25 and h > 25 and y > 22):
                #print letter+'-'+str(x)+','+str(y)+'-'+str(w)+','+str(h)
                #cv2.rectangle(regionx, (x, y), (x + w, y + h), color, 2)
                letras.append((letter,x))
    #cv2.imshow('img', regionx)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    letras = sorted(letras, key=lambda letra: letra[1])
    for letra in letras:
        dato+=letra[0]
    #print dato
    return dato

#per = leerImagenDeRequest()
