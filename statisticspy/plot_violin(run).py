import matplotlib.pyplot as plt
import json
import os
import numpy as np
from matplotlib.ticker import FormatStrFormatter


# 从文件读取数据的函数（如果有实际文件）
def read_data_from_files(folder_path):
    projects = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r') as f:
                data = json.load(f)
                projects.append(data)
    return projects

# 绘制小提琴图


def plot_violinplot(projects):
    # 提取每个项目的ratio数据
    all_ratios = []
    project_names = []

    for i, project in enumerate(projects):
        ratios = [commit_ratio['ratio']
                  for commit_ratio in project['commit_ratios']]
        all_ratios.append(ratios)
        project_names.append(project["project"])

    # 设置图片清晰度
    plt.rcParams['figure.dpi'] = 200

    # 计算小提琴图位置，缩短间距
    positions = range(1, len(all_ratios) + 1)
    spacing = 0.7  # 小提琴图之间的间距
    new_positions = [pos * spacing for pos in positions]

    # 创建小提琴图，通过width参数调整宽度
    fig, ax = plt.subplots(figsize=(12, 6))
    violin_parts = ax.violinplot(all_ratios, positions=new_positions,
                                 widths=0.5, showmeans=False, showmedians=True, showextrema=True)

    # 设置小提琴图的样式
    for i, pc in enumerate(violin_parts['bodies']):
        pc.set_facecolor('#66b3ff')
        pc.set_edgecolor('black')
        pc.set_linewidth(1)
        pc.set_alpha(0.7)

    # 设置中位数线的样式
    violin_parts['cmedians'].set_color('black')
    violin_parts['cmedians'].set_linewidth(1.5)

    # 设置四分位数范围的样式
    violin_parts['cbars'].set_color('black')
    violin_parts['cbars'].set_linewidth(1)

    # 设置最小值和最大值的样式
    violin_parts['cmins'].set_color('black')
    violin_parts['cmins'].set_linewidth(1)
    violin_parts['cmaxes'].set_color('black')
    violin_parts['cmaxes'].set_linewidth(1)

    plt.setp(ax.get_yticklabels(), fontsize=18.5)  # 左侧Y轴
    # 添加标题和标签
    ax.set_title('Violin Plot of Addition-to-Diff Ratio per BFC Across Projects',
                 fontsize=18.5, color='black', fontweight='bold')
    ax.set_xticks(new_positions)  # 设置x轴刻度位置
    ax.set_xticklabels(project_names, rotation=45, ha='center', fontsize=18.5)

    # 设置y轴格式为百分比
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    # 添加网格线
    ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

    # 调整x轴范围，消除左右空白
    if new_positions:
        x_min = min(new_positions) - spacing * 0.5
        x_max = max(new_positions) + spacing * 0.5
        ax.set_xlim(x_min, x_max)

    # 调整布局
    plt.tight_layout()

    # 显示图形
    # plt.show()

    # 保存图形（可选）
    plt.savefig('violin_plot_bfc_ratios.png', dpi=300, bbox_inches='tight')

# 主函数


def main():
    folder_path = "./statisticspy/bugFixFiles/"
    projects = read_data_from_files(folder_path)

    # 绘制小提琴图
    plot_violinplot(projects)


if __name__ == "__main__":
    main()
