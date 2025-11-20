"""菜单路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.menu_service import MenuService
from utils.auth_utils import token_required, admin_required

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/', methods=['GET'])
def get_menu_items():
    """获取菜单列表"""
    try:
        # 获取查询参数
        available_only = request.args.get('available_only', 'true').lower() == 'true'
        category = request.args.get('category')
        keyword = request.args.get('keyword')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        # 搜索功能
        if keyword:
            result = MenuService.search_menu_items(keyword, available_only)
            # 实现简单分页
            start = (page - 1) * per_page
            end = start + per_page
            paginated_items = result['menu_items'][start:end]

            return jsonify({
                'success': True,
                'data': {
                    'items': paginated_items,
                    'total': result['total'],
                    'page': page,
                    'per_page': per_page,
                    'pages': (result['total'] + per_page - 1) // per_page
                }
            }), 200

        # 获取分类菜单
        if category:
            result = MenuService.get_all_menu_items(available_only, category)
        else:
            result = MenuService.get_all_menu_items(available_only)

        if result['success']:
            # 实现简单分页
            start = (page - 1) * per_page
            end = start + per_page
            paginated_items = result['menu_items'][start:end]

            return jsonify({
                'success': True,
                'data': {
                    'items': paginated_items,
                    'total': result['total'],
                    'page': page,
                    'per_page': per_page,
                    'pages': (result['total'] + per_page - 1) // per_page
                }
            }), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取菜单分类"""
    try:
        result = MenuService.get_all_menu_items(available_only=True)
        if result['success']:
            # 提取所有分类
            categories = set()
            for item in result['menu_items']:
                categories.add(item['category'])

            # 格式化分类列表
            category_list = [
                {'value': 'all', 'label': '全部'}
            ]
            for cat in sorted(categories):
                category_list.append({'value': cat, 'label': cat.title()})

            return jsonify({
                'success': True,
                'data': category_list
            }), 200
        else:
            return jsonify({
                'success': True,
                'data': [
                    {'value': 'all', 'label': '全部'},
                    {'value': 'coffee', 'label': '咖啡'},
                    {'value': 'tea', 'label': '茶饮'},
                    {'value': 'dessert', 'label': '甜点'},
                    {'value': 'other', 'label': '其他'}
                ]
            }), 200
    except Exception as e:
        return jsonify({
            'success': True,
            'data': [
                {'value': 'all', 'label': '全部'},
                {'value': 'coffee', 'label': '咖啡'},
                {'value': 'tea', 'label': '茶饮'},
                {'value': 'dessert', 'label': '甜点'},
                {'value': 'other', 'label': '其他'}
            ]
        }), 200

@menu_bp.route('/popular', methods=['GET'])
def get_popular_items():
    """获取热门商品"""
    try:
        result = MenuService.get_all_menu_items(available_only=True)
        if result['success']:
            # 筛选热门商品
            popular_items = [item for item in result['menu_items'] if item.get('is_popular', False)]

            return jsonify({
                'success': True,
                'data': popular_items[:6]  # 返回前6个热门商品
            }), 200
        else:
            return jsonify({'success': False, 'errors': ['获取热门商品失败']}), 400
    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    """获取单个菜单项详情"""
    try:
        result = MenuService.get_menu_item_by_id(item_id)
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['menu_item']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': '商品不存在'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500