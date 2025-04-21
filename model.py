from deepface import DeepFace
from functions import pretty_print
from datetime import datetime

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

# DeepFace.build_model('Facenet512')

begin = datetime.now()

# face attr analysis
objs = DeepFace.analyze(
  img_path = "./imgs/woman1.jpg", 
  actions = ['emotion'],
  detector_backend='yunet'
)

end = datetime.now()

pretty_print(objs)

processing_time = end - begin

total_seconds = processing_time.total_seconds()
hours = int(total_seconds // 3600)
minutes = int((total_seconds % 3600) // 60)
seconds = total_seconds % 60

print(f"Processing Time: {hours}h {minutes}m {seconds:.2f}s")