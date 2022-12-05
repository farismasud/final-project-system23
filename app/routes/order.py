import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
    func
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.utils.auth_token import decode_auth_token
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.user import Users
from app.models.cart import Carts
from app.models.product import Products
from app.models.order import Orders
from . import order_bp, orders_bp


@order_bp.route("", methods=["POST"])
@decode_auth_token
def create_order(current_user):
    body = request.json
    method = body.get("shipping_method")
    address = body.get("shipping_address")
    user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
    
    for x in run_query(select(Carts.user_id, func.sum(Products.price*Carts.quantity)).filter(Carts.product_id==Products.id).where(Carts.user_id==current_user).group_by(Carts.user_id)):
        if method == "reguler":
            if x['sum_1'] < 200:
                total = int(x['sum_1']*(15/100))
                if total > run_query(select(Users.balance).where(Users.id==current_user))[0]['balance']:
                    return error_message(401,"your balance is not enough")
                else:
                    result_balance= int(run_query(select(Users.balance).where(Users.id==current_user))[0]['balance'])-total
                    run_query(insert(Orders).values(id=uuid.uuid4(),user_id=current_user,shipping_method=method,shipping_address=address,total_price=format(total),create_at=format_datetime(),create_by=user_name),True)
                    # run_query(update(Carts).values(status='soft_delete'),True)
                    products_result=[]
                    for x in run_query(select(Orders)):
                        for x in run_query(select(Carts,Products.image,Products.price,Products.title).filter(Products.id==Carts.product_id).where(Carts.user_id==current_user)):
                            products_result.append({"id":x['id'],"details":{"quantity":x["quantity"],"size":x["size"]},"price":x["price"],"image":x["image"],"name":x["title"]})
                    # run_query(insert(Orders).values(products=products_result),True)
                    run_query(update(Users).values(balance=result_balance).where(Users.id==current_user),True)
                    return success_message(200,"order success")
            elif x['sum_1'] >= 200:
                total = int(x['sum_1']*(20/100))
                if total > run_query(select(Users.balance).where(Users.id==current_user))[0]['balance']:
                    return error_message(401,"your balance is not enough")
                else:
                    run_query(insert(Orders).values(id=uuid.uuid4(),user_id=current_user,shipping_method=method,shipping_address=address,total_price=format(total),create_at=format_datetime(),create_by=user_name),True)
                    result_balance= int(run_query(select(Users.balance).where(Users.id==current_user))[0]['balance'])-total
                    # run_query(update(Carts).values(status='soft_delete'),True)
                    products_result=[]
                    for x in run_query(select(Orders)):
                        for x in run_query(select(Carts,Products.image,Products.price,Products.title).filter(Products.id==Carts.product_id).where(Carts.user_id==current_user)):
                            products_result.append({"id":x['id'],"details":{"quantity":x["quantity"],"size":x["size"]},"price":x["price"],"image":x["image"],"name":x["title"]})
                    # run_query(insert(Orders).values(products=products_result),True)
                    run_query(update(Users).values(balance=result_balance).where(Users.id==current_user),True)
                    return success_message(200,"order success")
        elif method == "next day":
            if x['sum_1'] < 300:
                total = int(x['sum_1']*(20/100))
                if total > run_query(select(Users.balance).where(Users.id==current_user))[0]['balance']:
                    return error_message(401,"your balance is not enough")
                else:
                    run_query(insert(Orders).values(id=uuid.uuid4(),user_id=current_user,shipping_method=method,shipping_address=address,total_price=format(total),create_at=format_datetime(),create_by=user_name),True)
                    result_balance= int(run_query(select(Users.balance).where(Users.id==current_user))[0]['balance'])-total
                    # run_query(update(Carts).values(status='soft_delete'),True)
                    products_result=[]
                    for x in run_query(select(Orders)):
                        for x in run_query(select(Carts,Products.image,Products.price,Products.title).filter(Products.id==Carts.product_id).where(Carts.user_id==current_user)):
                            products_result.append({"id":x['id'],"details":{"quantity":x["quantity"],"size":x["size"]},"price":x["price"],"image":x["image"],"name":x["title"]})
                    # run_query(insert(Orders).values(products=products_result),True)
                    run_query(update(Users).values(balance=result_balance).where(Users.id==current_user),True)
                    return success_message(200,"order success")
            elif x['sum_1'] >= 300:
                total = int(x['sum_1']*(25/10))
                if total > run_query(select(Users.balance).where(Users.id==current_user))[0]['balance']:
                    return error_message(401,"your balance is not enough")
                else:
                    run_query(insert(Orders).values(id=uuid.uuid4(),user_id=current_user,shipping_method=method,shipping_address=address,total_price=format(total),create_at=format_datetime(),create_by=user_name),True)
                    result_balance= int(run_query(select(Users.balance).where(Users.id==current_user))[0]['balance'])-total
                    # run_query(update(Carts).values(status='soft_delete'),True)
                    products_result=[]
                    for x in run_query(select(Orders)):
                        for x in run_query(select(Carts,Products.image,Products.price,Products.title).filter(Products.id==Carts.product_id).where(Carts.user_id==current_user)):
                            products_result.append({"id":x['id'],"details":{"quantity":x["quantity"],"size":x["size"]},"price":x["price"],"image":x["image"],"name":x["title"]})
                    # run_query(insert(Orders).values(products=products_result),True)
                    run_query(update(Users).values(balance=result_balance).where(Users.id==current_user),True)
                    return success_message(200,"order success")
            
    

@order_bp.route("", methods=["GET"])
@decode_auth_token
def user_orders(current_user):
    pass
    
@orders_bp.route("", methods=["GET"])
@decode_auth_token
def get_orders(current_user):
    data=[]
    name = run_query(select(Users.name).where(Users.id==current_user))[0]['name']
    user_id = run_query(select(Users.id).where(Users.id==current_user))[0]['id']
    user_email = run_query(select(Users.email).where(Users.id==current_user))[0]['email']
    total = 0
    
    for y in run_query(select(Orders.create_at,Orders.id).where(Orders.user_id==current_user)):
        for x in run_query(select(Carts.user_id,Orders, func.sum(Products.price*Carts.quantity)).filter(Carts.product_id==Products.id).where(Carts.user_id==current_user).group_by(Carts.user_id)):
            total = x['sum_1']
        data.append({"id":y['id'],"user_name":name,"create_at":y['create_at'],"user_id":user_id,"user_email":user_email,"total":total})
    return success_message(200,data)