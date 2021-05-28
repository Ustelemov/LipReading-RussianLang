import tensorflow as tf
import cv2
import numpy as np
import dlib

def shape_to_np(shape, dtype="int"):
  # initialize the list of (x, y)-coordinates
  coords = np.zeros((shape.num_parts, 2), dtype=dtype)

  # loop over all facial landmarks and convert them
  # to a 2-tuple of (x, y)-coordinates
  for i in range(0, shape.num_parts):
    coords[i] = (shape.part(i).x, shape.part(i).y)

  # return the list of (x, y)-coordinates
  return coords


class SSDFaceDetector():

    def __init__(self,model_path, input_width, input_height,det_threshold=0.3):

        self.det_threshold = det_threshold
        self.input_width = input_width
        self.input_height = input_height
        self.detection_graph = tf.Graph()


        with self.detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(model_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            self.sess = tf.compat.v1.Session(graph=self.detection_graph)

    
    def detect_face(self, image):

        h, w,c = image.shape

        image_res = cv2.resize(image, (self.input_width, self.input_height))
        image_np = cv2.cvtColor(image_res, cv2.COLOR_BGR2RGB)

        image_np_expanded = np.expand_dims(image_np, axis=0)
        image_tensor = self.detection_graph.get_tensor_by_name(
            'image_tensor:0')

        boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

        scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        classes = self.detection_graph.get_tensor_by_name(
            'detection_classes:0')
        num_detections = self.detection_graph.get_tensor_by_name(
            'num_detections:0')

        (boxes, scores, classes, num_detections) = self.sess.run([boxes, scores, classes, num_detections],feed_dict={image_tensor: image_np_expanded})

        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)

        filtered_score_index = np.argwhere(
            scores >= self.det_threshold).flatten()

        selected_boxes = boxes[filtered_score_index]

        faces = np.array([[
            int(x1 * w),
            int(y1 * h),
            int(x2 * w),
            int(y2 * h),
        ] for y1, x1, y2, x2 in selected_boxes])

        return faces

class DlibFaceAligner:
    def __init__(self,landmarks_path,model_path,SSD_input_w,SSD_input_h):
        # store the facial landmark predictor, desired output left
        # eye position, and desired output face width + height
        self.predictor = dlib.shape_predictor(landmarks_path)

        self.detector = SSDFaceDetector(model_path,input_width = SSD_input_w, input_height = SSD_input_h)

    def get_aligned_lips(self,cv2_frame,margin=50,desiredLeftLip = (0.05,0.5),desiredLipWidth=240,desiredLipHeight=240):
    
        coords = self.detector.detect_face(cv2_frame)

        if len(coords) == 0:
          return []
        else:
          x1, y1, x2, y2 = [int(c) for c in coords[0]]
          rect = dlib.rectangle(left=x1, top=y1, right=x2, bottom=y2)

          # dlib works with gray, so as image we're waiting for bgr opencv captured image and convert that to
          gray = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2GRAY)


          # convert the landmark (x, y)-coordinates to a NumPy array
          shape = self.predictor(gray, rect)
          shape = shape_to_np(shape)

          points = np.concatenate((shape[54:61], shape[64:68],shape[48:49],shape[49:54],shape[61:64]), axis=0)
          #bottom_lip = shape[54:61]+shape[64:68]+shape[48]
          #top_lip = shape[49:54]+shape[61:64]

          #Параметры кадра
          height, width, channels = cv2_frame.shape
          
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

          return self.align(lips_frame,[(left_x_convert,left_y_convert)],[right_convert],
                                  desiredLeftLip,desiredLipWidth,desiredLipHeight)


    def align(self,cv2_face_frame, leftEyePts,rightEyePts,desiredLeftEye = (0.35,0.35),desiredFaceWidth=256,desiredFaceHeight=256):
        
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
