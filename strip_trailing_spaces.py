#!/usr/bin/env python3
"""
strip_trailing_spaces.py
递归扫描目录，删除指定文本文件行尾的空格和制表符。
支持: .java, .gradle, .toml, .yml, .yaml, .properties, .json, .mcmeta
用法: python strip_trailing_spaces.py [目录路径] [--dry-run]
"""

import os
import sys
import argparse

# 处理的文件扩展名（白名单）
TARGET_EXTS = {
    '.java', '.gradle', '.toml', '.yml', '.yaml',
    '.properties', '.json', '.mcmeta', '.gitignore',
}

# 默认跳过的目录
DEFAULT_SKIP_DIRS = {
    '.git', '.svn', '.hg',
    'node_modules', '.venv', 'venv',
    '__pycache__', '.pytest_cache',
    '.gradle', 'build', 'out',
    '.idea', '.vscode',
    'target', 'dist',
    '.loom-cache', 'run',
}


def should_process(filepath):
    """判断文件扩展名是否在目标列表中"""
    _, ext = os.path.splitext(filepath)
    return ext.lower() in TARGET_EXTS


def strip_file(filepath, dry_run=False):
    """处理单个文件，返回 (是否修改, 处理的行数)"""
    try:
        with open(filepath, 'rb') as f:
            raw_lines = f.readlines()
    except (OSError, IOError):
        return False, 0

    new_lines = []
    modified = False
    stripped_lines = 0

    for line in raw_lines:
        if line.endswith(b'\r\n'):
            core = line[:-2]
            newline = b'\r\n'
        elif line.endswith(b'\n'):
            core = line[:-1]
            newline = b'\n'
        elif line.endswith(b'\r'):
            core = line[:-1]
            newline = b'\r'
        else:
            core = line
            newline = b''

        stripped = core.rstrip(b' \t')
        if stripped != core:
            stripped_lines += 1
            modified = True
        new_lines.append(stripped + newline)

    if modified:
        if not dry_run:
            with open(filepath, 'wb') as f:
                f.writelines(new_lines)
        return True, stripped_lines
    return False, 0


def walk_and_strip(root_dir, skip_dirs, dry_run=False):
    total_files = 0
    modified_files = 0
    total_stripped_lines = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not should_process(filepath):
                continue

            total_files += 1
            modified, lines = strip_file(filepath, dry_run=dry_run)
            if modified:
                modified_files += 1
                total_stripped_lines += lines
                action = "[DRY-RUN] 发现" if dry_run else "已处理"
                print(f"{action}: {filepath} ({lines} 行)")

    return total_files, modified_files, total_stripped_lines


def main():
    parser = argparse.ArgumentParser(
        description="递归删除目录下 Java/Gradle/TOML/YML/Properties/JSON/MCMeta 文件行尾的空格/制表符"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="要扫描的根目录（默认当前目录）"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅预览，不实际写入文件"
    )
    parser.add_argument(
        "--no-skip",
        action="store_true",
        help="不跳过 build/.git 等目录"
    )
    args = parser.parse_args()

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        print(f"错误: 不是有效目录: {root}")
        sys.exit(1)

    skip_dirs = set() if args.no_skip else DEFAULT_SKIP_DIRS

    print(f"扫描目录: {root}")
    print(f"目标类型: {', '.join(sorted(TARGET_EXTS))}")
    if args.dry_run:
        print("模式: 预览（不写入）")
    if args.no_skip:
        print("跳过目录: 无")
    print("-" * 50)

    total, modified, lines = walk_and_strip(root, skip_dirs, dry_run=args.dry_run)

    print("-" * 50)
    print(f"扫描文件数: {total}")
    print(f"涉及文件数: {modified}")
    print(f"清理行数:   {lines}")
    if args.dry_run and modified > 0:
        print("提示: 去掉 --dry-run 即可实际写入")


if __name__ == "__main__":
    main()
