# ZIKUU教材ノートブック

## 目的

- 科学教育の教材を共有する
- 興味があるものだけ、一人で遊びながら学べる

---

## 学習環境

- インターネットに接続できるPCだけ

---

## 学習方法

1. Google Colabを使う場合
    - Discordに掲示板を置き、そこにノートブックへのリンクを記載
    - リンクをクリックするとGoogle Colabのノートブックが開く
    - ノートブックには、学習を進めるための説明とプログラムコードが載っているので、説明を読みながらプログラムを動かすだけで結果が見える

2. Jupyter Notebookを自分のPCにインストールして使う場合

    - **Jupyter Notebook 実行環境の準備**を参照

## 教材一覧

<!-- ZIKUU_NOTEBOOKS_LIST:BEGIN -->
更新: 2026-01-12 16:16:26Z

- **[地球観測編①：だいち2号（ALOS-2）](./earth-observation-001-daichi2/)**
  - [earth_observation_intro.ipynb](https://colab.research.google.com/github/ZIKUU-SPACE/zikuu-notebooks/blob/main/earth-observation-001-daichi2/earth_observation_intro.ipynb)
<!-- ZIKUU_NOTEBOOKS_LIST:END -->
---

## Jupyter Notebook 実行環境の準備

このリポジトリの教材は、**Jupyter Notebook** 形式で提供されています。
以下のいずれかの方法で利用できます。

---

## 方法①：Google Colab（インストール不要・おすすめ）

環境構築をせずに、すぐ始めたい場合はこちら。

1. 各Notebook（`.ipynb`）を開く
2. 画面右上の **「Open in Colab」** をクリック
3. ブラウザ上でそのまま実行

### 特徴

* インストール不要
* GoogleアカウントがあればOK
* 初学者向け・教材用途に最適

---

## 方法②：ローカル環境（PCにインストール）

自分のPCでNotebookを実行したい場合。

### 1. Python をインストール

Python 3.10 以上を推奨します。

* [https://www.python.org/](https://www.python.org/)

※ Linux / macOS では多くの場合、すでに入っています。

---

### 2. venv（仮想環境）を作成（推奨）

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows の場合：

```bat
venv\\Scripts\\activate
```

---

### 3. Jupyter Notebook をインストール

```bash
python -m pip install --upgrade pip
python -m pip install notebook numpy matplotlib
```


---

### 4. Notebook を起動

```bash
jupyter notebook
```

または

```bash
jupyter lab
```

ブラウザが起動し、Notebook一覧が表示されます。

---

## このリポジトリの使い方

1. このリポジトリを clone する

```bash
git clone https://github.com/ZIKUU-SPACE/zikuu-notebooks.git
cd zikuu-notebooks
```

2. 学びたい教材フォルダを開く

```text
earth-observation-001-daichi2/
```

3. `.ipynb` を開いて、上から順に実行

---

## 対応方針（ZIKUU Notebooks）

* 特別なライブラリは **極力使わない**
* 数式よりも **考え方を重視**
* 教材は **入口として完結** させる

環境構築でつまずかないことを、最優先にしています。

---

## 補足：なぜ Jupyter Notebook なのか

* 説明とコードを同時に読める
* 試しながら理解できる
* 失敗しても壊れない

ZIKUU Notebooks は、
**「読む教材」ではなく「触る教材」**です。

