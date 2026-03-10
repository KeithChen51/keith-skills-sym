#!/usr/bin/env python3
"""
MBA/EMBA 论文研究方法顾问 - 动态论文检索脚本

通过 OpenAlex API（免费、无限流）为学生提供：
1. 延伸阅读推荐（某理论在某行业的近年高引用研究）
2. 论文元数据查询（通过 OpenAlex ID 获取最新引用量和开放获取信息）
3. 引用格式生成（GB/T 7714 和 APA 格式）

用法:
  python fetch_papers.py search <理论关键词> [行业关键词] [--years N]
  python fetch_papers.py enrich <openalex_id>
  python fetch_papers.py cite <openalex_id>

示例:
  python fetch_papers.py search "Porter five forces" "manufacturing"
  python fetch_papers.py search "technology acceptance model" "healthcare" --years 3
  python fetch_papers.py enrich W2123377363
  python fetch_papers.py cite W2123377363
"""

import sys
import json
import argparse

try:
    import requests
except ImportError:
    print("错误: 需要安装 requests 库。请运行: pip install requests")
    sys.exit(1)

BASE_URL = "https://api.openalex.org"
MAILTO = "mba-thesis-advisor@manus.im"  # polite pool identifier


def search_recent_papers(theory_keyword, industry_keyword=None, years=5, limit=5):
    """搜索某理论（在某行业）的近年高引用研究论文"""
    query = theory_keyword
    if industry_keyword:
        query = f"{theory_keyword} {industry_keyword}"

    from_year = 2026 - years

    params = {
        "search": query,
        "filter": f"publication_year:>{from_year},type:article",
        "sort": "cited_by_count:desc",
        "per_page": limit,
        "mailto": MAILTO,
    }

    try:
        resp = requests.get(f"{BASE_URL}/works", params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"API 请求失败: {e}")
        return

    results = data.get("results", [])
    if not results:
        print("未找到相关论文。请尝试调整关键词或扩大搜索年限。")
        return

    industry_label = f" × {industry_keyword}" if industry_keyword else ""
    print(f"\n延伸阅读推荐（{theory_keyword}{industry_label}，近{years}年高引用）\n")
    print("-" * 70)

    for i, work in enumerate(results, 1):
        title = work.get("title", "N/A")
        year = work.get("publication_year", "N/A")
        cited = work.get("cited_by_count", 0)
        doi = work.get("doi", "")

        # 作者
        authorships = work.get("authorships", [])
        if len(authorships) == 1:
            author_str = authorships[0].get("author", {}).get("display_name", "Unknown")
        elif len(authorships) == 2:
            names = [a.get("author", {}).get("display_name", "") for a in authorships]
            author_str = " & ".join(names)
        elif len(authorships) > 2:
            first = authorships[0].get("author", {}).get("display_name", "Unknown")
            author_str = f"{first} et al."
        else:
            author_str = "Unknown"

        # 期刊
        loc = work.get("primary_location", {}) or {}
        source = loc.get("source", {}) or {}
        journal = source.get("display_name", "N/A")

        # 开放获取
        oa = work.get("open_access", {}) or {}
        is_oa = oa.get("is_oa", False)
        oa_url = oa.get("oa_url", "")

        print(f"[{i}] {title}")
        print(f"    作者: {author_str} ({year})")
        print(f"    期刊: {journal}")
        print(f"    引用量: {cited:,}")
        if doi:
            print(f"    DOI: {doi}")
        print(f"    开放获取: {'是' if is_oa else '否'}", end="")
        if is_oa and oa_url:
            print(f" | 链接: {oa_url}")
        else:
            print()
        print()


def enrich_paper(openalex_id):
    """通过 OpenAlex ID 或 DOI 获取论文的最新元数据"""
    # 支持多种输入格式
    if openalex_id.startswith("10."):
        url = f"{BASE_URL}/works/doi:{openalex_id}"
    elif openalex_id.startswith("https://openalex.org/"):
        url = f"{BASE_URL}/works/{openalex_id.split('/')[-1]}"
    else:
        if not openalex_id.startswith("W"):
            openalex_id = f"W{openalex_id}"
        url = f"{BASE_URL}/works/{openalex_id}"
    params = {"mailto": MAILTO}

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        work = resp.json()
    except Exception as e:
        print(f"API 请求失败: {e}")
        return

    title = work.get("title", "N/A")
    year = work.get("publication_year", "N/A")
    cited = work.get("cited_by_count", 0)
    doi = work.get("doi", "")

    authorships = work.get("authorships", [])
    authors = [a.get("author", {}).get("display_name", "") for a in authorships[:5]]
    if len(authorships) > 5:
        authors.append(f"等{len(authorships)}人")

    loc = work.get("primary_location", {}) or {}
    source = loc.get("source", {}) or {}
    journal = source.get("display_name", "N/A")

    oa = work.get("open_access", {}) or {}
    is_oa = oa.get("is_oa", False)
    oa_url = oa.get("oa_url", "")

    print(f"\n论文详情")
    print("=" * 60)
    print(f"标题: {title}")
    print(f"作者: {', '.join(authors)}")
    print(f"年份: {year}")
    print(f"期刊/出版物: {journal}")
    print(f"引用量: {cited:,}")
    if doi:
        print(f"DOI: {doi}")
    print(f"开放获取: {'是' if is_oa else '否'}")
    if is_oa and oa_url:
        print(f"全文链接: {oa_url}")
    print()


