from deepface import DeepFace
from functions import pretty_print

models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
  "GhostFaceNet"
]

# face attr analysis
objs = DeepFace.analyze(
  img_path = "./imgs/woman1.jpg", 
  actions = ['emotion'],
)

pretty_print(objs)