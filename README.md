# tqdm1

tqdm は Python でコンソールにプログレスバーを表示するモジュールで、

- [tqdm · PyPI](https://pypi.org/project/tqdm/)
- [tqdm/tqdm at 0ed5d7f18fa3153834cbac0aa57e8092b217cc16](https://github.com/tqdm/tqdm/tree/0ed5d7f18fa3153834cbac0aa57e8092b217cc16)
- [tqdm documentation](https://tqdm.github.io/)

さまざまなプログラムで使用されているのだけど、vLLM でサーバを立てて systemd にしたときに、
tqdm のプログレスバーが journal でこんな感じになるのに気が付いた。

```console
Jan 24 02:29:46 ip-10-0-150-62 vllm[10311]: [77B blob data]
Jan 24 02:30:22 ip-10-0-150-62 vllm[10311]: [85B blob data]
Jan 24 02:31:00 ip-10-0-150-62 vllm[10311]: [85B blob data]
Jan 24 02:31:37 ip-10-0-150-62 vllm[10311]: [85B blob data]
Jan 24 02:32:03 ip-10-0-150-62 vllm[10311]: [85B blob data]
Jan 24 02:32:40 ip-10-0-150-62 vllm[10311]: [85B blob data]
Jan 24 02:33:18 ip-10-0-150-62 vllm[10311]: [85B blob data]
```

### 回避策として...

tqdm の動作は環境変数で制御できる。

具体的には [tqdm Objects](https://tqdm.github.io/docs/tqdm/#tqdm-objects) の引数、
例えば disable だったら `export TQDM_DISABLE=1` とかにすればいい。

## サンプルの実行

uv+PoeThePoet で書いてます。

```sh
uv sync
poe e1     # 標準的な tqdm()
poe e2     # 2秒に1回更新される tqdm()
poe e3     # 表示されない tqdm()
poe e4     # プログレスバーの表示を-*に変更
poe e5     # プログレスバー部分なし。後ろの 10000/10000 [00:06<00:00, 1661.24it/s] のとこだけ
poe e6     # プログレスバーなし。2秒に1回後ろの 10000/10000 [00:06<00:00, 1661.24it/s] のとこだけ行出力
```

設定するべき詳しい値は
[poe_tasks.toml](poe_tasks.toml)
の該当部分参照

## 結論

tqdm を使っているデーモン用の
systemd サービスファイルでは

- Environment="TQDM_DISABLE=1" にする
- または Environment="TQDM_BAR_FORMAT='{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]\n'" にする(一例)

といいと思う。

まあ内部で tqdm()の引数にがっちり記述してるかもしれないのでうまくいくとは限らない。試してみる価値はある。