def generate_citation(openalex_id):
    """通过 OpenAlex ID 或 DOI 生成 GB/T 7714 和 APA 引用格式"""
    # 支持多种输入格式
    if openalex_id.startswith("10."):
        url = f"{BASE_URL}/works/doi:{openalex_id}"
    elif openalex_id.startswith("https://openalex.org/"):
        url = f"{BASE_URL}/works/{openalex_id.split('/')[-1]}"
    else:
        if not openalex_id.startswith("W"):
            openalex_id = f"W{openalex_id}"
        url = f"{BASE_URL}/works/{openalex_id}"
    params = {"mailto": MAILTO}

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        work = resp.json()
    except Exception as e:
        print(f"API 请求失败: {e}")
        return

    title = work.get("title", "N/A")
    year = work.get("publication_year", "N/A")

    authorships = work.get("authorships", [])
    authors_last_first = []
    authors_first_last = []
    for a in authorships:
        name = a.get("author", {}).get("display_name", "")
        if name:
            parts = name.split()
            if len(parts) >= 2:
                last = parts[-1]
                first = " ".join(parts[:-1])
                authors_last_first.append(f"{last.upper()} {first[0]}")
                authors_first_last.append(f"{last}, {first[0]}.")
            else:
                authors_last_first.append(name.upper())
                authors_first_last.append(name)

    loc = work.get("primary_location", {}) or {}
    source = loc.get("source", {}) or {}
    journal = source.get("display_name", "N/A")
    work_type = work.get("type", "article")

    biblio = work.get("biblio", {}) or {}
    volume = biblio.get("volume", "")
    issue = biblio.get("issue", "")
    first_page = biblio.get("first_page", "")
    last_page = biblio.get("last_page", "")

    pages = ""
    if first_page and last_page:
        pages = f"{first_page}-{last_page}"
    elif first_page:
        pages = first_page

    # GB/T 7714 格式
    gbt_authors = ", ".join(authors_last_first[:3])
    if len(authors_last_first) > 3:
        gbt_authors += ", 等"

    if work_type in ["book", "monograph"]:
        gbt = f"{gbt_authors}. {title}[M]. {journal}, {year}."
    else:
        vol_info = ""
        if volume:
            vol_info = f", {volume}"
            if issue:
                vol_info += f"({issue})"
        if pages:
            vol_info += f": {pages}"
        gbt = f"{gbt_authors}. {title}[J]. {journal}, {year}{vol_info}."

    # APA 格式
    apa_authors = []
    for a in authorships[:6]:
        name = a.get("author", {}).get("display_name", "")
        parts = name.split()
        if len(parts) >= 2:
            last = parts[-1]
            initials = " ".join([p[0] + "." for p in parts[:-1]])
            apa_authors.append(f"{last}, {initials}")
        else:
            apa_authors.append(name)

    if len(authorships) > 6:
        apa_author_str = ", ".join(apa_authors[:6]) + ", ... " + apa_authors[-1]
    elif len(apa_authors) == 1:
        apa_author_str = apa_authors[0]
    elif len(apa_authors) == 2:
        apa_author_str = " & ".join(apa_authors)
    else:
        apa_author_str = ", ".join(apa_authors[:-1]) + ", & " + apa_authors[-1]

    if work_type in ["book", "monograph"]:
        apa = f"{apa_author_str} ({year}). *{title}*. {journal}."
    else:
        vol_str = ""
        if volume:
            vol_str = f"*{volume}*"
            if issue:
                vol_str += f"({issue})"
        if pages:
            vol_str += f", {pages}"
        apa = f"{apa_author_str} ({year}). {title}. *{journal}*, {vol_str}."

    print(f"\n引用格式")
    print("=" * 60)
    print(f"\nGB/T 7714 格式:")
    print(f"  {gbt}")
    print(f"\nAPA 格式:")
    print(f"  {apa}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="MBA/EMBA 论文研究方法顾问 - 动态论文检索工具"
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索某理论的近年高引用研究")
    search_parser.add_argument("theory", help="理论关键词（英文）")
    search_parser.add_argument("industry", nargs="?", default=None, help="行业关键词（可选）")
    search_parser.add_argument("--years", type=int, default=5, help="搜索近几年的论文（默认5年）")
    search_parser.add_argument("--limit", type=int, default=5, help="返回结果数量（默认5篇）")

    # enrich 命令
    enrich_parser = subparsers.add_parser("enrich", help="查询论文最新元数据")
    enrich_parser.add_argument("openalex_id", help="OpenAlex ID（如 W2123377363）")

    # cite 命令
    cite_parser = subparsers.add_parser("cite", help="生成引用格式")
    cite_parser.add_argument("openalex_id", help="OpenAlex ID（如 W2123377363）")

    args = parser.parse_args()

    if args.command == "search":
        search_recent_papers(args.theory, args.industry, args.years, args.limit)
    elif args.command == "enrich":
        enrich_paper(args.openalex_id)
    elif args.command == "cite":
        generate_citation(args.openalex_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
