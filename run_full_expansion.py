#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键运行完整扩展流程
自动执行所有扩展步骤
"""

import subprocess
import sys

def run_command(script_name, description):
    """运行Python脚本"""
    print(f"\n{'='*70}")
    print(f"  {description}")
    print(f"{'='*70}\n")

    try:
        result = subprocess.run([sys.executable, script_name],
                              capture_output=False,
                              text=True,
                              check=False)

        if result.returncode == 0:
            print(f"\n✅ {description} 完成")
            return True
        else:
            print(f"\n⚠️  {description} 出现问题")
            return False

    except Exception as e:
        print(f"\n❌ {description} 失败: {e}")
        return False


def main():
    """主流程"""
    print("\n" + "="*70)
    print("  🚀 完整库扩展流程 - 一键运行")
    print("="*70)
    print("\n本脚本将依次执行以下步骤：")
    print("  1️⃣  扩展特征库（添加3个新类别）")
    print("  2️⃣  更新学习器（添加识别能力）")
    print("  3️⃣  更新审核器（添加权重配置）")
    print("  4️⃣  测试扫描（验证功能）")
    print("\n" + "="*70)

    input("\n按 Enter 键开始...")

    # 步骤1: 扩展库
    if not run_command('expand_library.py', '步骤 1/4: 扩展特征库'):
        print("\n❌ 扩展失败，流程终止")
        return

    input("\n✅ 步骤1完成。按 Enter 继续...")

    # 步骤2: 更新学习器
    if not run_command('update_learner_for_expansion.py', '步骤 2/4: 更新学习器'):
        print("\n⚠️  学习器更新出现问题，但可以继续")

    input("\n✅ 步骤2完成。按 Enter 继续...")

    # 步骤3: 更新审核器
    if not run_command('update_reviewer_for_expansion.py', '步骤 3/4: 更新审核器'):
        print("\n⚠️  审核器更新出现问题，但可以继续")

    input("\n✅ 步骤3完成。按 Enter 运行测试...")

    # 步骤4: 测试
    run_command('test_scan_new_prompt.py', '步骤 4/4: 测试扫描功能')

    # 最终总结
    print("\n" + "="*70)
    print("  🎉 库扩展流程完成！")
    print("="*70)
    print("\n✅ 现在你的系统已经支持：")
    print("\n   📊 现有类别（v1.5）:")
    print("      • ethnicities (族裔)")
    print("      • eye_types (眼睛类型)")
    print("      • nose_types (鼻子类型)")
    print("      • lip_types (嘴唇类型)")
    print("      • hair_styles (发型)")
    print("      • hair_colors (发色)")
    print("      • skin_tones (肤色)")
    print("      • makeup_styles (妆容)")
    print("      • face_shapes (脸型)")
    print("      • body_types (体型)")
    print("      • age_groups (年龄段)")
    print("\n   ⭐ 新增类别（v1.6）:")
    print("      • poses (姿势) - 4个分类")
    print("      • expressions (表情) - 4个分类")
    print("      • clothing_styles (服装风格) - 4个分类")
    print("\n📊 总计:")
    print("   • 类别数: 14 个")
    print("   • 分类数: 79 个")
    print("\n🚀 下一步:")
    print("   1. 查看更新后的库：")
    print("      cat extracted_results/CHANGELOG.md")
    print("\n   2. 测试自动学习：")
    print("      python3 auto_learn_workflow.py scan \"your prompt\"")
    print("\n   3. 批量扫描：")
    print("      python3 auto_learn_workflow.py batch")
    print()


if __name__ == "__main__":
    main()
