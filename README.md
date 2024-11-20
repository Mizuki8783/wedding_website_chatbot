# Wedding Blog Assistant Chatbot
結婚関連のブログサイトのユーザーをサポートするチャットボットのバックエンドサーバー。Flask, LangChain, OpenAI, Pineconeで構築されており、ベクトルデータベースのコンテンツインデックスを利用して、ユーザーの質問に最も近い記事をデータベースから検索しを提供します。


## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key
- Pinecone API key
- LangChain API key

### Installation

1. レポジトリのクローン
```bash
git clone https://github.com/Mizuki8783/TSM.git
cd TSM/clients/wedding_website_chatbot
```

2. 依存関係のインストール
```bash
cd src
pip install -r requirements.txt
```

3. 環境変数の設定
```bash
cp .env.example .env
```
`.env`ファイルを編集して、APIキーを設定します:
- OPENAI_API_KEY
- PINECONE_API_KEY
- LANGCHAIN_API_KEY
- Other configuration settings

### Running the Application

```bash
python src/main.py
```

## Technology Stack

- バックエンドフレームワーク: Flask
- LLMモデル: OpenAI GPT
- LLMフレームワーク: LangChain
- ベクトルデータベース: Pinecone
- 追加のライブラリ:
  - langchain-openai: OpenAI integration
  - langchain-pinecone: Vector storage
  - python-dotenv: Environment management
  - firecrawl-py: Web crawling capabilities

## Project Structure

```
wedding_website_chatbot/
├── src/
│   ├── main.py           # Application entry point
│   ├── functions.py      # Article recommendation and search functions
│   ├── prompts.py        # Conversation templates and article indexing
│   └── requirements.txt  # Python dependencies
├── .env                  # Environment configuration
└── README.md            # Project documentation
```

## License

This project is licensed under the MIT License.
