
from flask import Blueprint, render_template, request,\
    redirect, url_for, session, jsonify

from app.models import User, House, Area, Facility
from utils import status_code
from utils.functions import is_login

house_blueprint = Blueprint('house', __name__)


@house_blueprint.route('my_house/', methods=['GET'])
@is_login
def my_house():
    return render_template('myhouse.html')


@house_blueprint.route('house_info/', methods=['GET'])
@is_login
def house_info():
    # 判断当前登录系统的用户是否实名认证，如果实名认证，返回该用户发布的房屋信息
    user = User.query.get(session['user_id'])
    if user.id_card:
        # 已经实名认证了,返回房屋信息
        houses = House.query.filter(House.user_id == session['user_id']).all()
        house_info = [house.to_dict() for house in houses]
        return jsonify(code=status_code.OK, house_info=house_info)
    else:
        # 没有实名认证
        return jsonify(status_code.USER_AUTH_NOT_VALID)


@house_blueprint.route('newhouse/', methods=['GET'])
def new_house():
    return render_template('newhouse.html')


@house_blueprint.route('area_facility/', methods=['GET'])
def area_facility():
    # 获取所有区域信息
    areas = Area.query.all()
    # 获取所有设施信息
    facilities = Facility.query.all()
    # 将设施和区域信息序列化
    area_info = [area.to_dict() for area in areas]
    facility_info = [facility.to_dict() for facility in facilities]
    return jsonify(code=status_code.OK, area_info=area_info,
                   facility_info=facility_info)


@house_blueprint.route('newhouse/', methods=['POST'])
def my_new_house():
    # 创建房屋信息
    data = request.form
    house = House()
    house.user_id = session['user_id']
    house.title = data.get('title')
    house.price = data.get('price')
    house.area_id = data.get('area_id')
    house.address = data.get('address')
    house.room_count = data.get('room_count')
    house.acreage = data.get('acreage')
    house.unit = data.get('unit')
    house.capacity = data.get('capacity')
    house.beds = data.get('beds')
    house.deposit = data.get('deposit')
    house.min_days = data.get('min_days')
    house.max_days = data.get('max_days')

    # 获取设施信息，使用getlist
    facilities = data.getlist('facility')
    for f_id in facilities:
        facility = Facility.query.get(f_id)
        # 添加房屋和设施的关联关系，多对多
        house.facilities.append(facility)
    # commit，在数据库中创建house和设施的中间表数据
    house.add_update()
    return jsonify(status_code.SUCCESS)



