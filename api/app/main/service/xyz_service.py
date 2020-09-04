import uuid
import datetime

from app.main import DbSession
from app.main.model.xyz import Xyz

def save_new_xyz(data):
    xyz = DbSession.query(Xyz).filter(Xyz.code==data['code']).first()
    
    if not xyz:
        new_xyz = Xyz(
            name=data['name'],
            code=data['code'],
            create_date=datetime.datetime.utcnow(),
            active=data['active']
        )
        save_changes(new_xyz)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Xyz already exists. Please Log in.',
        }
        return response_object, 409

def get_all_xyzs():
    return DbSession.query(Xyz).all()

def get_a_xyz(code):
    return DbSession.query(Xyz).filter(Xyz.code==code).first()

def get_xyz_version(id):
    return DbSession.query(XyzVersion).filter(XyzVersion.id==id).first()
    
def save_changes(xyz_obj):
    DbSession.add(xyz_obj)
    DbSession.commit()
    
def xyz_commit():
    DbSession.commit()
    
def xyz_delete(xyz_obj):
    DbSession.delete(xyz_obj)
    DbSession.commit()

