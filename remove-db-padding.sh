#!/bin/bash

# 引数のチェック
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <CSS file>"
    exit 1
fi

# コマンドライン引数
css_file="$1"
start_string="\/\* resize inline databases \*\/"
end_string="\/\* pull alias arrows back inline \*\/"

# MacOS と Linux の違いを吸収するための -i オプション
if [[ "$OSTYPE" == "darwin"* ]]; then
    # コメントの開始位置に /* を追加
    sed -i '' "/$start_string/{n;s/^/\/\*\n/;}" "$css_file"
    # コメントの終了位置に */ を追加
    sed -i '' "/$end_string/{s/^/*\/\n/;}" "$css_file"
else
    # コメントの開始位置に /* を追加
    sed -i "/$start_string/{n;s/^/\/\*\n/;}" "$css_file"
    # コメントの終了位置に */ を追加
    sed -i "/$end_string/{s/^/*\/\n/;}" "$css_file"
fi

echo "The section between '/* resize inline databases */' and '/* pull alias arrows back inline */' has been commented out in '$css_file'."