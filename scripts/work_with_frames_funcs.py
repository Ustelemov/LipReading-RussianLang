import face_recognition
import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont

#Функция для получения cv2-кадров лиц (возвращается список cv2 кадров) с отступом margin для границ лица
def get_faces_from_frame(cv2_frame, margin=10):
  # Перевед изображение из BGR-цвета (который использует OpenCV) в RGB (который необходим для face_recognition)
  rgb_frame = frame[:, :, ::-1]
  #Параметры кадра
  height, width, channels = cv2_frame.shape

  #Массив координат квадрата лица: верхней угол, правый угол, нижний угол, левый угол (top,right,bottom,left)
  face_locations = face_recognition.face_locations(rgb_frame)

  face_frames = []

  #Установим границы для сабфрейма-лица, проверив на выход за границы изображения
  for top,right,bottom,left in face_locations:
    yMin = top - margin if top - margin >= 0 else 0
    yMax = bottom + margin if bottom + margin < height  else height-1

    xMin = left - margin if left - margin >= 0 else 0
    xMax = right + margin if right + margin < width else width -1
  
    face_frames.append(cv2_frame[yMin:yMax,xMin:xMax])

  return face_frames

#Функция нормализации - может быть использована как для губ, так и для лица:
#Не будем переименовывать переменные
#В случае губ передается крайняя левая координата, в случае лица - координаты глаз
#cv2_face_frame - кадр с лицом (одним лицом)
#leftPts - точки левого глаза (у губ - крайняя левая точка)
#rightPts - точки правого глаза (у губ - крайняя правая точка)
#desiredLeftEye - желаемая позиция центроида (центра) левого глаза  (у губ - желаемая позиция левой точки)
#desiredFaceWidth - требуемый выходной размер изображения 
#desiredFaceHeight - требуемый выходной размер изображения 


