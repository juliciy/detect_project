import os


def collect_py_code(output_file='project_all_code.txt'):
    # 获取当前工作目录
    root_dir = os.getcwd()

    # 定义要排除的目录（可选）
    exclude_dirs = {'venv', '__pycache__', '.git'}

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 遍历目录树
        for root, dirs, files in os.walk(root_dir):
            # 跳过排除目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, root_dir)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            # 写入文件头
                            outfile.write(f"\n\n{'=' * 40}\n")
                            outfile.write(f"# File: {relative_path}\n")
                            outfile.write(f"{'=' * 40}\n\n")

                            # 写入文件内容
                            outfile.write(infile.read())

                            print(f"Processed: {relative_path}")

                    except Exception as e:
                        print(f"Error reading {relative_path}: {str(e)}")
                        continue


if __name__ == '__main__':
    collect_py_code()
    print("\nAll Python files have been collected to project_all_code.txt")
