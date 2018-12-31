# CognateSet #

CognateSet は、お互いの共通部分を持たない複数の集合を格納するデータ構造です。つまり集合の集合のような振る舞いをします。与えられた集合を格納し、部分的に共通する集合同士を結合します。CognateSet はミュータブルであり、join() や expand() のようなメソッドを使って集合を追加できます。既にいくつかの集合を格納している CognateSet インスタンスに、新たな集合を追加する場合は以下の図のようになります。

![説明](https://drive.google.com/uc?export=view&id=1Tdnt1T0LbcmrP16RJD_P4glnmHOvNWR1)

追加した集合と格納している集合に共通の要素がある場合は、それらの集合を1つに結合します。これにより、CognateSet インスタンスが持つ集合同士が共通要素を持たないことを保証します。

CognateSet はほかにも集合を削徐したり分割したりするメソッドを備えています。現在のところ、和 (union)、積 (intersection)、差 (difference)、対称差 (symmetric difference)といった数学的な演算はサポートしていません。

## 対応する言語バージョン ##
- Python 3.3以上

## モジュールの取得 ##
以下のコマンドでダウンロード。

`git clone https://github.com/masshash/CognateSet.git`

Pythonのモジュール検索パスの配下に、ダウンロードした cognateset.py を配置してください。

## 使用方法 ##

### インポート ###
```python
>>> from cognateset import CognateSet
```

### インスタンス作成 ###
```python
>>> cs = CognateSet() 
>>> cs
CognateSet()
```
あるいは最初にデータを与えることもできます。
```python
>>> cs = CognateSet([ {1, 2}, {3, 4} ])
>>> cs
CognateSet({1, 2}, {3, 4})
```
なお、インスタンスが格納するデータは順序を保証しません。そのため、常に同じ並びで表示されるとは限りません。

### 集合の追加、取得、削除 ###
集合の追加は **join(iterable)** メソッドを使用します。
```python
>>> cs
CognateSet({1, 2}, {3, 4})
>>> cs.join({5, 6})
>>> cs
CognateSet({1, 2}, {3, 4}, {5, 6})
>>> cs.join({4, 5})
>>> cs
CognateSet({1, 2}, {3, 4, 5, 6})
```
一度に複数の集合を追加するには **expand(other)** メソッドを使用します。
```python
>>> cs
CognateSet({1, 2}, {3, 4})
>>> cs.expand([ {4, 5}, {5, 6} ])
>>> cs
CognateSet({1, 2}, {3, 4, 5, 6})
```
集合の取得は **cognate(elem)** メソッドを使用します。elem を要素に持つ集合を set 型で返します。
```python
>>> cs
CognateSet({1, 2}, {3, 4})
>>> cs.cognate(1)
{1, 2}
>>> cs.cognate(4)
{3, 4}
```
集合の削除は **delcog(elem)** メソッドを使用します。elem を要素に持つ集合を削除します。
```python
>>> cs
CognateSet({1, 2}, {3, 4})
>>> if 4 in cs:
...     cs.delcog(4)
...
>>> cs
CognateSet({1, 2})
```
また、**delelem(elem)** メソッドを使用することで、elem に一致する要素を削除できます。
```python
>>> cs
CognateSet({1, 2}, {3, 4})
>>> cs.delelem(1)
>>> cs
CognateSet({2}, {3, 4})
>>> cs.delelem(2)
>>> cs
CognateSet({3, 4})
```

### 集合の分割 ###
たとえば、
```python
CognateSet({1, 2, 'A', 'B'})
```
を以下のように整数の集合と文字列の集合に分割したいとします。
```python
CognateSet({1, 2}, {'A', 'B'})
```
このような場合は、**reorg(iterable)** を使用します。
```python
>>> cs
CognateSet({1, 2, 'A', 'B'})
>>> cs.reorg({1, 2})
>>> cs
CognateSet({'A', 'B'}, {1, 2})
```
このメソッドは、格納している集合から iterable が持つ要素と等しい要素を取り除きます。そして iterable を追加します。

### イテレーション ###
```python
>>> cs
CognateSet({1, 2}, {3, 4})
>>> for cognate in cs:    # cognate には set 型が渡されます。
...     print(cognate)
...
{1, 2}
{3, 4}
```
**elements()** を使えば、全集合の要素をフラットにイテレートできます。
```python
>>> for element in cs.elements():
...     print(element)
...
1
2
3
4
```
elements() は、全集合の要素のビューを返します。

## ライセンス ##
コードは MIT ライセンスのもとに公開しています。詳細は LICENSE.txt を参照してください。
