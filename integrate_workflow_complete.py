#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI SEO Workflow Integration Script - Complete Version
完全版統合スクリプト：テキストファイルの内容を既存HTMLに完全統合
"""

import re
import html as html_lib

def read_text_file(file_path):
    """テキストファイルを読み込み"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_html_template(file_path):
    """既存HTMLファイルを読み込み"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_processes(text_content):
    """テキストから工程ごとに内容を抽出"""
    processes = {}

    # 工程の区切りパターン
    process_markers = [
        r'0\. キーワード選定',
        r'1\. Start - キーワード入力',
        r'2\. Search - 上位10サイト取得',
        r'2\.1\. Extract - 競合記事本文抽出',
        r'3\. クエリ分析・ペルソナ深掘り',
        r'4\. 共起語・関連キーワード抽出',
        r'5\. 競合分析・差別化',
        r'6\. 戦略的アウトライン生成',
        r'7\. 一次情報追加',
        r'8\. 本文生成',
        r'9\. ファクトチェック',
        r'10\. 最終リライト',
        r'11\. SEO記事完成',
        r'12\.'
    ]

    # 各工程の開始位置を検出
    lines = text_content.split('\n')
    current_process = None
    current_content = []

    for i, line in enumerate(lines):
        # 工程の開始を検出
        is_process_start = False
        for marker in process_markers:
            if re.match(marker, line.strip()):
                # 前の工程を保存
                if current_process is not None:
                    processes[current_process] = '\n'.join(current_content)

                # 新しい工程を開始
                current_process = line.strip()
                current_content = []
                is_process_start = True
                break

        if not is_process_start and current_process is not None:
            # 区切り線をスキップ
            if line.strip() == '________________':
                continue
            current_content.append(line)

    # 最後の工程を保存
    if current_process is not None:
        processes[current_process] = '\n'.join(current_content)

    return processes

def extract_section_content(text, section_name):
    """特定のセクションを抽出"""
    patterns = {
        '目的と内容': r'目的と内容\s*\n(.+?)(?=\n作業内容|\n【|\nプロンプト|\nGemini|\nChatGPT|\nClaude|\nシステム|\nモデル比較)',
        '作業内容': r'作業内容\s*\n(.+?)(?=\n決定事項|\n【|\nプロンプト|\nGemini|\nChatGPT|\nClaude|\nシステム|\nモデル比較)',
        'モデル比較': r'モデル比較・推奨\s*\n(.+?)(?=\n補足|\n________________|\Z)',
        '補足': r'補足[:：](.+?)(?=\n________________|\Z)',
    }

    pattern = patterns.get(section_name)
    if not pattern:
        return ""

    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def extract_prompts(text):
    """プロンプトを抽出"""
    prompts = []

    # より柔軟なパターンでプロンプトを検出
    # Gemini用プロンプト
    gemini_patterns = [
        r'Gemini用プロンプト[：:].*?\n(.+?)(?=\n(?:ChatGPT用プロンプト|Claude用プロンプト|システム実装例|モデル比較|補足|$))',
        r'Gemini用プロンプト\s*（[^）]+）[：:]?\s*\n(.+?)(?=\n(?:ChatGPT用プロンプト|Claude用プロンプト|システム実装例|モデル比較|補足|$))',
    ]
    for pattern in gemini_patterns:
        for match in re.finditer(pattern, text, re.DOTALL | re.IGNORECASE):
            content = match.group(1).strip()
            if len(content) > 50:  # 最小長チェック
                prompts.append(('Gemini', content))

    # ChatGPT用プロンプト
    chatgpt_patterns = [
        r'ChatGPT用プロンプト[：:].*?\n(.+?)(?=\n(?:Gemini用プロンプト|Claude用プロンプト|システム実装例|モデル比較|補足|$))',
        r'ChatGPT用プロンプト\s*（[^）]+）[：:]?\s*\n(.+?)(?=\n(?:Gemini用プロンプト|Claude用プロンプト|システム実装例|モデル比較|補足|$))',
    ]
    for pattern in chatgpt_patterns:
        for match in re.finditer(pattern, text, re.DOTALL | re.IGNORECASE):
            content = match.group(1).strip()
            if len(content) > 50:
                prompts.append(('ChatGPT', content))

    # Claude用プロンプト
    claude_patterns = [
        r'Claude用プロンプト[：:].*?\n(.+?)(?=\n(?:Gemini用プロンプト|ChatGPT用プロンプト|システム実装例|モデル比較|補足|$))',
        r'Claude用プロンプト\s*（[^）]+）[：:]?\s*\n(.+?)(?=\n(?:Gemini用プロンプト|ChatGPT用プロンプト|システム実装例|モデル比較|補足|$))',
    ]
    for pattern in claude_patterns:
        for match in re.finditer(pattern, text, re.DOTALL | re.IGNORECASE):
            content = match.group(1).strip()
            if len(content) > 50:
                prompts.append(('Claude', content))

    return prompts

def text_to_html_paragraphs(text):
    """テキストをHTMLの段落に変換"""
    if not text:
        return ""

    lines = text.split('\n')
    html_parts = []
    in_list = False
    list_items = []

    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_parts.append('<ul class="detail-list">')
                for item in list_items:
                    html_parts.append(f'<li>{html_lib.escape(item)}</li>')
                html_parts.append('</ul>')
                in_list = False
                list_items = []
            continue

        # リスト項目を検出
        list_match = re.match(r'^[\*\-]\s+(.+)', line)
        number_match = re.match(r'^\d+\.\s+(.+)', line)

        if list_match or number_match:
            content = list_match.group(1) if list_match else number_match.group(1)
            list_items.append(content)
            in_list = True
        else:
            if in_list:
                html_parts.append('<ul class="detail-list">')
                for item in list_items:
                    html_parts.append(f'<li>{html_lib.escape(item)}</li>')
                html_parts.append('</ul>')
                in_list = False
                list_items = []

            # 通常の段落
            html_parts.append(f'<p>{html_lib.escape(line)}</p>')

    # 残りのリストを処理
    if in_list:
        html_parts.append('<ul class="detail-list">')
        for item in list_items:
            html_parts.append(f'<li>{html_lib.escape(item)}</li>')
        html_parts.append('</ul>')

    return '\n'.join(html_parts)

def create_process_section_html(process_num, process_title, content):
    """工程のHTMLセクションを生成"""

    # 各サブセクションを抽出
    purpose = extract_section_content(content, '目的と内容')
    work_content = extract_section_content(content, '作業内容')
    model_comparison = extract_section_content(content, 'モデル比較')
    supplement = extract_section_content(content, '補足')
    prompts = extract_prompts(content)

    # セクションID
    section_id = f"process-{process_num}".replace('.', '-')

    html = f'''
    <section id="{section_id}">
        <h2>{process_title}</h2>
'''

    # 目的と内容
    if purpose:
        html += f'''
        <div class="principle-box">
            <h3>📌 目的と内容</h3>
            {text_to_html_paragraphs(purpose[:2000])}
        </div>
'''

    # 作業内容
    if work_content:
        html += f'''
        <div class="process-detail">
            <h3>🔧 作業内容</h3>
            {text_to_html_paragraphs(work_content[:2000])}
        </div>
'''

    # プロンプト
    if prompts:
        html += '''
        <div class="process-detail">
            <h3>🤖 AIモデル別プロンプト</h3>
'''
        for idx, (model_name, prompt_text) in enumerate(prompts):
            prompt_id = f"prompt-{section_id}-{idx}"

            # モデル別の色分け
            model_class = {
                'Gemini': 'gemini-prompt',
                'ChatGPT': 'chatgpt-prompt',
                'Claude': 'claude-prompt'
            }.get(model_name, 'default-prompt')

            html += f'''
            <h4>{model_name}用プロンプト</h4>
            <div class="prompt-box {model_class}">
                <button class="copy-btn" onclick="copyToClipboard('{prompt_id}')">📋 コピー</button>
                <pre id="{prompt_id}">{html_lib.escape(prompt_text)}</pre>
            </div>
'''
        html += '''
        </div>
'''

    # モデル比較
    if model_comparison:
        html += f'''
        <div class="comparison-box">
            <h3>⚖️ モデル比較・推奨</h3>
            {text_to_html_paragraphs(model_comparison[:1500])}
        </div>
'''

    # 補足（脳科学・行動経済学など）
    if supplement:
        html += f'''
        <div class="enhancement-box">
            <h3>🧠 脳科学・行動経済学・LLMO・KGI観点からの強化ポイント</h3>
            {text_to_html_paragraphs(supplement[:2500])}
        </div>
'''

    html += '''
    </section>
'''

    return html

def generate_navigation_html(processes_list):
    """ナビゲーションHTMLを生成"""
    nav_items = []

    for num, title in processes_list:
        section_id = f"process-{num}".replace('.', '-')
        short_title = title.replace('工程', '').replace(': ', ':')
        nav_items.append(f'<li><a href="#{section_id}">{short_title}</a></li>')

    return '\n'.join(nav_items)

def add_additional_styles(html_template):
    """追加のCSSスタイルを挿入"""
    additional_css = '''
        .detail-list {
            list-style: none;
            padding-left: 0;
        }

        .detail-list li {
            padding: 8px 0 8px 25px;
            position: relative;
            color: #f0d98d;
        }

        .detail-list li::before {
            content: "▸";
            position: absolute;
            left: 5px;
            color: #ffd700;
            font-weight: bold;
        }

        .prompt-box {
            position: relative;
            margin: 20px 0;
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, #2a2520 0%, #3a3020 50%, #2a2520 100%);
            border: 2px solid #ffd700;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5), 0 0 20px rgba(255, 215, 0, 0.2);
        }

        .prompt-box.gemini-prompt {
            border-color: #34a853;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5), 0 0 20px rgba(52, 168, 83, 0.2);
        }

        .prompt-box.chatgpt-prompt {
            border-color: #10a37f;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5), 0 0 20px rgba(16, 163, 127, 0.2);
        }

        .prompt-box.claude-prompt {
            border-color: #cc9b7a;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5), 0 0 20px rgba(204, 155, 122, 0.2);
        }

        .prompt-box pre {
            margin: 10px 0 0 0;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 5px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #f0d98d;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        .copy-btn {
            position: absolute;
            top: 15px;
            right: 15px;
            background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
            color: #1a1500;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            box-shadow: 0 2px 10px rgba(255, 215, 0, 0.3);
            transition: all 0.3s;
        }

        .copy-btn:hover {
            background: linear-gradient(135deg, #ffed4e 0%, #ffd700 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.5);
        }

        .process-detail {
            margin: 30px 0;
        }

        .comparison-box {
            background: linear-gradient(135deg, #1f2520 0%, #2a3020 50%, #1f2520 100%);
            border-left: 5px solid #34a853;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5), 0 0 20px rgba(52, 168, 83, 0.1);
        }

        .enhancement-box {
            background: linear-gradient(135deg, #252025 0%, #302030 50%, #252025 100%);
            border-left: 5px solid #cc9b7a;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5), 0 0 20px rgba(204, 155, 122, 0.1);
        }

        .enhancement-box h3, .comparison-box h3 {
            margin-top: 0;
        }
    '''

    # </style>タグの直前に追加CSSを挿入
    html_with_styles = re.sub(r'(</style>)', f'{additional_css}\n\\1', html_template)
    return html_with_styles

def integrate_into_html(html_template, sections_html, nav_html):
    """生成したセクションを既存HTMLテンプレートに統合"""

    # まず追加のスタイルを挿入
    html_template = add_additional_styles(html_template)

    # contentセクションを探して置き換え
    # 既存の<section>タグを新しい内容で置き換え
    content_pattern = r'(<div class="content">)(.*?)(</div>\s*</div>\s*</body>)'

    new_content = f'''\\1

        <!-- 概要セクション -->
        <section id="overview">
            <h2>📋 全体概要</h2>
            <div class="principle-box">
                <h4>本フロー全体を貫く最重要目標（KGI）：お問い合わせ率の最大化</h4>
                <p>ChatGPT（OpenAI GPT系）、Google Gemini、Anthropic Claudeという3つのLLMを活用し、SEO/LLMO記事作成の全工程（0〜12工程）を自動化するフロー設計です。</p>
                <p>各工程で脳科学・行動経済学・LLMO（AI検索最適化）の知見を統合し、最終的な「お問い合わせ行動」へと読者を導く設計となっています。</p>
                <ul class="detail-list">
                    <li><strong>不安・課題の認識フェーズ</strong>（扁桃体の活性化）</li>
                    <li><strong>理解・納得フェーズ</strong>（前頭前野の処理）</li>
                    <li><strong>行動決定フェーズ</strong>（線条体の報酬予測）</li>
                </ul>
            </div>
        </section>

        {sections_html}

        <!-- 完了セクション -->
        <section id="completion">
            <h2>✅ フロー完了</h2>
            <div class="principle-box">
                <h3>おめでとうございます！</h3>
                <p>全12工程のAI SEO記事自動化フローが完了しました。</p>
                <p>生成された記事は、脳科学・行動経済学・LLMOの知見を統合した、お問い合わせ獲得に最適化されたコンテンツです。</p>
            </div>
        </section>

\\3'''

    html_output = re.sub(content_pattern, new_content, html_template, flags=re.DOTALL)

    # ナビゲーションを更新
    nav_pattern = r'(<nav>.*?<ul>)(.*?)(</ul>.*?</nav>)'
    new_nav = f'\\1\n{nav_html}\n\\3'
    html_output = re.sub(nav_pattern, new_nav, html_output, flags=re.DOTALL)

    return html_output

def main():
    print("=" * 60)
    print("AI SEO Workflow 完全版統合スクリプト")
    print("=" * 60)

    # ファイルパス
    text_file = '/Users/apple/Desktop/dify/裏サイト/★門外不出★AI別SEO記事自動化フロー設計とモデル比較（完全版） (3).txt'
    html_template_file = '/Users/apple/Desktop/dify/ai-seo-workflow-secret.html'
    output_file = '/Users/apple/Desktop/dify/ai-seo-workflow-secret.html'

    print(f"\n📄 テキストファイルを読み込み中...")
    text_content = read_text_file(text_file)
    print(f"   ✓ {len(text_content):,} 文字を読み込みました")

    print(f"\n📄 HTMLテンプレートを読み込み中...")
    html_template = read_html_template(html_template_file)
    print(f"   ✓ {len(html_template):,} 文字を読み込みました")

    print(f"\n🔍 工程ごとに内容を解析中...")
    processes = parse_processes(text_content)
    print(f"   ✓ {len(processes)} 個の工程を検出しました")

    # 工程リスト
    process_list = [
        ('0', '工程0: キーワード選定'),
        ('1', '工程1: キーワード入力'),
        ('2', '工程2: 上位10サイト取得'),
        ('2-1', '工程2.1: 競合記事本文抽出'),
        ('3', '工程3: クエリ分析・ペルソナ深掘り'),
        ('4', '工程4: 共起語・関連キーワード抽出【心臓部】'),
        ('5', '工程5: 競合分析・差別化切り口発見'),
        ('6', '工程6: 戦略的アウトライン生成'),
        ('7', '工程7: 一次情報追加・知識ギャップ解消'),
        ('8', '工程8: 本文生成・10重チェック'),
        ('9', '工程9: ファクトチェック'),
        ('10', '工程10: 最終リライト・品質向上'),
        ('11', '工程11: SEO記事完成・最終出力'),
        ('12', '工程12: 拡張工程（将来用）'),
    ]

    print(f"\n🏗️  各工程のHTMLセクションを生成中...")
    all_sections_html = []
    total_prompts = 0

    for num, title in process_list:
        # 対応するテキストを探す
        process_content = None
        for key, value in processes.items():
            if f"{num}." in key or f"工程{num}" in key:
                process_content = value
                break

        if process_content:
            print(f"   ✓ {title}")
            section_html = create_process_section_html(num, title, process_content)
            all_sections_html.append(section_html)

            # プロンプト数をカウント
            prompts = extract_prompts(process_content)
            total_prompts += len(prompts)
        else:
            print(f"   ⚠ {title} - 内容が見つかりません")

    print(f"\n   合計: {len(all_sections_html)} セクション, {total_prompts} プロンプト")

    print(f"\n🔗 ナビゲーションを生成中...")
    nav_html = generate_navigation_html(process_list)

    print(f"\n🎨 HTMLテンプレートに統合中...")
    final_html = integrate_into_html(
        html_template,
        '\n'.join(all_sections_html),
        nav_html
    )

    print(f"\n💾 ファイルを保存中...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"   ✓ {output_file} に保存しました")
    print(f"   ✓ ファイルサイズ: {len(final_html):,} 文字")

    print("\n" + "=" * 60)
    print("✅ 完了しました！")
    print(f"   - {len(all_sections_html)} 個の工程セクションを統合")
    print(f"   - {total_prompts} 個のプロンプトにコピー機能を追加")
    print(f"   - 黄金テーマのデザインを維持")
    print("=" * 60)

if __name__ == '__main__':
    main()
