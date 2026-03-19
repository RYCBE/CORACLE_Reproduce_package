import csv

def load_bug_version_dict(txt_file_path):
    """
    从txt文件加载bugissue和对应版本列表的字典（用第一个冒号分割）
    :param txt_file_path: txt文件路径
    :return: 格式为 {bugissue: [version1, version2,...]} 的字典
    """
    bug_version_dict = {}
    
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:  # 跳过空行
                continue
            # 按第一个冒号分割，得到bugissue和版本列表字符串
            parts = line.split(':', 1)
            if len(parts) != 2:
                continue  # 格式异常的行跳过
            
            bug_issue = parts[0].strip()  # 提取bugissue（如CXF-6137）
            versions_str = parts[1].strip().strip('[]')  # 去除前后的中括号
            
            # 处理版本列表：分割、去引号、去空格
            versions = []
            for v in versions_str.split(','):
                clean_v = v.strip().strip("'\"")  # 去除单/双引号和空格
                if clean_v:  # 跳过空字符串
                    versions.append(clean_v)
            
            bug_version_dict[bug_issue] = versions
    return bug_version_dict

def process_csv(csv_input_path, csv_output_path, bug_version_dict):
    """
    处理CSV文件，校验每行的bugissue和version，在末尾追加Yes/No，并保存新CSV
    :param csv_input_path: 原始CSV文件路径
    :param csv_output_path: 处理后的CSV输出路径
    :param bug_version_dict: bug和版本映射的字典
    """
    with open(csv_input_path, 'r', encoding='utf-8') as infile, \
         open(csv_output_path, 'w', encoding='utf-8', newline='') as outfile:
        
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)
        
        for row_num, row in enumerate(csv_reader, 1):
            if len(row) < 5:  # 确保行有足够列数（至少包含bugissue和version）
                print(f"第{row_num}行数据不完整，直接追加No并保存")
                row.append("No")
                csv_writer.writerow(row)
                continue
            
            # 提取关键信息：第2列是bugissue，第5列是version
            bug_issue = row[1].strip()
            raw_version = row[4].strip()
            # 统一版本格式（CSV里是2.0-M1 → txt里是cxf-2.0-m1这类格式）
            normalized_version = f"cxf-{raw_version.lower()}"
            
            # 核心校验逻辑
            if bug_issue in bug_version_dict:
                if normalized_version in bug_version_dict[bug_issue]:
                    row.append("Yes")
                else:
                    row.append("No")
            else:
                row.append("No")
            
            # 写入处理后的行
            csv_writer.writerow(row)
            # 打印每行处理结果（可选，便于调试）
            # print(f"第{row_num}行: {bug_issue} | {raw_version} → {normalized_version} → {row[-1]}")

if __name__ == "__main__":
    # ========== 请修改为你的实际文件路径 ==========
    TXT_FILE = "./1/issue_pred_map.txt"       # 你的txt文件路径
    CSV_INPUT_FILE = "./Van_data/CXFVRes.csv"     # 原始CSV文件路径
    CSV_OUTPUT_FILE = "./Van_data_2026/CXFVRes.csv"  # 处理后的CSV输出路径
    
    # 1. 加载bug-版本字典
    print("正在加载bug版本字典...")
    bug_version_dict = load_bug_version_dict(TXT_FILE)
    print(f"成功加载 {len(bug_version_dict)} 个bugissue的版本映射")
    
    # 2. 处理CSV文件并输出结果
    print("\n开始处理CSV文件...")
    process_csv(CSV_INPUT_FILE, CSV_OUTPUT_FILE, bug_version_dict)
    print(f"\n处理完成！结果已保存至: {CSV_OUTPUT_FILE}")