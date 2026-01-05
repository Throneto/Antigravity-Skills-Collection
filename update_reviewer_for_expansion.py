#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新审核器 - 为新类别添加权重
为 smart_reviewer.py 的新类别添加重要性权重
"""

import shutil
from datetime import datetime

def update_reviewer():
    """更新smart_reviewer.py以支持新类别权重"""

    reviewer_path = "smart_reviewer.py"

    print("="*70)
    print("  🔄 更新审核器 - 添加新类别权重")
    print("="*70 + "\n")

    # 备份原文件
    backup_path = f"smart_reviewer_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    shutil.copy2(reviewer_path, backup_path)
    print(f"📦 备份已创建: {backup_path}\n")

    # 读取现有文件
    with open(reviewer_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经更新过
    if "'poses':" in content and "'expressions':" in content:
        print("⚠️  审核器似乎已经包含新类别权重")
        print("   如需重新更新，请手动修改\n")
        return

    print("🔍 添加新类别的重要性权重...\n")

    # 找到category_importance字典
    importance_start = content.find('self.category_importance = {')

    if importance_start != -1:
        # 找到字典的结束
        dict_end = content.find('}', importance_start)

        # 在结束前添加新的权重
        new_weights = """,
            'poses': 0.9,              # 姿势对人像很重要
            'expressions': 1.0,        # 表情是人像核心要素
            'clothing_styles': 0.75    # 服装风格中等重要"""

        updated_content = content[:dict_end] + new_weights + '\n        ' + content[dict_end:]

        print("✅ 已添加类别重要性权重:")
        print("   • poses: 0.9 (高重要性)")
        print("   • expressions: 1.0 (最高重要性)")
        print("   • clothing_styles: 0.75 (中等重要性)\n")

        # 保存更新后的文件
        with open(reviewer_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print("="*70)
        print("  ✅ 审核器更新完成！")
        print("="*70)
        print("\n📝 更新摘要:")
        print("   ✅ 为3个新类别添加了重要性权重")
        print("   ✅ 审核器现在可以正确评估新类别特征")
        print(f"\n📦 备份文件: {backup_path}")
        print("\n💡 权重说明:")
        print("   • 1.0 = 最高重要性（expressions, eye_types...）")
        print("   • 0.9 = 高重要性（poses, skin_tones...）")
        print("   • 0.7-0.8 = 中等重要性（clothing_styles, accessories...）")
        print("\n🎉 现在可以测试完整的扩展功能了！")
        print("   运行: python3 test_scan_new_prompt.py\n")

    else:
        print("❌ 未找到category_importance字典，请手动添加")
        print("\n请在SmartReviewer.__init__方法中添加：")
        print("   'poses': 0.9,")
        print("   'expressions': 1.0,")
        print("   'clothing_styles': 0.75\n")


if __name__ == "__main__":
    update_reviewer()
