from main import RealtimeTrainsPy
from datetime import datetime, date

system = RealtimeTrainsPy(complexity = "c", username = "rttapi_anonymous44401", password = "f44db35aa6c55279e0992420fac629511ee1320b")

system.get_service(service_uid = "G54071")