def align(cv2_face_frame, leftEyePts,rightEyePts,desiredLeftEye = (0.35,0.35),desiredFaceWidth=256,desiredFaceHeight=256):
  
  leftEyePts = np.asarray(leftEyePts)
  rightEyePts = np.asarray(rightEyePts)

  #вычисляем центр масс каждого глаза
  leftEyeCenter = leftEyePts.mean(axis=0).astype("int")
  rightEyeCenter = rightEyePts.mean(axis=0).astype("int")

  #вычисляем угол между центроидами глаз
  dY = rightEyeCenter[1] - leftEyeCenter[1]
  dX = rightEyeCenter[0] - leftEyeCenter[0]

  #Изначальная формула: angle = np.degrees(np.arctan2(dY, dX))-180. -180 убрал за ненадобностью?
  angle = np.degrees(np.arctan2(dY, dX))

  #Вычисляем желательную X координату правого глаза, основываясь на желательной координате левого глаза
  desiredRightEyeX = 1.0 - desiredLeftEye[0]

  #вычисляем величину масштабирования
  #c помошью вычисления отношения между текущим расстоянием между глазами
  #и желательным расстоянием между глазами 
  dist = np.sqrt((dX ** 2) + (dY ** 2))
  desiredDist = (desiredRightEyeX - desiredLeftEye[0])
  desiredDist *= desiredFaceWidth
  scale = desiredDist / dist

  #вычисляем центр (х,y)-координаты (медианную точку)
  #между двумя глазами
  eyesCenter = ((leftEyeCenter[0] + rightEyeCenter[0]) // 2,
  (leftEyeCenter[1] + rightEyeCenter[1]) // 2)

  #Создаем матрицу преобразования
  M = cv2.getRotationMatrix2D(eyesCenter, angle, scale)

  #Изменяем компоненты матрицы
  tX = desiredFaceWidth * 0.5
  tY = desiredFaceHeight * desiredLeftEye[1]
  M[0, 2] += (tX - eyesCenter[0])
  M[1, 2] += (tY - eyesCenter[1])

  #применяем аффиное преобразование
  (w, h) = (desiredFaceWidth,desiredFaceHeight)
  output = cv2.warpAffine(cv2_face_frame, M, (w, h),flags=cv2.INTER_CUBIC)

  return output

#Функция получение массива выравненных лиц
#для этого потребуется получить массив лиц с помощью get_faces_from_frame (с каким-то margin) 
#cv2_frame - cv2 кадр с лицами
#desiredLeftEye - желаемая позиция центроида (центра) левого глаза
#desiredFaceWidth - требуемый выходной размер изображения (лица)
#desiredFaceHeight - требуемый выходной размер изображения (лица)

def get_aligned_faces(cv2_frame,margin=10,desiredLeftEye = (0.35,0.35),desiredFaceWidth=256,desiredFaceHeight=256):
  #список выровненных кадров лиц
  aligned_faces = []

  for f in get_faces_from_frame(cv2_frame,margin): 
    rgb_frame = f[:, :, ::-1]
    face_locations = face_recognition.face_landmarks(rgb_frame)
    
    face_aligned = align_face(f,face_locations[0]['left_eye'],face_locations[0]['right_eye'],desiredLeftEye,desiredFaceWidth,desiredFaceHeight)
    aligned_faces.append(face_aligned)

  return aligned_faces

def draw_point(cv2_frame,point):
  cv2.circle(cv2_frame, point, 1, (255, 255, 255), -1)  

def draw_points(cv2_frame,points):
	for (x, y) in points:
		draw_point(cv2_frame,(x,y))
  
#Функция возвращающая точки нижний губы (bottom_lip) и верхней губы (top_lip) для каждого лица на кадре 
def get_lips_points(cv2_frame):
  rgb_frame = cv2_frame[:, :, ::-1]
  face_locations = face_recognition.face_landmarks(rgb_frame)

  lips = []

  for loc in face_locations:
    lips.append({'bottom_lip':loc['bottom_lip'],'top_lip':loc['top_lip']})
  return lips

#Функция рисующая точки губ для каждого лица
def draw_lips_points(cv2_frame):
  for lips in get_lips_points(cv2_frame):
    draw_points(cv2_frame,lips['bottom_lip']+lips['top_lip'])

#Здесь мы не можем создать отдельную функцию для получения губ с margin
#А потом искать в них точки, только по губам он точки не найдет
def get_aligned_lips(cv2_frame,margin=50,desiredLeftLip = (0.05,0.5),desiredLipWidth=320,desiredLipHeight=240):
  
  aligned_lips = []

  face_locations = get_lips_points(cv2_frame)

  #Параметры кадра
  height, width, channels = cv2_frame.shape
  
  for loc in face_locations:
    points = loc['bottom_lip']+loc['top_lip']
    
    #Получим точки максимальные и минимальные по X и Y
    xMax_p = max(points,key = lambda item: item[0])
    xMin_p = min(points,key = lambda item: item[0])
    
    yMax_p = max(points,key = lambda item: item[1])
    yMin_p = min(points,key = lambda item: item[1])
    
    #Удостоверимся, что не выходим за кадр
    xMax_m = xMax_p[0]+margin if xMax_p[0]+margin<width else width-1
    xMin_m = xMin_p[0]-margin if xMin_p[0]-margin>=0 else 0

    yMax_m = yMax_p[1]+margin if yMax_p[1]+margin<height else height-1
    yMin_m = yMin_p[1]-margin if yMin_p[1]-margin>=0 else 0

    lips_frame = cv2_frame[yMin_m:yMax_m,xMin_m:xMax_m]

    #Переведем координаты в координаты нового кадра
    #От x_min отняли margin либо если расстояние до 0 была меньше margin, то эту разницу
    left_x_convert = margin if xMin_p[0]>margin else xMin_p[0]

    #Посмотрим какова была разница между y координатой крайней точки и минимальной y координатой
    #И добавим marin, либо меньше как и с left_x_convert
    left_y_convert = (xMin_p[1]-yMin_p[1])+margin if yMin_p[1]>margin else yMin_p[1]


    #Теперь посмотрим какая разница была у правой точки с левой и добавим эту разницу
    right_convert = (left_x_convert+(xMax_p[0]-xMin_p[0]),left_y_convert+(xMax_p[1]-xMin_p[1]))

    aligned_lips.append(align(lips_frame,[(left_x_convert,left_y_convert)],[right_convert],
                              desiredLeftLip,desiredLipWidth,desiredLipHeight))
  return aligned_lips

#Используется DejaVuSans.ttf, чтобы мочь писать и на русском
def label_on_frame(cv2_frame,label,point=(10,10),fontsize=24,font_path='/content/DejaVuSans.ttf',color=(255,255,255,0)):
  font = ImageFont.truetype(font_path, fontsize)
  
  rgb_frame = cv2_frame[:,:,::-1]
  img_pil = Image.fromarray(rgb_frame)

  draw = ImageDraw.Draw(img_pil)
  draw.text(point, label , font=font, fill=color)
  
  frame_texted = np.asarray(img_pil)
  frame_texted = frame_texted[:,:,::-1]

  return frame_texted
