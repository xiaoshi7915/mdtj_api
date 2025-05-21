"""
用户模型类
"""

class User:
    """用户模型类"""
    
    def __init__(self, data=None):
        """
        初始化用户对象
        
        Args:
            data: 用户数据字典
        """
        if data is None:
            data = {}
            
        self.id = data.get('id')
        self.name = data.get('name', '')
        self.contact_info = data.get('contact_info', '')
        self.id_card_number = data.get('id_card_number', '')
        self.address = data.get('address', '')
        self.verified = data.get('verified', False)
        self.verification_result = data.get('verification_result', '')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
    
    def to_dict(self):
        """
        转换为字典
        
        Returns:
            dict: 用户信息字典
        """
        return {
            'id': self.id,
            'name': self.name,
            'contact_info': self.contact_info,
            'id_card_number': self.id_card_number,
            'address': self.address,
            'verified': self.verified,
            'verification_result': self.verification_result,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }
    
    def __repr__(self):
        """字符串表示"""
        return f"<User {self.name} ({self.id_card_number})>" 