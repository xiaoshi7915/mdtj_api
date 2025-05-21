"""
受理单模型类
"""

class AppealRecord:
    """受理单模型类"""
    
    def __init__(self, data=None):
        """
        初始化受理单对象
        
        Args:
            data: 受理单数据字典
        """
        if data is None:
            data = {}
            
        self.id = data.get('id')
        self.case_number = data.get('case_number', '')
        self.person_name = data.get('person_name', '')
        self.contact_info = data.get('contact_info', '')
        self.gender = data.get('gender', '')
        self.id_card_number = data.get('id_card_number', '')
        self.address = data.get('address', '')
        self.incident_time = data.get('incident_time', '')
        self.incident_location = data.get('incident_location', '')
        self.incident_description = data.get('incident_description', '')
        self.people_involved = data.get('people_involved', '')
        self.submitted_materials = data.get('submitted_materials', '')
        self.handling_department = data.get('handling_department', '')
        self.handling_status = data.get('handling_status', '')
        self.expected_completion = data.get('expected_completion', '')
        self.create_time = data.get('create_time')
        self.qr_code = data.get('qr_code', '')
        self.markdown_doc = data.get('markdown_doc', '')
    
    def to_dict(self):
        """
        转换为字典
        
        Returns:
            dict: 受理单信息字典
        """
        return {
            'id': self.id,
            'case_number': self.case_number,
            'person_name': self.person_name,
            'contact_info': self.contact_info,
            'gender': self.gender,
            'id_card_number': self.id_card_number,
            'address': self.address,
            'incident_time': self.incident_time,
            'incident_location': self.incident_location,
            'incident_description': self.incident_description,
            'people_involved': self.people_involved,
            'submitted_materials': self.submitted_materials,
            'handling_department': self.handling_department,
            'handling_status': self.handling_status,
            'expected_completion': self.expected_completion,
            'create_time': str(self.create_time) if self.create_time else None,
            'qr_code': self.qr_code,
            'markdown_doc': self.markdown_doc
        }
    
    def __repr__(self):
        """字符串表示"""
        return f"<AppealRecord {self.case_number} - {self.person_name}>" 