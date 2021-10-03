Flutter で見出し行・列固定のスクロール
======

Update: 2021-10-03

Flutter でExcelの「ウィンドウ枠の固定」と同じように見出し行・列固定のスクロールするサンプルを作ってみました。たかだか数十行のプログラムでこんなに簡単にできるとは・・・

<iframe width="560" height="315" src="https://www.youtube.com/embed/Ioyb_S5W4pU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

見出し列だけ、もしくは、見出し行だけ固定ならスクロールする部品を使ってプログラム無しでできます。でも、両方をやろうとすると縦か横のどちらかの見出しと本体がバラバラに動くことになります。それを ``ScrollController`` を使って同期させます。

[Is it possible to detect source of ScrollNotification in NotificationListener](https://stackoverflow.com/questions/60487509/is-it-possible-to-detect-source-of-scrollnotification-in-notificationlistener)
を参考にしました。

作ったもの

```
class DataSheet extends Widget {
  final double height;
  final double width;
  final double fixedHeight;
  final double fixedWidth;
  final Widget origin;
  final Widget colTitles;
  final Widget rowTitles;
  final Widget data;
  final ScrollController _titleScrollController = ScrollController();
  final ScrollController _dataScrollController = ScrollController();

  DataSheet({
    Key? key,
    required this.height,
    required this.width,
    required this.fixedHeight,
    required this.fixedWidth,
    required this.origin,
    required this.colTitles,
    required this.rowTitles,
    required this.data,
  }) : super(key: key);

  @override
  Element createElement() {
    return Container(
      width: width,
      height: height,
      alignment: Alignment.topLeft,
      decoration: const BoxDecoration(
        border: Border(
          top: BorderSide(color: Colors.blueGrey, width: 1.0),
          left: BorderSide(color: Colors.blueGrey, width: 1.0),
        ),
      ),
      child: Column(
        children: [
          Row(
            children: [
              origin,
              SizedBox(
                width: width - fixedWidth - 1.0,
                child: NotificationListener<ScrollNotification>(
                  onNotification: (ScrollNotification scrollInfo) {
                    _dataScrollController.jumpTo(_titleScrollController.offset);
                    return false;
                  },
                  child: SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    controller: _titleScrollController,
                    child: colTitles,
                  ),
                ),
              ),
            ],
          ),
          SizedBox(
            height: height - fixedHeight - 1.0,
            child: SingleChildScrollView(
              scrollDirection: Axis.vertical,
              child: Row(
                children: [
                  SizedBox(
                    width: fontSizeBody * 4,
                    child: rowTitles,
                  ),
                  SizedBox(
                    width: width - fixedWidth - 1.0,
                    child: NotificationListener<ScrollNotification>(
                      onNotification: (ScrollNotification scrollInfo) {
                        _titleScrollController
                            .jumpTo(_dataScrollController.offset);
                        return false;
                      },
                      child: SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        controller: _dataScrollController,
                        child: data,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    ).createElement();
  }
}
```

呼び出し元

```
    Widget build(BuildContext context) {
      return ...
         ... ...
        DataSheet(
          height: constraints.maxHeight - 96.0 - fontSizeBody * 2,
          width: constraints.maxWidth - fontSizeBody * 2,
          fixedHeight: fontSizeBody * 4,
          fixedWidth: fontSizeBody * 4,
          origin: origin,
          colTitles: colTitles,
          rowTitles: rowTitles,
          data: data,
        )
         ... ...
    }
```

中身

```
class DataCell extends Widget {
  final double height;
  final double width;
  final Widget child;
  final Color? color;

  const DataCell({
    Key? key,
    required this.height,
    required this.width,
    required this.child,
    this.color,
  }) : super(key: key);

  @override
  Element createElement() {
    return Container(
      color: color,
      height: height,
      width: width,
      decoration: const BoxDecoration(
        border: Border(
          right: BorderSide(color: Colors.blueGrey, width: 1.0),
          bottom: BorderSide(color: Colors.blueGrey, width: 1.0),
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(
          vertical: fontSizeBody / 4,
          horizontal: fontSizeBody / 4,
        ),
        child: child,
      ),
    ).createElement();
  }
}
DataCell origin = const DataCell(
  height: fontSizeBody * 4,
  width: fontSizeBody * 4,
  child: Text(''),
);

Row colTitles = Row(
  children: dataCols
      .map<Widget>(
        (value) => value == 'D'
            ? Column(
                children: [
                  DataCell(
                    height: fontSizeBody * 2,
                    width: fontSizeBody * 7,
                    child: Text(
                      value,
                      textAlign: TextAlign.center,
                    ),
                  ),
                  Row(
                    children: const [
                      DataCell(
                        height: fontSizeBody * 2,
                        width: fontSizeBody * 3.5,
                        child: Text(
                          'x',
                          textAlign: TextAlign.center,
                        ),
                      ),
                      DataCell(
                        height: fontSizeBody * 2,
                        width: fontSizeBody * 3.5,
                        child: Text(
                          'y',
                          textAlign: TextAlign.center,
                        ),
                      ),
                    ],
                  )
                ],
              )
            : DataCell(
                height: fontSizeBody * 4,
                width: fontSizeBody * 4,
                child: Text(
                  value,
                  textAlign: TextAlign.center,
                ),
              ),
      )
      .toList(),
);

Column rowTitles = Column(
  children: dataRows
      .map<Widget>(
        (value) => DataCell(
          height: fontSizeBody * (value == '5' ? 4 : 2),
          width: fontSizeBody * 4,
          child: Text(
            value,
            textAlign: TextAlign.center,
          ),
        ),
      )
      .toList(),
);

Column data = Column(
  children: dataRows
      .map<Widget>(
        (value1) => Row(
          children: dataCols
              .map<Widget>(
                (value2) => value2 == 'D'
                    ? Row(
                        children: [
                          DataCell(
                            height: fontSizeBody * (value1 == '5' ? 4 : 2),
                            width: fontSizeBody * 3.5,
                            child: Text(
                              value2 + value1 + 'x',
                              textAlign: TextAlign.center,
                            ),
                          ),
                          DataCell(
                            height: fontSizeBody * (value1 == '5' ? 4 : 2),
                            width: fontSizeBody * 3.5,
                            child: Text(
                              value2 + value1 + 'y',
                              textAlign: TextAlign.center,
                            ),
                          ),
                        ],
                      )
                    : (value1 == '5' && value2 == 'B')
                        ? const DataCell(
                            height: fontSizeBody * 4,
                            width: fontSizeBody * 4,
                            child: Icon(Icons.comment, size: fontSizeBody * 2),
                          )
                        : DataCell(
                            height: fontSizeBody * (value1 == '5' ? 4 : 2),
                            width: fontSizeBody * 4,
                            child: Text(
                              value2 + value1,
                              textAlign: TextAlign.center,
                            ),
                          ),
              )
              .toList(),
        ),
      )
      .toList(),
);

List<String> dataCols = [
  'A',
  'B',
  'C',
   ... ...
  'Z',
];
List<String> dataRows = [
  '1',
  '2',
  '3',
   ... ...
  '50',
];

```



Tag: flutter dart material
