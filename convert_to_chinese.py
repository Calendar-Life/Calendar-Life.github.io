#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量将HTML文件转换为中文版本的脚本
"""

import os
import re
from pathlib import Path

# 英文到中文的映射字典
translations = {
    # 页面标题和导航
    'App Website Template': '应用网站模板',
    'Home': '首页',
    'Home Wave1': '首页波浪1',
    'Home Wave2': '首页波浪2',
    'Home Curve': '首页曲线',
    'Home Curve1': '首页曲线1',
    'Home Curve2': '首页曲线2',
    'Home Curve3': '首页曲线3',
    'Home Curve4': '首页曲线4',
    'Home Default': '首页默认',
    'Home Gradient': '首页渐变',
    'Home Particle': '首页粒子',
    'Home Clip': '首页剪辑',
    'Pages': '页面',
    'About Us': '关于我们',
    'Feature': '功能',
    'Screenshot': '截图',
    'Team': '团队',
    'Pricing': '价格',
    '404 Error': '404错误',
    'Contact Us': '联系我们',
    'Contact': '联系',
    'Blog': '博客',
    'Blog Grid List': '博客网格列表',
    'Blog details': '博客详情',
    
    # 主要内容
    'Our Best Provide To Service our App': '我们为您的应用提供最佳服务',
    'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do elit eiusmod tempor incididunt dolore.': '我们致力于为您提供最优质的应用开发服务，让您的想法变成现实。',
    'Discove More': '了解更多',
    'Amazing Feature': '令人惊叹的功能',
    'Lorem elementum Sed congue nisl dolorSed congue nisl dolor Lorem elementum Sed congue nisl dolor Sed.': '我们提供最先进的技术和创新的解决方案，让您的应用脱颖而出。',
    'Notification view': '通知视图',
    'Lorem ipsum dolor sit amet elit sed eiusmod tempor.': '智能通知系统，让用户及时了解重要信息。',
    'Secure Data': '数据安全',
    'Creative Design': '创意设计',
    'Life Time Service': '终身服务',
    'Cloud Storage': '云存储',
    'Pixel Perfect': '像素完美',
    'How It Works': '如何使用',
    'App Screenshot': '应用截图',
    'Client Review': '客户评价',
    'Choose Your Plan': '选择您的套餐',
    'Our Best App': '我们的最佳应用',
    'Meet Our Team': '认识我们的团队',
    'Get In Touch': '联系我们',
    'Stay Connected with us': '与我们保持联系',
    'Subcribe to Newletter Now': '立即订阅我们的新闻通讯',
    
    # 表单标签
    'Your Name': '您的姓名',
    'Your Email': '您的邮箱',
    'Your Message': '您的留言',
    'Enter Name': '请输入姓名',
    'Enter Email': '请输入邮箱',
    'Enter Message': '请输入留言',
    'Send Message': '发送留言',
    'Submit Your Message!': '提交您的留言！',
    
    # 联系信息
    'Home Address': '公司地址',
    'Mobile Number': '联系电话',
    'Email Address': '邮箱地址',
    '1 Grafton Street, Dublin, Ireland University.': '北京市朝阳区建国门外大街1号，国贸大厦。',
    '+135 773 321 4442': '+86 138 0013 8000',
    'demo@example.com': 'info@5gapps.com',
    
    # 页脚
    'Quick Links': '快速链接',
    'Support Links': '支持链接',
    'Follow Us': '关注我们',
    'Get Stared': '开始使用',
    'Our Team': '我们的团队',
    'About Us': '关于我们',
    'Need Helps': '需要帮助',
    'Our Faq': '常见问题',
    'Our Service': '我们的服务',
    'Protfolio': '作品集',
    'Apps Download': '应用下载',
    'Our News': '我们的新闻',
    
    # 价格套餐
    'Free': '免费版',
    'Basic': '基础版',
    'Premium': '高级版',
    'Buy Now': '立即购买',
    '1 GB Disk Space': '1 GB 存储空间',
    '500 MB Bandwidth': '500 MB 带宽',
    '3 Sub Domain': '3 个子域名',
    '5 Email Account': '5 个邮箱账户',
    '24/7 Support': '24/7 支持',
    'Help center access': '帮助中心访问',
    
    # 客户评价
    'Ar-Rahman': '张明',
    'Al-Azim': '李强',
    'Ar-Raqib': '王芳',
    'App Desinger': '应用设计师',
    'CEO': '首席执行官',
    'Markating': '市场营销',
    
    # 其他
    'portfolio': '应用展示',
    'shape image': '装饰图形',
    'rafi App': '5gapps 应用',
    'Copyright - All Right Reserved.': '版权所有 - 保留所有权利。',
    'For Google Play': '适用于Google Play',
    'For Windows': '适用于Windows',
    'Get in': '在',
    'Your Email': '您的邮箱',
    
    # 补充的英文到中文映射
    'Wave1': '波浪1',
    'Wave2': '波浪2',
    'Curve1': '曲线1',
    'Curve2': '曲线2',
    'Curve3': '曲线3',
    'Curve4': '曲线4',
    'Default': '默认',
    'Gradient': '渐变',
    'Particle': '粒子',
    'Clip': '剪辑',
    
    # Lorem ipsum 占位符文本
    'Lorem ipsum dolor sit amet elit , consectetur adipiscing , sed eiusmod tempor sit amet elit dolor sit amet elit.': '我们提供多种灵活的套餐选择，满足不同规模和需求的企业和个人用户。',
    'Lorem ipsum available but the majority have or  suffered alteration in some form, by injected humour.': '这款应用的设计非常出色，用户体验流畅，功能强大。我们团队的工作效率得到了显著提升。',
    'Lorem ipsum dolor sit amet elit , consectetur adipiscing , sed eiusmod tempor sit amet elit dolor sit amet elit Lorem ipsum dolor sit amet elit , consectetur adipiscing , sed eiusmod tempor sit amet elit dolor sit amet elit.': '立即下载我们的应用，体验前所未有的便捷和高效。支持Android和iOS平台，随时随地享受优质服务。',
    'Lorem elementum Sed congue nisl dolorSed congue nisl dolor Lorem elementum Sed congue nisl dolor Sed Lorem elementum Sed congue nisl dolorSed congue nisl dolor Lorem elementum Sed congue nisl dolor Sed Lorem elementum Sed.': '我们提供详细的使用教程和24/7客户支持，确保您在使用过程中遇到任何问题都能得到及时帮助。',
    'Lorem elementum Sed congue nisl dolorSed congue nisl dolor Lorem elementum Sed congue nisl dolor Sed Lorem elementum Sed congue nisl dolorSed congue nisl dolor Lorem elementum Sed.': '我们的应用设计简单易用，让您轻松上手。通过直观的界面和智能化的功能，您可以快速掌握所有操作。',
    'Lorem ipsum dolor sit amet elit , consectetur adipiscing , sed eiusmod tempor sit amet elit dolor sit amet elit.': '听听我们客户的真实反馈，了解他们对我们产品和服务的评价。',
    'Sed congue nisl dolorSed congue nisl dolor, id dapibus leo elementum posuere.Sed congue nisl dolorSed congue nisl dolor, id dapibus leo. Sed congue nisl dolorSed congue nisl.': '我们致力于为用户提供最优质的应用体验，通过创新的技术和贴心的服务，让您的数字生活更加便捷高效。',
    'Sed congue nisl dolorSed congue nisl dolor, id dapibus leo elementum posuere.': '关注我们的社交媒体，获取最新的产品更新、技术资讯和行业动态。',
    'Laoet elementum Sed congue nisl dolorSed congue nisl dolor dapibus leo elementum posuere Ut aliquam metus quis.': '我们随时准备为您提供帮助和支持，欢迎通过以下方式联系我们。',
    'Browse our app screenshots to experience smooth user interactions and beautiful visual design.': '浏览我们应用的精彩界面，体验流畅的用户交互和精美的视觉设计。',
    'We have a team of experienced and skilled professionals dedicated to providing you with the highest quality products and services.': '我们拥有一支经验丰富、技术精湛的专业团队，致力于为您提供最优质的产品和服务。',
    'We have the best FAQ to provide you with comprehensive help and answers.': '我们拥有最佳FAQ，为您提供最全面的帮助和解答。',
    'We provide the most advanced technology and innovative solutions to make your app stand out.': '我们提供最先进的技术和创新的解决方案，让您的应用脱颖而出。',
}

def convert_html_file(file_path):
    """转换单个HTML文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修改语言属性
        content = re.sub(r'<html lang="en">', '<html lang="zh-CN">', content)
        
        # 替换英文文本
        for english, chinese in translations.items():
            content = content.replace(english, chinese)
        
        # 替换价格（美元到人民币）
        content = re.sub(r'\$(\d+\.?\d*)', lambda m: f'¥{int(float(m.group(1)) * 6.4)}', content)
        
        # 替换alt属性中的英文
        content = re.sub(r'alt="portfolio"', 'alt="应用展示"', content)
        content = re.sub(r'alt="shape image"', 'alt="装饰图形"', content)
        content = re.sub(r'alt=""', 'alt="图片"', content)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已转换: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败 {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始批量转换HTML文件为中文版本...")
    
    # 获取当前目录下的所有HTML文件
    html_files = list(Path('.').glob('*.html'))
    
    if not html_files:
        print("❌ 未找到HTML文件")
        return
    
    print(f"📁 找到 {len(html_files)} 个HTML文件")
    
    success_count = 0
    for html_file in html_files:
        if convert_html_file(html_file):
            success_count += 1
    
    print(f"\n🎉 转换完成！成功转换 {success_count}/{len(html_files)} 个文件")
    print("✨ 所有HTML文件已成功转换为中文版本")

if __name__ == "__main__":
    main()
