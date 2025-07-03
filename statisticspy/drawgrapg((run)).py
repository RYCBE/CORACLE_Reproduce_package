import matplotlib.pyplot as plt
import json
import numpy as np
from matplotlib.ticker import PercentFormatter
from matplotlib.lines import Line2D

# 项目列表
Pro_list = [
    'CAMEL',
    'CXF',
    'IGNITE',
    'JCR',
    'KARAF',
    'MNG',
    'MYFACES',
    'OPENMEETINGS',
    'PDFBOX',
    'WICKET',
]

pro_list = ["camel",
            "cxf",
            "ignite",
            "jackrabbit",
            "karaf",
            "maven",
            "myfaces",
            "openmeetings",
            "pdfbox",
            "wicket"]

# 项目名称映射
P2p = {}
for i in range(len(pro_list)):
    P2p[Pro_list[i]] = pro_list[i]

# 数据准备
datas = []
for pro in Pro_list:
    with open(f'./statisticspy/JiraIssueInfo1simple/{pro}JiraIssueInfo.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        datas.append(data)

# 计算others值
for data in datas:
    data["others"] = data["all_issue"] - \
        data["no_AV_issue"] - data["inconsistent_AV_issue"]

# 提取数据
projects = [data["project"] for data in datas]
no_av_issues = [data["no_AV_issue"] for data in datas]
inconsistent_av_issues = [data["inconsistent_AV_issue"] for data in datas]
others = [data["others"] for data in datas]
all_issues = [data["all_issue"] for data in datas]
max_all_issue = max(all_issues)

# 设置图形参数
fig, ax1 = plt.subplots(figsize=(14, 10))  # 增加图形宽度以容纳更多项目
bar_width = 0.6
index = np.arange(len(projects))

# 计算每个项目的两个比例值
# no_AV_issue占比
ratios1 = [na / ai for na, ai in zip(no_av_issues, all_issues)]
# inconsistent_AV_issue占比
ratios2 = [ia / ai for ia, ai in zip(inconsistent_av_issues, all_issues)]


# 定义颜色
colors = ['#5DA5DA', '#FAA43A', '#60BD68']  # 蓝色、橙色、绿色

# 绘制柱状图
plt.bar(index, others, bar_width, label='Others', color=colors[2])
plt.bar(index, inconsistent_av_issues, bar_width, bottom=others,
        label='Inconsistent AV Issue', color=colors[1])
plt.bar(index, no_av_issues, bar_width, bottom=[a+b for a, b in zip(others, inconsistent_av_issues)],
        label='No AV Issue', color=colors[0])

# 创建右侧y轴（百分比）
ax2 = ax1.twinx()

# 设置右侧y轴为百分比格式，范围0-100%
ax2.set_ylim(0, 100)  # 直接设置为百分比范围
ax2.yaxis.set_major_formatter(PercentFormatter())  # 不指定xmax参数
ax2.set_ylabel('Percentage of Total Issues', fontsize=18.5, color='black')

# 设置右侧y轴刻度为0, 20, 40, 60, 80, 100
ax2.set_yticks(np.linspace(0, 100, 6))

# 设置左侧y轴范围，使其最高点与右侧100%对齐
ax1.set_ylim(0, 5000)  # 左侧y轴最高点设置为总问题数的最大值

# 关闭右侧y轴的网格线
ax2.grid(False)

# 定义绘图函数


def plot_ratio_points_and_lines(ratios, all_issues, color_idx, label_offset, label_text):
    """
    绘制比例点和连接线

    参数:
    ratios: 比例值列表
    all_issues: 总问题数列表
    color_idx: 颜色索引
    label_offset: 标签垂直偏移量
    label_text: 图例文本
    """
    x_positions = []
    y_positions = []

    for i, (ratio, ai) in enumerate(zip(ratios, all_issues)):
        # 计算百分比值（范围0-100）
        percent_value = ratio * 100

        # 记录位置数据
        x_positions.append(i)
        y_positions.append(percent_value)

        # 添加圆形点
        plt.scatter(i, percent_value, s=50,
                    color=colors[color_idx], marker='o', edgecolors='black')

        # 添加百分比标签
        plt.text(i, percent_value + label_offset, f'{percent_value:.1f}%',
                 ha='center', fontsize=18.5, color='black', fontweight='bold')

    # 连接所有点（虚线）
    line, = plt.plot(x_positions, y_positions,
                     color=colors[color_idx], linestyle='--', linewidth=2, alpha=0.7, label=label_text)

    return line  # 返回线条对象用于创建图例


# 绘制比例点和连线，并获取线条对象
line1 = plot_ratio_points_and_lines(
    ratios1, all_issues, 0, 1, 'No AV Issue Ratio')
line2 = plot_ratio_points_and_lines(
    ratios2, all_issues, 1, 1, 'Inconsistent AV Issue Ratio')

# 创建自定义图例
legend_elements = [
    # 柱状图图例
    Line2D([0], [0], marker='s', color='w', label='No AV Issue',
           markerfacecolor=colors[0], markersize=10),
    Line2D([0], [0], marker='s', color='w', label='Inconsistent AV Issue',
           markerfacecolor=colors[1], markersize=10),
    Line2D([0], [0], marker='s', color='w', label='Others',
           markerfacecolor=colors[2], markersize=10),

    # 比例线图例
    Line2D([0], [0], color=colors[0], linestyle='--',
           lw=2, label='No AV Issue Ratio'),
    Line2D([0], [0], color=colors[1], linestyle='--',
           lw=2, label='Inconsistent AV Issue Ratio'),

    # 比例点图例
    Line2D([0], [0], marker='o', color='w', label='Ratio Points',
           markerfacecolor='none', markeredgecolor='black', markersize=6)
]

# 添加标签和标题
plt.xlabel('Project', fontsize=18.5)
ax1.set_ylabel('Issue Count', fontsize=18.5, color='black')
plt.title('The proportion of issues containing unavailable AV information',
          fontsize=18.5, fontweight='bold')

# 设置x轴标签旋转角度，避免重叠
# 使用面向对象的方式设置X轴标签
ax1.set_xticks(index)
ax1.set_xticklabels(projects, fontsize=18.5, rotation=45, ha='center')

# 调整Y轴刻度字体大小
plt.setp(ax1.get_yticklabels(), fontsize=18.5)  # 左侧Y轴
plt.setp(ax2.get_yticklabels(), fontsize=18.5)  # 右侧Y轴


# 添加图例
plt.legend(handles=legend_elements, loc='upper right', fontsize=18.5)

# 添加网格线（仅左侧y轴）
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# 调整布局
plt.tight_layout()

# # 显示图形
# plt.show()

# 保存图形（可选）
plt.savefig('inaccessibleAVRatio.png', dpi=300, bbox_inches='tight')
