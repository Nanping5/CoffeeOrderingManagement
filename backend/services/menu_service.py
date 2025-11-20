"""菜单服务"""
from models.menu import MenuItem
from extensions import db
from utils.auth_utils import save_file, allowed_file
import os

class MenuService:
    """菜单服务类"""

    @staticmethod
    def get_all_menu_items(available_only=True, category=None):
        """获取所有菜单项"""
        try:
            query = MenuItem.query

            # 筛选可用商品
            if available_only:
                query = query.filter_by(is_available=True)

            # 按分类筛选
            if category:
                query = query.filter_by(category=category)

            menu_items = query.order_by(MenuItem.category, MenuItem.name).all()
            return {
                'success': True,
                'menu_items': [item.to_dict() for item in menu_items],
                'total': len(menu_items)
            }

        except Exception as e:
            return {'success': False, 'errors': [f'获取菜单失败: {str(e)}']}

    @staticmethod
    def get_menu_item_by_id(item_id):
        """根据ID获取菜单项"""
        try:
            menu_item = MenuItem.query.get(item_id)
            if not menu_item:
                return {'success': False, 'errors': ['菜单项不存在']}

            return {
                'success': True,
                'menu_item': menu_item.to_dict()
            }

        except Exception as e:
            return {'success': False, 'errors': [f'获取菜单项失败: {str(e)}']}

    @staticmethod
    def create_menu_item(item_data, image_file=None):
        """创建菜单项"""
        try:
            # 验证数据
            errors = MenuService._validate_menu_data(item_data)
            if errors:
                return {'success': False, 'errors': errors}

            # 处理图片上传
            image_url = None
            if image_file and allowed_file(image_file.filename):
                upload_folder = 'static/uploads/menu'
                image_url = save_file(image_file, upload_folder)
                if image_url:
                    image_url = '/' + image_url.replace('\\', '/')  # 统一路径分隔符

            # 创建菜单项
            menu_item = MenuItem(
                name=item_data.get('name'),
                description=item_data.get('description'),
                price=item_data.get('price'),
                category=item_data.get('category', 'coffee'),
                image_url=image_url,
                is_available=item_data.get('is_available', True)
            )

            db.session.add(menu_item)
            db.session.commit()

            return {
                'success': True,
                'message': '菜单项创建成功',
                'menu_item': menu_item.to_dict()
            }

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [f'创建菜单项失败: {str(e)}']}

    @staticmethod
    def update_menu_item(item_id, item_data, image_file=None):
        """更新菜单项"""
        try:
            menu_item = MenuItem.query.get(item_id)
            if not menu_item:
                return {'success': False, 'errors': ['菜单项不存在']}

            # 验证数据
            errors = MenuService._validate_menu_data(item_data, is_update=True)
            if errors:
                return {'success': False, 'errors': errors}

            # 处理图片上传
            if image_file and allowed_file(image_file.filename):
                upload_folder = 'static/uploads/menu'
                image_url = save_file(image_file, upload_folder)
                if image_url:
                    image_url = '/' + image_url.replace('\\', '/')  # 统一路径分隔符
                    item_data['image_url'] = image_url

            # 更新菜单项
            allowed_fields = ['name', 'description', 'price', 'category', 'image_url', 'is_available']
            for field in allowed_fields:
                if field in item_data:
                    setattr(menu_item, field, item_data[field])

            db.session.commit()

            return {
                'success': True,
                'message': '菜单项更新成功',
                'menu_item': menu_item.to_dict()
            }

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [f'更新菜单项失败: {str(e)}']}

    @staticmethod
    def delete_menu_item(item_id):
        """删除菜单项"""
        try:
            menu_item = MenuItem.query.get(item_id)
            if not menu_item:
                return {'success': False, 'errors': ['菜单项不存在']}

            # 检查是否有关联的订单
            if menu_item.order_items.count() > 0:
                return {'success': False, 'errors': ['该菜单项有关联订单，无法删除']}

            # 删除图片文件
            if menu_item.image_url:
                try:
                    file_path = menu_item.image_url.lstrip('/')
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except:
                    pass  # 删除文件失败不影响数据库操作

            db.session.delete(menu_item)
            db.session.commit()

            return {
                'success': True,
                'message': '菜单项删除成功'
            }

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [f'删除菜单项失败: {str(e)}']}

    @staticmethod
    def toggle_menu_item_availability(item_id):
        """切换菜单项可用状态"""
        try:
            menu_item = MenuItem.query.get(item_id)
            if not menu_item:
                return {'success': False, 'errors': ['菜单项不存在']}

            menu_item.is_available = not menu_item.is_available
            db.session.commit()

            status_text = '上架' if menu_item.is_available else '下架'
            return {
                'success': True,
                'message': f'菜单项{status_text}成功',
                'menu_item': menu_item.to_dict()
            }

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [f'更新状态失败: {str(e)}']}

    @staticmethod
    def get_menu_categories():
        """获取所有菜单分类"""
        try:
            categories = MenuItem.get_categories()
            return {
                'success': True,
                'categories': categories
            }

        except Exception as e:
            return {'success': False, 'errors': [f'获取分类失败: {str(e)}']}

    @staticmethod
    def get_popular_items(limit=10):
        """获取热门商品"""
        try:
            popular_items = MenuItem.get_popular_items(limit)
            result = []
            for item_data in popular_items:
                menu_item = MenuItem.query.get(item_data.menu_id)
                if menu_item:
                    item_dict = menu_item.to_dict()
                    item_dict['total_quantity'] = item_data.total_quantity
                    result.append(item_dict)

            return {
                'success': True,
                'popular_items': result
            }

        except Exception as e:
            return {'success': False, 'errors': [f'获取热门商品失败: {str(e)}']}

    @staticmethod
    def search_menu_items(keyword, available_only=True):
        """搜索菜单项"""
        try:
            query = MenuItem.query

            # 筛选可用商品
            if available_only:
                query = query.filter_by(is_available=True)

            # 搜索关键词
            if keyword:
                search_pattern = f'%{keyword}%'
                query = query.filter(
                    (MenuItem.name.like(search_pattern)) |
                    (MenuItem.description.like(search_pattern)) |
                    (MenuItem.category.like(search_pattern))
                )

            menu_items = query.order_by(MenuItem.category, MenuItem.name).all()

            return {
                'success': True,
                'menu_items': [item.to_dict() for item in menu_items],
                'total': len(menu_items)
            }

        except Exception as e:
            return {'success': False, 'errors': [f'搜索失败: {str(e)}']}

    @staticmethod
    def _validate_menu_data(data, is_update=False):
        """验证菜单数据"""
        errors = []

        if not data:
            errors.append('请提供菜单信息')
            return errors

        if not is_update or 'name' in data:
            name = data.get('name', '').strip()
            if not name:
                errors.append('菜单项名称不能为空')
            elif len(name) > 100:
                errors.append('菜单项名称不能超过100个字符')

        if not is_update or 'price' in data:
            price = data.get('price')
            if price is None:
                errors.append('价格不能为空')
            elif not isinstance(price, (int, float)) or price <= 0:
                errors.append('价格必须大于0')
            elif price > 999999.99:
                errors.append('价格不能超过999999.99')

        if not is_update or 'category' in data:
            category = data.get('category', '').strip()
            if not category:
                errors.append('分类不能为空')
            elif len(category) > 50:
                errors.append('分类不能超过50个字符')

        if 'description' in data:
            description = data.get('description', '').strip()
            if description and len(description) > 1000:
                errors.append('描述不能超过1000个字符')

        return errors