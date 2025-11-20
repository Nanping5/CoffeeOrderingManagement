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
                'menu_items': paginated_items,
                'total': result['total'],
                'page': page,
                'per_page': per_page,
                'pages': (result['total'] + per_page - 1) // per_page
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
                'menu_items': paginated_items,
                'total': result['total'],
                'page': page,
                'per_page': per_page,
                'pages': (result['total'] + per_page - 1) // per_page
            }), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    """获取单个菜单项详情"""
    try:
        result = MenuService.get_menu_item_by_id(item_id)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/', methods=['POST'])
@admin_required
def create_menu_item():
    """创建菜单项（仅管理员）"""
    try:
        data = request.form.to_dict()
        image_file = request.files.get('image')

        result = MenuService.create_menu_item(data, image_file)
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/<int:item_id>', methods=['PUT'])
@admin_required
def update_menu_item(item_id):
    """更新菜单项（仅管理员）"""
    try:
        data = request.form.to_dict()
        image_file = request.files.get('image')

        result = MenuService.update_menu_item(item_id, data, image_file)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/<int:item_id>', methods=['DELETE'])
@admin_required
def delete_menu_item(item_id):
    """删除菜单项（仅管理员）"""
    try:
        result = MenuService.delete_menu_item(item_id)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/<int:item_id>/toggle', methods=['PATCH'])
@admin_required
def toggle_menu_item_availability(item_id):
    """切换菜单项可用状态（仅管理员）"""
    try:
        result = MenuService.toggle_menu_item_availability(item_id)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取所有菜单分类"""
    try:
        result = MenuService.get_menu_categories()
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/popular', methods=['GET'])
def get_popular_items():
    """获取热门商品"""
    try:
        limit = int(request.args.get('limit', 10))
        result = MenuService.get_popular_items(limit)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/search', methods=['GET'])
def search_menu_items():
    """搜索菜单项"""
    try:
        keyword = request.args.get('q', '').strip()
        if not keyword:
            return jsonify({'success': False, 'errors': ['搜索关键词不能为空']}), 400

        available_only = request.args.get('available_only', 'true').lower() == 'true'
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        result = MenuService.search_menu_items(keyword, available_only)
        if result['success']:
            # 实现简单分页
            start = (page - 1) * per_page
            end = start + per_page
            paginated_items = result['menu_items'][start:end]

            return jsonify({
                'success': True,
                'menu_items': paginated_items,
                'total': result['total'],
                'page': page,
                'per_page': per_page,
                'pages': (result['total'] + per_page - 1) // per_page,
                'keyword': keyword
            }), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/category/<category_name>', methods=['GET'])
def get_menu_by_category(category_name):
    """根据分类获取菜单项"""
    try:
        available_only = request.args.get('available_only', 'true').lower() == 'true'
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        result = MenuService.get_all_menu_items(available_only, category_name)
        if result['success']:
            # 实现简单分页
            start = (page - 1) * per_page
            end = start + per_page
            paginated_items = result['menu_items'][start:end]

            return jsonify({
                'success': True,
                'menu_items': paginated_items,
                'category': category_name,
                'total': result['total'],
                'page': page,
                'per_page': per_page,
                'pages': (result['total'] + per_page - 1) // per_page
            }), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@menu_bp.route('/stats', methods=['GET'])
@admin_required
def get_menu_stats():
    """获取菜单统计信息（仅管理员）"""
    try:
        from models.menu import MenuItem
        from extensions import db

        # 总菜单项数量
        total_items = MenuItem.query.count()
        available_items = MenuItem.query.filter_by(is_available=True).count()

        # 按分类统计
        category_stats = db.session.query(
            MenuItem.category,
            db.func.count(MenuItem.id).label('count')
        ).group_by(MenuItem.category).all()

        categories = []
        for cat, count in category_stats:
            available_count = MenuItem.query.filter_by(
                category=cat, is_available=True
            ).count()
            categories.append({
                'category': cat,
                'total': count,
                'available': available_count
            })

        return jsonify({
            'success': True,
            'stats': {
                'total_items': total_items,
                'available_items': available_items,
                'unavailable_items': total_items - available_items,
                'categories': categories
            }
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500