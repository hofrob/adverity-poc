from app_poc.orm import core
from app_poc.query import base

MODEL = core.Episode


get_by_id = base.create_one_by(MODEL, MODEL.id)
list_all = base.create_list_by(MODEL, joins=[MODEL.channels])
