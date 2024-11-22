from app_poc.orm import core
from app_poc.query import base

MODEL = core.ChannelDetail


list_all = base.create_list_by(MODEL)
