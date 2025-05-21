-- 矛盾调解身份验证服务数据库初始化脚本

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    contact_info VARCHAR(20) NOT NULL COMMENT '联系方式',
    id_card_number VARCHAR(18) NOT NULL COMMENT '身份证号',
    address VARCHAR(255) DEFAULT '' COMMENT '联系地址',
    verified BOOLEAN DEFAULT FALSE COMMENT '是否已验证',
    verification_result TEXT COMMENT '验证结果',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT='用户身份信息表';

-- 创建验证记录表
CREATE TABLE IF NOT EXISTS verification_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID',
    request_data TEXT COMMENT '请求数据',
    response_data TEXT COMMENT '响应数据',
    status VARCHAR(20) COMMENT '验证状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) COMMENT='身份验证日志表';

-- 创建历史受理单记录表
CREATE TABLE IF NOT EXISTS appeal_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_number VARCHAR(50) NOT NULL COMMENT '受理编号',
    person_name VARCHAR(50) NOT NULL COMMENT '姓名',
    contact_info VARCHAR(20) DEFAULT NULL COMMENT '联系方式',
    gender VARCHAR(10) DEFAULT NULL COMMENT '性别',
    id_card_number VARCHAR(20) DEFAULT NULL COMMENT '身份证号',
    address VARCHAR(255) DEFAULT NULL COMMENT '地址',
    incident_time VARCHAR(50) DEFAULT NULL COMMENT '事件时间',
    incident_location VARCHAR(255) DEFAULT NULL COMMENT '事件地点',
    incident_description TEXT COMMENT '事件描述',
    people_involved VARCHAR(10) DEFAULT NULL COMMENT '涉及人数',
    submitted_materials TEXT COMMENT '提交材料',
    handling_department VARCHAR(50) DEFAULT NULL COMMENT '处理部门',
    handling_status VARCHAR(20) DEFAULT NULL COMMENT '处理状态',
    expected_completion VARCHAR(50) DEFAULT NULL COMMENT '预计完成时间',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    qr_code VARCHAR(255) DEFAULT NULL COMMENT '二维码URL或数据',
    markdown_doc TEXT COMMENT 'Markdown格式文档'
) COMMENT='历史受理单记录表';

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_id_card_number ON users(id_card_number);
CREATE INDEX IF NOT EXISTS idx_appeal_id_card_number ON appeal_records(id_card_number);
CREATE INDEX IF NOT EXISTS idx_appeal_case_number ON appeal_records(case_number);
CREATE INDEX IF NOT EXISTS idx_appeal_contact_info ON appeal_records(contact_info); 